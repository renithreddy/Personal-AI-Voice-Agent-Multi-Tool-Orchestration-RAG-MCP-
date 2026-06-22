# Project Progress Tracker

> This file is the source of truth for project status. Update it at the end of every working session. At the start of a new session (especially a new chat with Claude), paste or share this file first so context is fully restored — don't rely on chat memory alone.

**Project:** Personal AI Voice Agent (Multi-Tool Orchestration + RAG + MCP)
**Repo:** Personal-AI-Voice-Agent-Multi-Tool-Orchestration-RAG-MCP-
**Dev environment:** GitHub Codespaces
**Full plan reference:** See `personal-ai-agent-project-plan.md` for the complete phased roadmap.

---

## Current Phase
**Phase 1 — Core MVP** (target: 1-2 weeks, must end with a live deployed link)

## Status as of: Session 3

### Done
- [x] GitHub repo created (Public, README on, .gitignore: Python template, License: MIT)
- [x] GitHub Codespace created (Southeast Asia region)
- [x] Python virtual environment (`venv`) created and activated
- [x] `requirements.txt` created, core packages installed (fastapi, uvicorn, streamlit, anthropic, openai, python-dotenv, requests, google-genai, groq)
- [x] `backend/` folder created with `llm.py` (provider-agnostic LLM wrapper) and `main.py` (FastAPI app with `/` health check and `/chat` endpoint)
- [x] FastAPI server runs successfully, health check (`GET /`) confirmed working via `/docs` Swagger UI
- [x] `.env` file correctly set up and confirmed ignored by git
- [x] Switched LLM from Gemini → Groq → Claude (Anthropic) — `llm.py` updated, Claude responses confirmed working via Swagger UI
- [x] Anthropic API credit purchased and key added to `.env`
- [x] `frontend/` folder created with `app.py` (Streamlit chat UI) — not yet tested

### In Progress
- [ ] Run Streamlit frontend and confirm it connects to FastAPI backend end-to-end

### Next Up
- [ ] Test Streamlit chat UI (open second terminal → `cd frontend` → `streamlit run app.py`)
- [ ] Confirm full text chat loop works: type in Streamlit → FastAPI → Claude → response displayed
- [ ] Add weather tool (first tool-calling integration)
- [ ] Add Gmail tool with OTP filter
- [ ] Add visual card display in Streamlit for tool results
- [ ] Docker + deploy to Render/Railway (live URL)

---

## Key Decisions Made So Far
- Dev environment: GitHub Codespaces (chosen over AWS EC2 + Remote-SSH for faster start)
- Deployment target: Render or Railway free tier for Phase 1 (AWS migration possible later)
- Build order: text chat loop first → STT → TTS → tools → security filter → deploy
- LLM brain built as a swappable wrapper (`get_llm_response()` in `llm.py`) — changing providers only requires editing this one file, nothing else in the app changes
- Final LLM provider: Claude (`claude-sonnet-4-6`) via Anthropic API — confirmed working
- Security requirement (non-negotiable): OTP/sensitive email content must be filtered out via regex/pattern matching BEFORE reaching the LLM context — not yet implemented, planned for Gmail tool step
- API/MCP split: direct APIs for sensitive integrations (Gmail, Calendar), MCP reserved for lower-stakes/extensible tools (to-do, Notion) — planned for Phase 2
- Embeddings for RAG (Phase 2): plan to use local Hugging Face `sentence-transformers` models (free, no API calls)

## Blockers / Issues Encountered (and resolutions)
- **`.env` file naming**: initially created as `enivronmental_variables.env` — renamed via `mv`, confirmed git ignores it
- **`UnboundLocalError` in `llm.py`**: missing `global _client` line inside `get_client()` — fixed
- **Gemini API key bug**: Google AI Studio issuing broken `AQ.` prefix keys — known unresolved Google bug, switched to Groq then Claude instead
- **Security note**: live API keys accidentally pasted in chat twice — both rotated immediately. Rule: never paste real key values in chat, use placeholders only

---

## API Keys / Accounts Needed (NEVER put actual keys in this file)
| Service | Needed for | Status |
|---|---|---|
| Anthropic (Claude) | LLM brain (final choice) | Obtained and working |
| Gemini (Google AI Studio) | LLM brain (attempted) | Broken — AQ. key bug, not usable |
| Groq | LLM brain (temp attempt) | Obtained — replaced by Claude |
| OpenAI (Whisper) | Speech-to-text | Not yet |
| ElevenLabs | Text-to-speech | Not yet |
| OpenWeatherMap | Weather tool | Not yet |
| Google Cloud Console | Gmail + Calendar OAuth | Not yet |

---

## How to Resume a Session
1. Open Codespace
2. Run `source venv/bin/activate`
3. Share this file's current contents with Claude at the start of the conversation
4. Terminal 1: `cd backend && uvicorn main:app --reload`
5. Terminal 2: `cd frontend && streamlit run app.py`
6. Continue from "Next Up" above