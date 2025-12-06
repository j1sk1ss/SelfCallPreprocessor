import re

class SelfcallExtractor:
    # typedef struct [tag]? { body } alias ;
    _typedef_re = re.compile(
        r"""
        typedef\s+struct
            \s*(?P<tag>\w+)?      
            \s*\{(?P<body>.*?)\}\s*
            (?P<alias>\w+)\s*;
        """, re.DOTALL | re.VERBOSE
    )

    # struct name { body };
    _struct_re = re.compile(
        r"""
        struct\s+(?P<name>\w+)\s*\{(?P<body>.*?)\}\s*;
        """, re.DOTALL | re.VERBOSE
    )

    # processor::selfcall
    _processor_selfcall_re = re.compile(
        r"/\*\s*processor::selfcall\s*\*/"
    )

    def __init__(self, code: str):
        self.original_code = code

    def _extract_methods(self, body: str) -> list[str]:
        methods = []
        pattern = re.compile(
            r"""
            (?P<rettype>[\w\s\*\(\)]+?)
            \(\s*\*\s*(?P<fname>\w+)\s*\)
            \s*\(
                (?P<args>[^)]*)
            \)
            \s*;
            """, re.DOTALL | re.VERBOSE
        )

        for m in pattern.finditer(body):
            args = m.group("args")
            if "processor::selfcall" in args:
                methods.append(m.group("fname"))

        uniq = []
        for f in methods:
            if f not in uniq:
                uniq.append(f)

        return uniq

    def _replace_processor_selfcall(self, code: str, struct_name: str) -> str:
        pattern = self._processor_selfcall_re
        repl = f"struct {struct_name}*"

        def do_replace(match: re.Match):
            start = match.start()
            end   = match.end()

            tail = code[end:]
            limit = re.search(r'[);]', tail)
            if limit:
                tail = tail[:limit.start()]

            stripped = tail.lstrip()
            if not stripped:
                return repl

            return f"{repl}, "

        return pattern.sub(do_replace, code)

    def extract(self) -> tuple[dict[str, list[str]], str]:
        result: dict[str, list[str]] = {}
        code = self.original_code
        typedef_matches = list(self._typedef_re.finditer(code))
        for m in typedef_matches:
            tag = m.group("tag")
            alias = m.group("alias")
            body = m.group("body")

            struct_name = tag or f"__anon_struct_{alias}"

            methods = []
            methods.extend(self._extract_methods(body))
            methods.extend(self._extract_methods(body))
            if len(methods) <= 0:
                continue

            if not tag:
                old = m.group(0)
                new = f"typedef struct {struct_name} {{{body}}} {alias};"
                code = code.replace(old, new)

            uniq = []
            for f in methods:
                if f not in uniq:
                    uniq.append(f)

            result[alias] = uniq
            result[struct_name] = uniq.copy()

            code = self._replace_processor_selfcall(code, struct_name)

        struct_matches = list(self._struct_re.finditer(code))
        for m in struct_matches:
            name = m.group("name")
            body = m.group("body")

            methods = []
            methods.extend(self._extract_methods(body))
            methods.extend(self._extract_methods(body))
            if len(methods) <= 0:
                continue

            uniq = []
            for f in methods:
                if f not in uniq:
                    uniq.append(f)

            result[name] = uniq
            code = self._replace_processor_selfcall(code, name)

        return result, code

