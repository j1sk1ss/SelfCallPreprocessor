import re
import difflib

import sys
sys.path.extend(['.', '..'])
from pycparser import c_parser, c_generator
from loguru import logger

from pathlib import Path
from misc.preprocessor import SelfcallExtractor
from misc.selfcaller import SelfCallHiddenAdder

TESTS_DIR = Path("tests")
START = "/*EXPECTED_CODE"
END = "EXPECTED_CODE*/"

def extract_expected_code(path: Path) -> str:
    text = path.read_text(encoding="utf8")

    pattern = rf"{re.escape(START)}(.*?){re.escape(END)}"
    match = re.search(pattern, text, flags=re.DOTALL)
    if not match:
        raise RuntimeError(f"Expected block not found in {path}")

    block = match.group(1).strip()

    code_match = re.search(r"```c(.*?)```", block, flags=re.DOTALL)
    if code_match:
        return code_match.group(1).strip()

    return block

def run_processor(c_file: Path) -> str:
    processor: SelfcallExtractor = SelfcallExtractor(c_file.read_text(encoding="utf8"))
    symtab, struct_graph, code = processor.extract()
    parser = c_parser.CParser()
    ast = parser.parse(code)
    
    v: SelfCallHiddenAdder = SelfCallHiddenAdder(symtab=symtab, struct_graph=struct_graph)
    v.visit(ast)
    
    generator = c_generator.CGenerator()
    return str(generator.visit(ast))

def run_all_tests():
    for c_file in TESTS_DIR.glob("*.c"):
        logger.info(f"=== {c_file.name} ===")

        expected = extract_expected_code(c_file)
        got = run_processor(c_file).strip()

        if got == expected:
            logger.success("PASSED")
            continue

        logger.error("FAILED — diff dump:\n")
        diff = difflib.unified_diff(
            expected.splitlines(),
            got.splitlines(),
            fromfile="expected",
            tofile="got",
            lineterm=""
        )
        
        for line in diff:
            print(line)

if __name__ == "__main__":
    run_all_tests()
