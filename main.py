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
    parser.add_argument('--file', default=None, help='Source C file for the SeflCall preprocessing')
    parser.add_argument('--directory', default=None, help='Source C file for the SeflCall preprocessing')
    parser.add_argument('--include', default=None, help='Source include folder for the project')
    parser.add_argument('--symtable', default=None, help='Source an symtable.smt file for the SeflCall preprocessing')
    parser.add_argument("--save-symtab", action="store_true", help="Dump a built symtable")
    args = parser.parse_args()
    
    if not args.file and not args.directory:
        logger.error("--file or --directory options are required!")
        exit(0)
    
    if args.directory:
        pass
    elif args.file:
        with open(args.file) as f:
            processor: SelfcallExtractor = SelfcallExtractor(f.read())
            symtab, struct_graph = processor.build_symtable()
            processed_code: str = processor.process_code()
            
            logger.info(f"Annotated functions: {symtab}")
            logger.info(f"Structure' dependency graph: {struct_graph}")
            logger.info(f"Pre-processed code:\n```c\n{processed_code}```")
            
            parser = c_parser.CParser()
            ast = parser.parse(processed_code)
            
            v: SelfCallHiddenAdder = SelfCallHiddenAdder(symtab=symtab, struct_graph=struct_graph)
            v.visit(ast)
            
            generator = c_generator.CGenerator()
            logger.info(f"Processed code:\n```c\n{generator.visit(ast)}```")
