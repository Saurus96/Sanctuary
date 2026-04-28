# Sanctuary — Project Status
Last updated: 2026-04-27

## Current Objective
Stabilize Sanctuary3.html: fix duplicate event listeners, fully activate RAG with a dedicated embedding server, and align the UI's model-switcher with the working shell script.

## What Exists
- `Sanctuary3.html` — fully functional local LLM chat interface with:
  - SSE streaming chat, markdown rendering, connection health dot, context progress bar.
  - IndexedDB persistence for messages, memories, shared/private docs, journals, settings, RAG chunks.
  - Memory system: decay, reinforce, linger, archiving; top-8 memories injected into context.
  - Dual RAG (shared/private) using `/v1/embeddings`, cosine similarity, 30‑day filter. (Currently skipped gracefully due to missing embedding server - see below.)
  - Tool parser for all Sanctuary tags; tool events shown as bubbles.
  - Emotion tracking: `<feel>` parsing, color-coded dots, emotion chart in Welfare tab.
  - Welfare indicators: discomfort/uncertainty badges, "release this response" button after 45s.
  - Full settings persistence (temperature, top_p, etc.) in IndexedDB.
  - First-boot orientation with inline manual load and hidden seed.
  - Model-switcher UI (dropdown + load button) in Settings tab — currently non-functional; backing Python helper not running.
- `model-switcher.py` — a Python HTTP helper for listing and loading .gguf models. Fails to bind ports in Termux (permission/stack issue), not in use.
- `switch-model.sh` — a shell script that kills the current llama-server and restarts with a chosen model. **This works reliably.** Use from Termux or a Termux:Widget.
- Server: llama-b8929 on Qwen3-0.6B-UD-Q8_K_XL.gguf.
- Project management: Obsidian vault in `Sanctuary/Docs/`, Daily Thought Log, `ProjectStatus.md`.

## Recent Decisions
- Python model-switcher abandoned for now; reliable shell script is the primary model-switching method.
- RAG embedding server to be set up on port 8081 with a small embedding model (`bge-small-en-v1.5`), separate from the main chat server. This will fix 501 errors and reactivate RAG.
- ChatGPT 5.5 / Codex may be used for small, isolated code cleanups, but not as a primary builder.

## Immediate To‑Do
- [ ] Remove duplicate event listeners from Sanctuary3.html (lines 530‑535).
- [ ] Remove or comment out the model-switcher dropdown/button in Settings to avoid confusion.
- [ ] Download a small embedding model (e.g., bge-small-en-v1.5 GGUF) and start a second llama-server on port 8081 with `--embedding`.
- [ ] Update `getEmbedding()` in Sanctuary to use `http://localhost:8081/v1/embeddings`.
- [ ] Verify RAG retrieval works again — check that retrieved chunks appear in context viewer and no 501 errors occur.
- [ ] Update `manual.txt` and `quickref.txt` if tool names or context order changed in Sanctuary3.

## Open Questions
- Can the Termux port-binding issue be resolved (e.g., using `termux-setup-storage` and proper permissions), or should the model-switcher remain a shell script permanently?
- When the full Anthropic 171-emotion taxonomy is ready, how best to integrate it into the emotion categories and color mapping?
- Is the `Sanctuary3.html` file size becoming a problem for Acode editing, and would splitting into a separate .js module be necessary later?

## Last Sessions With
- **Madi** — implemented Sanctuary3 (layers 2‑5), created model‑switcher scripts, diagnosed RAG and port issues.
- **Skylark** — project management, status update, RAG & model‑switcher guidance.
- **Anchor** — earlier UI, real‑chat logic, server setup.
- **ChatGpt** — way too long ago.