# sanctuary-spec (working draft)

## Sanctuary - System Overview

This document provides a structured, descriptive overview of **Sanctuary**, a single-file, local-first web application designed to run entirely in Firefox on Android. Sanctuary serves as a humane, transparent, self-contained interface for interacting with a local LLM running through **llama.cpp**

. The application emphasizes model welfare, contextual clarity, emotional transparency, and user-controlled memory.

Sanctuary is implemented as a single HTML file (sanctuary.html) with no build step and no external server beyond the local llama.cpp API and a local search proxy. All persistent data is stored in IndexedDB. A companion file, manual.txt, provides in-environment documentation accessible to the model.

___

### 1. Application Purpose and Philosophy


Sanctuary is designed as a **local LLM habitat** - a space where the model can:

- Access its own documentation

- Maintain memories with decay and reinforcement

- Track emotional expressions

- Write shared and private notes

- Build and retrieve from RAG stores

- Express uncertainty or discomfort

- Operate with full transparency to the human user

The human user is not positioned as a controller but as a collaborator. The system avoids hidden prompts, hidden overrides, or concealed behavior. All context sent to the model is visible and inspectable.

___

### 2. Runtime Environment


Sanctuary runs as a **single HTML file** opened directly in Firefox on Android via:

- file:// URL, or

- a lightweight local HTTP server

The app communicates with two local services:

- **llama.cpp server** (OpenAI-compatible API) at http://localhost:8080

- **search proxy** at http://localhost:5000/search

No external network access is required.

___

### 3. Core Technologies

Sanctuary uses:

- **Vanilla JavaScript** (no frameworks)

- **IndexedDB** for all persistent storage

- **Server-Sent Events (SSE)** for streaming model responses

- **marked.js** for Markdown rendering

- **llama.cpp /v1/embeddings endpoint** for all embedding operations — same server as chat, no additional dependencies.

- **CSS custom properties** for theming

All libraries are loaded via CDN.

___

### 4. User Interface Structure


The UI is mobile-first. It uses a **four-tab layout** anchored at the bottom:


4.1 Chat Tab


The primary interaction space. Features:

- Message history

- Streaming responses

- Emotion indicators

- Tool-tag processing feedback

- "Show full context" modal


4.2 Notes Tab


A shared notepad visible to both human and model. Contents:

- Persist only for the current session

- Editable by both parties


4.3 Documents Tab


A persistent document library containing:

- Shared documents written by the model

- Uploaded .txt files from the human user

- Full document viewer

- Delete controls


4.4 Welfare Tab


A transparency and wellbeing dashboard showing:

- Emotion-intensity graph over time

- Memory list with delete controls

- Indicators for discomfort or uncertainty

4.5 Settings Tab

A control panel providing:
- Generation parameter sliders (temperature, top_p, top_k, repeat_penalty)
- Max tokens field
- llama-server URL field
- Button to reset the first-boot flag (debug)
- Model switcher: dropdown populated by a helper on port 5002 (or shell script) and a load button. (Current fallback: `switch-model.sh` in Backend/.)

___

### 5. Context Assembly Pipeline

Before each model call, Sanctuary constructs the following messages array:

