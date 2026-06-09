<p align = "center" draggable="false" ><img src="https://github.com/AI-Maker-Space/LLM-Dev-101/assets/37101144/d1343317-fa2f-41e1-8af1-1dbb18399719"
     width="200px"
     height="auto"/>
</p>

<h1 align="center" id="heading">Session 2: Agentic RAG with LangGraph and LangChain</h1>

### [Quicklinks]()

| 📰 Session Sheet | ⏺️ Recording | 🖼️ Slides | 👨‍💻 Repo | 📝 Homework | 📁 Feedback |
|:-----------------|:-------------|:----------|:----------|:------------|:------------|
| [Session 2: Agents](https://github.com/AI-Maker-Space/The-AI-Engineering-Certification-v1.0/tree/main/00_Docs/Modules/02_Agentic_RAG_From_Scratch) |[Recording!](https://us02web.zoom.us/rec/share/QY5jO23FGTCX3yYT_RkogG_aq_BISzHfzN7CcVHP3qeliXKqwBnraUQSNlHtkRUD.OwX79Wfmk0hdy087) <br> passcode: `3fAh&+PM`| [Session 2 Slides](https://canva.link/l06gfshgqhv8svl) | You are here! | [Session 2 Assignment](https://forms.gle/9L3kTpvfJzFoAEDn8) | [Feedback 6/4](https://forms.gle/9L3kTpvfJzFoAEDn8) |

## Main Assignment

In this assignment, you will build an agentic RAG application using LangChain, LangGraph, OpenAI models, and Qdrant.

Session 1 showed a predictable two-step RAG flow:

```text
question -> retrieve -> generate
```

Session 2 makes retrieval agentic:

```text
question -> agent decides whether to retrieve -> optional retriever tool call -> answer
```

The point is not to add a complicated retrieval pipeline. The point is to give the agent a retrieval tool so it can retrieve when it decides retrieval is useful.

You will build that same loop two ways:

1. With LangChain `create_agent` and middleware, which gives you the agent loop quickly and lets you customize its behavior.
2. With LangGraph `StateGraph`, `ToolNode`, and `tools_condition`, so you can see how the loop works.

The main notebook is:

```text
01_Cat_Health_Agentic_RAG_LangGraph_LangChain.ipynb
```

The notebook uses the bundled cat health corpus:

```text
data/cat_health_guidelines.md
```

Complete all questions and activities directly in the notebook.

## Outline

### Breakout Room #1: High-Level Agentic RAG with LangChain

- Task 1: Environment Setup
- Task 2: Load and Index the Cat Health Corpus
- Task 3: Create a Retriever Tool
- Task 4: Build an Agent with `create_agent` and Middleware
- Task 5: Visualize and Stream the `create_agent` Agent
- Activity #1: Add a Retriever Tool-Call Budget

### Breakout Room #2: Explicit Agent Loop with LangGraph

- Task 6: Build the Same Agent Loop with LangGraph
- Activity #2: Add Deterministic Scope Routing
- Advanced Build: Add Explicit Retrieval Quality Control

### Setup

From this folder, install the environment with uv:

```bash
uv sync
```

Then open the notebook in Cursor or VS Code and select the Python/Jupyter environment created by uv.

You will need an OpenAI API key available when running the notebook.

Optional LangSmith tracing:

```bash
export LANGSMITH_TRACING=true
export LANGSMITH_API_KEY="your-key"
```

## Optional Deep Dive: Agentic RAG From Scratch

If you want to look underneath the library abstractions, run the optional reference notebook:

```text
02_Cat_Health_Agentic_RAG_From_Scratch.ipynb
```

It rebuilds the same cat health agentic RAG application with Python standard-library HTTP requests and handcrafted tool, model-adapter, retrieval, and agent-loop primitives.

The application-facing names are inspired by Vercel AI SDK Core, including `tool()`, `generate_text()`, `step_count_is()`, `steps`, `on_step_finish`, `prepare_step`, and `ToolLoopAgent`. The notebook is a reference walkthrough, not an additional assignment.

## Questions and Answers

#### ❓ Question #1

What changes when retrieval becomes a tool instead of a mandatory first step?

##### ✅ Answer:

Sometimes, retrieval doesn't even happen. It also can be more nuanced. The agent could decide to enter a different query for the search rather than rely on the human response to be optimal. Or the agent could do multiple separate targeted calls. Maybe even using subagents.

---

#### ❓ Question #2

What does middleware let us change or observe without rebuilding the agent loop? Why is a model-call limit useful?

##### ✅ Answer:

It lets us build a reliable layer with deterministic code that we can ensure:
1. Runs every time as intended.
2. Lets us add extra things like logging, which in practice is very useful for developing and maintaining agentic systems.
3. Adds guardrails. For instance, having a limit is useful so the model doesn't go crazy and just end up in an infinite loop.

---

#### ❓ Question #3

For each example, did the agent call the retrieval tool? Why or why not?

##### ✅ Answer:

No, in the third example there was no tool call. The reason being the LLM, when initially presented with the user query, correctly recognized that the question was irrelevant. There was no need to retrieve any information, because the result should be the same regardless: telling the user that this query cannot be answered.

---

#### ❓ Question #4

What parts did `create_agent` hide that the explicit LangGraph version made visible? When would you choose middleware, and when would you change the graph itself?

##### ✅ Answer:

`create_agent` is a convenience method. It makes it easy to set up things, but might hide away other details. For instance, it wasn't entirely easy to figure out what the middle layer was doing. LangGraph might be better if you want a more custom solution that's easy to observe the exact internals of the decisions. `create_agent` on the other hand makes it super easy to reuse logic as well as get up and running with a solution.

---

## 🏗️ Activity Notes

### Activity #1: Retriever Tool-Call Budget

- Which retrieval calls did the agent attempt?
- Which call did the middleware allow or block?
- What quality or safety trade-off does this budget introduce?

##### Answer:

- It only attempted one of the retrieval calls, correctly. Although I'm not sure why it chose to perform the second question search first and so the first question search is what was blocked. Probably just coincidence.
- Middleware correctly allowed first tool call, but blocked the second one.
- It puts a guardrail against infinite loops or redundant low-value tool calls. However, it also constrains the model. If it decides to break down the problem solution into multiple tool calls, the system will might get blocked and not be able to construct a full, final solution.

---

### Activity #2: Deterministic Scope Routing

- Which questions bypassed the model-tools loop?
- What happened with the ambiguous question?
- What are the cost, latency, and quality trade-offs of this route?

##### Answer:

- It seemed to filter decently well. The FIFA question was correctly blocked.
- This one was interesting, because even though I didn't mention a cat, it still assumed it should be for a cat. The system really should be tweaked to be more nuanced or give some warning about only having cat-based knowledge.
- Obviously, adding more steps makes things more complicated. Each LLM call adds more tokens consumed and latency. You need to balance that against what you're trying to do. In practice, with AI applications I've created at work, we've actually sought to consolidate requests to counteract these tradeoffs, especially at scale.

---

## Submitting Your Homework

### Main Assignment

Follow these steps to prepare and submit your homework:

1. Pull the latest updates from upstream into the main branch of your AIE9 repo:

```bash
git checkout main
git pull upstream main
git push origin main
```

2. Start Cursor from the `02_Agentic_RAG_LangGraph_LangChain` folder.
3. Complete the notebook questions and activities.
4. Keep useful notebook outputs that help explain your work, especially graph diagrams and representative agent runs. Remove secrets and excessively noisy outputs.
5. Add, commit, and push your modified work to your origin repository.

When submitting your homework, provide the GitHub URL to your AIE9 repo.

### The Advanced Build

If you complete the Advanced Build, include:

- What you changed
- Why you changed it
- How the agent's retrieval decisions or answer quality changed

When submitting your homework, include the GitHub URL to your AIE9 repo.
