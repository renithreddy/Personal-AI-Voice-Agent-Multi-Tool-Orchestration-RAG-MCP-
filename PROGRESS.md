# Project Progress Tracker

> This file is the source of truth for project status. At the start of any new session, paste this file + run `cat backend/llm.py backend/main.py frontend/app.py` and share that output too — so Claude has both the plan AND the actual current code.

**Project:** Personal AI Voice Agent (Multi-Tool Orchestration + RAG + MCP)
**Repo:** Personal-AI-Voice-Agent-Multi-Tool-Orchestration-RAG-MCP-
**Dev environment:** GitHub Codespaces
**Full plan reference:** See `personal-ai-agent-project-plan.md` for the complete phased roadmap.

---

## Current Phase
**Phase 1 — Core MVP** (target: 1-2 weeks, must end with a live deployed link)

## Status as of: Session 3

---

## COMPLETE PHASE 1 BUILD ORDER (step by step)

### Step 1 — Basic text chat loop ✅ DONE
- [x] FastAPI backend (`backend/main.py`) with `/` health check and `/chat` endpoint
- [x] Provider-agnostic LLM wrapper (`backend/llm.py`) using Claude (`claude-sonnet-4-6`)
- [x] Claude responses confirmed working via Swagger UI (`/docs`)

### Step 2 — Streamlit frontend 🔄 IN PROGRESS
- [x] `frontend/app.py` created with chat UI code
- [ ] **NEXT ACTION: Test it** — open second terminal → `cd frontend` → `streamlit run app.py`
- [ ] Confirm full loop works: type in Streamlit → hits FastAPI `/chat` → Claude responds → displayed in UI
- [ ] Fix any connection errors between Streamlit and FastAPI if they appear

### Step 3 — Weather tool (first tool-calling integration) ⏳ NOT STARTED
- [ ] Get free OpenWeatherMap API key (openweathermap.org, no credit card)
- [ ] Add `OPENWEATHERMAP_API_KEY` to `.env`
- [ ] Create `backend/tools/weather.py` — function that calls OpenWeatherMap API
- [ ] Update `backend/main.py` to define the weather tool for Claude's function calling
- [ ] Update `backend/llm.py` to pass tools to Claude and handle tool_use responses
- [ ] Test: ask "what's the weather in Hyderabad?" → Claude should call the weather tool automatically
- [ ] Update Streamlit to show a weather card when weather tool is called

### Step 4 — Gmail tool with OTP/sensitive-info filter ⏳ NOT STARTED
- [ ] Set up Google Cloud Console project
- [ ] Enable Gmail API, create OAuth 2.0 credentials
- [ ] Add Gmail OAuth credentials to `.env`
- [ ] Create `backend/tools/gmail.py` with:
  - `authenticate_gmail()` — handles OAuth flow
  - `filter_sensitive_emails()` — regex filter for OTPs/verification codes (runs BEFORE LLM sees content)
  - `get_important_emails()` — fetches recent emails, runs filter, returns safe summary
- [ ] Add Gmail tool to Claude's function calling in `main.py`
- [ ] Test: ask "any important emails?" → Claude calls Gmail tool → filtered summary returned
- [ ] Update Streamlit to show email list card when Gmail tool is called

### Step 5 — Voice input (Speech-to-Text) ⏳ NOT STARTED
- [ ] Get OpenAI API key (for Whisper STT — free tier available)
- [ ] Add `OPENAI_API_KEY` to `.env`
- [ ] Add `openai` package usage for Whisper in `backend/tools/stt.py`
- [ ] Add mic recording button to Streamlit frontend
- [ ] Record audio in browser → send to backend → transcribe via Whisper → feed as text to `/chat`
- [ ] Test: speak a question → transcribed → Claude answers

