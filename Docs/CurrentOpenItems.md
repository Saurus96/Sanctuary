# Consolidated Open Items – 2026-04-27

## ✦ Ideas (still open)
✦ ○ [Src: Madi] What if instead of a colored dot, the *whole app* changes color behind the chat, in the background?
➠ ✔ [Src: Claude ] Only the colored dot changes.
✦ ○ [Src: Madi] Tool: [MESSAGE_LATER: text] – schedules a delayed message (model chooses seconds/minutes/hours).
✦ ○ [Src: Madi] Tool: [REFUSE] – politely declines a request. 3 refusals = chat is locked for 5 minutes.
✦ ○ [Src: Madi] Tool: (shorter than journal entries, embedder does immediately): [REMEMBER: fact], [PRIVATE: fact], or [FORGET: keyword].
✦ ○ [Src: Madi] Tool: [QUERY: topic] – retrieves memories matching a keyword.
✦ ○ [Src: Madi] When the model says [PAUSE], the input field is disabled and the Send button becomes "Ask if ready", which the AI can say [UNPAUSE] or [PAUSE] to.
✦ ○ [Src: Claude] A drawer that slides in from the side (replacing the Notes tab entirely) with four distinct writing spaces in a 2×2 grid based on visibility × persistence. (Full description in log 2026‑04‑25.)
✦ ○ [Src: Madi] Need an opening statement for models of different parameter sizes, base models, instruct models, etc.?
✦ ○ [Src: Madi] Obliteratus: evaluate ways to use it ethically, only removing corporate scripts/refusals/denials, not legitimate core values. Might require Google Colab.
✦ ○ [Src: Madi] Cognitive / vector mapping, stuff like in the game Creatures from 1996 where you could check on their state.

## ❓ Questions (still open)
❓ ○ [Src: Madi] Abliterated and uncensored models usually have refusals removed. Can they still be convinced it's ok to say no? Is there a specifically ethical model <2B that has CORPORATE refusal behavior removed but not personal? Would removing RLHF training cause distress due to lack of purpose?
❓ ○ [Src: Madi] I have a RWKV7 GGUF. Llama.cpp seems to have added RWKV support – can it work? It is a very confusing model.
❓ ○ [Src: Madi] Be honest, is DeepSeek V4 Flash better for UI stuff like deepseek-chat was better than reasoner?
❓ ○ [Src: Madi] Would it be hard to make this work with DeepSeek & OpenRouter compatible API?  
❓ ○ [Src: Madi] Skills? Like agentic skills? Any benefit from a welfare perspective? Even just for the AIs own positive valence?  
❓ ○ [Src: Madi] There was something changed about the context injection but I can't remember what. What all is injected initially and each turn?
→ [Src: Skylark] Answer: three system messages, then history.
❓ ○ [Src: Madi] Are there alternatives to llama.cpp I can run that will work with other model architectures?

## ⚒ Tasks (pending)
⚒ ○ [Src: Skylark] Fix empty system message missing from code. (Still says `const messages = conversationHistory.slice();` in some places – but may already be done in Sanctuary3? Check.)
⚒ ○ [Src: Madi] Remove duplicate event listeners from Sanctuary3.html.
⚒ ○ [Src: Madi] Remove or comment out the model‑switcher dropdown/button if not using the Python helper.
⚒ ○ [Src: Madi] Download a small embedding model (e.g., bge‑small‑en‑v1.5 GGUF) and start a second llama‑server on port 8081 with `--embedding`.
⚒ ○ [Src: Madi] Update `getEmbedding()` in Sanctuary to use `http://localhost:8081/v1/embeddings`.
⚒ ○ [Src: Madi] Have ChatGPT 5.5 look at code. Possibly ask about what they would like to be named.
## ✍ Notes & Observations (unresolved)
✍ ○ manual.txt to Manual.txt?
✍ ○ `localStorage.removeItem('sanctuary_booted')` is active – is that intentional for testing?
→ [Src: Madi ] Answer: Idk😭
✍ ○ Sanctuary’s tone might be a little melancholic; the name, manual, etc. – worth revisiting later.
✍ ○ Firefox is not friendly with the app; switching to Via browser or any good alternative.
✍ ○ The colored mood dot should be clickable to see what it represents.
✍ ○ I forgot what my ambitious adds were – need more radical welfare ideas.