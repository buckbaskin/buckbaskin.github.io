---
Title: Making a Website More Accessible: Part 2
Category: Building
Tags: Accessibility
Date: 2018-12-30
Updated: 2018-12-30
Summary: In this blog post, I'm going to work on bringing a nicer experience to people who use screen readers by adding ARIA landmarks and roles.
---

In this blog post, I'm going to work on bringing a nicer experience to people who use screen readers by adding ARIA landmarks and roles. ARIA stands for Accessible Rich Internet Applications. Landmarks are key points on the page common across many applications where a user might want to jump to easily. This work continues changes I'm making based on suggestions from Ben Robertson's blog post on [accessibility for screen readers](https://benrobertson.io/accessibility/designing-layouts-for-screen-readers).

# Feature: ARIA Roles

## Potential Roles

For more information, see the W3.org [ARIA doc](https://www.w3.org/TR/wai-aria-1.1).

1. `banner` - Site info at the top of the page
2. `complementary` - Alternate information that could be useful. An example might be weather information on a web page about a baseball game
3. `contentinfo` - A region with additional information about the page, for example a copyright or privacy notice
4. `form` - The div containing the elements of a form, see also search
5. `main` - The main content of the page. I should probably use this as the canonical name instead of content.
6. `navigation` - Elements for getting around the page
7. `region` - An important section of the page
8. `search` - Self explanatory

For me, I'm interested in banner and main. I might get into some of the other roles in the future, but right now my content tends to focus on a single topic and the navigation isn't too complicated. Ben's article also recommends header, section and the content class to go with the main role.

# Feature: ARIA Labels

[Ben's post](https://benrobertson.io/accessibility/designing-layouts-for-screen-readers#using-appropriate-aria-labels) also suggests using ARIA labels to help augment what the screen reader can provide. Recommended labels include "Primary Menu" for navigation and main-title ("Main Content") for the title. This feature is really part of making the ARIA roles and landmarks more helpful to the user.

# Conclusion

In conclusion, I've added some additional semantic labels to my templates that should make my pages more easy to navigate with a screen reader. It's been a fun experiment into making websites more accessible. I hope to learn more about accessibility and demonstrate it here. If there's something I'm missing or doing incorrectly, let me know on Twitter [@beBaskin](https://twitter.com/beBaskin).