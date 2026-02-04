---
Title: Tools for thought - Ship's Log 5
Category: Building
Tags: Research, Practices, Discovery, TIL
Date: 2026-02-04
Updated: 2026-02-04
Summary: I figured out how to run SentenceTransformer models local-only without network (I think)
---

This one is a shorter post as a note to self for locally running models.

The default behavior for `sentence_transformers` is to download a model from HuggingFace

To make the model run locally:

```
mkdir local_models/all-MiniLM-L6-v2/

pip install huggingface_hub
hf download sentence-transformers/all-MiniLM-L6-v2 --local-dir local_models/all-MiniLM-L6-v2/
```

Then in code:

```python
MODEL = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
```

Becomes

```python
MODEL = SentenceTransformer("local_models/all-MiniLM-L6-v2", local_files_only=True)
```