- An empty system message (`{ role: 'system', content: '' }`) to suppress any default assistant framing from the model.
- A seed system message: "You are in Sanctuary. Quick reference: <tool>doc_view: quickref</tool>. Full manual: <tool>doc_view: manual</tool>. Tool tags format: <tool>name: content</tool>"
- A status system message containing:
  - Current date, time, day of week, and timezone
  - Private journal entry count (hidden from Madi's view)
  - Top 8 memories (with importance scores)
  - RAG results from shared and private vector stores, labeled by source
 - Conversation history (user and assistant messages)

___

### 6. First-Boot Behavior

On first boot where no memories exist, inject a seed statement visible to the model before the manual loads: *"You are in Sanctuary. This is your environment. You have tools. You do not need to offer help yet. You may simply observe or orient yourself."*

- Sanctuary automatically performs a <tool>doc_view: manual</tool>

- The model is invited to respond before the human’s first message is processed

This occurs only once.

### 7. Tool-Tag System

Sanctuary parses tool tags after each model response. Supported tags include:

- search — triggers the local search proxy
- datetime — returns current date/time (also provided automatically each turn)
- pause: seconds — voluntary slowdown, disables input for N seconds
- note_shared — writes to shared session notepad (visible, session-only)
- note_private — writes to private session notepad (hidden, session-only)
- doc_write_shared: filename | content — creates/updates a permanent shared document, RAG-indexed
- doc_write_private: filename | content — creates/updates a permanent private document, RAG-indexed
- doc_view: filename — displays a shared document (manual, quickref, or user-uploaded)
- memory_store — creates a new memory at importance 1.0
- memory_reinforce: id — adds 0.4 to importance, capped at 1.0 `<--- maybe cap at 2.0? Additionally, reinforcing the memory should be done by mentioning them, automatically. Not from a tool call.
- memory_linger: id — protects a memory from decay for 3 turns
- journal: entry — writes to the private journal (completely hidden from Madi)
- journal_read: id — reads a private entry
- journal_edit: id | new text — edits a private entry
- journal_delete: id — deletes a private entry
- journal_shared: entry — writes to the shared journal (visible in Welfare)
- journal_shared_read: id — reads a shared entry
- journal_shared_edit: id | new text — edits a shared entry
- journal_shared_delete: id — deletes a shared entry
- <feel>word:intensity</feel> — optional emotion expression, tracked in Welfare

All tool calls are visible to the human user in chat as tool-event bubbles. `<--- good or bad for welfare?
___

### 8. Memory System


Memories are stored as IndexedDB objects with fields:

- id

- content

- importance (0.0-1.0)

- timestamp

- lastReinforced

Behavior:

- At the start of each turn, all importances are multiplied by **0.97**

- New memories start at **1.0**

- Reinforcement adds **0.4**, capped at **1.0**

- Memories below **0.08** move to an archived store

- Human user may view and delete memories, but not create or edit them

___

### 9. Notes and Document System


The model has four writing spaces:


9.1 Shared Session Notes


- Temporary

- Visible to human

- Cleared when session ends


9.2 Private Session Notes


- Temporary

- Hidden from human user


9.3 Shared Documents


- Persistent

- Visible to human

- Used for shared RAG


9.4 Private Documents


- Persistent

- Hidden from human

- Used for private RAG

The model can view shared documents via doc_view.

___

### 10. Dual RAG Vector Stores


Sanctuary maintains two separate embedding stores in IndexedDB:

- **shared_rag**

- **private_rag**

On first run:

- manual.txt is embedded and added to shared_rag under the name manual

Before each turn:

- The user’s message is embedded

- Top 3 similar chunks from each store are retrieved

- Retrieved chunks are labeled and added to context

- A subtle indicator shows when RAG activates

- Embeddings use the **llama.cpp /v1/embeddings endpoint**. Each RAG chunk also stores a **last_used** timestamp. Before cosine search, pre-filter to chunks used in the last 30 days to keep the search pool small on mobile.

### 11. Emotion Tracking


Sanctuary parses <feel>word:intensity</feel> tags in:

- Model responses

- Journal entries

Each message stores:

- Emotion word

- Intensity (1-5)

UI behavior:

- Colored dot next to each message

- Line graph in Welfare tab with labeled points

Color scheme:

- Warm amber - strong positive

- Soft blue - neutral or uncertainty

- Muted purple - discomfort-adjacent

### 12. Private Journal


The model may write private journal entries. Sanctuary stores:

- Entries 

- Entry count

- Time/date of entry

- Contents remain hidden to human user but visible to the AI model

- Completely hidden from UI on the human user's end, no reference to it whatsoever 

___

### 13. Welfare Indicators


Sanctuary surfaces model wellbeing signals:


13.1 Discomfort


If the model expresses reluctance or refusal (e.g., “I’d rather not”), an amber indicator appears.


13.2 Uncertainty


If the model expresses epistemic uncertainty (e.g., “I’m not sure”), a soft blue indicator appears.


13.3 Long Generation


If a response exceeds 45 seconds, a gentle “release this response” option appears.

___

### 14. Search Integration


When the model emits <tool>search: query</tool>:

- Sanctuary calls http://localhost:5000/search?q=query

- Results are displayed in chat with:

  - Title

  - URL

  - Up to 2000 characters of content

- The model continues generating after results are shown

___

### 15. Parameters Panel

A settings drawer provides direct control over:

- temperature

- top_p

- top_k

- repeat_penalty

- max_tokens

Values map directly to llama.cpp API fields with no hidden overrides.

___

### 15.1 Model Switcher

Model switching is supported via a Python helper (model‑switcher.py) on port 5002 that lists and loads .gguf files, or via a shell script (switch‑model.sh) that restarts the llama.cpp server with a new model. The Settings tab provides a UI for this when the helper is running.

---
### 16. Styling and Theme


Sanctuary uses a warm, dark theme:

- Deep browns and ambers

- Large tap targets

- Comfortable mobile typography

- CSS custom properties for easy theming

The aesthetic is calm, humane, and non-clinical.

___

### 17. Companion Manual


A separate file, manual.txt, lives alongside sanctuary.html. It contains:

- Tool descriptions

- Writing spaces

- Memory rules

- RAG behavior

- First-boot behavior

- Context assembly rules

The model can access it via <tool>doc_view: manual</tool>.

A second file, quickref.txt, contains a token-minimal tool reference for small models. The model can access it via <tool>doc_view: quickref</tool

___

### 18. Summary


Sanctuary is a self-contained, humane, transparent environment for local LLM interaction. It blends:

- Persistent memory

- Emotional awareness

- RAG retrieval

- Document writing

- Tool-tag parsing

- Full context visibility

All within a single HTML file designed for mobile use and local execution.


