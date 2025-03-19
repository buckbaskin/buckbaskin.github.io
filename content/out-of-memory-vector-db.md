---
Title: Out Of Memory VectorDB
Category: Building
Tags: Research, Discovery, Vector Database, sqlite
Date: 2025-02-25
Updated: 2025-03-18
Summary: Last I left off, I had way more content that I wanted to embed and search relative to what my laptop could keep in memory, leaving me with no interactive tooling. Where to go from there? Let's start with sqlite-vec
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

Sqlite also has a nice benefit that the database is managed as a single file,
so it's easy to experiment and blow away unwanted experimental directions, or
checkpoint and restore if I'd like.

# Process

I really did enjoy the fairly simple interface of 
[Kagi's vectordb](https://github.com/kagisearch/vectordb/tree/main), 
so I'm going to stick to re-implementing that approach (and also borrowing the
embeddings).

## Testing

Sticking to the same interface also offers me the opportunity to write some
fairly straightforward testing for the project by writing each test with two
test cases: the oracle (the existing database) and the new version, based by
sqlite.

This leverages a nice feature of pytest called 
[parameterized testing](https://docs.pytest.org/en/stable/example/parametrize.html)

The process looks something like:

1. Use the existing kagi Memory class as the model
2. Implement a new class with the same interface
3. Fill out the class implementation with sqlite-vec
4. Assert I can reproduce the same results

My original testing used the pytest feature
[tmp_path](https://docs.pytest.org/en/6.2.x/tmpdir.html) to allow for temporary
memory files managed by the test runner; however, in the end I think it's
easier to use sqlite's in-memory database (but allowing for me to run tests as
if it's backed by a sqlite file.


# Links

## Content To Explore

... once I finish this implementation tangent to expand the knowledge base size I can manage

- https://arxiv.org/category_taxonomy
- https://arxiv.org/search/?query=compressive+sensing&searchtype=all&source=header
- https://arxiv.org/search/?query=simd&searchtype=all&source=header

## VectorDB implementations

- https://github.com/kagisearch/vectordb/blob/main/vectordb/memory.py
- https://github.com/jina-ai/vectordb/ (alternative vector db)

### sqlite-vec

- https://til.simonwillison.net/sqlite/sqlite-vec
- https://github.com/asg017/sqlite-vec
- https://github.com/asg017/sqlite-vec/blob/main/examples/simple-python/demo.py
- https://alexgarcia.xyz/sqlite-vec/features/vec0.html#metadata
- https://www.sqlite.org/vtab.html
- https://docs.python.org/3/library/sqlite3.html#sqlite3.Cursor.fetchone

## Pytest Testing

- https://docs.pytest.org/en/stable/example/parametrize.html
- https://docs.pytest.org/en/6.2.x/tmpdir.html
- https://stackoverflow.com/questions/36070031/creating-a-temporary-directory-in-pytest

## Python and Makefile Curiosities

- https://stackoverflow.com/questions/17330160/how-does-the-property-decorator-work-in-python

- https://stackoverflow.com/questions/3267145/makefile-execute-another-target
