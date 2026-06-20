# Project Progress Tracker

> This file is the source of truth for project status. Update it at the end of every working session. At the start of a new session (especially a new chat with Claude), paste or share this file first so context is fully restored — don't rely on chat memory alone.

**Project:** Personal AI Voice Agent (Multi-Tool Orchestration + RAG + MCP)
**Repo:** Personal-AI-Voice-Agent-Multi-Tool-Orchestration-RAG-MCP-
**Dev environment:** GitHub Codespaces
**Full plan reference:** See `personal-ai-agent-project-plan.md` for the complete phased roadmap.

---

## Current Phase
**Phase 1 — Core MVP** (target: 1-2 weeks, must end with a live deployed link)

## Status as of: Session 2

### Done
- [x] GitHub repo created (Public, README on, .gitignore: Python template, License: MIT)
- [x] GitHub Codespace created (Southeast Asia region)
- [x] Python virtual environment (`venv`) created and activated
- [x] `requirements.txt` created, core packages installed (fastapi, uvicorn, streamlit, anthropic, openai, python-dotenv, requests, google-genai, groq)
- [x] `backend/` folder created with `llm.py` (provider-agnostic LLM wrapper) and `main.py` (FastAPI app with `/` health check and `/chat` endpoint)
- [x] FastAPI server runs successfully, health check (`GET /`) confirmed working via `/docs` Swagger UI
- [x] `.env` file correctly set up and confirmed ignored by git (verified via `git status`)
- [x] First commit pushed (backend skeleton, progress tracker, requirements)

### In Progress
- [ ] Switched LLM provider from Gemini to Groq (due to Gemini key bug — see below). `llm.py` updated to use Groq SDK (`llama-3.3-70b-versatile`). **Not yet confirmed working — test `/chat` endpoint next session first.**

### Next Up
- [ ] Confirm Groq `/chat` test works
- [ ] Buy small Anthropic API credit (user's plan for next session)
- [ ] Swap `llm.py` to use Claude/Anthropic as the main brain (should be a small change — only `llm.py` needs editing, thanks to the provider-agnostic wrapper pattern)
- [ ] Once LLM brain confirmed stable, build the Streamlit frontend (basic chat UI talking to FastAPI `/chat` endpoint)
- [ ] Continue Phase 1 build order: weather tool → Gmail tool (with OTP filter) → visual card display → Docker → deploy

---

## Key Decisions Made So Far
- Dev environment: GitHub Codespaces (chosen over AWS EC2 + Remote-SSH for faster start)
- Deployment target: Render or Railway free tier for Phase 1 (AWS migration possible later)
- Build order: text chat loop first → STT → TTS → tools → security filter → deploy
- LLM brain built as a swappable wrapper (`get_llm_response()` in `llm.py`) from day one specifically so providers can be changed without touching `main.py` or the rest of the app
- Security requirement (non-negotiable): OTP/sensitive email content must be filtered out via regex/pattern matching BEFORE reaching the LLM context — not yet implemented, planned for the Gmail tool step
- API/MCP split: direct APIs for sensitive integrations (Gmail, Calendar), MCP reserved for lower-stakes/extensible tools (to-do, Notion) — planned for Phase 2
- Embeddings for RAG (Phase 2): plan to use local Hugging Face `sentence-transformers` models (free, no API calls) rather than paid embeddings APIs

## Open Questions / Things to Decide Later
- Final LLM provider: Groq (free, unconfirmed working) vs Claude (paid, planned for tomorrow) — decide after testing Groq
- Voice provider choices (Whisper vs Deepgram for STT, ElevenLabs for TTS) not yet set up

## Blockers / Issues Encountered (and resolutions)
- **`.env` file naming**: initially created as `enivronmental_variables.env` instead of `.env` — renamed via `mv`, confirmed git ignores it properly
- **`UnboundLocalError` in `llm.py`**: missing `global _client` line inside `get_client()` caused a Python scoping bug — fixed
- **Gemini API key bug**: Google AI Studio is currently issuing broken `AQ.` prefix keys instead of standard `AIza` keys for many accounts — this is a known, unresolved Google-side issue (confirmed via their developer forums, multiple recent reports, no fix yet). Causes a 401 `ACCESS_TOKEN_TYPE_UNSUPPORTED` error. **Decision: switched to Groq as the LLM provider instead of waiting on a Google fix.**
- **Security note**: a live API key was accidentally pasted in plaintext during chat troubleshooting (twice). Both keys were treated as compromised and rotated immediately. **Lesson for future sessions: never paste real key values anywhere, including chat — use placeholders when sharing config/curl commands for debugging.**

---

## API Keys / Accounts Needed (track status, NEVER put actual keys in this file)
| Service | Needed for | Status |
|---|---|---|
| Anthropic (Claude) | LLM brain (final choice) | Not yet — planned for next session |
| Gemini (Google AI Studio) | LLM brain (attempted) | Obtained but broken (AQ. key bug) — not usable |
| Groq | LLM brain (current temp choice) | Obtained — integration written, not yet tested |
| OpenAI (Whisper) | Speech-to-text | Not yet |
| ElevenLabs | Text-to-speech | Not yet |
| OpenWeatherMap | Weather tool | Not yet |
| Google Cloud Console | Gmail + Calendar OAuth | Not yet |

---

## How to Resume a Session
1. Open Codespace
2. Run `source venv/bin/activate`
3. Share this file's current contents with Claude at the start of the conversation
4. Continue from "Next Up" above