import sys
import mistune
from mistune.renderers.markdown import MarkdownRenderer


class SimpleText(MarkdownRenderer):
    def __init__(self, raw_code=False, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.in_preamble = 2

        self.raw_code = raw_code

    def _default(self, args, kwargs):
        print("args")
        print(args)
        print("kwargs")
        print(kwargs)
        1 / 0

    def link(self, token, state):
        return self.render_children(token, state)

    def image(self, token, state):
        return self.render_children(token, state) + "\n"

    def emphasis(self, token, state):
        self._default(token, state)

    def strong(self, token, state):
        return self.render_children(token, state)

    def codespan(self, token, state):
        return token["raw"]

    def linebreak(self, token, state):
        self._default(token, state)

    def softbreak(self, token, state):
        return " "

    def inline_html(self, *args, **kwargs):
        if self.raw_code:
            return token["raw"]
        return "\n"

    def paragraph(self, token, state):
        return self.render_children(token, state) + "\n"

    def heading(self, token, state):
        if self.in_preamble <= 0:
            return self.render_children(token, state) + "\n"
        else:
            self.in_preamble -= 1
            return "\n"

    def blank_line(self, *args, **kwargs):
        return "\n"

    def thematic_break(self, token, state):
        self.in_preamble -= 1
        if self.in_preamble <= 0:
            self._default(token, state)
        else:
            return ""

    def block_text(self, token, state):
        return self.render_children(token, state)

    def block_code(self, token, state):
        if self.raw_code:
            return token["raw"]

        return "\n"

    def block_quote(self, token, state):
        return self.render_children(token, state) + "\n"

    def block_html(self, *args, **kwargs):
        if self.raw_code:
            return token["raw"]
        return "\n"

    def block_error(self, *args, **kwargs):
        self._default(args, kwargs)

    def list(self, token, state):
        return (
            "\n\n".join((self.render_children(li, state) for li in token["children"]))
            + "\n\n"
        )

    def list_item(self, *args, **kwargs):
        self._default(args, kwargs)


def main(file_path):
    format_markdown = mistune.create_markdown(renderer=SimpleText(), plugins=[])

    with open(file_path) as f:
        print(format_markdown(f.read()))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise ValueError("Expects one file argument")

    file_path = sys.argv[1]
    # print(file_path)
    main(file_path)
