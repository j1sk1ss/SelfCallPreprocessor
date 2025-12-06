import re

class SelfcallExtractor:
    """
    typedef struct NAME { ... } ALIAS;
    {
        "NAME"  -> [attribute functions]
        "ALIAS" -> [attribute functions]
    }
    """

    _typedef_re = re.compile(
        r"""
        typedef\s+struct
            \s*(?P<tag>\w+)?
            \s*\{(?P<body>.*?)\}\s*
            (?P<alias>\w+)\s*;
        """,
        re.DOTALL | re.VERBOSE
    )

    _struct_re = re.compile(
        r"""
        struct\s+(?P<name>\w+)\s*\{(?P<body>.*?)\}\s*;
        """,
        re.DOTALL | re.VERBOSE
    )

    _fp_with_attr_re = re.compile(
        r"""
        (?P<rettype>[\w\s\*\(\)\[\]]+?)
        \s*
        __attribute__\s*\(\(\s*(?P<attrs>[^)]+?)\)\)
        \s*\(\s*\*\s*(?P<fname>\w+)\s*\)
        \s*\(\s*(?P<args>[^;)]*?)\s*\)
        \s*;
        """,
        re.DOTALL | re.VERBOSE
    )
    
    _attr_remove_re = re.compile(
        r"__attribute__\s*\(\([^)]*\)\)",
        re.DOTALL
    )

    def __init__(self, code: str):
        self.code = code

    def _extract_methods(self, body: str) -> list[str]:
        methods = []
        for m in self._fp_with_attr_re.finditer(body):
            if "selfcall" in m.group("attrs"):
                methods.append(m.group("fname"))
        
        out = []
        for f in methods:
            if f not in out:
                out.append(f)
        
        return out

    def extract(self) -> tuple:
        result = {}

        for m in self._typedef_re.finditer(self.code):
            tag = m.group("tag")
            alias = m.group("alias")
            body = m.group("body")

            methods = self._extract_methods(body)
            result[alias] = methods
            struct_name = tag or alias
            result[struct_name] = methods.copy()

        for m in self._struct_re.finditer(self.code):
            name = m.group("name")
            body = m.group("body")
            methods = self._extract_methods(body)
            result[name] = methods

        cleaned_code = self._attr_remove_re.sub("", self.code)
        return result, cleaned_code
