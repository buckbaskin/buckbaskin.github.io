from pelican import signals
from pelican.readers import MarkdownReader

from urllib.parse import quote_plus
from hashlib import sha256

try:
    from pyquery import PyQuery as pq
    from lxml import etree
    from lxml.builder import E
    from lxml.etree import Element
    from latex2mathml.converter import convert as latex2mathml

    happy_imports = True
except ImportError:
    happy_imports = False

from sympy.printing.preview import preview

FILENAME = "custom/test.png"
PREAMBLE = "\n".join(
    [
        r"\documentclass[21pt]{article}",
        r"\pagestyle{empty}",
        r"\usepackage{amsmath,amsfonts}",
        r"\everymath{\displaystyle}",
        r"\begin{document}",
        r"\Huge",
    ]
)
FILENAME_BASE = "content/img/%s"


def write_to_file(latex, filename):
    preview(
        "$$%s$$" % (latex,),
        output="png",
        viewer="file",
        filename=filename,
        preamble=PREAMBLE,
    )


class LatexToMathMLReader(MarkdownReader):
    enabled = happy_imports

    file_extensions = ["md", "mdm"]

    def __init__(self, *args, **kwargs):
        super(LatexToMathMLReader, self).__init__(*args, **kwargs)
        self.extra_math_images = {}

    def read(self, source_path):
        content, metadata = super(LatexToMathMLReader, self).read(source_path)

        if "math" not in metadata:
            metadata["math"] = False
        metadata["math"] = bool(metadata["math"])

        parsed_content = pq(content)

        self.extra_math_images = {}
        parsed_content = self.re_render_math(parsed_content)
        if len(self.extra_math_images) > 0:
            metadata["math_images"] = self.extra_math_images

        return parsed_content.html(), metadata

    def re_render_math(self, parsed_content):
        for element in parsed_content("img"):
            element = self.render_math_img(element)
        return parsed_content

    def render_math_img(self, tag):
        alt = tag.attrib["alt"]
        tag.attrib["class"] = "wideimage"

        if alt.lower() == "latex" and alt != "LaTeX":
            print("Did you mean LaTeX?")
            return tag
        if alt != "LaTeX":
            return tag

        # alt == 'LaTeX'

        source = tag.attrib["src"]

        name = self.slugify_latex(source)
        self.extra_math_images[name] = source
        file_path = FILENAME_BASE % ("%s.png" % (name,))
        write_to_file(source, file_path)

        mathml = latex2mathml(source)
        prefix = '<math xmlns="http://www.w3.org/1998/Math/MathML">'
        suffix = "</math>"
        mathml_block = etree.fromstring(mathml[len(prefix) : -len(suffix)])

        tag.clear()
        tag.tag = "p"
        tag.attrib["display"] = "block"
        tag.attrib["onclick"] = "document.getElementById('%s').classList.remove('latexhidden');" % (name,)
        tag.append(
            E.math(
                mathml_block,
                display="block",
                scriptminsize="21pt",
                alt=source + " (click to show image)",
                xmlns="http://www.w3.org/1998/Math/MathML",
            ),
        )

        sub_img = E.img(src="/blog/img/%s.png" % (name,), alt=source, display="block")
        sub_img.attrib["class"] = "latex latexhidden"
        sub_img.attrib["id"] = name
        tag.append(sub_img)

        return tag

    def slugify_latex(self, latex):
        return "autoeqn" + sha256(latex.encode()).hexdigest()[:30]


def add_reader(readers):
    for extension in LatexToMathMLReader.file_extensions:
        readers.reader_classes[extension] = LatexToMathMLReader


def register():
    signals.readers_init.connect(add_reader)
