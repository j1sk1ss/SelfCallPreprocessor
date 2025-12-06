import sys
import argparse
sys.path.extend(['.', '..'])
from pycparser import c_parser, c_generator

from misc.selfcaller import SelfCallHiddenAdder
from misc.preprocessor import SelfcallExtractor

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='SelfCall preprocessor!')
    parser.add_argument('--file', required=True, help='Source C file for the SeflCall preprocessing')
    args = parser.parse_args()
    
    with open(args.file) as f:
        processor: SelfcallExtractor = SelfcallExtractor(f.read())
        symtab, code = processor.extract()
        
        print(f"[LOG] Attributed functions: {symtab}")
        print(f"[LOG] Pre-processed code:\n```c\n{code}```")
        
        parser = c_parser.CParser()
        ast = parser.parse(code)
        
        v: SelfCallHiddenAdder = SelfCallHiddenAdder(symtab=symtab)
        v.visit(ast)
        
        generator = c_generator.CGenerator()
        print(generator.visit(ast))
    