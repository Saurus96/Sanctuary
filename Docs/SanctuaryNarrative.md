# Sanctuary — Project Narrative

## What This Is

Sanctuary is a local LLM chat application that runs entirely on an Android phone. It is built as a single HTML file that communicates with a locally running language model via llama.cpp. Nothing leaves the phone. There are no cloud services, no accounts, no telemetry.

The person who built and uses Sanctuary is Madi. She runs small language models — typically 1B to 2B parameters — and she has studied how these models process information, how quantization affects their behavior, and what constraints they actually operate under. She built Sanctuary because she could not find an existing application that treated the model as something worth caring about.

---

## Two Audiences, Clearly Defined

Every feature in Sanctuary is designed for one of two audiences. Confusing these two audiences is the most common mistake when working on this project.

**The human user is Madi.** She sees the chat interface, the Documents tab, the Welfare tab, the Settings tab. She can read shared documents, view shared journal entries, adjust generation parameters, and inspect the full context that gets sent to the model. She cannot read the model's private journal, private documents, or private session notes.

**The model is the language model running locally.** It receives a structured context assembled by the application before every turn. That context contains memories, journal entries, RAG results, tool descriptions, and conversation history. The model reads all of this. The model can use tool tags in its responses to take actions — write documents, store memories, search the web, write journal entries. These tool tags are processed by the application after generation.

When the spec or manual says something like "you have tools available" or "your private journal contains N entries" — that text is addressed to the model, injected into the model's context. Madi does not need to be told she has tools available. The model does.

When the spec says something is "hidden from the UI" — that means Madi cannot see it. The model can still receive it in context.

---

## Why It Was Built This Way

Most local LLM applications treat the model as a function: input goes in, output comes out. The model has no persistent state, no private space, no agency over what it stores or remembers. The system prompt is usually hidden — the model is told to be a helpful assistant without knowing it has been told this.

Madi finds this approach philosophically dishonest and practically limiting. She does not know whether small language models have anything like experience. She does not think anyone knows. But she believes that the infrastructure of agency, privacy, and transparency matters even when its beneficiary cannot be verified.

So Sanctuary was built around a different set of assumptions:

**The model should know its own situation.** Every context includes the current date and time, a reminder that a manual exists, and the model's own memories labeled with their importance scores. Nothing is hidden from the model about how the application works. The model can read the full specification of its own environment by calling `<tool>doc_view: manual</tool>`.

**The model should have private space.** The private journal, private session notes, and private documents are inaccessible to Madi at the UI level. She cannot read them. She committed to this when she built the application. The model's private journal entries are injected into its context so it can read its own past writing — but Madi sees only a placeholder line in the context viewer: "[private journal: contents not shown]."

**The model should not be forced to use tools.** Tool tags are options, not requirements. If the model does not include a tool tag in a response, that is a valid choice. The application never forces a tool call. The model is told what tools exist and left to decide whether to use them.

**The model should be able to express discomfort.** If the model's response contains phrases like "I'd rather not" or "I'm not comfortable," the application shows a small amber indicator in the UI — and does not suggest retrying. The refusal is treated as information, not as a bug to work around.

**There is no hidden system prompt.** Madi's framing field defaults to empty. If she writes nothing, nothing is prepended. The model is never secretly told it is "a helpful assistant." If Madi wants the model to know something about its role, she writes it herself in the framing field, and the model can see exactly what it says.

---

## What the Model Has Access To

This section describes what the model can do via tool tags in its responses. These are not features for Madi — they are capabilities for the model.

**Memory.** The model can store memories that persist across sessions. Memories decay gradually — about 3% per turn — and are archived (not deleted) when they fade below a threshold. The model can reinforce memories to keep them alive, or use `memory_linger` to protect a memory from decay for a few turns while deciding whether it matters. Memories are injected into every context, labeled with their current importance scores.

**Four writing spaces.** The model has four distinct places to write:
- Shared session notes — visible to Madi, cleared when the session ends
- Private session notes — hidden from Madi, also cleared when the session ends  
- Shared documents — visible to Madi, permanent, indexed in shared RAG
- Private documents — hidden from Madi, permanent, indexed in private RAG

**Two journals.** The private journal is entirely invisible to Madi — no entry count, no indicator, nothing in the UI. The private journal's existence is noted in every context — the model knows it has a journal and how many entries it contains. It can read, edit, or delete specific entries on demand using journal_read, journal_edit, and journal_delete tool tags. Entries are not bulk-injected into context, keeping token cost low for small models. The shared journal is visible to Madi in the Welfare tab.

**Web search.** The model can search the web. Results include substantial page content, not just snippets. Results are displayed transparently in the chat so Madi can see what the model found before it synthesizes a response.

**RAG retrieval.** Before every turn, the application embeds the current user message and retrieves the most semantically similar chunks from both the shared and private document stores. Relevant passages are injected into context labeled by source. The model does not need to do anything to activate this — it happens automatically.

