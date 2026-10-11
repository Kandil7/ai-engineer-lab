"""DevMate Streamlit UI - a chat over an ingested repository.

A polished, self-contained demo surface over the DevMate API:
- a chat transcript with streaming-style answers
- source cards with relevance scores
- token usage per answer
- a sidebar with service status, settings, and a local ingest control

Talks to the API at DEVMATE_API_URL. No API key is needed to run the UI; the
API holds the provider keys.
"""

import os

import httpx
import streamlit as st

API_URL = os.getenv("DEVMATE_API_URL", "http://localhost:8000")
if not API_URL.startswith(("http://", "https://")):
    API_URL = f"http://{API_URL}"

TIMEOUT = 120.0

st.set_page_config(page_title="DevMate", layout="wide")

_CSS = """
<style>
#MainMenu, header, footer {visibility: hidden;}
.block-container {padding-top: 1.2rem; max-width: 1100px;}
.dm-hero {
  background: linear-gradient(135deg, #4f46e5 0%, #0ea5e9 100%);
  color: #fff; padding: 1.1rem 1.4rem; border-radius: 14px; margin-bottom: 1rem;
}
.dm-hero h1 {margin: 0; font-size: 1.5rem; font-weight: 700;}
.dm-hero p {margin: .3rem 0 0; opacity: .92; font-size: .9rem;}
.dm-pill {display: inline-block; padding: .15rem .6rem; border-radius: 999px;
  font-size: .75rem; font-weight: 600;}
.dm-pill.ok {background: rgba(34,197,94,.16); color: #16a34a;}
.dm-pill.bad {background: rgba(239,68,68,.16); color: #dc2626;}
.dm-src {border: 1px solid rgba(128,128,128,.25); border-radius: 10px;
  padding: .6rem .8rem; margin: .4rem 0; background: rgba(128,128,128,.05);}
.dm-src .meta {font-size: .74rem; opacity: .7; margin-bottom: .25rem;}
.dm-score {float: right; font-size: .72rem; padding: .08rem .45rem;
  border-radius: 999px; background: rgba(79,70,229,.16); color: #6366f1;}
.dm-src pre {white-space: pre-wrap; word-break: break-word; margin: 0;
  font-size: .8rem; opacity: .92;}
</style>
"""
st.markdown(_CSS, unsafe_allow_html=True)

st.markdown(
    """
    <div class="dm-hero">
      <h1>DevMate</h1>
      <p>Ask questions about a code repository. Answers are grounded in retrieved sources.</p>
    </div>
    """,
    unsafe_allow_html=True,
)


def _health() -> tuple[bool, str]:
    """Return (ok, status_text) for the API health endpoint."""
    try:
        data = httpx.get(f"{API_URL}/health", timeout=5.0).json()
        return True, str(data.get("status", "unknown"))
    except Exception:
        return False, "unreachable"


def _render_sources(contexts: list) -> None:
    """Render retrieved chunks as source cards."""
    if not contexts:
        return
    st.caption(f"Sources ({len(contexts)})")
    for ctx in contexts:
        meta = ctx.get("metadata") or {}
        filename = meta.get("filename") or meta.get("source") or ctx.get("id", "source")
        score = ctx.get("score")
        badge = f'<span class="dm-score">{score:.3f}</span>' if isinstance(score, float) else ""
        body = (ctx.get("content") or "")[:900]
        st.markdown(
            f'<div class="dm-src">{badge}'
            f'<div class="meta">{filename} &middot; {ctx.get("id", "")}</div>'
            f"<pre>{body}</pre></div>",
            unsafe_allow_html=True,
        )


def _ask(question: str, use_reranker: bool) -> dict | None:
    """Call the RAG endpoint and return the JSON payload, or None on failure."""
    try:
        resp = httpx.post(
            f"{API_URL}/ai/rag/query",
            json={"query": question, "stream": False, "use_reranker": use_reranker},
            timeout=TIMEOUT,
        )
        resp.raise_for_status()
        return resp.json()
    except Exception as exc:
        st.error(f"Request failed: {exc}")
        return None


if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    ok, status_text = _health()
    pill = "ok" if ok else "bad"
    st.markdown(
        f"**Service** &nbsp; <span class='dm-pill {pill}'>{status_text}</span>",
        unsafe_allow_html=True,
    )
    st.text_input("API URL", value=API_URL, disabled=True)
    st.divider()
    st.subheader("Settings")
    use_reranker = st.toggle(
        "Use reranker", value=True, help="Reorder retrieved chunks before answering."
    )
    if st.button("Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.divider()
    with st.expander("Ingest a repo (server path)"):
        st.caption("Local/dev only: the cloud demo ingests its baked-in sample corpus on startup.")
        repo_path = st.text_input(
            "Repository path", placeholder="projects/04-ai-engineering/devmate"
        )
        if st.button("Ingest", use_container_width=True) and repo_path.strip():
            try:
                with st.spinner("Ingesting..."):
                    r = httpx.post(
                        f"{API_URL}/ingest", json={"repo_path": repo_path.strip()}, timeout=TIMEOUT
                    )
                if r.status_code == 200:
                    st.success(f"Ingested {r.json().get('chunks_created', '?')} chunks")
                else:
                    st.error(r.json().get("detail", r.text))
            except Exception as exc:
                st.error(f"Ingest failed: {exc}")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant":
            _render_sources(message.get("contexts", []))
            usage = message.get("usage") or {}
            if usage:
                st.caption(
                    f"tokens {usage.get('total_tokens', '?')} "
                    f"&middot; {message.get('latency_ms', 0):.0f} ms "
                    f"&middot; id {message.get('request_id', '')}"
                )

prompt = st.chat_input("Ask about the repository...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Retrieving and answering..."):
            payload = _ask(prompt, use_reranker)
        if payload is None:
            st.stop()
        assert payload is not None
        answer = payload.get("answer", "")
        st.markdown(answer)
        _render_sources(payload.get("contexts", []))
        usage = payload.get("usage") or {}
        if usage:
            st.caption(
                f"tokens {usage.get('total_tokens', '?')} "
                f"&middot; {payload.get('latency_ms', 0):.0f} ms "
                f"&middot; id {payload.get('request_id', '')}"
            )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "contexts": payload.get("contexts", []),
            "usage": usage,
            "latency_ms": payload.get("latency_ms", 0.0),
            "request_id": payload.get("request_id", ""),
        }
    )
