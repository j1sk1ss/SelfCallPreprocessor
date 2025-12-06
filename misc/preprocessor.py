import re

class SelfcallExtractor:
    _typedef_re = re.compile(
        r"""
        typedef\s+struct
            \s*(?P<tag>\w+)?      
            \s*\{(?P<body>.*?)\}\s*
            (?P<alias>\w+)\s*;
        """, re.DOTALL | re.VERBOSE
    )

    _struct_re = re.compile(
        r"""
        struct\s+(?P<name>\w+)\s*\{(?P<body>.*?)\}\s*;
        """, re.DOTALL | re.VERBOSE
    )

    _processor_selfcall_re = re.compile(
        r"/\*\s*processor::selfcall\s*\*/"
    )

    _field_re = re.compile(
        r"""
            (?P<full>
                (?P<type>(?:struct\s+)?\w+(?:\s+\w+)*?)
                \s*
                (?P<pointers>\*+)?
                \s*
                (?P<name>\w+)
                \s*;
            )
        """,
        re.VERBOSE
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

    def _extract_field_types(self, body: str) -> list[tuple[str, str]]:
        out = []
        for m in self._field_re.finditer(body):
            t = m.group("type")
            field = m.group("name")
            t = t.replace("struct ", "").strip()
            if t in { 
                "int", "long", "short", "char", "float", "double", "void",
                "unsigned", "signed", "size_t", "uint32_t", "uint64_t" 
            }:
                continue

            out.append((t, field))

        return out

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

    def extract(self) -> tuple[dict[str, list[str]], dict[str, list[str]], str]:
        result: dict[str, list[str]] = {}
        deps: dict[str, list[str]] = {}

        code = self.original_code

        typedef_matches = list(self._typedef_re.finditer(code))
        for m in typedef_matches:
            tag   = m.group("tag")
            alias = m.group("alias")
            body  = m.group("body")

            struct_name = tag or f"__anon_struct_{alias}"

            methods = []
            methods.extend(self._extract_methods(body))
            methods.extend(self._extract_methods(body))

            field_types = self._extract_field_types(body)

            if not tag and len(methods) > 0:
                old = m.group(0)
                new = f"typedef struct {struct_name} {{{body}}} {alias};"
                code = code.replace(old, new)

            uniq_methods = []
            for f in methods:
                if f not in uniq_methods:
                    uniq_methods.append(f)

            if len(methods) == 0:
                struct_name = alias

            if uniq_methods:
                result[alias] = uniq_methods
                result[struct_name] = uniq_methods.copy()

            deps[alias] = field_types.copy()
            deps[struct_name] = field_types.copy()

            code = self._replace_processor_selfcall(code, struct_name)

        struct_matches = list(self._struct_re.finditer(code))
        for m in struct_matches:
            name = m.group("name")
            body = m.group("body")

            methods = []
            methods.extend(self._extract_methods(body))
            methods.extend(self._extract_methods(body))

            field_types = self._extract_field_types(body)

            uniq = []
            for f in methods:
                if f not in uniq:
                    uniq.append(f)

            if uniq:
                result[name] = uniq

            deps[name] = field_types.copy()

            code = self._replace_processor_selfcall(code, name)

        return result, deps, code

if __name__ == '__main__':
    worker: SelfcallExtractor = SelfcallExtractor(
        code="""
typedef struct {
    int (*foo)( /* processor::selfcall */ );
} a_t;

typedef struct {
    a_t a;
} b_t;

typedef struct {
    b_t b;
} c_t;
        """
    )
    
    result, deps, code = worker.extract()
    expected_result = {
        "a_t": ["foo"],
        "__anon_struct_a_t": ["foo"],
    }

    expected_deps = {
        "a_t": [],
        "__anon_struct_a_t": [],
        "b_t": [("a_t", "a")],
        "c_t": [("b_t", "b")],
    }

    assert result == expected_result, f"result mismatch:\n{result}\n!=\n{expected_result}"
    assert deps == expected_deps, f"deps mismatch:\n{deps}\n!=\n{expected_deps}"

    print("Ok")
