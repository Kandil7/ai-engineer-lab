# Auto Checkpoint (pre-compaction snapshot)

- Time: 2026-09-30T15:01:45.965Z
- Session: ses_f0d5544d8ffeYn6xaf8tToeSgY
- Project: D:\AI\Projects\fullstack-ai-engineer-lab

## Recent user messages (tail)
- **user**: ultra think harder to reviwe full @.ai/ and full @docs\ and @docs/product\ in full details and review full @AGENTS.md 
Called the Read tool with the following input: {"filePath":"D:\\AI\\Projects\\fullstack-ai-engineer-lab\\docs\\product\\"}
<path>D:\AI\Projects\fullstack-ai-engineer-lab\docs\product</path>
<type>directory</type>
<entries>
12-month-plan.md
agents/
ai-learning-operating-manual.md
feature-priorities.md
learning-strategy.md
scope-definition.md
workflows/
workspace-goals.md

(8 entries)
</entries>
Called the Read tool with the following input: {"filePath":"D:\\AI\\Projects\\fullstack-ai-engineer-lab\\AGENTS.md"}
<path>D:\AI\Projects\fullstack-ai-engineer-lab\AGENTS.md</path>
<type>file</type>
<content>
1: # AGENTS.md — Full-Stack AI Engineer Lab
2: 
3: Repo-centric learning + execution workspace. Active project: DevMate (`projects/04-ai-engineering/devmate/`).
4: What to work on: `docs/tracking/current-focus.md`. Plan of record: `docs/roadmap/active-track-10-week.md`.
5: 
6: ## Verify like CI does
7: 
8: `make` and `pwsh` are not installed on this machine. Use `powershell` (5.1) and these
9: direct commands instead. Git Bash exists for shell bits.
10: 
11: DevMate gate — working directory `projects/04-ai-engineering/devmate/`, python at
12: `.venv/Scripts/python.exe`:
13: 
14: ```powershell
15: & .venv/Scripts/python.exe -m ruff check .
16: & .venv/Scripts/python.exe -m ruff format --check .
17: & .venv/Scripts/python.exe -m mypy src/
18: & .venv/Scripts/python.e
- **user**: update @AGENTS.md 
Called the Read tool with the following input: {"filePath":"D:\\AI\\Projects\\fullstack-ai-engineer-lab\\AGENTS.md"}
<path>D:\AI\Projects\fullstack-ai-engineer-lab\AGENTS.md</path>
<type>file</type>
<content>
1: # AGENTS.md — Full-Stack AI Engineer Lab
2: 
3: Repo-centric learning + execution workspace. Active project: DevMate (`projects/04-ai-engineering/devmate/`).
4: What to work on: `docs/tracking/current-focus.md`. Plan of record: `docs/roadmap/active-track-10-week.md`.
5: 
6: ## Verify like CI does
7: 
8: `make` and `pwsh` are not installed on this machine. Use `powershell` (5.1) and these
9: direct commands instead. Git Bash exists for shell bits.
10: 
11: DevMate gate — working directory `projects/04-ai-engineering/devmate/`, python at
12: `.venv/Scripts/python.exe`:
13: 
14: ```powershell
15: & .venv/Scripts/python.exe -m ruff check .
16: & .venv/Scripts/python.exe -m ruff format --check .
17: & .venv/Scripts/python.exe -m mypy src/
18: & .venv/Scripts/python.exe -m pytest -q --cov=devmate --cov-report=term-missing
19: ```
20: 
21: Single test: `& .venv/Scripts/python.exe -m pytest tests/unit/test_cost.py -q`. Unit tests need no API key.
22: `llm`-marked tests need a real key and never run in CI. No test file currently carries
23: the `integration` marker, so `make test-int` collects nothing; when such tests exist
24: they need `docker compose -f infra/docker/docker-compose.yml up -d postgres redis qdrant` first.
25: 
26: Workspace validators — all
- **user**: ultra think hader to review full **توصيتي:** امشِ في مسار واحد متدرّج من Python لحد امتلاك نظام AI في الإنتاج، واجعل *Athar* مشروع التخرّج المستمر، لا مشروعًا تؤجله لنهاية الدراسة. سأكتب الخريطة «من الصفر» كما طلبت، لكن بما أنك تعرف البرمجة وFastAPI وRAG بالفعل، استخدم المراحل الأولى **كاختبار إتقان وسدّ فجوات**، لا كإلزام بإعادة كل كورس من بدايته.

الهدف النهائي ليس لقبًا أو قائمة أدوات؛ هو أن تستطيع تصميم نظام AI، بناءه، تقييمه، نشره، ثم تشغيله وتحسينه بقرارات موثقة. هذا ينسجم مع خريطة Andrew Ng التي تجمع بناء تطبيقات AI، أساسيات هندسة البرمجيات، coding agents، والحكم على ما ينبغي بناؤه. [deeplearning](https://www.deeplearning.ai/the-batch/the-ai-engineering-skills-map)

## كيف تستخدم الخريطة

**التقدير الزمني التخطيطي:** نحو 12–18 شهرًا لشخص يبدأ Python من الصفر ويدرس ويبني بانتظام. في حالتك، قد تختصر الأساسيات وتخصص نحو 6–9 أشهر لسد فجوات الإنتاج؛ **هذه ليست مدة مضمونة ولا تقييمًا لمستواك الحالي**. لا تنتقل من مرحلة لمجرد انتهاء مدتها: انتقل عندما تنجح في *اختبار الخروج* المكتوب لها.

| الرمز | معناه |
|---|---|
| **أساسي** | تحتاج تنفيذه بنفسك دون الاعتماد الكلي على agent أو tutorial |
| **عملي** | تحتاج اتخاذ قرارات فيه وتشغيله واختبار فشله |
| **تخصص لاحق** | تتعمّق فيه عندما يثبته الحمل أو متطلبات الوظيفة |

ابدأ محليًا قدر الإمكان، واستعمل GPU cloud أو خدمات مدفوعة فقط لتجارب لا يكفيها جهازك. ولا تربط التقدم بأداة واحدة: المفاهيم والقياسات تسبق اختيار framework.

## المرحلة 1: أساس هندسي متين

### 1) Python من الصفر إلى كود إنتاجي — أساسي

**الموضوعات، بالترتيب:**
- 
- **user**: ultra think harder to implement all in full details and with full content in full detials and check @docs/product\ 
Called the Read tool with the following input: {"filePath":"D:\\AI\\Projects\\fullstack-ai-engineer-lab\\docs\\product\\"}
<path>D:\AI\Projects\fullstack-ai-engineer-lab\docs\product</path>
<type>directory</type>
<entries>
12-month-plan.md
agents/
ai-learning-operating-manual.md
feature-priorities.md
IMPLEMENTATION-GUIDE.md
learning-strategy.md
scope-definition.md
workflows/
workspace-goals.md

(9 entries)
</entries>
- **user**: continue and implement all in detials
- **user**: continue and implement all in detials

> Regenerate a curated checkpoint with /checkpoint.