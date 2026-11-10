/* Study Studio engine — Phase 1.
 *
 * Reads one CHAPTER_DATA object from the page and renders the reading
 * environment: three reading modes, four language modes, a sticky outline
 * with progress, an inline word layer, a command palette, a selection
 * toolbar, and an in-page self-test.
 *
 * Rules this file keeps:
 *   - no network, no framework, no imports;
 *   - the engine knows nothing about the chapter subject;
 *   - `pointermove` performs no layout read; work happens in one rAF;
 *   - only `transform` and `opacity` are animated;
 *   - every storage access is wrapped and falls back to memory.
 */

(function () {
  'use strict';

  /* ============================================================ constants */

  var STORAGE_ROOT = 'studio.';
  var LANG_MODES = ['en', 'en-hints', 'ar', 'test'];
  var READING_MODES = ['focus', 'skim', 'deep'];
  var HIGHLIGHT_COLORS = ['yellow', 'green', 'blue', 'pink'];
  var STATUS_NEW = 'new';
  var STATUS_LEARNING = 'learning';
  var STATUS_KNOWN = 'known';

  /* The hit-test shape. Vertical distance is weighted 3x and the candidate
   * must live in the pointer's line band, so the search box is roughly
   * 40px wide and 13px tall — the shape a word actually occupies. */
  var VERTICAL_WEIGHT = 3;
  var BAND_SLACK = 6;

  /* ============================================================ dom helpers */

  function $(selector, root) {
    return (root || document).querySelector(selector);
  }

  function $$(selector, root) {
    return Array.prototype.slice.call((root || document).querySelectorAll(selector));
  }

  function make(tag, attrs, children) {
    var node = document.createElement(tag);
    if (attrs) {
      Object.keys(attrs).forEach(function (name) {
        var value = attrs[name];
        if (value === null || value === undefined || value === false) {
          return;
        }
        if (name === 'text') {
          node.textContent = String(value);
        } else if (name === 'class') {
          node.className = String(value);
        } else {
          node.setAttribute(name, value === true ? '' : String(value));
        }
      });
    }
    (children || []).forEach(function (child) {
      if (child === null || child === undefined) {
        return;
      }
      node.appendChild(typeof child === 'string' ? document.createTextNode(child) : child);
    });
    return node;
  }

  function clear(node) {
    while (node && node.firstChild) {
      node.removeChild(node.firstChild);
    }
  }

  function announce(message) {
    var region = document.getElementById('live-region');
    if (!region) {
      return;
    }
    region.textContent = '';
    window.setTimeout(function () {
      region.textContent = message;
    }, 30);
  }

  /* ============================================================ storage */

  /* A safe wrapper around localStorage with an in-memory fallback. */
  function createStore(namespace) {
    var memory = {};
    var usable = false;

    try {
      var probe = '__studio_probe__';
      window.localStorage.setItem(probe, '1');
      window.localStorage.removeItem(probe);
      usable = true;
    } catch (err) {
      usable = false;
    }

    function full(name) {
      return namespace + '.' + name;
    }

    return {
      available: usable,
      get: function (name, fallback) {
        var raw = null;
        try {
          raw = usable ? window.localStorage.getItem(full(name)) : memory[name];
        } catch (err) {
          raw = memory[name];
        }
        if (raw === null || raw === undefined) {
          return fallback;
        }
        try {
          return JSON.parse(raw);
        } catch (err) {
          return fallback;
        }
      },
      set: function (name, value) {
        var raw = null;
        try {
          raw = JSON.stringify(value);
        } catch (err) {
          return false;
        }
        memory[name] = raw;
        if (!usable) {
          return false;
        }
        try {
          window.localStorage.setItem(full(name), raw);
          return true;
        } catch (err) {
          usable = false;
          return false;
        }
      },
      remove: function (name) {
        delete memory[name];
        try {
          window.localStorage.removeItem(full(name));
        } catch (err) {
          /* nothing to do; the in-memory copy is already gone */
        }
      }
    };
  }

  var globalStore = createStore(STORAGE_ROOT);

  /* ============================================================ state */

  var state = {
    chapter: null,
    store: null,
    key: null,
    langMode: 'en',
    readingMode: 'focus',
    openSections: {},
    currentSection: null,
    explainOpen: {},
    confusionStep: {},
    notes: [],
    highlights: [],
    userCards: [],
    wordStatus: {},
    understood: {},
    hideKnown: false,
    cursor: null,
    hovered: null,
    paletteItems: [],
    paletteIndex: 0,
    sessionStart: Date.now(),
    glossaryByTerm: {},
    glossaryById: {},
    conceptById: {},
    labById: {}
  };

  var articleEl = null;
  var outlineListEl = null;
  var popoverEl = null;
  var miniCardEl = null;
  var toolbarEl = null;
  var paletteOverlayEl = null;
  var paletteInputEl = null;
  var paletteListEl = null;

  /* ============================================================ chapter data */

  function readChapterData() {
    var node = document.getElementById('chapter-data');
    if (!node) {
      throw new Error('the chapter-data script block is missing');
    }
    return JSON.parse(node.textContent);
  }

  function sectionById(id) {
    var found = null;
    state.chapter.sections.forEach(function (section) {
      if (section.id === id) {
        found = section;
      }
    });
    return found;
  }

  function paraKey(sectionId, index) {
    return sectionId + ':' + index;
  }

  /* ============================================================ text helpers */

  /* Split a paragraph into word tokens, keeping their offsets. */
  function tokenize(text) {
    var tokens = [];
    var re = /\S+/g;
    var match = re.exec(text);
    while (match !== null) {
      tokens.push({ word: match[0], start: match.index, end: match.index + match[0].length });
      match = re.exec(text);
    }
    return tokens;
  }

  /* A comparable form of a token: lower case, no surrounding punctuation. */
  function normalize(text) {
    return String(text)
      .toLowerCase()
      .replace(/^[^\w\u0600-\u06ff]+|[^\w\u0600-\u06ff]+$/g, '');
  }

  function normalizeSequence(text) {
    return String(text)
      .toLowerCase()
      .split(/\s+/)
      .map(normalize)
      .filter(function (part) {
        return part.length > 0;
      });
  }

  function countWords(text) {
    var tokens = tokenize(text || '');
    return tokens.length;
  }

  /* ============================================================ markup helpers */

  function arabicBlock(className, text, id) {
    var node = make('div', { class: 'ar-block ' + (className || ''), id: id || null });
    var body = make('p', { class: 'ar', lang: 'ar', dir: 'rtl', text: text });
    node.appendChild(body);
    return node;
  }

  function aiBadge() {
    return make('span', { class: 'ai-badge', text: 'AI', 'aria-hidden': 'true' });
  }

  /* Inline SVG markup arrives from the chapter file. It is parsed in a
   * detached document, stripped of scripts and event handlers, and only
   * then imported into the page. */
  function buildSafeSvg(markup) {
    var root = null;
    try {
      var xml = new DOMParser().parseFromString(markup, 'image/svg+xml');
      if (!xml.getElementsByTagName('parsererror').length && xml.documentElement) {
        root = xml.documentElement;
      }
    } catch (err) {
      root = null;
    }
    if (!root) {
      /* No namespace or malformed markup: fall back to the HTML parser. */
      var html = new DOMParser().parseFromString('<div id="studio-svg-host">' + markup, 'text/html');
      var host = html.getElementById('studio-svg-host');
      root = host ? host.firstElementChild : null;
    }
    if (!root) {
      return null;
    }

    $$('script', root).forEach(function (node) {
      node.parentNode.removeChild(node);
    });
    $$('*', root).forEach(function (node) {
      Array.prototype.slice.call(node.attributes).forEach(function (attr) {
        var name = attr.name.toLowerCase();
        var value = attr.value || '';
        if (name.indexOf('on') === 0) {
          node.removeAttribute(attr.name);
        } else if ((name === 'href' || name === 'xlink:href' || name === 'src') && value.indexOf('#') !== 0) {
          node.removeAttribute(attr.name);
        }
      });
    });
    return document.importNode(root, true);
  }

  /* ============================================================ word layer */

  /* Build the word spans for one paragraph.
   *
   * `.w` stays `display: inline` so text breaks and justification behave
   * normally. The scale target is the inner `.wi` box, because a transform
   * does not apply to a non-replaced inline box (measured in Chrome). The
   * inner box is an inline-block of identical height to the line, so the
   * line box never grows and the paragraph height never changes. */
  function buildWordSpans(text, tokens, glossaryHits) {
    var fragment = document.createDocumentFragment();
    var cursor = 0;

    tokens.forEach(function (token, index) {
      if (token.start > cursor) {
        fragment.appendChild(document.createTextNode(text.slice(cursor, token.start)));
      }
      var outer = make('span', { class: 'w', 'aria-hidden': 'true' });
      outer.setAttribute('data-wi', String(index));
      var inner = make('span', { class: 'wi', text: token.word });
      outer.appendChild(inner);

      var hit = glossaryHits[index];
      if (hit) {
        outer.setAttribute('data-word-id', hit.entry.id);
        applyWordStatus(outer, token.word);
        if (hit.entry.technical && hit.first) {
          /* The badge is a mouse affordance. The same information is
           * reachable from the keyboard through the word popover, which
           * is why the badge is hidden from assistive technology. */
          var badge = make('span', { class: 'tech-badge', 'aria-hidden': 'true' });
          badge.setAttribute('data-word-id', hit.entry.id);
          fragment.appendChild(outer);
          fragment.appendChild(badge);
          cursor = token.end;
          return;
        }
      }
      fragment.appendChild(outer);
      cursor = token.end;
    });

    if (cursor < text.length) {
      fragment.appendChild(document.createTextNode(text.slice(cursor)));
    }
    return fragment;
  }

  /* Find which glossary entries appear in a paragraph, per word index. */
  function matchGlossary(tokens) {
    var hits = {};
    var normalizedTokens = tokens.map(function (token) {
      return normalize(token.word);
    });

    state.chapter.glossary.forEach(function (entry) {
      var needle = normalizeSequence(entry.term);
      if (needle.length === 0) {
        return;
      }
      for (var i = 0; i + needle.length <= normalizedTokens.length; i++) {
        var matched = true;
        for (var j = 0; j < needle.length; j++) {
          if (normalizedTokens[i + j] !== needle[j]) {
            matched = false;
            break;
          }
        }
        if (matched) {
          for (var k = 0; k < needle.length; k++) {
            hits[i + k] = { entry: entry, first: k === 0 };
          }
          i += needle.length - 1;
        }
      }
    });
    return hits;
  }

  function applyWordStatus(span, wordText) {
    var status = state.wordStatus[normalize(wordText)];
    if (!status) {
      /* A curated word the learner has not judged yet counts as new. */
      status = span.getAttribute('data-word-id') ? STATUS_NEW : null;
    }
    if (status) {
      span.setAttribute('data-status', status);
    } else {
      span.removeAttribute('data-status');
    }
  }

  function refreshWordStatuses(root) {
    $$('.w[data-word-id]', root || articleEl).forEach(function (span) {
      applyWordStatus(span, span.textContent);
    });
  }

  /* ------------------------------------------------- the word rect cache */

  var wordCache = {
    words: [],
    bands: [],
    built: false
  };

  /* Rects are stored in document coordinates, so scrolling never
   * invalidates them. The cache is rebuilt when the layout can have
   * changed: a resize, a font swap, a content reflow, or a reading-mode
   * switch. */
  function rebuildWordRects() {
    var nodes = $$('.w', articleEl);
    var words = [];
    var scrollX = window.scrollX || 0;
    var scrollY = window.scrollY || 0;

    for (var i = 0; i < nodes.length; i++) {
      var node = nodes[i];
      var rect = node.getBoundingClientRect();
      if (rect.width === 0 && rect.height === 0) {
        continue;
      }
      words.push({
        el: node,
        text: node.textContent,
        left: rect.left + scrollX,
        right: rect.right + scrollX,
        top: rect.top + scrollY,
        bottom: rect.bottom + scrollY
      });
    }

    var bands = [];
    for (var j = 0; j < words.length; j++) {
      var word = words[j];
      var band = null;
      for (var b = 0; b < bands.length; b++) {
        if (Math.abs(bands[b].top - word.top) < 2 && Math.abs(bands[b].bottom - word.bottom) < 2) {
          band = bands[b];
          break;
        }
      }
      if (!band) {
        band = { top: word.top, bottom: word.bottom, start: j, end: j + 1 };
        bands.push(band);
      } else {
        band.end = j + 1;
      }
      words[j].band = band;
    }

    wordCache.words = words;
    wordCache.bands = bands;
    wordCache.built = true;
  }

  function scheduleRectRebuild() {
    if (wordCache.pending) {
      return;
    }
    wordCache.pending = true;
    window.requestAnimationFrame(function () {
      wordCache.pending = false;
      rebuildWordRects();
    });
  }

  /* The band whose vertical range is closest to the pointer. */
  function bandForPoint(y) {
    var bands = wordCache.bands;
    var best = null;
    var bestGap = Infinity;
    for (var i = 0; i < bands.length; i++) {
      var band = bands[i];
      var gap = y < band.top ? band.top - y : (y > band.bottom ? y - band.bottom : 0);
      if (gap < bestGap) {
        bestGap = gap;
        best = band;
      }
    }
    if (!best || bestGap > BAND_SLACK + 40) {
      return null;
    }
    return best;
  }

  /* The nearest word, found anisotropically and inside one line band. */
  function findNearestWord(clientX, clientY) {
    if (!wordCache.built) {
      rebuildWordRects();
    }
    var px = clientX + (window.scrollX || 0);
    var py = clientY + (window.scrollY || 0);
    var band = bandForPoint(py);
    if (!band) {
      return null;
    }
    var best = null;
    var bestScore = Infinity;
    for (var i = band.start; i < band.end; i++) {
      var word = wordCache.words[i];
      var vDist = py < word.top ? word.top - py : (py > word.bottom ? py - word.bottom : 0);
      var hDist = px < word.left ? word.left - px : (px > word.right ? px - word.right : 0);
      var score = hDist + VERTICAL_WEIGHT * vDist;
      if (score < bestScore) {
        bestScore = score;
        best = word;
      }
    }
    return best;
  }

  /* ------------------------------------------------- hover and cursor */

  function setHoveredWord(entry) {
    var previous = state.hovered;
    if (previous && previous.el) {
      previous.el.classList.remove('is-hover');
    }
    state.hovered = entry || null;
    if (entry && entry.el) {
      entry.el.classList.add('is-hover');
    }
  }

  function setCursorWord(paraNode, index) {
    if (state.cursor && state.cursor.el) {
      state.cursor.el.classList.remove('is-cursor');
    }
    var words = paraNode ? $$('.w', paraNode) : [];
    if (!words.length) {
      state.cursor = null;
      return null;
    }
    var bounded = Math.max(0, Math.min(index, words.length - 1));
    var word = words[bounded];
    word.classList.add('is-cursor');
    state.cursor = { el: word, index: bounded, para: paraNode, total: words.length };
    announce('Word ' + (bounded + 1) + ' of ' + words.length + ': ' + word.textContent);
    return state.cursor;
  }

  /* ============================================================ rendering */

  function renderSectionHead(section, accentIndex) {
    var head = make('div', { class: 'section-head' });

    var toggle = make('button', {
      class: 'section-toggle',
      type: 'button',
      'aria-expanded': 'false',
      'aria-controls': 'body-' + section.id,
      id: 'toggle-' + section.id
    });
    var chevron = make('span', { class: 'chev', 'aria-hidden': 'true', text: '›' });
    toggle.appendChild(chevron);
    toggle.appendChild(make('span', { text: section.title }));
    toggle.addEventListener('click', function () {
      toggleSection(section.id);
    });
    head.appendChild(toggle);

    head.appendChild(make('span', { class: 'section-level', text: 'Level ' + section.level }));

    var tools = make('div', { class: 'section-tools' });
    var understood = make('button', {
      class: 'btn btn-sm',
      type: 'button',
      id: 'understood-' + section.id,
      text: 'Mark understood'
    });
    understood.addEventListener('click', function () {
      toggleUnderstood(section.id);
    });
    tools.appendChild(understood);

    var confused = make('button', {
      class: 'btn btn-sm',
      type: 'button',
      id: 'confused-' + section.id,
      text: "I'm confused"
    });
    confused.addEventListener('click', function () {
      revealConfusion(section.id);
    });
    tools.appendChild(confused);
    head.appendChild(tools);

    return head;
  }

  function renderPrediction(section) {
    var card = make('div', { class: 'predict', id: 'predict-' + section.id });
    card.appendChild(make('p', { class: 'predict-q', text: section.prediction.question }));
    var answer = make('p', { class: 'predict-a', id: 'predict-answer-' + section.id, hidden: true });
    answer.appendChild(make('span', { text: section.prediction.answer }));
    card.appendChild(answer);
    var button = make('button', {
      class: 'btn btn-sm',
      type: 'button',
      text: 'Reveal the answer'
    });
    button.addEventListener('click', function () {
      answer.hidden = false;
      button.disabled = true;
      button.textContent = 'Answer revealed';
      announce('Prediction answer revealed.');
    });
    card.appendChild(button);
    return card;
  }

  function renderStudyAid(section) {
    var box = make('div', { class: 'aid' });
    var label = make('div', { class: 'aid-label' });
    label.appendChild(make('span', { text: 'Why this matters' }));
    label.appendChild(aiBadge());
    box.appendChild(label);
    box.appendChild(make('p', { text: section.studyAid.whyItMatters }));
    return box;
  }

  function renderConfusion(section) {
    var box = make('div', { class: 'confusion', id: 'confusion-' + section.id });
    var label = make('div', { class: 'aid-label' });
    label.appendChild(make('span', { text: 'Unpack it' }));
    label.appendChild(aiBadge());
    box.appendChild(label);
    box.appendChild(
      make('p', {
        class: 'sim-note',
        id: 'confusion-hint-' + section.id,
        text: 'Press "I\'m confused" to unpack this section in three steps: plain English, then Arabic, then an analogy.'
      })
    );

    var steps = [
      { key: 'simpleEnglish', label: 'In plain English', text: section.confusion.simpleEnglish },
      { key: 'simpleArabic', label: 'In Arabic', text: section.confusion.simpleArabic },
      { key: 'analogy', label: 'As an analogy', text: section.confusion.analogy }
    ];

    steps.forEach(function (step, index) {
      var node = make('div', {
        class: 'confusion-step' + (step.key === 'simpleArabic' ? ' ar-block' : ''),
        id: (step.key === 'simpleArabic' ? 'ar-confusion-' : 'confusion-step-') + section.id + '-' + index,
        hidden: true
      });
      node.appendChild(make('div', { class: 'pop-label', text: step.label }));
      if (step.key === 'simpleArabic') {
        node.appendChild(make('p', { class: 'ar', lang: 'ar', dir: 'rtl', text: step.text }));
      } else {
        node.appendChild(make('p', { text: step.text }));
      }
      box.appendChild(node);
    });

    return box;
  }

  function renderParagraph(paragraph, sectionId, index) {
    var key = paraKey(sectionId, index);
    var wrap = make('div', { class: 'para-wrap', 'data-para-key': key, 'data-para-index': String(index) });
    var text = paragraph.text || '';
    var tokens = tokenize(text);
    var hits = matchGlossary(tokens);

    var para = make('p', { class: 'para' });
    para.setAttribute('aria-label', text);
    para.setAttribute('tabindex', '0');
    para.setAttribute('data-para-key', key);

    if (paragraph.kind === 'list') {
      para.classList.add('list-para');
      para.appendChild(buildWordSpans(text, tokens, hits));
      wrap.appendChild(para);
      var list = make('ul');
      (paragraph.items || []).forEach(function (item) {
        var itemTokens = tokenize(item);
        var itemHits = matchGlossary(itemTokens);
        var li = make('li');
        var itemPara = make('p', { class: 'para' });
        itemPara.setAttribute('aria-label', item);
        itemPara.setAttribute('tabindex', '0');
        itemPara.setAttribute('data-para-key', key + ':' + list.children.length);
        itemPara.appendChild(buildWordSpans(item, itemTokens, itemHits));
        li.appendChild(itemPara);
        list.appendChild(li);
      });
      wrap.appendChild(list);
    } else if (paragraph.kind === 'code') {
      para.appendChild(buildWordSpans(text, tokens, hits));
      wrap.appendChild(para);
      var pre = make('pre');
      var code = make('code', { text: paragraph.code || '' });
      pre.appendChild(code);
      wrap.appendChild(pre);
    } else if (paragraph.kind === 'formula') {
      para.classList.add('formula-para');
      para.appendChild(buildWordSpans(text, tokens, hits));
      wrap.appendChild(para);
      var formula = make('p', { class: 'formula-para' });
      formula.appendChild(make('code', { text: paragraph.formula || '' }));
      wrap.appendChild(formula);
      if (paragraph.symbols && paragraph.symbols.length) {
        var symbols = make('ul', { class: 'symbols' });
        paragraph.symbols.forEach(function (symbol) {
          symbols.appendChild(make('li', { text: symbol.symbol + ' — ' + symbol.meaning }));
        });
        wrap.appendChild(symbols);
      }
    } else if (paragraph.kind === 'quote') {
      para.classList.add('quote-para');
      para.appendChild(buildWordSpans(text, tokens, hits));
      wrap.appendChild(para);
    } else {
      para.appendChild(buildWordSpans(text, tokens, hits));
      wrap.appendChild(para);
    }

    if (paragraph.explainArabic) {
      var explain = make('div', {
        class: 'ar-explain ar-block',
        id: 'ar-explain-' + sectionId + '-' + index,
        'data-para-key': key,
        hidden: true
      });
      var explainLabel = make('div', { class: 'aid-label' });
      explainLabel.appendChild(make('span', { text: 'In Arabic' }));
      explainLabel.appendChild(aiBadge());
      explain.appendChild(explainLabel);
      explain.appendChild(make('p', { class: 'ar', lang: 'ar', dir: 'rtl', text: paragraph.explainArabic }));
      wrap.appendChild(explain);
    }

    var tools = make('div', { class: 'para-tools' });
    if (paragraph.explainArabic) {
      var explainButton = make('button', {
        class: 'btn btn-sm',
        type: 'button',
        text: 'Explain',
        'data-explain-for': key,
        'aria-expanded': 'false'
      });
      explainButton.addEventListener('click', function () {
        toggleParagraphExplain(key);
      });
      tools.appendChild(explainButton);
    }
    wrap.appendChild(tools);

    wrap.appendChild(
      make('div', {
        class: 'recall-prompt',
        text: 'Recall mode: the text is hidden. Say the section out loud, then switch back to check.'
      })
    );

    return wrap;
  }

  function renderSkimView(section) {
    var box = make('div', { class: 'section-skim' });
    if (section.keySentences && section.keySentences.length) {
      var keyList = make('ul', { class: 'skim-key' });
      section.keySentences.forEach(function (sentence) {
        keyList.appendChild(make('li', { text: sentence }));
      });
      box.appendChild(keyList);
    }
    if (section.takeaways && section.takeaways.length) {
      box.appendChild(make('div', { class: 'pop-label', text: 'Takeaways' }));
      var takeList = make('ul', { class: 'skim-take' });
      section.takeaways.forEach(function (takeaway) {
        takeList.appendChild(make('li', { text: takeaway }));
      });
      box.appendChild(takeList);
    }
    return box;
  }

  function renderArticle() {
    clear(articleEl);
    var sections = state.chapter.sections.slice().sort(function (a, b) {
      return a.order - b.order;
    });

    sections.forEach(function (section, index) {
      var node = make('section', {
        class: 'chapter-section',
        id: 'section-' + section.id,
        'data-section': section.id,
        'data-accent': String(index % 8),
        'data-open': '1'
      });
      node.appendChild(renderSectionHead(section, index));

      var body = make('div', { class: 'section-body', id: 'body-' + section.id });
      body.appendChild(renderPrediction(section));

      var full = make('div', { class: 'section-full' });
      full.appendChild(renderStudyAid(section));
      full.appendChild(renderConfusion(section));
      section.paragraphs.forEach(function (paragraph, paragraphIndex) {
        full.appendChild(renderParagraph(paragraph, section.id, paragraphIndex));
      });
      body.appendChild(full);
      body.appendChild(renderSkimView(section));

      node.appendChild(body);
      articleEl.appendChild(node);
    });
  }

  /* ============================================================ outline */

  function renderOutline() {
    clear(outlineListEl);
    var sections = state.chapter.sections.slice().sort(function (a, b) {
      return a.order - b.order;
    });
    sections.forEach(function (section) {
      var item = make('li', { class: 'outline-item' });
      var button = make('button', {
        class: 'outline-btn',
        type: 'button',
        id: 'outline-' + section.id,
        'data-section': section.id
      });

      var ring = make('span', { class: 'ring', 'aria-hidden': 'true' });
      ring.style.setProperty('--p', '0');
      button.appendChild(ring);
      button.appendChild(make('span', { class: 'outline-title', text: section.title }));
      button.addEventListener('click', function () {
        focusSection(section.id);
      });
      item.appendChild(button);
      outlineListEl.appendChild(item);
    });
    updateOutline();
  }

  function sectionProgress(sectionId) {
    if (state.understood[sectionId]) {
      return 1;
    }
    if (state.openSections[sectionId]) {
      return 0.55;
    }
    return 0;
  }

  function updateOutline() {
    var sections = state.chapter.sections;
    var total = 0;
    sections.forEach(function (section) {
      total += sectionProgress(section.id);
      var button = document.getElementById('outline-' + section.id);
      if (!button) {
        return;
      }
      var fg = $('.ring', button);
      if (fg) {
        fg.style.setProperty('--p', String(sectionProgress(section.id)));
      }
      button.setAttribute('aria-current', state.currentSection === section.id ? 'true' : 'false');
      var understood = document.getElementById('understood-' + section.id);
      if (understood) {
        understood.setAttribute('aria-pressed', state.understood[section.id] ? 'true' : 'false');
        understood.textContent = state.understood[section.id] ? 'Understood' : 'Mark understood';
      }
    });

    var percent = sections.length ? Math.round((total / sections.length) * 100) : 0;
    var bar = document.getElementById('progress-bar');
    var fill = document.getElementById('progress-fill');
    if (fill) {
      fill.style.width = percent + '%';
    }
    if (bar) {
      bar.setAttribute('aria-valuenow', String(percent));
    }

    var meta = document.getElementById('outline-meta');
    if (meta) {
      var words = 0;
      sections.forEach(function (section) {
        section.paragraphs.forEach(function (paragraph) {
          words += countWords(paragraph.text);
        });
      });
      meta.textContent =
        'About ' + state.chapter.meta.estMinutes + ' min · ' + words + ' words · ' + percent + '% read';
    }
  }

  /* ============================================================ panels */

  function panel(title, body, open) {
    var details = make('details', { class: 'panel' });
    if (open) {
      details.setAttribute('open', 'open');
    }
    details.appendChild(make('summary', { text: title }));
    var inner = make('div', { class: 'panel-body' });
    inner.appendChild(body);
    details.appendChild(inner);
    return details;
  }

  function renderDashboard() {
    var body = make('div');
    var understood = 0;
    state.chapter.sections.forEach(function (section) {
      if (state.understood[section.id]) {
        understood += 1;
      }
    });
    var known = 0;
    state.chapter.glossary.forEach(function (entry) {
      if (state.wordStatus[normalize(entry.term)] === STATUS_KNOWN) {
        known += 1;
      }
    });
    var minutes = Math.max(0, Math.round((Date.now() - state.sessionStart) / 60000));

    var rows = [
      ['Sections understood', understood + ' / ' + state.chapter.sections.length],
      ['Words marked known', known + ' / ' + state.chapter.glossary.length],
      ['Chapter flashcards', String(state.chapter.flashcards.length)],
      ['Your flashcards', String(state.userCards.length)],
      ['Notes', String(state.notes.length)],
      ['Highlights', String(state.highlights.length)],
      ['Quiz items', String(state.chapter.quiz.length)],
      ['Minutes in this session', String(minutes)]
    ];
    rows.forEach(function (row) {
      var line = make('div', { class: 'stat-row' });
      line.appendChild(make('span', { text: row[0] }));
      line.appendChild(make('span', { class: 'stat-val', text: row[1] }));
      body.appendChild(line);
    });

    if (!state.store.available) {
      body.appendChild(
        make('p', {
          class: 'sim-note',
          text: 'Storage is unavailable in this browser, so progress is kept in memory for this session only.'
        })
      );
    }

    var next = nextBestAction();
    body.appendChild(make('div', { class: 'pop-label', text: 'Next best action' }));
    body.appendChild(make('p', { text: next }));

    var toggle = make('label', { class: 'stat-row' });
    var box = make('input', { type: 'checkbox', id: 'hide-known' });
    box.checked = state.hideKnown;
    box.addEventListener('change', function () {
      setHideKnown(box.checked);
    });
    toggle.appendChild(box);
    toggle.appendChild(make('span', { text: 'Show only words I do not know' }));
    body.appendChild(toggle);

    return body;
  }

  function nextBestAction() {
    var unread = null;
    var sections = state.chapter.sections;
    for (var i = 0; i < sections.length; i++) {
      if (!state.understood[sections[i].id]) {
        unread = sections[i];
        break;
      }
    }
    if (unread) {
      return 'Read "' + unread.title + '" and mark it understood.';
    }
    var weak = null;
    state.chapter.glossary.forEach(function (entry) {
      if (!weak && state.wordStatus[normalize(entry.term)] !== STATUS_KNOWN) {
        weak = entry;
      }
    });
    if (weak) {
      return 'Review the word "' + weak.term + '" and mark it known.';
    }
    return 'Every section and every curated word is covered. Revisit the flashcards.';
  }

  function renderGlossaryPanel() {
    var body = make('div');
    var list = make('ul', { class: 'list-plain' });
    state.chapter.glossary.forEach(function (entry) {
      var item = make('li');
      var button = make('button', { class: 'term-btn', type: 'button', text: entry.term });
      button.addEventListener('click', function () {
        jumpToWord(entry.id);
      });
      item.appendChild(button);
      if (entry.technical) {
        item.appendChild(make('span', { class: 'ai-badge', text: 'technical' }));
      }
      item.appendChild(make('div', { class: 'back', text: entry.meaningEn }));
      list.appendChild(item);
    });
    body.appendChild(list);
    return body;
  }

  function renderFlashcardsPanel() {
    var body = make('div');
    var list = make('div', { class: 'card-list' });
    state.chapter.flashcards.forEach(function (card) {
      var details = make('details', { id: 'flashcard-' + card.id });
      details.appendChild(make('summary', { text: card.front }));
      var back = make('div', { class: 'back' });
      back.appendChild(make('p', { text: card.back }));
      if (card.code) {
        var pre = make('pre');
        pre.appendChild(make('code', { text: card.code }));
        back.appendChild(pre);
      }
      if (card.backAr) {
        var ar = make('p', { class: 'ar', lang: 'ar', dir: 'rtl', text: card.backAr });
        back.appendChild(ar);
      }
      details.appendChild(back);
      list.appendChild(details);
    });
    body.appendChild(list);

    if (state.userCards.length) {
      body.appendChild(make('div', { class: 'pop-label', text: 'Your cards' }));
      var mine = make('div', { class: 'card-list' });
      state.userCards.forEach(function (card) {
        var details = make('details', { id: 'usercard-' + card.id });
        details.appendChild(make('summary', { text: card.front }));
        details.appendChild(make('div', { class: 'back', text: card.back }));
        mine.appendChild(details);
      });
      body.appendChild(mine);
    }
    return body;
  }

  function renderLabsPanel() {
    var body = make('div');
    state.chapter.labs.forEach(function (lab) {
      var card = make('div', { class: 'card-list', id: 'lab-' + lab.id });
      var details = make('details');
      details.appendChild(make('summary', { text: lab.title }));
      var inner = make('div', { class: 'back' });
      inner.appendChild(make('p', { text: lab.goal }));
      inner.appendChild(make('p', { class: 'sim-note', text: lab.simulationNote }));
      var tasks = make('ol');
      lab.tasks.forEach(function (task) {
        var step = make('li');
        step.appendChild(make('p', { text: task.prompt }));
        step.appendChild(make('p', { class: 'sim-note', text: task.check }));
        tasks.appendChild(step);
      });
      inner.appendChild(tasks);
      var takeaway = make('p');
      takeaway.appendChild(document.createTextNode(lab.takeawayEn));
      inner.appendChild(takeaway);
      if (lab.takeawayAr) {
        inner.appendChild(make('p', { class: 'ar', lang: 'ar', dir: 'rtl', text: lab.takeawayAr }));
      }
      details.appendChild(inner);
      card.appendChild(details);
      body.appendChild(card);
    });
    return body;
  }

  function renderConceptsPanel() {
    var body = make('div');
    var map = state.chapter.conceptMap;
    map.nodes.forEach(function (node) {
      var chip = make('span', { class: 'node', id: 'concept-' + node.id, text: node.label });
      chip.setAttribute('role', 'button');
      chip.setAttribute('tabindex', '0');
      chip.addEventListener('click', function () {
        showConceptCard(node);
      });
      chip.addEventListener('keydown', function (event) {
        if (event.key === 'Enter' || event.key === ' ') {
          event.preventDefault();
          showConceptCard(node);
        }
      });
      body.appendChild(chip);
    });
    body.appendChild(make('div', { class: 'pop-label', text: 'Relations' }));
    var relations = make('ul', { class: 'list-plain' });
    map.edges.forEach(function (edge) {
      var from = state.conceptById[edge.from];
      var to = state.conceptById[edge.to];
      relations.appendChild(
        make('li', {
          text: (from ? from.label : edge.from) + ' → ' + (to ? to.label : edge.to) + ' (' + edge.relation + ')'
        })
      );
    });
    body.appendChild(relations);
    return body;
  }

  function renderFiguresPanel() {
    var body = make('div');
    state.chapter.figures.forEach(function (figure) {
      var holder = make('div', { class: 'figure-holder', id: 'figure-' + figure.id });
      var svg = buildSafeSvg(figure.svg);
      if (svg) {
        holder.appendChild(svg);
      }
      body.appendChild(holder);
      body.appendChild(make('p', { text: figure.captionEn }));
      body.appendChild(make('p', { class: 'ar', lang: 'ar', dir: 'rtl', text: figure.captionAr }));
    });
    return body;
  }

  function renderQuizPanel() {
    var body = make('div');
    state.chapter.quiz.forEach(function (item) {
      var details = make('details', { id: 'quiz-' + item.id });
      details.appendChild(make('summary', { text: item.prompt }));
      var inner = make('div', { class: 'back' });
      if (item.options && item.options.length) {
        var options = make('ul');
        item.options.forEach(function (option) {
          options.appendChild(make('li', { text: option }));
        });
        inner.appendChild(options);
      }
      var answer = make('p');
      answer.appendChild(make('strong', { text: 'Answer: ' }));
      answer.appendChild(document.createTextNode(item.answer.join(' | ')));
      inner.appendChild(answer);
      inner.appendChild(make('p', { text: item.explanationEn }));
      inner.appendChild(make('p', { class: 'ar', lang: 'ar', dir: 'rtl', text: item.explanationAr }));
      details.appendChild(inner);
      body.appendChild(details);
    });
    return body;
  }

  function renderExtrasPanel() {
    var body = make('div');
    body.appendChild(make('div', { class: 'pop-label', text: 'Collocations' }));
    var collocations = make('ul', { class: 'list-plain' });
    state.chapter.collocations.forEach(function (item) {
      var entry = make('li');
      entry.appendChild(make('strong', { text: item.phrase }));
      entry.appendChild(make('div', { class: 'ar', lang: 'ar', dir: 'rtl', text: item.meaningAr }));
      if (item.example) {
        entry.appendChild(make('div', { class: 'back', text: item.example }));
      }
      collocations.appendChild(entry);
    });
    body.appendChild(collocations);

    body.appendChild(make('div', { class: 'pop-label', text: 'Connected chapters' }));
    var connections = make('ul', { class: 'list-plain' });
    state.chapter.connections.forEach(function (item) {
      var entry = make('li');
      entry.appendChild(make('strong', { text: item.title }));
      if (item.note) {
        entry.appendChild(make('div', { class: 'back', text: item.note }));
      }
      connections.appendChild(entry);
    });
    body.appendChild(connections);

    body.appendChild(make('div', { class: 'pop-label', text: 'Source' }));
    body.appendChild(make('p', { text: state.chapter.meta.sourceTitle }));
    body.appendChild(make('p', { class: 'sim-note', text: state.chapter.meta.attribution }));
    return body;
  }

  function renderPanels() {
    var host = document.getElementById('panels');
    if (!host) {
      return;
    }
    clear(host);
    host.appendChild(panel('Dashboard', renderDashboard(), true));
    host.appendChild(panel('Vocabulary', renderGlossaryPanel(), false));
    host.appendChild(panel('Flashcards', renderFlashcardsPanel(), false));
    host.appendChild(panel('Labs', renderLabsPanel(), false));
    host.appendChild(panel('Concept map', renderConceptsPanel(), false));
    host.appendChild(panel('Figures', renderFiguresPanel(), false));
    host.appendChild(panel('Quiz', renderQuizPanel(), false));
    host.appendChild(panel('Notes and highlights', renderNotesPanel(), false));
    host.appendChild(panel('Collocations, connections, credits', renderExtrasPanel(), false));
  }

  function renderNotesPanel() {
    var body = make('div');
    if (!state.notes.length && !state.highlights.length) {
      body.appendChild(make('p', { class: 'sim-note', text: 'Nothing saved yet.' }));
      return body;
    }
    state.notes.forEach(function (note, index) {
      var entry = make('div', { class: 'card-list' });
      var details = make('details');
      details.appendChild(make('summary', { text: note.text }));
      details.appendChild(make('div', { class: 'back', text: note.note }));
      entry.appendChild(details);
      body.appendChild(entry);
    });
    return body;
  }

  function refreshDashboard() {
    var host = document.getElementById('panels');
    if (!host) {
      return;
    }
    var first = host.querySelector('.panel');
    if (!first) {
      return;
    }
    var body = $('.panel-body', first);
    if (!body) {
      return;
    }
    var fresh = renderDashboard();
    clear(body);
    while (fresh.firstChild) {
      body.appendChild(fresh.firstChild);
    }
  }

  /* ============================================================ behaviour */

  function toggleSection(sectionId) {
    if (state.readingMode === 'focus') {
      var wasOpen = !!state.openSections[sectionId];
      state.openSections = {};
      if (!wasOpen) {
        state.openSections[sectionId] = true;
        state.currentSection = sectionId;
      } else {
        state.currentSection = null;
      }
    } else {
      state.openSections[sectionId] = !state.openSections[sectionId];
    }
    applySectionStates();
  }

  function focusSection(sectionId) {
    if (state.readingMode === 'focus') {
      state.openSections = {};
      state.openSections[sectionId] = true;
      state.currentSection = sectionId;
      applySectionStates();
    }
    var node = document.getElementById('section-' + sectionId);
    if (node) {
      node.scrollIntoView({ block: 'start' });
      var toggle = document.getElementById('toggle-' + sectionId);
      if (toggle) {
        toggle.focus({ preventScroll: true });
      }
    }
    announce('Section: ' + (sectionById(sectionId) || {}).title);
  }

  function applySectionStates() {
    $$('.chapter-section', articleEl).forEach(function (node) {
      var id = node.getAttribute('data-section');
      var open = !!state.openSections[id];
      node.setAttribute('data-open', open ? '1' : '0');
      var toggle = document.getElementById('toggle-' + id);
      if (toggle) {
        toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      }
      var answer = document.getElementById('predict-answer-' + id);
      var button = $('#predict-' + id + ' .btn');
      if (answer && button) {
        /* The answer stays locked until the section is open and read. */
        button.disabled = !open;
        if (!open) {
          answer.hidden = true;
          button.textContent = 'Reveal the answer';
        }
      }
    });
    updateOutline();
  }

  function toggleUnderstood(sectionId) {
    state.understood[sectionId] = !state.understood[sectionId];
    state.store.set('understood', state.understood);
    updateOutline();
    refreshDashboard();
    announce(state.understood[sectionId] ? 'Marked as understood.' : 'Marked as not understood.');
  }

  function revealConfusion(sectionId) {
    var step = state.confusionStep[sectionId] || 0;
    var node = document.getElementById('confusion-step-' + sectionId + '-' + step) ||
      document.getElementById('ar-confusion-' + sectionId + '-' + step);
    if (!node) {
      return;
    }
    node.hidden = false;
    state.confusionStep[sectionId] = step + 1;
    var hint = document.getElementById('confusion-hint-' + sectionId);
    if (hint) {
      hint.hidden = true;
    }
    var button = document.getElementById('confused-' + sectionId);
    if (button) {
      var labels = ["I'm confused", 'Show the simpler version', 'Show the Arabic', 'Show the analogy'];
      button.textContent = labels[Math.min(state.confusionStep[sectionId], labels.length - 1)];
    }
    announce('Unpacked step ' + (step + 1) + '.');
  }

  function toggleParagraphExplain(key) {
    state.explainOpen[key] = !state.explainOpen[key];
    var block = document.querySelector('.ar-explain[data-para-key="' + key + '"]');
    var button = document.querySelector('[data-explain-for="' + key + '"]');
    if (block) {
      block.hidden = !state.explainOpen[key];
    }
    if (button) {
      button.setAttribute('aria-expanded', state.explainOpen[key] ? 'true' : 'false');
    }
  }

  function setLanguageMode(mode) {
    if (LANG_MODES.indexOf(mode) === -1) {
      mode = 'en';
    }
    state.langMode = mode;
    document.body.setAttribute('data-lang-mode', mode);
    document.body.classList.toggle('lang-ar-visible', mode === 'en-hints' || mode === 'ar');
    var select = document.getElementById('lang-mode');
    if (select) {
      select.value = mode;
    }
    $$('.ar-explain', articleEl).forEach(function (block) {
      var key = block.getAttribute('data-para-key');
      var open = mode === 'ar' || !!state.explainOpen[key];
      block.hidden = !open;
      var button = document.querySelector('[data-explain-for="' + key + '"]');
      if (button) {
        button.setAttribute('aria-expanded', open ? 'true' : 'false');
      }
    });
    state.store.set('langMode', mode);
    scheduleRectRebuild();
  }

  function setReadingMode(mode) {
    if (READING_MODES.indexOf(mode) === -1) {
      mode = 'focus';
    }
    state.readingMode = mode;
    document.body.setAttribute('data-reading-mode', mode);
    var select = document.getElementById('reading-mode');
    if (select) {
      select.value = mode;
    }
    if (mode === 'focus') {
      if (!state.currentSection) {
        state.currentSection = state.chapter.sections[0].id;
      }
      state.openSections = {};
      state.openSections[state.currentSection] = true;
    } else {
      state.openSections = {};
      state.chapter.sections.forEach(function (section) {
        state.openSections[section.id] = true;
      });
    }
    applySectionStates();
    state.store.set('readingMode', mode);
    scheduleRectRebuild();
  }

  function setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    var select = document.getElementById('theme');
    if (select) {
      select.value = theme;
    }
    globalStore.set('theme', theme);
    scheduleRectRebuild();
  }

  function setHideKnown(value) {
    state.hideKnown = !!value;
    document.body.classList.toggle('hide-known', state.hideKnown);
    state.store.set('hideKnown', state.hideKnown);
  }

  /* ============================================================ speech */

  var speech = {
    supported: typeof window.speechSynthesis !== 'undefined' && typeof window.SpeechSynthesisUtterance !== 'undefined',
    voices: [],
    ready: false
  };

  function refreshVoices() {
    if (!speech.supported) {
      return;
    }
    var voices = [];
    try {
      voices = window.speechSynthesis.getVoices() || [];
    } catch (err) {
      voices = [];
    }
    speech.voices = voices;
    if (voices.length) {
      speech.ready = true;
      $$('#word-popover select[data-voice-select]').forEach(function (select) {
        fillVoiceSelect(select);
      });
    }
  }

  function fillVoiceSelect(select) {
    clear(select);
    var preferred = speech.voices.filter(function (voice) {
      var lang = (voice.lang || '').toLowerCase();
      return lang.indexOf('en-us') === 0 || lang.indexOf('en-gb') === 0;
    });
    var list = preferred.length ? preferred : speech.voices;
    list.forEach(function (voice) {
      select.appendChild(make('option', { value: voice.voiceURI, text: voice.name + ' (' + voice.lang + ')' }));
    });
    select.hidden = false;
  }

  function initSpeech() {
    if (!speech.supported) {
      return;
    }
    refreshVoices();
    try {
      if (typeof window.speechSynthesis.addEventListener === 'function') {
        window.speechSynthesis.addEventListener('voiceschanged', refreshVoices);
      } else {
        window.speechSynthesis.onvoiceschanged = refreshVoices;
      }
    } catch (err) {
      /* a browser without the event still speaks with the default voice */
    }
  }

  function speak(text, options) {
    if (!speech.supported) {
      return false;
    }
    try {
      var utterance = new window.SpeechSynthesisUtterance(text);
      utterance.lang = 'en-US';
      if (options && options.rate) {
        utterance.rate = options.rate;
      }
      if (options && options.voiceURI) {
        speech.voices.forEach(function (voice) {
          if (voice.voiceURI === options.voiceURI) {
            utterance.voice = voice;
            utterance.lang = voice.lang || 'en-US';
          }
        });
      }
      window.speechSynthesis.cancel();
      window.speechSynthesis.speak(utterance);
      return true;
    } catch (err) {
      return false;
    }
  }

  /* ============================================================ popover */

  function closePopover() {
    if (popoverEl) {
      popoverEl.hidden = true;
      clear(popoverEl);
    }
  }

  function closeMiniCard() {
    if (miniCardEl) {
      miniCardEl.hidden = true;
      clear(miniCardEl);
    }
  }

  function positionFloating(node, rect) {
    var width = node.offsetWidth || 320;
    var height = node.offsetHeight || 200;
    var left = rect.left + rect.width / 2 - width / 2;
    var top = rect.bottom + 10;
    if (left < 8) {
      left = 8;
    }
    if (left + width > window.innerWidth - 8) {
      left = window.innerWidth - width - 8;
    }
    if (top + height > window.innerHeight - 8) {
      top = Math.max(8, rect.top - height - 10);
    }
    node.style.left = Math.round(left) + 'px';
    node.style.top = Math.round(top) + 'px';
  }

  function popoverRow(label, text, extraClass) {
    var row = make('div', { class: 'pop-row' });
    row.appendChild(make('div', { class: 'pop-label', text: label }));
    var body = make('p', { class: extraClass || null, text: text });
    row.appendChild(body);
    return row;
  }

  function openWordPopover(wordEl) {
    if (!wordEl || !popoverEl) {
      return;
    }
    var text = wordEl.textContent;
    var entry = null;
    var wordId = wordEl.getAttribute('data-word-id');
    if (wordId) {
      entry = state.glossaryById[wordId];
    }
    var paragraph = wordEl.closest('.para');
    var explainBlock = null;
    if (paragraph) {
      var key = paragraph.getAttribute('data-para-key');
      explainBlock = document.querySelector('.ar-explain[data-para-key="' + key + '"]');
    }

    clear(popoverEl);
    var head = make('div', { class: 'pop-head' });
    head.appendChild(make('span', { class: 'pop-word', text: text }));
    if (entry && entry.ipa) {
      head.appendChild(make('span', { class: 'pop-ipa', text: '/' + entry.ipa + '/' }));
    }
    if (entry) {
      head.appendChild(make('span', { class: 'pop-type', text: entry.wordType }));
    }
    popoverEl.appendChild(head);

    /* pronunciation */
    if (speech.supported) {
      var speakRow = make('div', { class: 'speak-row' });
      var playButton = make('button', { class: 'btn btn-sm', type: 'button', id: 'speak-btn', text: 'Play' });
      var handler = function () {
        var rate = 0.95;
        var voiceURI = '';
        var rateInput = popoverEl.querySelector('input[data-rate]');
        var voiceSelect = popoverEl.querySelector('select[data-voice-select]');
        if (rateInput) {
          rate = parseFloat(rateInput.value) || 0.95;
        }
        if (voiceSelect && !voiceSelect.hidden) {
          voiceURI = voiceSelect.value;
        }
        speak(text, { rate: rate, voiceURI: voiceURI });
        announce('Playing: ' + text);
      };
      playButton.addEventListener('click', handler);
      playButton.setAttribute('data-wired', '1');
      playButton.__speakHandler = handler;
      speakRow.appendChild(playButton);

      var rateLabel = make('label', { text: 'Rate' });
      var rateInput = make('input', {
        type: 'range',
        min: '0.5',
        max: '1.5',
        step: '0.05',
        value: '0.95',
        'data-rate': '1'
      });
      rateInput.style.minHeight = '32px';
      rateLabel.appendChild(rateInput);
      speakRow.appendChild(rateLabel);

      var voiceSelect = make('select', { 'data-voice-select': '1', hidden: true });
      voiceSelect.setAttribute('aria-label', 'Voice');
      if (speech.ready && speech.voices.length) {
        fillVoiceSelect(voiceSelect);
      }
      speakRow.appendChild(voiceSelect);
      popoverEl.appendChild(speakRow);
    } else {
      var fallback = make('div', { class: 'speak-fallback', 'data-speech-fallback': '1' });
      fallback.appendChild(
        make('span', { text: 'This browser cannot play pronunciation. The meaning below is the same.' })
      );
      popoverEl.appendChild(fallback);
    }

    if (entry) {
      popoverEl.appendChild(popoverRow('In plain English', entry.meaningEn));
      var arRow = make('div', { class: 'pop-row' });
      arRow.appendChild(make('div', { class: 'pop-label', text: 'In Arabic' }));
      arRow.appendChild(make('p', { class: 'ar', lang: 'ar', dir: 'rtl', text: entry.meaningAr }));
      popoverEl.appendChild(arRow);
      if (entry.example) {
        popoverEl.appendChild(popoverRow('Example', entry.example, 'pop-example'));
      }
      if (entry.conceptId || entry.labId) {
        var links = make('div', { class: 'mini-links' });
        if (entry.conceptId) {
          links.appendChild(make('a', { href: '#concept-' + entry.conceptId, text: 'Concept node' }));
        }
        if (entry.labId) {
          links.appendChild(make('a', { href: '#lab-' + entry.labId, text: 'Lab' }));
        }
        popoverEl.appendChild(links);
      }
    } else {
      popoverEl.appendChild(
        popoverRow('Glossary', 'This word is not in the curated glossary, so it carries no entry.')
      );
      if (explainBlock) {
        var arabicNode = explainBlock.querySelector('.ar');
        var arabicText = arabicNode ? arabicNode.textContent : '';
        var paraRow = make('div', { class: 'pop-row' });
        paraRow.appendChild(make('div', { class: 'pop-label', text: 'Arabic explanation of this paragraph' }));
        paraRow.appendChild(make('p', { class: 'ar', lang: 'ar', dir: 'rtl', text: arabicText }));
        popoverEl.appendChild(paraRow);
      }
    }

    var actions = make('div', { class: 'pop-actions' });
    var addCard = make('button', { class: 'btn btn-sm', type: 'button', text: 'Add to flashcards' });
    addCard.addEventListener('click', function () {
      addUserCard(text, entry ? entry.meaningEn : (explainBlock ? explainBlock.textContent : text));
      announce('Added to your flashcards.');
    });
    actions.appendChild(addCard);

    var markKnown = make('button', { class: 'btn btn-sm', type: 'button', text: 'Mark as known' });
    markKnown.addEventListener('click', function () {
      setWordStatus(text, STATUS_KNOWN);
      announce(text + ' marked as known.');
    });
    actions.appendChild(markKnown);

    var explainArabic = make('button', { class: 'btn btn-sm', type: 'button', text: 'Explain in Arabic' });
    explainArabic.addEventListener('click', function () {
      if (explainBlock) {
        explainBlock.hidden = false;
        state.explainOpen[explainBlock.getAttribute('data-para-key')] = true;
        explainBlock.scrollIntoView({ block: 'center' });
      } else if (entry) {
        var arRow2 = popoverEl.querySelector('.ar');
        if (arRow2) {
          arRow2.scrollIntoView({ block: 'nearest' });
        }
      }
    });
    actions.appendChild(explainArabic);
    popoverEl.appendChild(actions);

    popoverEl.hidden = false;
    positionFloating(popoverEl, wordEl.getBoundingClientRect());
    var firstButton = popoverEl.querySelector('button');
    if (firstButton) {
      firstButton.focus({ preventScroll: true });
    }
  }

  function showConceptCard(node) {
    if (!miniCardEl) {
      return;
    }
    clear(miniCardEl);
    miniCardEl.appendChild(make('div', { class: 'pop-word', text: node.label }));
    miniCardEl.appendChild(make('div', { class: 'pop-type', text: node.kind }));
    if (node.definition) {
      miniCardEl.appendChild(popoverRow('Definition', node.definition));
    }
    if (node.sectionId) {
      var link = make('a', { href: '#section-' + node.sectionId, text: 'Open the section' });
      var links = make('div', { class: 'mini-links' });
      links.appendChild(link);
      miniCardEl.appendChild(links);
    }
    miniCardEl.hidden = false;
    positionFloating(miniCardEl, document.getElementById('concept-' + node.id).getBoundingClientRect());
  }

  function setWordStatus(wordText, status) {
    var key = normalize(wordText);
    state.wordStatus[key] = status;
    state.store.set('wordStatus', state.wordStatus);
    $$('.w[data-word-id]', articleEl).forEach(function (span) {
      applyWordStatus(span, span.textContent);
    });
    refreshDashboard();
  }

  function addUserCard(front, back) {
    var card = {
      id: 'u' + (state.userCards.length + 1),
      front: front,
      back: back,
      kind: 'term'
    };
    state.userCards.push(card);
    state.store.set('userCards', state.userCards);
    renderPanels();
    refreshDashboard();
  }

  /* ============================================================ selection */

  function selectedWordRange() {
    var selection = window.getSelection();
    if (!selection || selection.isCollapsed || selection.rangeCount === 0) {
      return null;
    }
    var range = selection.getRangeAt(0);
    if (!articleEl.contains(range.commonAncestorContainer)) {
      return null;
    }
    var startEl = closestWord(range.startContainer);
    var endEl = closestWord(range.endContainer);
    if (!startEl || !endEl) {
      return null;
    }
    var all = $$('.w', articleEl);
    var from = all.indexOf(startEl);
    var to = all.indexOf(endEl);
    if (from === -1 || to === -1) {
      return null;
    }
    if (from > to) {
      var swap = from;
      from = to;
      to = swap;
    }
    return {
      from: from,
      to: to,
      text: selection.toString().trim(),
      paragraph: startEl.closest('.para'),
      rect: range.getBoundingClientRect()
    };
  }

  function closestWord(node) {
    var element = node.nodeType === 1 ? node : node.parentNode;
    while (element && element !== document.body) {
      if (element.classList && element.classList.contains('w')) {
        return element;
      }
      element = element.parentNode;
    }
    return null;
  }

  function hideToolbar() {
    if (toolbarEl) {
      toolbarEl.hidden = true;
      clear(toolbarEl);
    }
  }

  function showToolbar() {
    var picked = selectedWordRange();
    if (!picked || !picked.text || !toolbarEl) {
      hideToolbar();
      return;
    }
    clear(toolbarEl);

    HIGHLIGHT_COLORS.forEach(function (color) {
      var swatch = make('button', {
        class: 'swatch',
        type: 'button',
        'data-color': color,
        'aria-label': 'Highlight in ' + color
      });
      swatch.addEventListener('click', function () {
        applyHighlight(picked, color);
        hideToolbar();
      });
      toolbarEl.appendChild(swatch);
    });

    var noteButton = make('button', { class: 'btn btn-sm', type: 'button', text: 'Add note' });
    noteButton.addEventListener('click', function () {
      showNoteEntry(toolbarEl, picked);
    });
    toolbarEl.appendChild(noteButton);

    var explainButton = make('button', { class: 'btn btn-sm', type: 'button', text: 'Explain in Arabic' });
    explainButton.addEventListener('click', function () {
      explainSelectionInArabic(picked);
      hideToolbar();
    });
    toolbarEl.appendChild(explainButton);

    var cardButton = make('button', { class: 'btn btn-sm', type: 'button', text: 'Add to flashcards' });
    cardButton.addEventListener('click', function () {
      var back = 'Selected from ' + (picked.paragraph ? picked.paragraph.getAttribute('data-para-key') : 'the chapter');
      addUserCard(picked.text, back);
      hideToolbar();
    });
    toolbarEl.appendChild(cardButton);

    toolbarEl.hidden = false;
    positionFloating(toolbarEl, picked.rect);
  }

  function showNoteEntry(host, picked) {
    var entry = make('div', { class: 'note-entry' });
    var input = make('input', { type: 'text', 'aria-label': 'Note text', placeholder: 'Your note' });
    var save = make('button', { class: 'btn btn-sm', type: 'button', text: 'Save' });
    save.addEventListener('click', function () {
      var value = input.value.trim();
      if (!value) {
        return;
      }
      var note = {
        text: picked.text,
        note: value,
        paraKey: picked.paragraph ? picked.paragraph.getAttribute('data-para-key') : '',
        from: picked.from,
        to: picked.to
      };
      state.notes.push(note);
      state.store.set('notes', state.notes);
      renderPanels();
      refreshDashboard();
      announce('Note saved.');
      hideToolbar();
    });
    entry.appendChild(input);
    entry.appendChild(save);
    host.appendChild(entry);
    input.focus();
  }

  function explainSelectionInArabic(picked) {
    var para = picked.paragraph;
    if (!para) {
      return;
    }
    var key = para.getAttribute('data-para-key');
    var block = document.querySelector('.ar-explain[data-para-key="' + key + '"]');
    if (block) {
      block.hidden = false;
      state.explainOpen[key] = true;
      block.scrollIntoView({ block: 'center' });
      announce('Arabic explanation shown.');
    } else {
      announce('This paragraph has no Arabic explanation.');
    }
  }

  function applyHighlight(picked, color) {
    var words = $$('.w', articleEl);
    for (var i = picked.from; i <= picked.to && i < words.length; i++) {
      HIGHLIGHT_COLORS.forEach(function (name) {
        words[i].classList.remove('hl-' + name);
      });
      words[i].classList.add('hl-' + color);
    }
    var paraKey = picked.paragraph ? picked.paragraph.getAttribute('data-para-key') : '';
    state.highlights.push({
      paraKey: paraKey,
      from: picked.from,
      to: picked.to,
      color: color
    });
    state.store.set('highlights', state.highlights);
    refreshDashboard();
  }

  function restoreHighlights() {
    state.highlights.forEach(function (mark) {
      var words = $$('.w', articleEl);
      for (var i = mark.from; i <= mark.to && i < words.length; i++) {
        words[i].classList.add('hl-' + mark.color);
      }
    });
  }

  /* ============================================================ palette */

  function paletteItems() {
    var items = [];
    state.chapter.sections.forEach(function (section) {
      items.push({
        kind: 'Section',
        label: section.title,
        hint: 'Section ' + section.order,
        run: function () {
          focusSection(section.id);
        }
      });
    });
    state.chapter.glossary.forEach(function (entry) {
      items.push({
        kind: 'Word',
        label: entry.term,
        hint: entry.wordType,
        run: function () {
          jumpToWord(entry.id);
        }
      });
    });
    state.chapter.flashcards.forEach(function (card) {
      items.push({
        kind: 'Flashcard',
        label: card.front,
        hint: card.kind,
        run: function () {
          openDetails('flashcard-' + card.id);
        }
      });
    });
    state.userCards.forEach(function (card) {
      items.push({
        kind: 'Flashcard',
        label: card.front,
        hint: 'yours',
        run: function () {
          openDetails('usercard-' + card.id);
        }
      });
    });
    state.chapter.labs.forEach(function (lab) {
      items.push({
        kind: 'Lab',
        label: lab.title,
        hint: lab.kind,
        run: function () {
          openDetails('lab-' + lab.id);
        }
      });
    });
    state.chapter.conceptMap.nodes.forEach(function (node) {
      items.push({
        kind: 'Concept',
        label: node.label,
        hint: node.kind,
        run: function () {
          showConceptCard(node);
        }
      });
    });
    state.chapter.quiz.forEach(function (item) {
      items.push({
        kind: 'Quiz',
        label: item.prompt,
        hint: item.type,
        run: function () {
          openDetails('quiz-' + item.id);
        }
      });
    });
    return items;
  }

  function openDetails(id) {
    var node = document.getElementById(id);
    if (!node) {
      return;
    }
    if (node.tagName === 'DETAILS') {
      node.open = true;
    }
    var panel = node.closest('details.panel');
    if (panel) {
      panel.open = true;
    }
    node.scrollIntoView({ block: 'center' });
    announce('Jumped to ' + id);
  }

  function jumpToWord(wordId) {
    var target = document.querySelector('.w[data-word-id="' + wordId + '"]');
    if (!target) {
      announce('That word is not used in the running text.');
      return;
    }
    target.scrollIntoView({ block: 'center' });
    window.setTimeout(function () {
      openWordPopover(target);
    }, 60);
  }

  function renderPalette(query) {
    var items = state.paletteItems;
    var lowered = (query || '').toLowerCase().trim();
    var matches = items.filter(function (item) {
      if (!lowered) {
        return true;
      }
      return (item.label + ' ' + item.hint + ' ' + item.kind).toLowerCase().indexOf(lowered) !== -1;
    });
    clear(paletteListEl);
    state.paletteIndex = 0;
    matches.slice(0, 60).forEach(function (item, index) {
      var node = make('li', {
        class: 'palette-item',
        role: 'option',
        id: 'palette-item-' + index,
        'aria-selected': index === 0 ? 'true' : 'false'
      });
      node.appendChild(make('span', { class: 'palette-kind', text: item.kind }));
      node.appendChild(make('span', { text: item.label }));
      node.addEventListener('click', function () {
        closePalette();
        item.run();
      });
      paletteListEl.appendChild(node);
    });
    if (!matches.length) {
      paletteListEl.appendChild(make('li', { class: 'palette-item', text: 'Nothing matches.' }));
    }
  }

  function movePaletteSelection(delta) {
    var items = $$('.palette-item', paletteListEl);
    if (!items.length) {
      return;
    }
    items.forEach(function (item) {
      item.setAttribute('aria-selected', 'false');
    });
    state.paletteIndex = (state.paletteIndex + delta + items.length) % items.length;
    var current = items[state.paletteIndex];
    current.setAttribute('aria-selected', 'true');
    current.scrollIntoView({ block: 'nearest' });
  }

  function openPalette() {
    state.paletteItems = paletteItems();
    renderPalette('');
    paletteOverlayEl.hidden = false;
    paletteInputEl.value = '';
    paletteInputEl.focus();
    announce('Command palette open.');
  }

  function closePalette() {
    if (paletteOverlayEl) {
      paletteOverlayEl.hidden = true;
    }
  }

  /* ============================================================ events */

  function bindEvents() {
    var pointer = { x: null, y: null };
    var rafId = 0;

    articleEl.addEventListener('pointermove', function (event) {
      /* No layout read here: only the pointer coordinates are stored. */
      pointer.x = event.clientX;
      pointer.y = event.clientY;
      if (rafId === 0) {
        rafId = window.requestAnimationFrame(function () {
          rafId = 0;
          if (pointer.x === null) {
            return;
          }
          var found = findNearestWord(pointer.x, pointer.y);
          setHoveredWord(found);
        });
      }
    });

    articleEl.addEventListener('pointerleave', function () {
      setHoveredWord(null);
    });

    articleEl.addEventListener('click', function (event) {
      var badge = event.target.closest ? event.target.closest('.tech-badge') : null;
      if (badge) {
        event.preventDefault();
        openMiniCard(badge.getAttribute('data-word-id'));
        return;
      }
      var word = event.target.closest ? event.target.closest('.w') : null;
      if (word) {
        openWordPopover(word);
        setCursorWord(word.closest('.para'), $$('.w', word.closest('.para')).indexOf(word));
      }
    });

    articleEl.addEventListener('keydown', function (event) {
      if (event.key === 'Escape') {
        closePopover();
        closeMiniCard();
        hideToolbar();
        return;
      }
      var para = event.target.closest ? event.target.closest('.para') : null;
      if (!para) {
        return;
      }
      if (event.key === 'ArrowRight' || event.key === 'ArrowLeft') {
        event.preventDefault();
        var words = $$('.w', para);
        if (!words.length) {
          return;
        }
        var current = state.cursor && state.cursor.para === para ? state.cursor.index : -1;
        var next = current + (event.key === 'ArrowRight' ? 1 : -1);
        if (next < 0) {
          next = 0;
        }
        if (next > words.length - 1) {
          next = words.length - 1;
        }
        setCursorWord(para, next);
      } else if (event.key === 'Enter') {
        event.preventDefault();
        if (state.cursor && state.cursor.el) {
          openWordPopover(state.cursor.el);
        }
      }
    });

    document.addEventListener('mouseup', function () {
      window.setTimeout(function () {
        showToolbar();
      }, 0);
    });

    document.addEventListener('keydown', function (event) {
      if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === 'k') {
        event.preventDefault();
        if (paletteOverlayEl.hidden) {
          openPalette();
        } else {
          closePalette();
        }
        return;
      }
      if (event.key === 'Escape') {
        closePopover();
        closeMiniCard();
        hideToolbar();
        closePalette();
      }
    });

    if (paletteInputEl) {
      paletteInputEl.addEventListener('input', function () {
        renderPalette(paletteInputEl.value);
      });
      paletteInputEl.addEventListener('keydown', function (event) {
        if (event.key === 'ArrowDown') {
          event.preventDefault();
          movePaletteSelection(1);
        } else if (event.key === 'ArrowUp') {
          event.preventDefault();
          movePaletteSelection(-1);
        } else if (event.key === 'Enter') {
          event.preventDefault();
          var items = $$('.palette-item', paletteListEl);
          if (items[state.paletteIndex]) {
            items[state.paletteIndex].click();
          }
        }
      });
    }

    if (paletteOverlayEl) {
      paletteOverlayEl.addEventListener('click', function (event) {
        if (event.target === paletteOverlayEl) {
          closePalette();
        }
      });
    }

    var langSelect = document.getElementById('lang-mode');
    if (langSelect) {
      langSelect.addEventListener('change', function () {
        setLanguageMode(langSelect.value);
        announce('Language mode: ' + langSelect.value);
      });
    }

    var readingSelect = document.getElementById('reading-mode');
    if (readingSelect) {
      readingSelect.addEventListener('change', function () {
        setReadingMode(readingSelect.value);
        announce('Reading mode: ' + readingSelect.value);
      });
    }

    var themeSelect = document.getElementById('theme');
    if (themeSelect) {
      themeSelect.addEventListener('change', function () {
        setTheme(themeSelect.value);
      });
    }

    var paletteButton = document.getElementById('open-palette');
    if (paletteButton) {
      paletteButton.addEventListener('click', function () {
        openPalette();
      });
    }

    window.addEventListener('resize', scheduleRectRebuild);

    var lastScrollHeight = 0;
    var lastArticleHeight = 0;
    window.addEventListener('scroll', function () {
      /* Only rebuild when the scroll changed the layout, not on every tick. */
      var height = document.documentElement.scrollHeight;
      var articleHeight = articleEl.offsetHeight;
      if (height !== lastScrollHeight || articleHeight !== lastArticleHeight) {
        lastScrollHeight = height;
        lastArticleHeight = articleHeight;
        scheduleRectRebuild();
      }
    });

    if (document.fonts && document.fonts.ready && typeof document.fonts.ready.then === 'function') {
      document.fonts.ready.then(function () {
        scheduleRectRebuild();
      });
      if (typeof document.fonts.addEventListener === 'function') {
        document.fonts.addEventListener('loadingdone', scheduleRectRebuild);
      }
    }

    if (typeof window.ResizeObserver === 'function') {
      var observer = new window.ResizeObserver(function () {
        scheduleRectRebuild();
      });
      observer.observe(articleEl);
    }

    var motionQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
    var applyMotion = function () {
      document.body.classList.toggle('reduced-motion', motionQuery.matches);
      document.body.setAttribute('data-reduced-motion', motionQuery.matches ? 'true' : 'false');
    };
    applyMotion();
    if (typeof motionQuery.addEventListener === 'function') {
      motionQuery.addEventListener('change', applyMotion);
    } else if (typeof motionQuery.addListener === 'function') {
      motionQuery.addListener(applyMotion);
    }

    var narrowQuery = window.matchMedia('(max-width: 860px)');
    var applyNarrow = function () {
      document.body.setAttribute('data-narrow', narrowQuery.matches ? 'true' : 'false');
    };
    applyNarrow();
    if (typeof narrowQuery.addEventListener === 'function') {
      narrowQuery.addEventListener('change', applyNarrow);
    } else if (typeof narrowQuery.addListener === 'function') {
      narrowQuery.addListener(applyNarrow);
    }
  }

  function openMiniCard(wordId) {
    if (!miniCardEl) {
      return;
    }
    var entry = state.glossaryById[wordId];
    if (!entry) {
      return;
    }
    clear(miniCardEl);
    miniCardEl.appendChild(make('div', { class: 'pop-word', text: entry.term }));
    miniCardEl.appendChild(make('div', { class: 'pop-type', text: entry.wordType + (entry.technical ? ' · technical' : '') }));
    var row = make('div', { class: 'pop-row' });
    row.appendChild(make('div', { class: 'pop-label', text: 'In Arabic' }));
    row.appendChild(make('p', { class: 'ar', lang: 'ar', dir: 'rtl', text: entry.meaningAr }));
    miniCardEl.appendChild(row);
    if (entry.meaningEn) {
      miniCardEl.appendChild(popoverRow('In plain English', entry.meaningEn));
    }
    var links = make('div', { class: 'mini-links' });
    if (entry.conceptId) {
      links.appendChild(make('a', { href: '#concept-' + entry.conceptId, text: 'Concept node' }));
    }
    if (entry.labId) {
      links.appendChild(make('a', { href: '#lab-' + entry.labId, text: 'Lab' }));
    }
    miniCardEl.appendChild(links);
    miniCardEl.hidden = false;
    var anchor = document.querySelector('.tech-badge[data-word-id="' + wordId + '"]');
    if (anchor) {
      positionFloating(miniCardEl, anchor.getBoundingClientRect());
    }
  }

  /* ============================================================ boot */

  function loadState() {
    state.wordStatus = state.store.get('wordStatus', {}) || {};
    state.notes = state.store.get('notes', []) || [];
    state.highlights = state.store.get('highlights', []) || [];
    state.userCards = state.store.get('userCards', []) || [];
    state.understood = state.store.get('understood', {}) || {};
    state.hideKnown = !!state.store.get('hideKnown', false);
    var savedLang = state.store.get('langMode', 'en');
    var savedReading = state.store.get('readingMode', 'focus');
    var savedTheme = globalStore.get('theme', 'light');
    setTheme(savedTheme);
    setHideKnown(state.hideKnown);
    setLanguageMode(savedLang);
    state.readingMode = savedReading;
    document.body.setAttribute('data-reading-mode', savedReading);
  }

  function boot() {
    state.chapter = readChapterData();
    state.key = state.chapter.meta.chapterId;
    state.store = createStore(STORAGE_ROOT + state.key + '.');

    state.chapter.glossary.forEach(function (entry) {
      state.glossaryById[entry.id] = entry;
      state.glossaryByTerm[normalize(entry.term)] = entry;
    });
    state.chapter.conceptMap.nodes.forEach(function (node) {
      state.conceptById[node.id] = node;
    });
    state.chapter.labs.forEach(function (lab) {
      state.labById[lab.id] = lab;
    });

    articleEl = $('#article');
    outlineListEl = $('#outline-list');
    popoverEl = $('#word-popover');
    miniCardEl = $('#mini-card');
    toolbarEl = $('#sel-toolbar');
    paletteOverlayEl = $('#palette-overlay');
    paletteInputEl = $('#palette-input');
    paletteListEl = $('#palette-list');

    document.getElementById('studio-title').textContent = state.chapter.meta.title;
    document.getElementById('studio-subtitle').textContent = state.chapter.meta.subtitle;
    document.getElementById('studio-source').textContent =
      state.chapter.meta.sourceType + ' · ' + state.chapter.meta.license;
    document.title = state.chapter.meta.title + ' — Study Studio';

    loadState();
    renderArticle();
    renderOutline();
    renderPanels();
    restoreHighlights();
    bindEvents();
    initSpeech();

    if (state.readingMode === 'focus') {
      state.currentSection = state.chapter.sections[0].id;
      state.openSections[state.currentSection] = true;
    } else {
      state.chapter.sections.forEach(function (section) {
        state.openSections[section.id] = true;
      });
    }
    applySectionStates();
    setReadingMode(state.readingMode);

    window.requestAnimationFrame(function () {
      rebuildWordRects();
      if (isSelfTest()) {
        window.setTimeout(runSelfTest, 60);
      }
    });
  }

  function isSelfTest() {
    try {
      return new URLSearchParams(window.location.search).get('selftest') === '1';
    } catch (err) {
      return window.location.search.indexOf('selftest=1') !== -1;
    }
  }

  /* ============================================================ self test */

  function runSelfTest() {
    var results = [];

    function assert(condition, message) {
      if (!condition) {
        throw new Error(message);
      }
    }

    function check(id, name, body) {
      var reason = '';
      try {
        body();
      } catch (err) {
        reason = err && err.message ? err.message : String(err);
      }
      results.push({ id: id, name: name, ok: !reason, reason: reason });
    }

    function visibleParagraph() {
      var paras = $$('.para', articleEl);
      for (var i = 0; i < paras.length; i++) {
        if (paras[i].getBoundingClientRect().height > 0) {
          return paras[i];
        }
      }
      return paras[0] || null;
    }

    function pickWord() {
      rebuildWordRects();
      for (var i = 0; i < wordCache.words.length; i++) {
        if (wordCache.words[i].text && wordCache.words[i].text.length > 3) {
          return wordCache.words[i];
        }
      }
      return wordCache.words[0] || null;
    }

    /* 2 — hover causes no layout shift */
    check('2', 'word hover causes no layout shift', function () {
      var para = visibleParagraph();
      assert(para, 'no visible paragraph was found');
      var word = para.querySelector('.w');
      assert(word, 'no word span was found in the paragraph');
      var before = para.getBoundingClientRect().height;
      word.classList.add('is-hover');
      var after = para.getBoundingClientRect().height;
      word.classList.remove('is-hover');
      var delta = Math.abs(after - before);
      assert(delta <= 1, 'paragraph height changed by ' + delta.toFixed(3) + 'px');
    });

    /* 3 — nearest word is the one under the pointer */
    check('3', 'nearest word is the one under the pointer', function () {
      var word = pickWord();
      assert(word, 'no word was found');
      var rect = word.el.getBoundingClientRect();
      var x = rect.left + rect.width / 2;
      var y = rect.top + rect.height / 2;
      var found = findNearestWord(x, y);
      assert(found, 'the hit test returned no word');
      assert(found.el === word.el, 'picked "' + found.text + '" instead of "' + word.text + '"');
    });

    /* 4 — the popover opens and the play button is wired */
    check('4', 'popover opens and the play button is wired', function () {
      var word = pickWord();
      assert(word, 'no word was found');
      openWordPopover(word.el);
      assert(popoverEl, 'the popover element is missing');
      assert(!popoverEl.hidden, 'the popover stayed hidden after opening');
      var button = popoverEl.querySelector('#speak-btn');
      var fallback = popoverEl.querySelector('[data-speech-fallback]');
      if (speech.supported) {
        assert(button, 'the play button is missing');
        assert(button.getAttribute('data-wired') === '1', 'the play button has no handler');
        assert(typeof button.__speakHandler === 'function', 'the play button handler is not callable');
      } else {
        assert(fallback, 'no graceful fallback was shown for a browser without speech');
      }
      closePopover();
    });

    /* 5 — the four language modes switch */
    check('5', 'all four language modes switch', function () {
      var arabicHint = document.getElementById('ar-confusion-s1-1');
      var arabicExplain = document.getElementById('ar-explain-s1-0');
      assert(arabicHint, 'the Arabic hint probe is missing');
      assert(arabicExplain, 'the Arabic paragraph probe is missing');

      /* reveal the confusion steps so the probe is in a known state */
      var confused = document.getElementById('confused-s1');
      for (var i = 0; i < 3; i++) {
        if (confused) {
          confused.click();
        }
      }

      var expectations = [
        ['en', 'none', 'none'],
        ['en-hints', 'block', 'none'],
        ['ar', 'block', 'block'],
        ['test', 'none', 'none']
      ];
      expectations.forEach(function (row) {
        setLanguageMode(row[0]);
        var hintDisplay = window.getComputedStyle(arabicHint).display;
        var explainDisplay = window.getComputedStyle(arabicExplain).display;
        assert(
          hintDisplay === row[1],
          'mode ' + row[0] + ': Arabic hint display was "' + hintDisplay + '", expected "' + row[1] + '"'
        );
        assert(
          explainDisplay === row[2],
          'mode ' + row[0] + ': Arabic paragraph display was "' + explainDisplay + '", expected "' + row[2] + '"'
        );
      });
      setLanguageMode('en');
    });

    /* 12 — keyboard, reduced motion, mobile */
    check('12', 'keyboard, reduced motion and mobile layout', function () {
      /* keyboard: the main controls are reachable in the tab order */
      var tabbables = $$(
        'a[href], button:not([disabled]), input:not([disabled]), select:not([disabled]), ' +
          'textarea:not([disabled]), [tabindex]:not([tabindex="-1"])',
        document.body
      ).filter(function (node) {
        return node.getClientRects().length > 0;
      });
      var ids = tabbables.map(function (node) {
        return node.id || '';
      });
      ['lang-mode', 'reading-mode', 'theme', 'open-palette', 'toggle-s1', 'understood-s1'].forEach(function (id) {
        assert(ids.indexOf(id) !== -1, 'the tab order never reaches "' + id + '"');
      });

      /* keyboard: arrow keys move the word cursor inside a paragraph */
      var para = visibleParagraph();
      assert(para, 'no visible paragraph was found');
      para.focus();
      var before = state.cursor ? state.cursor.index : -1;
      para.dispatchEvent(new KeyboardEvent('keydown', { key: 'ArrowRight', bubbles: true }));
      var after = state.cursor ? state.cursor.index : -1;
      assert(after === before + 1, 'ArrowRight moved the word cursor from ' + before + ' to ' + after);
      para.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', bubbles: true }));

      /* reduced motion: the static equivalent replaces the scale */
      var word = para.querySelector('.w');
      assert(word, 'no word span was found');
      document.body.classList.add('reduced-motion');
      word.classList.add('is-hover');
      var inner = word.querySelector('.wi');
      var transform = window.getComputedStyle(inner).transform;
      var glow = window.getComputedStyle(inner, '::after');
      word.classList.remove('is-hover');
      document.body.classList.remove('reduced-motion');
      assert(
        transform === 'none' || transform === 'matrix(1, 0, 0, 1, 0, 0)',
        'the reduced-motion transform was "' + transform + '" instead of none'
      );
      assert(parseFloat(glow.opacity) > 0.5, 'the reduced-motion static highlight is missing');
      assert(
        glow.backgroundColor && glow.backgroundColor !== 'rgba(0, 0, 0, 0)',
        'the reduced-motion highlight has no colour'
      );

      /* mobile: the outline survives a narrow viewport */
      var outline = document.getElementById('outline');
      assert(outline, 'the outline is missing');
      var rect = outline.getBoundingClientRect();
      assert(rect.width > 0 && rect.height > 0, 'the outline collapsed to zero size');
      assert(rect.left >= -1, 'the outline starts left of the viewport');
      assert(
        rect.right <= window.innerWidth + 1,
        'the outline overflows the viewport by ' + (rect.right - window.innerWidth).toFixed(1) + 'px'
      );
      assert(
        document.documentElement.scrollWidth <= window.innerWidth + 4,
        'the page scrolls horizontally by ' +
          (document.documentElement.scrollWidth - window.innerWidth).toFixed(1) +
          'px'
      );
      assert(
        document.body.getAttribute('data-narrow') !== null,
        'the engine did not register the narrow viewport query'
      );
    });

    var passed = 0;
    var failed = 0;
    var lines = results.map(function (result) {
      if (result.ok) {
        passed += 1;
        return 'PASS ' + result.id + ' ' + result.name;
      }
      failed += 1;
      return 'FAIL ' + result.id + ' ' + result.name + ': ' + result.reason;
    });
    var summary = 'SELFTEST ' + passed + ' passed ' + failed + ' failed';
    lines.push(summary);

    document.title = summary;
    clear(document.body);
    var pre = make('pre', { id: 'selftest-output' });
    pre.textContent = lines.join('\n');
    document.body.appendChild(pre);
  }

  /* ============================================================ start */

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
