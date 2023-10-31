---
Title: Adding Card Support
Category: Building
Tags: Social Media
Date: 2018-12-31
Updated: 2023-10-30
Summary: What are cards? How can I automate making a nicely rendered preview for the articles I write?
---

What are cards? How can I automate making a nicely rendered preview for the articles I write? If they're something I can add easily, it'll make it easier to share my work on social media without affecting the site itself.

# What are cards anyway?

They're nice previews that Twitter or other social media sites can use to dress up a link when it's shared. It provides extra information to encourage a user to click the link.

# Can I automate them?

Yes. I found a helpful [article](https://www.technorms.com/45925/create-shareable-website-facebook-twitter-sharing-tags) by Kyle Nazario. Funny enough, I couldn't find Kyle, but let me know if I missed an obvious link. Jinja templates' `{{ article.* }}` fields within the ``{{ block head }}`` allow for inserting the correct metadata on the article pages.

## Twitter Cards

Twitter cards work with the following tags, split between the base (where I can add universal information) and article pages, where I can fill in the complete metadata (creator, title, description, etc.).

The base HTML extras are as follows:

- `<meta name="tag" content="tag data">`
- `<meta name="twitter:card" content="summary"></meta>`
- `<meta name="twitter:site" content="@beBaskin"></meta>`

The article HTML adds the following:

- `<meta name="twitter:creator" content="@beBaskin"></meta>`
- `<meta name="twitter:title" content="{{article.title}}"></meta>`
- `<meta name="description" content="{{article.summary}}" />`
- `<meta name="twitter:description" content="{{article.summary}}"></meta>`

This post is a little shorter than usual, but it adds an interesting feature that I enjoy.
