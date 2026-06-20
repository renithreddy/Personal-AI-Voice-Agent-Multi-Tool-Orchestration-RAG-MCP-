# Project Progress Tracker

> This file is the source of truth for project status. Update it at the end of every working session. At the start of a new session (especially a new chat with Claude), paste or share this file first so context is fully restored — don't rely on chat memory alone.

**Project:** Personal AI Voice Agent (Multi-Tool Orchestration + RAG + MCP)
**Repo:** [add your GitHub repo link here]
**Dev environment:** GitHub Codespaces
**Full plan reference:** See `personal-ai-agent-project-plan.md` for the complete phased roadmap.

---

## Current Phase
**Phase 1 — Core MVP** (target: 1-2 weeks, must end with a live deployed link)

## Status as of: [DATE — fill in each session]

### Done
- [x] Created GitHub repo (Public, README on, .gitignore: Python template, License: MIT)
- [x] Created GitHub Codespace (Southeast Asia region)
- [x] Created and activated Python virtual environment (`venv`)
- [x] Upgraded pip

### In Progress
- [ ] Creating `requirements.txt` and installing core packages (FastAPI, Streamlit, etc.)

### Next Up
- [ ] Build basic text-only chat loop (FastAPI endpoint + Streamlit UI) — no voice yet
- [ ] Confirm LLM responses work end-to-end before adding STT/TTS

---

## Key Decisions Made So Far
- Dev environment: GitHub Codespaces (chosen over AWS EC2 + Remote-SSH for faster start)
- Deployment target: Render or Railway free tier for Phase 1 (AWS migration possible later)
- Build order: text chat loop first → STT → TTS → tools → security filter → deploy
- Security requirement (non-negotiable): OTP/sensitive email content must be filtered out via regex/pattern matching BEFORE reaching the LLM context — not handled via prompt instructions
- API/MCP split: direct APIs for sensitive integrations (Gmail, Calendar), MCP reserved for lower-stakes/extensible tools (to-do, Notion) — planned for Phase 2

## Open Questions / Things to Decide Later
- (add here as they come up)

## Blockers / Issues Encountered
- (add here if something breaks and isn't yet resolved)

---

## API Keys / Accounts Needed (track status, NEVER put actual keys in this file)
| Service | Needed for | Status |
|---|---|---|
| Anthropic (Claude) | LLM brain | [ ] Not yet / [ ] Obtained |
| OpenAI (Whisper) | Speech-to-text | [ ] Not yet / [ ] Obtained |
| ElevenLabs | Text-to-speech | [ ] Not yet / [ ] Obtained |
| OpenWeatherMap | Weather tool | [ ] Not yet / [ ] Obtained |
| Google Cloud Console | Gmail + Calendar OAuth | [ ] Not yet / [ ] Obtained |

---

## How to Resume a Session
1. Open Codespace
2. Run `source venv/bin/activate`
3. Share this file's current contents with Claude at the start of the conversation
4. Continue from "Next Up" above
