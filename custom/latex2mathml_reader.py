from pelican import signals
from pelican.readers import MarkdownReader

# TODO: Add a if condition to disable parser if this fails
from pyquery import PyQuery as pq
from lxml import etree
from lxml.builder import E
from lxml.etree import Element

class LatexToMathMLReader(MarkdownReader):
    enabled = True

    file_extensions = ['mdm']

    def __init__(self, *args, **kwargs):
        super(LatexToMathMLReader, self).__init__(*args, **kwargs)

    def read(self, source_path):
        print('Input:')
        print('> Source Path')
        print(source_path)

        content, metadata = super(LatexToMathMLReader, self).read(source_path)

        if 'math' not in metadata:
            metadata['math'] = False
        metadata['math'] = bool(metadata['math'])
        
        if not metadata['math']:
            return content, metadata

        print('Output:')

        parsed_content = pq(content)
        print('rendering')
        parsed_content = self.re_render_math(parsed_content)

        print('outer html')
        print(parsed_content.html())

        return parsed_content.html(), metadata

    def re_render_math(self, parsed_content):
        for element in parsed_content('img'):
            element = self.render_math_img(element)
        return parsed_content

    def render_math_img(self, tag):
        alt = tag.attrib['alt']

        if alt != 'LaTeX':
            print('rendering as img %s' % (tag,))
            return tag
    
        # alt == 'LaTeX'
        
        source = tag.attrib['src']
        tag.tag = 'math'

        hardcoded = r'<semantics><mrow><mi>v</mi><mo stretchy="false" form="prefix">(</mo><mi>t</mi><mo stretchy="false" form="postfix">)</mo><mo>=</mo><msub><mi>v</mi><mn>0</mn></msub><mo>+</mo><mfrac><mn>1</mn><mn>2</mn></mfrac><mi>a</mi><msup><mi>t</mi><mn>2</mn></msup></mrow><annotation encoding="application/x-tex">v(t) = v_0 + \frac{1}{2}at^2</annotation></semantics>'
        semantics = etree.fromstring(hardcoded)

        tag.attrib['display'] = 'block'
        tag.attrib['xmlns']='http://www.w3.org/1998/Math/MathML'
        tag.attrib['src'] = source
        tag.attrib['alt'] = source
        tag.clear()
        tag.append(semantics)
        print('children')
        print(list(tag))
        print('rendering as fake %s' % (tag,))
        return tag


def add_reader(readers):
    for extension in LatexToMathMLReader.file_extensions:
        readers.reader_classes[extension] = LatexToMathMLReader

def register():
    signals.readers_init.connect(add_reader)

