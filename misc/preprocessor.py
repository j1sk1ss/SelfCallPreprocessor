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
    
    _comments = re.compile(
        r"""
        //.*?$            |
        /\*.*?\*/
        """,
        re.DOTALL | re.MULTILINE | re.VERBOSE
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

        return self._processor_selfcall_re.sub(do_replace, code)

    def build_symtable(self) -> tuple[dict[str, list[str]], dict[str, list[str]]]:
        symtable: dict[str, list[str]] = {}
        dep_graph: dict[str, list[str]] = {}
        
        for m in self._typedef_re.finditer(self.original_code):
            tag   = m.group("tag")
            alias = m.group("alias")
            body  = m.group("body")

            methods = []
            methods.extend(self._extract_methods(body))
            methods.extend(self._extract_methods(body))

            field_types = self._extract_field_types(body)
            uniq_methods = []
            for f in methods:
                if f not in uniq_methods:
                    uniq_methods.append(f)

            if len(methods) == 0:
                struct_name = alias
            else:
                struct_name = tag or f"__anon_struct_{alias}"
                
            if uniq_methods:
                symtable[alias] = uniq_methods
                symtable[struct_name] = uniq_methods.copy()

            dep_graph[alias] = field_types.copy()
            dep_graph[struct_name] = field_types.copy()

        for m in self._struct_re.finditer(self.original_code):
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
                symtable[name] = uniq

            dep_graph[name] = field_types.copy()

        return symtable, dep_graph

    def process_code(self) -> str:
        code = self.original_code
        for m in self._typedef_re.finditer(code):
            tag   = m.group("tag")
            alias = m.group("alias")
            body  = m.group("body")

            methods = []
            methods.extend(self._extract_methods(body))
            methods.extend(self._extract_methods(body))

            struct_name = tag or f"__anon_struct_{alias}"
            new_body = self._replace_processor_selfcall(body, struct_name)
            if not tag and len(methods) > 0:
                old = m.group(0)
                new = f"typedef struct {struct_name} {{{new_body}}} {alias};"
                code = code.replace(old, new)
            else:
                old_body = m.group("body")
                if old_body != new_body:
                    old = m.group(0)
                    start = old.find("{") + 1
                    end = old.rfind("}")
                    new_definition = old[:start] + new_body + old[end:]
                    code = code.replace(old, new_definition)

            uniq_methods = []
            for f in methods:
                if f not in uniq_methods:
                    uniq_methods.append(f)

            if len(methods) == 0:
                struct_name = alias

        for m in self._struct_re.finditer(code):
            name = m.group("name")
            code = self._replace_processor_selfcall(code, name)

        code = re.sub(self._comments, "", code)
        return code

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

/*EXPECTED_CODE
EXPECTED_CODE*/
        """
    )
    
    result, deps = worker.build_symtable()
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

    expected: str = """
typedef struct __anon_struct_a_t {
    int (*foo)( struct __anon_struct_a_t* );
} a_t;

typedef struct {
    a_t a;
} b_t;

typedef struct {
    b_t b;
} c_t;
    """

    assert worker.process_code().strip() == expected.strip(), "Resuled code mismatch!"
    print("Ok")