### Step 6 — Voice output (Text-to-Speech) ⏳ NOT STARTED
- [ ] Get ElevenLabs API key (free tier — limited characters/month, enough for dev/demo)
- [ ] Add `ELEVENLABS_API_KEY` to `.env`
- [ ] Create `backend/tools/tts.py` — sends Claude's text reply to ElevenLabs, returns audio
- [ ] Add audio playback to Streamlit frontend (auto-plays Claude's response)
- [ ] Pick a JARVIS-like voice from ElevenLabs pre-made voices (British, calm, clear)
- [ ] Test full voice loop: speak → transcribe → Claude thinks → spoken response plays

### Step 7 — "Just a minute" latency masking ⏳ NOT STARTED
- [ ] Detect when Claude needs to call a tool (vs answering directly)
- [ ] If tool call needed: immediately speak filler phrase ("One moment, sir") via TTS
- [ ] Run tool call in background while filler plays
- [ ] Speak real answer when tool result is ready
- [ ] This makes it feel like JARVIS instead of a frozen app during API calls

### Step 8 — Docker + Deploy ⏳ NOT STARTED
- [ ] Create `Dockerfile` for the FastAPI backend
- [ ] Create `docker-compose.yml` to run backend + frontend together
- [ ] Test Docker build locally in Codespaces
- [ ] Push to GitHub
- [ ] Deploy backend to Render (free tier) — connect GitHub repo, auto-deploy on push
- [ ] Deploy frontend to Render or Streamlit Cloud (free)
- [ ] Confirm live URL works from incognito browser — full voice chat end to end
- [ ] Update README with architecture diagram + live demo link

---

## PHASE 2 PLAN (after Phase 1 is fully deployed)
- Google Calendar API integration (read/create events)
- AI news tool: Hacker News API + arXiv API combined
- MCP integration: Notion or Google Tasks MCP for to-dos
- RAG: ingest arXiv papers, chunk/embed with Hugging Face sentence-transformers, store in ChromaDB
- Async pipeline upgrade (proper background task handling)

## PHASE 3 PLAN (after Phase 2 is deployed)
- Persistent conversation memory across sessions (SQLite)
- Daily proactive briefing mode (morning summary of emails/calendar/weather/AI news)
- Wake-word or push-to-talk mechanism
- Observability/logging of tool-calling decisions
- (Stretch) Barge-in handling

---

## Key Decisions Made So Far
- Dev environment: GitHub Codespaces
- Deployment target: Render free tier for Phase 1
- LLM: Claude (`claude-sonnet-4-6`) via Anthropic API — confirmed working
- LLM wrapper pattern: `get_llm_response()` in `llm.py` is the only file that changes when swapping providers
- Security (non-negotiable): email OTP filter runs BEFORE content reaches LLM — not a prompt instruction
- API vs MCP split: direct APIs for Gmail/Calendar (sensitive), MCP for Notion/Tasks (extensible, lower risk)
- RAG embeddings (Phase 2): local Hugging Face `sentence-transformers` — free, no API cost
- Voice: Whisper for STT, ElevenLabs for TTS, latency masking via async filler phrase

## Blockers / Issues Encountered (and resolutions)
- **`.env` naming**: created as `enivronmental_variables.env` — renamed via `mv`, git ignores confirmed
- **`UnboundLocalError` in `llm.py`**: missing `global _client` — fixed
- **Gemini API key bug**: AQ. prefix keys broken on Google's side — switched to Claude
- **Security**: two API keys accidentally pasted in chat — both rotated. Rule: placeholders only in chat

---

## API Keys / Accounts Needed (NEVER put actual key values in this file)
| Service | Needed for | Phase | Status |
|---|---|---|---|
| Anthropic (Claude) | LLM brain | 1 | ✅ Obtained and working |
| OpenWeatherMap | Weather tool | 1 | ⏳ Not yet |
| Google Cloud Console | Gmail OAuth | 1 | ⏳ Not yet |
| OpenAI (Whisper) | Speech-to-text | 1 | ⏳ Not yet |
| ElevenLabs | Text-to-speech | 1 | ⏳ Not yet |
| Gemini (Google AI Studio) | Attempted LLM | — | ❌ Broken (AQ. key bug) |
| Groq | Temp LLM attempt | — | Replaced by Claude |

---

## How to Resume a Session (do this every time)
1. Open Codespace
2. Run `source venv/bin/activate`
3. Paste this `PROGRESS.md` into the new chat
4. Also run and paste output of: `cat backend/llm.py backend/main.py frontend/app.py`
5. Claude now has full context — continue from the first unchecked item in the build order above
6. Terminal 1: `cd backend && uvicorn main:app --reload`
7. Terminal 2: `cd frontend && streamlit run app.py`
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