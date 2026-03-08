from pycparser import c_ast
from src.symtable import Symtable

class AstWalker(c_ast.NodeVisitor):
    def __init__(self, smt: Symtable) -> None:
        self.smt: Symtable = smt
        self.s_id: int = 0
        
    def visit_Compound(self, node: c_ast.Node) -> None:
        self.s_id += 1
        self.generic_visit(node)
        self.s_id -= 1

    def get_current_scope(self) -> int:
        return self.s_id
