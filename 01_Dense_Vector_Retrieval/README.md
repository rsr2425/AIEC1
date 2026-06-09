<p align = "center" draggable="false" ><img src="https://github.com/AI-Maker-Space/LLM-Dev-101/assets/37101144/d1343317-fa2f-41e1-8af1-1dbb18399719"
     width="200px"
     height="auto"/>
</p>

<h1 align="center" id="heading">Session 1: Dense Vector Retrieval</h1>

### [Quicklinks]()

| 📰 Module Sheet                                                                 | ⏺️ Recording | 🖼️ Slides | 👨‍💻 Repo       | 📝 Homework | 📁 Feedback |
| :------------------------------------------------------------------------------- | :----------- | :-------- | :------------ | :---------- | :---------- |
| [Dense Vector Retrieval](../00_Docs/Modules/01_Dense_Vector_Retrieval/README.md) |[Recording!](https://us02web.zoom.us/rec/share/sHWvo0Nd1aI0SEhKecOLEX9kFGVJJAdYfsKiuTmm8t85W48Z2lnjpnzTy8jAd8R5.PwuqibGwAZhvDd8c) <br> passcode: `C62n^@Q!`| [Session 1 Slides](https://canva.link/htfqf8i39yejyhn) | You are here! | [Session 1 Assignment](https://forms.gle/Z9qskfVaAvPjn6gz8) | [Feedback 6/2](https://forms.gle/21a2uoL9DVZPwgJP6) |


## 🏗️ How AIM Does Assignments

> 📅 **Assignments will always be released to students as live class begins.** We will never release assignments early.

Each assignment will have a few of the following categories of exercises:

- ❓ **Questions** - these will be questions that you will be expected to gather the answer to. These can appear as general questions, or questions meant to spark a discussion in your breakout rooms.

- 🏗️ **Activities** - these will be work or coding activities meant to reinforce specific concepts or theory components.

- 🚧 **Advanced Builds (optional)** - Take on a challenge. These builds require you to create something with minimal guidance outside of the documentation.

## Main Assignment

In this assignment, you will build a vector RAG application using LangChain v1, OpenAI embeddings, and Qdrant.

The main notebook is:

```text
01_Cat_Health_Vector_RAG_LangChain_Qdrant.ipynb
```

The notebook uses the bundled cat health guideline PDF in `data/cat_health_guidelines.pdf`.

### Setup

From this folder, install the environment with uv:

```bash
uv sync
```

Then open the notebook in Cursor or VS Code and select the Python/Jupyter environment created by uv.

You will also need an OpenAI API key available when running the notebook.

---

## 🏗️ Activity #1: Embedding Similarity

Run the embedding similarity primer in the notebook.

You will compare embeddings for terms like:

- `king`
- `queen`
- `banana`
- `cat`
- `veterinarian`
- `cat health guidelines`

#### ❓Question #1

Why is cosine similarity useful for dense vector retrieval?

##### ✅ Answer:

It allows you to compare random strings of text in ways you couldn't do before. You can now do math to get an objective number which tells you relatively how related arbitrary strings are. It ties back directly to the meaning and context of the text.

## 🏗️ Activity #2: Build the Vector RAG Pipeline

Run the notebook sections that:

1. Load the PDF into LangChain `Document` objects
2. Split the document into chunks
3. Embed the chunks
4. Store the chunk embeddings in in-memory Qdrant
5. Retrieve relevant chunks with similarity scores
6. Generate an answer grounded in retrieved context

#### ❓Question #2

Why is metadata important for a RAG application?

##### ✅ Answer:

Metadata helps contextualize chunks for a RAG application. Remember that a chunk is more or less a random string that might not make sense in isolation. It can be helpful to retrieve that context back to make the RAG application better. Maybe you want to pass that as part of the prompt. Maybe you want to include this (as well as the chunk) when citing the sources used for a response. You could even recover all the chunks associated with any specific document and include those whenever your retrieval system returns a single chunk. All of these things require metadata to make it possible.

#### ❓Question #3

What tradeoff do we make when choosing chunk size and chunk overlap?

##### ✅ Answer:

By breaking down documents into chunks, you are able to:
1. Include the most relevant information to a response. To answer a specific question, you often won't need the entire document.
2. Maximize the valuable content you can fit into a context window. You can include information from many more documents when you only include relevant chunks.

So smaller chunk sizes give you more flexibility. However, smaller chunk size also means you have more chunks you have to sift through, which might have performance implications.

Chunk overlap is related to this tradeoff as well. 0 overlap means you minimize redundant tokens passed to the prompt as well as number of tokens generated overall. However, depending on how you chunk documents, the chunks themselves may not contain all relevant information. Maybe important pieces are between two chunks, and are indecipherable because it's partially in one chunk and another that may or may not have been picked up by the retrieval system.

#### ❓Question #4

What does a similarity score help you understand, and what does it not prove by itself?

##### ✅ Answer:

It helps you understand the degree to which two strings are talking about the same topic. The absolute number also doesn't matter as much (especially since different models can provide different absolute scores). However, they are useful to indicate relative similarity. You can use them to sort your chunks and only grab the most important pieces.

It does not PROVE that two strings are related or speaking to the same topic. In RAG, it's used only to help filter down and maximize the number of relevant chunks when we limit ourselves to passing say the top 10 most relevant chunks to the LLM to get an answer.

---

## 🏗️ Activity #3: Vibe Check Retrieval Quality

Run the notebook's vibe check queries and inspect both:

- The retrieved context
- The generated answer

#### ❓Question #5

For the vibe check queries, did the retrieved context seem relevant before generation? Why or why not?

##### ✅ Answer:

Just going off the vibes, it seems pretty decent. They seem relevant for answering questions about a cat's health. The scores don't seem high per se (all around ~0.5) but directionally that's right and it's hard to make any determination based on absolute similarity score.

---

## 🏗️ Activity #4: Tune Retrieval

Improve retrieval quality by changing one or more of:

- Chunk size
- Chunk overlap
- Retrieval `k`
- Query wording

Document what changed and whether retrieval improved.

##### Settings Changed:

| Setting | Before | After |
|---|---|---|
| `chunk_size` | 1000 | 500 |
| `chunk_overlap` | 200 | 100 |
| `k` | 4 | 10 |

##### Results:

With smaller chunks and a higher `k`, the retrieval returned more sources spread across more pages. The answers still looked reasonable and were well-cited.

**Did retrieval improve?** Hard to say definitively — without being a subject matter expert (SME), it's hard to judge whether the additional sources were genuinely more relevant or just more numerous. The scores were similar (~0.52–0.60). But validating true retrieval quality really requires domain expertise to confirm the right information was surfaced. I also hard more of an issue with formatting, which seems to have somehow gotten worse with more sources. Definitely needs some prompt tuning.

---

## Optional Deep Dive: RAG From Scratch

If you want to look underneath the library abstractions, run the optional reference notebook:

```text
02_Cat_Health_Vector_RAG_From_Scratch.ipynb
```

It builds the same retrieval pipeline again with only:

- `pypdf` for extracting text from the PDF
- Python standard-library HTTP requests for calling OpenAI
- Handcrafted document, chunking, embedding, similarity-search, vector-store, and generation primitives

This notebook is a reference walkthrough, not an additional assignment. Its purpose is to make the responsibilities hidden by LangChain, Qdrant, and provider SDKs visible.

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

2. Start Cursor from the `01_Dense_Vector_Retrieval` folder.
3. Complete the notebook.
4. Answer the questions in this `README.md`.
5. Add, commit, and push your modified work to your origin repository.

When submitting your homework, provide the GitHub URL to your AIE9 repo.
