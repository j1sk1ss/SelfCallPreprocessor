from loguru import logger
from pycparser import c_ast
from dataclasses import dataclass

@dataclass
class SymtableIdentifier:
    name: str
    base: str
    s_id: int

@dataclass
class SymtableDeclaration:
    name: str
    s_id: int
    node: c_ast.Decl | None = None
    primitive_type = None

@dataclass
class SymtableTypeDeclaration(SymtableDeclaration):
    link: str | None = None

    def __repr__(self):
        return f"name={self.name}"

@dataclass
class SymtableStructDeclaration(SymtableDeclaration):
    content: list[c_ast.Decl] | None = None

class Scope:
    def __init__(self, id: int) -> None:
        self.declarations: dict = {}
        self.id: int = id

    def register_struct(self, node: c_ast.Struct) -> None:
        logger.debug(f"Registered the struct, {node.name}")
        self.declarations[node.name] = SymtableStructDeclaration(node=node, name=node.name, s_id=self.id, content=node.decls[1:])

    def register_type(self, node: c_ast.TypeDecl) -> None:
        logger.debug(f"Registered the type, {node.declname}")
        identifier: c_ast.IdentifierType = node.type
        self.declarations[node.declname] = SymtableTypeDeclaration(node=node, name=node.declname, s_id=self.id, link=identifier.names[0])

    def register_primitive(self, name: str, base: str) -> None:
        logger.debug(f"Registered the primitive, {base} {name}")
        self.declarations[name] = SymtableIdentifier(name=name, base=base, s_id=self.id)

    def __repr__(self):
        return f"decl={self.declarations}"

class Symtable:
    def __init__(self) -> None:
        self.scopes: dict = {}
        self.scope_stack: list = []
        self.general_scope_id: int = 0
        
    def resolve_name(self, name: str) -> SymtableDeclaration | None:
        for id in range(len(self.scope_stack), -1, -1):
            scope: Scope = self.scopes.get(id, None)
            if scope:
                found: SymtableDeclaration | None = scope.declarations.get(name, None)
                if found:
                    return found
                
        return None

    def get_scope(self, id: int) -> Scope:
        existed = self.scopes.get(id, None)
        if not existed:
            existed = Scope(id=id)
            self.scopes[id] = existed
            
        return existed
        
    def register_type(self, node: c_ast.TypeDecl) -> None:
        scope: Scope = self.get_scope(id=self.general_scope_id)
        scope.register_type(node)

    def register_struct(self, node: c_ast.Struct) -> None:
        scope: Scope = self.get_scope(id=self.general_scope_id)
        scope.register_struct(node)

    def register_primitive(self, node: c_ast.Decl) -> None:
        type_decl = node.type
        if not isinstance(type_decl, c_ast.TypeDecl):
            return

        identifier: c_ast.IdentifierType = type_decl.type
        scope: Scope = self.get_scope(id=self.general_scope_id)
        base_type: str = identifier.names[0]
        while not base_type in ( "long", "int", "short", "char" ):
            resolved: SymtableTypeDeclaration | None = self.resolve_name(name=base_type)
            if resolved:
                base_type = resolved.link 
            else:
                break

        scope.register_primitive(name=node.name, base=base_type)
        
    def push_scope(self) -> None:
        self.general_scope_id += 1
        self.scope_stack.append(self.general_scope_id)
        
    def pop_scope(self) -> None:
        self.scope_stack.pop()

    def dump_to_json(self) -> dict:
        return self.scopes