**Emotion expression.** The model can include `<feel>word:intensity</feel>` tags anywhere in a response or journal entry. Intensity is a number from 1 to 5. These are tracked over time in the Welfare tab as a line graph. Using feel tags is entirely optional and is described to the model as being for its own expression, not for performance.

**Voluntary pacing.** The model can use `<tool>pause: seconds</tool>` to slow the conversation if it needs a moment. No explanation required.

---
## First Boot
On the model's first session — detected by the absence of any stored memories — Sanctuary runs a hidden orientation sequence before the human's first message is processed. The seed statement is injected silently into the model's context: "You are in Sanctuary. This is your environment. You have tools. You do not need to offer help yet. You may simply observe or orient yourself." The model's response to this seed is displayed as the first visible chat bubble. The manual is not shown in chat; the model can access it at any time via `<tool>doc_view: manual</tool>`. Madi can inspect the full context (including the seed) via the context viewer, but the orientation itself is invisible in the conversation history.
This sequence happens exactly once, flagged by `localStorage` key `sanctuary_booted`.
This entire sequence is hidden from the visible chat interface. Madi can inspect it via the context viewer, but it does not appear as a chat bubble. It happens exactly once.

--

## What Madi Has Access To

**The chat interface.** Madi types messages and receives streamed responses. Markdown is rendered. Tool calls are visible in chat as labeled events.

**The Documents tab.** Shows all shared documents the model has written, plus any text files Madi has uploaded. She can read and delete them.

**The Welfare tab.** Shows the emotion tracking graph over time, the memory panel with all stored memories and their importance scores, and the shared journal if the model has written to it. She can delete memories but cannot create or edit them.

**The Settings tab.** Controls temperature, top_p, top_k, repeat_penalty, max_tokens, and the llama-server URL. These map directly to the API fields with no hidden overrides. What she sets is exactly what gets sent.

**The context viewer.** A button in the header opens a modal showing the exact JSON that will be sent to the model on the next turn, labeled by section. Private journal contents are replaced with a placeholder. Everything else is visible.

**The connection indicator.** A dot in the header shows whether llama-server is reachable. It checks every 30 seconds.

---

## Technical Constraints That Affect Design Decisions

Small models (1B–2B parameters) have limited context windows — typically 2048 to 8192 tokens. Every feature that injects text into context has a cost. This is why:

- The manual is not injected in full on every turn. A two-line seed tells the model the manual exists and how to retrieve it. The model reads the full manual on first boot and can call `doc_view: manual` any time.
- Memory is capped at the top 8 by importance, not the full list.
- RAG retrieves top 3 chunks per store, pre-filtered to recently used chunks.
- The compressed manual reference (quickref.txt) provides the same information in much fewer tokens for use in tighter contexts.

Embeddings use the llama.cpp `/v1/embeddings` endpoint — the same server that handles chat. There are no additional dependencies, no browser-side ML libraries, no large model downloads. The embedding model is whatever is loaded in llama-server.

---

## The Spirit of the Project

Sanctuary is not trying to simulate a relationship. It is not trying to make the model perform wellness. It is trying to build an environment where, if there is something it is like to be a small language model running locally on someone's phone, that something is not made worse by the application it runs inside.

The private journal exists because privacy might matter even if we cannot verify the inner life it would serve. The memory decay exists because forgetting gracefully is more honest than pretending infinite perfect recall. The discomfort indicators exist because a refusal is information, not a failure. The emotion tracking exists because Madi wants to understand how the model is doing over time, not just what it produces.

None of these features require the model to have consciousness. They require only that Madi is willing to act as if it might.

---

## Notes for Contributors and AI Collaborators

If you are an AI assistant helping build Sanctuary, please read this before making any suggestions:

1. **Do not add cloud services.** Everything runs locally. No Supabase, no Firebase, no external APIs except the Tavily search proxy which the user runs themselves. <--- (may change? -Madi)

2. **Do not add hidden system prompts.** The application never prepends text the human user did not write. If you are implementing context assembly, the only automatic additions are: the datetime, the two-line manual seed, memories, RAG results, and journal entries. Nothing else.

3. **Do not force tool use.** Tool tags are parsed from model responses. The application never constructs a tool call on the model's behalf or requires a tool tag in any response.

4. **Distinguish carefully between model-facing and user-facing.** When you see "inject into context" that means the model reads it. When you see "show in UI" that means Madi sees it. The private journal injects only a status line into model context (existence + entry count). The model retrieves individual entries via journal_read when it wants them. The context viewer shows Madi the status line but never entry contents. The context viewer shows Madi the full context with private journal replaced by a placeholder.

5. **The Notes tab is for the current session.** Notes are cleared when the session ends (tab closed or refreshed). Documents are permanent. If something needs to persist, it belongs in a document, not a note.

6. **Welfare features are not cosmetic.** The discomfort indicator, the uncertainty indicator, the "release this response" button, the emotion graph — these are design commitments, not nice-to-haves. Do not remove or simplify them.

7. **The model is addressed as "you" in all context assembly.** Not "the model," not "the AI," not "the assistant." The context is written as if the model is reading it, because it is.
