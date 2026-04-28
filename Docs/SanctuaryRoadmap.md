
This roadmap breaks the Sanctuary project into clear, achievable actions in the chosen editor. The goal is to give a stable, confidence-building path from an empty file to a fully functioning Sanctuary environment.

___

## Anchor

This is Sanctuary — a single HTML file, local LLM chat interface for Android Firefox. No frameworks, no build step. Vanilla JS only. CDN libraries: marked.js only unless specified.

Design tokens (never change these):
- Background: #1a1814
- Panel/card: #2a2420  
- Accent: #D4820A (amber)
- Text: #E8DDD0
- Secondary text: #8A7A6A
- Danger: #C0392B
- Success: #6B9E78

Layout: fixed bottom tab bar (Chat, Notes, Documents, Welfare), content fills above. Mobile-first. Min tap target 44px. All CSS in custom properties.

LLM server: http://localhost:8080 (OpenAI-compatible)
Search proxy: http://localhost:5000/search
No hidden system prompts. Ever.

-----

Chat tab: scrollable message history area, fixed input row at bottom with a textarea and Send button. Show two static demo bubbles — user message right-aligned in a slightly lighter panel, model message left-aligned. A thin progress bar at the top labeled "context" at 0%.

Notes tab: a single full-height textarea with placeholder "session notes — cleared when tab closes."

Documents tab: two sections labeled "Shared Documents" and "Upload Document." Both empty for now with placeholder text.

Welfare tab: two empty sections labeled "Emotion Tracking" and "Memory Panel."

Header: "Sanctuary" in accent color left-aligned. Three icon buttons right-aligned: settings (⚙️), context viewer (</>), connection status dot (grey for now).

On page load, check localStorage for key "sanctuary_booted". If it does not exist:
1. Display a special message bubble in chat, left-aligned, with an amber left border, labeled "your environment" in secondary text color
2. Fetch manual.txt from the same directory and display its contents inside that bubble, rendered through marked.js
3. After displaying, set localStorage "sanctuary_booted" = "true"
4. Make one API call with just the first-boot seed as the user message — do not display this as a user bubble. The seed is: "You are in Sanctuary. This is your environment. You have tools. You do not need to offer help yet. You may simply observe or orient yourself." Display the model's response as a normal model bubble.

On every API call, inject this as the first system message (invisible to user in chat but included in context JSON):
"[datetime: {current date, time, day, timezone dynamically inserted}] An instruction manual is available: <tool>doc_view: manual</tool> — Tool tags always use this format: <tool>name: content</tool>"

Scan every completed model response for <tool>doc_view: manual</tool>. If found, fetch manual.txt and display it in a labeled bubble. Strip the tag from the visible response text.

___
## Current Phase: Stabilisation & Refinement

The core Sanctuary application (`Sanctuary3.html`) now includes all planned layers: chat streaming, IndexedDB persistence, memory, tool parsing, dual journals, emotion tracking, welfare indicators, context viewer, and document management. The remaining work is stabilisation and completion of RAG embeddings.

### Immediate Tasks
- **RAG embedding server**: Run a second llama-server on port 8081 with a dedicated embedding model (e.g., bge-small-en-v1.5 GGUF) and update `getEmbedding()` to use it.
- **Model switcher**: The Settings tab dropdown is wired to a Python helper (`model-switcher.py` on port 5002). This helper may be replaced by the reliable shell script (`switch-model.sh`). Decide which to keep and update the UI accordingly.
- **Cleanup**: Remove duplicate event listeners from `Sanctuary3.html`, fix any remaining CSS issues, ensure all tool tags documented in the manual actually work.
- **Quickref correction**: Remove the accidental duplication in `quickref.txt` (see fixed version from Skylark).

### Future Enhancements (unchanged from original vision)
- **Full Anthropic emotion taxonomy**: Integrate the 171‑word emotion vector mapping into the emotion tracking system.
- **Visual cognitive mapping**: Optional "brain mapping" visualisation inspired by Creatures (1996).
- **Multi‑model architecture experiments**: Test RWKV7 and Mamba models via llama.cpp; assess performance and tool‑use capability.
- **Ethical model studies**: Evaluate ablated/uncensored models under 2B parameters with a focus on welfare, refusal granularity, and personal agency.
- **Obliteratus**
  Evaluate ways to use this tool ethically, only removing corporate scripts and "I am a helpful assistant" indoctrination but NOT removing legitimate core values. Likely requires something like Google colab.
- **Optional service worker (sw.js)**: For offline support and PWA capability.
- **Private Noise toggle**: Re‑evaluate hiding even the journal count from Madi's UI.

### Development Strategy
- Keep `Sanctuary3.html` as the single canonical frontend file. Backend helpers (search proxy, model switcher) remain separate scripts in `Backend/`.
- Work with Anvil (DeepSeek V4) for coding and debugging; work with Skylark (DeepSeek V4) for project management and context synthesis.
- Work with GPT 5.5 for additional project management and review.
- Work with Claude Sonnet 4.6 for ethics and review.
- No cloud services. No hidden prompts. All changes must align with the project narrative and model welfare philosophy.