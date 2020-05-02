---
Title: Rendering Math ML
Category: Building
Tags: MathML, MathJax, Rendering, Yak Shaving
Date: 2020-05-01
Updated: 2020-05-01
Summary: I'd like to render mathematical equations nicely in the browser. MathML seems like the right tool, but it's not supported everywhere.
---

I'd like to render mathematical equations nicely in the browser. MathML
seems like the right tool, but it's not supported everywhere.

# Exploring Ways to Get Math to the Web

Examples are based on Pandoc's [math demo
text](https://pandoc.org/demo/math.text) and Mozilla's [MathML Torture
Test](https://mdn.mozillademos.org/en-US/docs/Mozilla/MathML_Project/MathML_Torture_Test$samples/MathML_Torture_Test)

<!-- TODO! Check on the licensing for the two example pages. -->

## First Attempt

Write it and see what Pelican does without modification:

`$v(t) = v_0 + \frac{1}{2}at^2$`

Renders as:

$v(t) = v_0 + \frac{1}{2}at^2$

Unfortunately, Pelican doesn't know what to do with it, so I just get the plain
text.

## Second Attempt

Embed an html fragment using Jinja include syntax. This would allow me to
compile the latex into MathML using other tools, such as Pandoc.

{% include '/index.html' %}

## Third Attempt

Just to confirm things would work, I'm copying some raw MathML here from the
Pandoc example. I made one small edit to change the display from `inline` to
`block`.

<math display="block" xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mrow><mi>v</mi><mo stretchy="false" form="prefix">(</mo><mi>t</mi><mo stretchy="false" form="postfix">)</mo><mo>=</mo><msub><mi>v</mi><mn>0</mn></msub><mo>+</mo><mfrac><mn>1</mn><mn>2</mn></mfrac><mi>a</mi><msup><mi>t</mi><mn>2</mn></msup></mrow><annotation encoding="application/x-tex">v(t) = v_0 + \frac{1}{2}at^2</annotation></semantics></math>

With a little styling modification to the CSS, it'll actually work out nicely.
I'm just adding `10px` of padding for now and I can come back to it later if
that doesn't work.

## Render it as an image

This would likely slow down the page loading with lots of images for math, but
it could work. I'd also have to change how my image styling works slightly
because I'd expect the math equations to be different proportions than the usual
images taken with a camera.

This is promising, but I'd like to see if I can use web technologies to do
better.

## Manual Scripting

One thing I'm considering is using some sort of automation to find and replace
Latex code with rendered MathML using some external tool. I could use an easily
matched regex (e.g. `![Math](.*)`) and then strip the leading and trailing
parenthesis and substitute the middle section of the match with whatever MathML
rendering I get.

Now to figure out if I can do better than manually copying in MathML.

## Customizing Pelican

Pelican provides support for
[plugins](https://docs.getpelican.com/en/4.0.1/plugins.html) that can be used to
modify or replace how certain parts of the
[internals](https://docs.getpelican.com/en/4.0.1/internals.html) work. I think
the easiest thing to do here would be to implement a new reader that interrupts
the existing Markdown Reader (preferred, yay code re-use!) or borrows its 
implementation (taking inspiration from open source software, I should 
contribute it back).

I'm just going to say, their pretty short version of the Markdown reader in
their
[docs](https://docs.getpelican.com/en/4.0.1/internals.html#how-to-implement-a-new-reader)
does not match the
[source](https://github.com/getpelican/pelican/blob/e87717d27c8689ae288d1ab244648f38d20e3ddf/pelican/readers.py#L281-L343)
which is noticeably more complicated. The `read` function is pretty close
though.

To best leverage the existing code, I can either call something before the read
function and then call the existing read function, or I can capture the output
of the existing read and modify it. I'll need to do a little sleuthing to figure
out what each looks like.

Time passes...

In the end, I decided to parse the HTML output of the original Markdown parser,
then find special `img` tags with the alt text `LaTeX`. From there, I edit that
tag in place to move the original LaTeX source to the alt text and render the
LaTeX into the child elements as MathML. This is effectively using some Python
libraries and Pelican to take the "Scripting" approach.

The end Markdown syntax looks like:

`![LaTeX](insert^{LaTeX}_{here})`

And rendered:

![LaTeX](insert^{LaTeX}_{here})

Useful: Pelican [source](https://github.com/getpelican/pelican)

Also Useful: Pelican [plugin library](https://github.com/getpelican/pelican-plugins)

# But What about Unsupported Browsers?

I'm looking at you Chrome

I think the answer may involve using a [Sympy
viewer](https://stackoverflow.com/questions/1381741/converting-latex-code-to-images-or-other-displayble-format-with-python)

