---
Title: Making a Website More Accessible
Category: Building
Tags: Accessibility
Date: 2018-12-28
Updated: 2018-12-28
Summary: In reading online, I've always preferred simple, fast-loading websites that are easy to read and don't get in my way from reading their content. In this blog post, I'm going to work on bringing that experience to people who use screen readers.
---

In reading online, I've always preferred simple, fast-loading websites that are easy to read and don't get in my way from reading their content. In this blog post, I'm going to work on bringing that experience to people who use screen readers.

# Rant

## TL DR

This section covers my motivation for why I spend time learning about how to make a better web site, and the short version is that I'm annoyed with common problems that I feel have simple solutions. As part of being a better web-creating citizen, I'd like to improve my ability to bring content to anyone and everyone who reads the site:

## Longer Version, Skip at Will

The thing I hate most, and it's worst on mobile, is a website that continually loads more BS and jumps the content around when I'm trying to read it. There are many news articles or interesting tech articles I've stopped reading, regardless of interest, because the website is unusable with ads and other things loading when I've already scrolled through multiple mobile screens of content.

My second most hated experience is the triple-popup, usually on a website that wants me to use their app instead (top popup), wants me to agree to being tracked to read news or a blog post (bottom popup), and wants me to subscribe to a newsletter so they can track my email engagement too (overlay popup).

In all this, I try to take the time, when I make websites I aim to make them simple, load quickly and primarily focused on content. One area that I can certainly learn to improve is accessibility, and I found an interesting [article](https://benrobertson.io/accessibility/designing-layouts-for-screen-readers) that talks about how to improve readability for screen readers. The article is written by Ben Robertson, who has an entire [blog](https://benrobertson.io/blog/) that covers accessibility topics. Go check out his work.

With accessibility designs in mind, a generated website makes it easy to add accessibility features across all pages.

# Feature 1: A Skip Link

The first step is to add a skip link. This is a link that allows the screen reader to present an early option that goes directly to the main content (remember how I talked about focus on the content?). It's primary use is to skip navigation headers or other similar content if a sidebar is used and it's a good first step to help out those using screen readers. On my website, its primary function is going to be skipping the Building and Breaking title.

## Steps

1. Add a main id to the correct pages in the template
2. Add a link to the top of the page in the template that skips directly to the content labelled with the id `main`
3. Add some css to hide it until it comes in focus

## Step 1: Something to reference

I'm going to cheat on this step and use the existing `content` link that I already have in templates. I also think it's a little more descriptive, but I leave that up to you. At the time of writing (Git commit [b351ec1](https://github.com/buckbaskin/buckbaskin.github.io/commit/b351ec18568f7c9117870e2a2f4bf5cb5a205b2d)) I'm only using the content section in two templates, so I'm going to move that into the base template. If you take a look at the next Git commit (commit [0a4f4be](https://github.com/buckbaskin/buckbaskin.github.io/commit/0a4f4beb27a70136930bc771b18a5079dadb8db4)), you'll see the changes I made to generate a `content` section across every page on the site.

## Step 2: A New Link

The link Ben suggests looks something like:

`<a href="#content" class="skip">Skip to main content</a>`

I'm going to add this to my base template above where I add the section. This way, all pages with a `content` section will also get the link. You can see this fast change in the commit [647b542](https://github.com/buckbaskin/buckbaskin.github.io/commit/647b5423c1b1a2911e47d49eec41e4ac7b4dd814).

## Step 3: The CSS

I'll admit this CSS comes pretty directly from Ben's post, so I recommend you go read up on it in the [skip link section](https://benrobertson.io/accessibility/designing-layouts-for-screen-readers#skip-link) of his blog post. The end result I settled on is shown in the commit [d6280ba](https://github.com/buckbaskin/buckbaskin.github.io/commit/d6280bac9856488a720e05ffa6b9daf9b75d6513).

# Conclusion

Today I've taken my first (simple) steps to making my site more accessible, and I hope I've shown that it's easy to make your site more accessible too. You can find more of my work about accessibility by checking out the [accessibility tag feed](/blog/tag/accessibility.html). I'm also hoping to learn more by checking out an [accessibility reference](https://developers.google.com/web/tools/chrome-devtools/accessibility/reference) by [Kayce Basques](https://developers.google.com/web/resources/contributors/kaycebasques) from Google.