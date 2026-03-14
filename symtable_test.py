import sys
import argparse
sys.path.extend(['.', '..'])

import pyfiglet
from pycparser import c_parser, c_ast
from loguru import logger

from src.symtable import Symtable
from src.walkers.declaration import DeclarationWalker
from src.directive import DirectiveParser

if __name__ == '__main__':
    ascii_banner = pyfiglet.figlet_format("SelfCall preprocessor!")
    print(ascii_banner)
    
    parser = argparse.ArgumentParser(description='SelfCall preprocessor!')
    parser.add_argument('--file', default=None, help='Source C file for the SeflCall preprocessing')
    parser.add_argument('--include', default=None, help='Source an include folder for the project')
    parser.add_argument("--emit-ast", action="store_true", help="Emit the produced AST")
    args = parser.parse_args()
    
    if not args.file and not args.directory:
        logger.error("--file or --directory options are required!")
        exit(0)
    
    if args.file:
        with open(args.file) as f:
            processor: DirectiveParser = DirectiveParser(f.read())
            symtab, struct_graph = processor.build_symtable()
            processed_code: str = processor.process_code()
            
            logger.info(f"Annotated functions: {symtab}")
            logger.info(f"Structure' dependency graph: {struct_graph}")
            logger.info(f"Pre-processed code:\n```c\n{processed_code}```")
            
            parser = c_parser.CParser()
            ast: c_ast.FileAST = parser.parse(processed_code)
            if args.emit_ast:
                ast.show()
            
            smt: Symtable = Symtable()
            v: DeclarationWalker = DeclarationWalker(smt=smt)
            v.visit(ast)
            
            print(smt.dump_to_json())
