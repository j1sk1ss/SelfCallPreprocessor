import sys
import argparse
sys.path.extend(['.', '..'])

import pyfiglet
from pycparser import c_parser, c_generator
from loguru import logger

from misc.selfcaller import SelfCallHiddenAdder
from misc.preprocessor import SelfcallExtractor

if __name__ == '__main__':
    ascii_banner = pyfiglet.figlet_format("SelfCall preprocessor!")
    print(ascii_banner)
    
    parser = argparse.ArgumentParser(description='SelfCall preprocessor!')
    parser.add_argument('--file', required=True, help='Source C file for the SeflCall preprocessing')
    parser.add_argument('--include', default=None, help='Source include folder for the project')
    parser.add_argument('--symtable', default=None, help='Source an symtable.smt file for the SeflCall preprocessing')
    parser.add_argument("--save-symtab", action="store_true", help="Dump a built symtable")
    args = parser.parse_args()
    
    with open(args.file) as f:
        processor: SelfcallExtractor = SelfcallExtractor(f.read())
        symtab, code = processor.extract()
        
        logger.info(f"Attributed functions: {symtab}")
        logger.info(f"Pre-processed code:\n```c\n{code}```")
        
        parser = c_parser.CParser()
        ast = parser.parse(code)
        
        v: SelfCallHiddenAdder = SelfCallHiddenAdder(symtab=symtab)
        v.visit(ast)
        
        generator = c_generator.CGenerator()
        logger.info(f"Processed code:\n```c\n{generator.visit(ast)}```")
