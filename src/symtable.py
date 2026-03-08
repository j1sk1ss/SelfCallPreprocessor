from pycparser import c_ast
from dataclasses import dataclass

@dataclass
class SymtableDeclaration:
    node: c_ast.Decl = None
    name: str
    primitive_type = None
    s_id: int

@dataclass
class SymtableStructDeclaration(SymtableDeclaration):
    base: c_ast.Struct

class Scope:
    def __init__(self, id: int) -> None:
        self.declarations: dict = {}
        self.id: int = id

    def register_struct_definition(self, node: c_ast.Decl) -> None:
        self.declarations[node.name] = SymtableStructDeclaration(node=node, name=node.name, id=self.id, base=node.children())

    def register_primitive(self, node: c_ast.Decl) -> None:
        self.declarations[node.name] = SymtableDeclaration(node=node, name=node.name, id=self.id)

    def resolve_name(self, name: str) -> SymtableDeclaration | None:
        return self.declarations.get(name, None)

class Symtable:
    def __init__(self) -> None:
        self.scopes: dict = {}
        self.general_scope_id: int = 0
        
    def get_scope(self, id: int) -> Scope:
        existed = self.scopes.get(id, None)
        if not existed:
            existed = Scope(id=id)
            self.scopes[id] = existed
            
        return existed
        
    def register_struct_definition(self, node: c_ast.TypeDecl) -> None:
        scope: Scope = self.get_scope(id=self.general_scope_id)
        
    def register_primitive(self, node: c_ast.Decl) -> None:
        scope: Scope = self.get_scope(id=self.general_scope_id)
        if node.type in ( "long", "int", "short", "char" ):
            scope.register_primitive(node=node)
        
    def push_scope(self) -> None:
        self.general_scope_id += 1
        
    def pop_scope(self) -> None:
        self.general_scope_id -= 1
