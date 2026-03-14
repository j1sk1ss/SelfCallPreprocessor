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
        
    def visit_Typedef(self, node: c_ast.Typedef):
        self.smt.register_type(node=node.type)
        self.generic_visit(node)

    def visit_Decl(self, node: c_ast.Decl):
        if isinstance(node.type, c_ast.Struct):
            self.smt.register_struct(node=node.type)
        else:
            self.smt.register_primitive(node=node)
        self.generic_visit(node)
