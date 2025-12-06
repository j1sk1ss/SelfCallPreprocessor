from pycparser import c_ast

def _get_base_type_from_decl(node) -> str | None:
    if isinstance(node, c_ast.Decl):
        return _get_base_type_from_decl(node.type)
    elif isinstance(node, c_ast.PtrDecl):
        return _get_base_type_from_decl(node.type)
    elif isinstance(node, c_ast.TypeDecl):
        return _get_base_type_from_decl(node.type)
    elif isinstance(node, c_ast.IdentifierType):
        return node.names[0]
    
    return None
    
def _get_name_from_cast(node) -> str | None:
    if isinstance(node, c_ast.Cast):
        return _get_name_from_cast(node.expr)
    elif isinstance(node, c_ast.ID):
        return node.name
    
    return None

class SelfCallHiddenAdder(c_ast.NodeVisitor):
    """Main AST walker. The main task of this walker is:
        - Find a structure's function call
        - Determine a type of this structure
        - Check a symtable for a __attribute__((selfcall)) attribute

    Args:
        c_ast (_type_): Default constructor for an AST walker
    """
    def __init__(self):
        self.scopes = [{}]
        
    def push_scope(self) -> None:
        self.scopes.append({})

    def pop_scope(self) -> None:
        self.scopes.pop()

    def add_symbol(self, name: str, decl) -> None:
        self.scopes[-1][name] = decl

    def lookup(self, name: str):
        for scope in reversed(self.scopes):
            if name in scope.keys():
                return scope[name]
            
        return None
        
    def visit_Decl(self, node):
        self.add_symbol(node.name, node)
        self.generic_visit(node)

    def visit_Compound(self, node):
        self.push_scope()
        self.generic_visit(node)
        self.pop_scope()
        
    def visit_FuncCall(self, node):
        try:
            if isinstance(node.name, c_ast.StructRef):
                if node.name.type in ['->', '.']:
                    structure_name: str | None = None
                    struct_field: str = node.name.field.name
                    base_structure: str | None = None
                    
                    args: list | None = None
                    if node.args:
                        args = []
                        for i in node.args.exprs:
                            args.append(i)
                    
                    if isinstance(node.name.name, c_ast.Cast):
                        structure_name = _get_name_from_cast(node.name.name)
                        base_structure = node.name.name.to_type.type.type.type.names[0]
                    elif isinstance(node.name.name, c_ast.ID):
                        structure_name = node.name.name.name
                        base_structure = self.lookup(structure_name)
                        if base_structure:
                            base_structure = _get_base_type_from_decl(base_structure)
                        
                    print(f"[{base_structure}] {structure_name}.{struct_field}")
        except Exception as ex:
            print(ex)
