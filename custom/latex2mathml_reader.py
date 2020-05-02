from pelican import signals
from pelican.readers import MarkdownReader

try:
    from pyquery import PyQuery as pq
    from lxml import etree
    from lxml.builder import E
    from lxml.etree import Element
    from latex2mathml.converter import convert as latex2mathml
    happy_imports = True
except ImportError:
    happy_imports = False


class LatexToMathMLReader(MarkdownReader):
    enabled = happy_imports

    file_extensions = ['md', 'mdm']

    def __init__(self, *args, **kwargs):
        super(LatexToMathMLReader, self).__init__(*args, **kwargs)

    def read(self, source_path):
        content, metadata = super(LatexToMathMLReader, self).read(source_path)

        if 'math' not in metadata:
            metadata['math'] = False
        metadata['math'] = bool(metadata['math'])
        
        if not metadata['math']:
            return content, metadata

        parsed_content = pq(content)
        parsed_content = self.re_render_math(parsed_content)

        return parsed_content.html(), metadata

    def re_render_math(self, parsed_content):
        for element in parsed_content('img'):
            element = self.render_math_img(element)
        return parsed_content

    def render_math_img(self, tag):
        alt = tag.attrib['alt']

        if alt != 'LaTeX':
            return tag
    
        # alt == 'LaTeX'
        
        source = tag.attrib['src']

        tag.clear()
        tag.tag = 'math'

        mathml = latex2mathml(source)
        prefix = '<math xmlns="http://www.w3.org/1998/Math/MathML">'
        suffix = '</math>'
        mathml_block = etree.fromstring(mathml[len(prefix):-len(suffix)])

        tag.attrib['display'] = 'block'
        tag.attrib['scriptminsize'] = '21pt'
        tag.attrib['xmlns'] = "http://www.w3.org/1998/Math/MathML"
        tag.attrib['alt'] = source

        tag.append(E.semantics(mathml_block))
        return tag


def add_reader(readers):
    for extension in LatexToMathMLReader.file_extensions:
        readers.reader_classes[extension] = LatexToMathMLReader

def register():
    signals.readers_init.connect(add_reader)

