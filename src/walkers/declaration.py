from pycparser import c_ast

from src.symtable import Symtable
from src.walkers.base import AstWalker

class DeclarationWalker(AstWalker):
    def __init__(self, smt: Symtable) -> None:
        super().__init__(smt)
        
    def visit_Compound(self, node: c_ast.Node) -> None:
        self.smt.push_scope()
        self.generic_visit(node)
        self.smt.pop_scope()
        
    def visit_Decl(self, node: c_ast.Decl):
        self.generic_visit(node)
