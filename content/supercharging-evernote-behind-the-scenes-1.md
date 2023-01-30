---
Title: Behind the Scenes 2023-01-13 - Supercharging Evernote
Category: Building
Tags: Python, Knowledge Base, Evernote, scikit-learn, Markdown
Date: 2023-01-15
Updated: 2023-01-29
Summary: The first day of the project started with a focus on getting TF-IDF set up and connecting the data to the format that scikit-learn expects. Also, a brief diversion to start with small data before going to the big data approach.
---

The first day of the project started with a focus on getting TF-IDF set up and
connecting the data to the format that scikit-learn expects. Also, a brief
diversion to start with small data before going to the big data approach.

# A Brief Diversion

I decided to start the project with "small data" to make it easier to debug and
understand what's working and how it's working. Instead of using the full
Evernote database and the parsing that requires, I opted to use the blog
content I already have from what I've written. I still have tags, but the
format is much easier to work with (Markdown documents).

# Creating the dataset

To create the dataset, I needed to match the format of a scikit-learn dataset
used in the
[tutorial](https://scikit-learn.org/stable/auto_examples/text/plot_document_clustering.html):

- dataset.target : list of labels
- dataset.data : list of document text content

To do that, I need to turn Markdown text into documents and labels (tags). My
initial approach was to do some manual parsing of the YAML frontmatter (iterate
until a line starts with "Tags:")  and then return the text as the rest;
however, it leads to having to sort out line detritus (https, etc) from each
document. To solve this and better use the known structure of a Markdown
document, I opted to use a Markdown renderer
[mistune](https://github.com/lepture/mistune), but instead of rendering to HTML
or true Markdown, I used the rendering process to strip out Markdown formatting
characters. This (combined with filtering out the front matter) left the
document ready for use with text down to just what I'd be reading when I'm
reading the document.

    :::python
    class StripRenderer(MarkdownRenderer):
        def __init__(self, strip_code=True):
            self.strip_code = strip_code

        def image(self, token, state=None):
            return " "

        def emphasis(self, token, state=None):
            return self.render_children(token, state) + " "

        def strong(self, token, state=None):
            return self.render_children(token, state) + " "

        def link(self, token, state=None):
            return self.render_children(token, state) + " "

        def codespan(self, token, state=None):
            if not self.strip_code:
                return token["raw"] + " "
            return " "

        def heading(self, token, state=None):
            return self.render_children(token, state) + "\n"

        def thematic_break(self, token, state=None):
            return "\n\n"

        def block_code(self, token, state=None):
            if not self.strip_code:
                return token["raw"] + " "
            return " "

With the simplified text content for each document and the tags, it's
straightforward to move to the next step

# Feature Extraction

The feature extraction approach is TF-IDF (see the [project
introduction](/blog/project-concept-supercharging-evernote.html) for more about
TF-IDF). With the tutorial's guidance, the dataset created and scikit-learn's
high quality interface, the vectorization step is pretty concise:

    vectorizer = TfidfVectorizer(
        lowercase=True,
        token_pattern=r"(?u)\b\w\w\w+\b",  # 3 or more alphanumeric
        ngram_range=(1, 3), 
        max_df=0.5,  # maximum in half of documents
        min_df=2,  # minimum in 2 documents
        stop_words="english",
        norm="l2",
        use_idf=True,
        smooth_idf=True,
    )


    X_tfidf = vectorizer.fit_transform(dataset.data)

A couple of things to call out here:

- Use 3 or more alphanumeric characters for the tokens instead of the default
- Use n-grams up to 3. This means that patterns involving combinations of words (e.g. state estimation) can still be picked up in the analysis
- I'm using the default stop words

At this point we can iterate through the documents and word weightings, but
still need to do a few more steps (K-means clustering, finding the top terms
per cluster). With that built, we'll be able to meet the goals of the project,
including finding missing tags and discovering new combinations of ideas in the
data.

