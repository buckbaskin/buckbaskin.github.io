---
Title: Out Of Memory VectorDB
Category: Building
Tags: Research, Discovery, Vector Database, sqlite
Date: 2025-02-25
Updated: 2025-02-27
Summary: Building
---

[Last I left off]({filename}/tools-for-thought-ships-log-03.md), I had way more
content that I wanted to embed and search relative to what my laptop could keep
in memory, leaving me with no interactive tooling.

# Research

My initial point of research is 
[Simon Willison's post about sqlite-vec](https://til.simonwillison.net/sqlite/sqlite-vec)
for working with embeddings in sqlite. There are many vector databases out
there, but I've grown quite found of sqlite and appreciate that it's available
almost everywhere.

- [Github page for the extension](https://github.com/asg017/sqlite-vec)
- [Python documentation](https://alexgarcia.xyz/sqlite-vec/python.html)
- [Python demo.py](https://github.com/asg017/sqlite-vec/blob/main/examples/simple-python/demo.py)

# Process

I really did enjoy the fairly simple interface of 
[Kagi's vectordb](https://github.com/kagisearch/vectordb/tree/main), 
so I'm going to stick to re-implementing that approach (and also borrowing the
embeddings).

## Testing

Pytest

[parameterized testing](https://docs.pytest.org/en/stable/example/parametrize.html)

[tmp_path](https://docs.pytest.org/en/6.2.x/tmpdir.html) to allow for temporary memory files


1. Use the existing kagi Memory class as the model
2. Implement a new class with the same interface
3. Fill out the class implementation with sqlite-vec
4. Assert I can reproduce the same results

# Links

- https://arxiv.org/category_taxonomy
- https://arxiv.org/search/?query=compressive+sensing&searchtype=all&source=header
- https://arxiv.org/search/?query=simd&searchtype=all&source=header
- https://github.com/kagisearch/vectordb/blob/main/vectordb/memory.py
- https://github.com/jina-ai/vectordb/ (alternative vector db)
- https://til.simonwillison.net/sqlite/sqlite-vec
- https://github.com/asg017/sqlite-vec
- https://github.com/asg017/sqlite-vec/blob/main/examples/simple-python/demo.py
- https://alexgarcia.xyz/sqlite-vec/features/vec0.html#metadata
- https://www.sqlite.org/vtab.html

- https://docs.pytest.org/en/stable/example/parametrize.html
- https://docs.pytest.org/en/6.2.x/tmpdir.html
- https://stackoverflow.com/questions/36070031/creating-a-temporary-directory-in-pytest

- https://stackoverflow.com/questions/16913086/ubuntu-add-directory-to-python-path
- https://stackoverflow.com/questions/17330160/how-does-the-property-decorator-work-in-python

- https://docs.python.org/3/library/sqlite3.html#sqlite3.Cursor.fetchone

- https://stackoverflow.com/questions/3267145/makefile-execute-another-target

# P.S.

The title refers to my computer being out of memory, as well as a vector
database that exists outside of the constraints of the memory of one machine
