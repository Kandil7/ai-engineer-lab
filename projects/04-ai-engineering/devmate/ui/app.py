"""DevMate Streamlit UI - ask questions about an ingested repository.

A read-only demo surface that talks to the DevMate API (DEVMATE_API_URL):
a health indicator, an ask box, and the returned answer with its sources
and token usage. No API key is needed to run the UI; the API holds the key.
"""

import os

import httpx
import streamlit as st

API_URL = os.getenv("DEVMATE_API_URL", "http://localhost:8000")
if not API_URL.startswith(("http://", "https://")):
    API_URL = f"http://{API_URL}"
REQUEST_TIMEOUT = 120.0

st.set_page_config(page_title="DevMate", layout="wide")
st.title("DevMate")
st.caption("Ask questions about a code repository. Answers are grounded in retrieved sources.")

with st.sidebar:
    st.subheader("Service")
    try:
        health = httpx.get(f"{API_URL}/health", timeout=5.0).json()
        st.success(f"API status: {health.get('status', 'unknown')}")
    except Exception as exc:
        st.error(f"API unreachable at {API_URL}: {exc}")
    st.text_input("API URL", value=API_URL, disabled=True)

question = st.text_input("Question", placeholder="How does chunking work?")

if st.button("Ask", type="primary") and question.strip():
    data: dict = {}
    with st.spinner("Retrieving and answering..."):
        try:
            response = httpx.post(
                f"{API_URL}/ai/rag/query",
                json={"query": question, "stream": False},
                timeout=REQUEST_TIMEOUT,
            )
            response.raise_for_status()
            data = response.json()
        except Exception as exc:
            st.error(f"Request failed: {exc}")

    if data:
        st.subheader("Answer")
        st.write(data.get("answer", ""))

        contexts = data.get("contexts", [])
        st.subheader(f"Sources ({len(contexts)})")
        for ctx in contexts:
            with st.expander(str(ctx.get("id", "context"))):
                st.caption(str(ctx.get("metadata", {})))
                st.code(str(ctx.get("content", "")), language=None)

        usage = data.get("usage") or {}
        if usage:
            st.caption(f"Usage: {usage}")
