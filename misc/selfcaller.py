from pycparser import c_ast
from misc.ast import ASTool

class SelfCallHiddenAdder(c_ast.NodeVisitor):
    """Main AST walker. The main task of this walker is:
        - Find a structure' function call.
        - Determine a type of this structure.

    Args:
        c_ast (_type_): Default constructor for an AST walker.
    """
    def __init__(self, symtab: dict, struct_graph: dict):
        self.struct_graph = struct_graph
        self.symtab = symtab
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
        
    def _proceed_structcall(self, node) -> None:
        if isinstance(node, c_ast.FuncCall):
            if isinstance(node.name, c_ast.StructRef):
                struct_node, field_chain = ASTool.resolve_structref(node.name)
                base_struct_type: str | None = None
                
                if isinstance(struct_node, c_ast.ID) or isinstance(struct_node, c_ast.ArrayRef):
                    base_struct_type = self._resolve_base_struct_type(struct_node=struct_node, field_chain=field_chain)
                elif isinstance(struct_node, c_ast.Cast):
                    base_struct_type = ASTool.get_base_type_from_cast(struct_node)
                
                func_name, _ = field_chain[-1]
                args = node.args.exprs if node.args else []
                if (
                    base_struct_type and
                    func_name in self.symtab.get(base_struct_type, []) and
                    not ASTool.has_self_argument(base_struct_type, args)
                ):
                    self_node = ASTool.find_self_for_call(node)
                    if self_node:
                        if node.args:
                            node.args.exprs.insert(0, self_node)
                        else:
                            node.args = c_ast.ParamList(params=[ self_node ])

        elif isinstance(node, c_ast.StructRef):
            self._proceed_structcall(node.name)

    def _resolve_base_struct_type(self, struct_node: c_ast.Node, field_chain: list[tuple]) -> str:
        def _get_name(node: c_ast.Node) -> str:
            while not isinstance(node, str):
                node = node.name
            return node
        
        struct_declaration: c_ast.Node = self.lookup(_get_name(struct_node))
        while not isinstance(struct_declaration, c_ast.IdentifierType):
            struct_declaration = struct_declaration.type
            
        declaration_type: str = struct_declaration.names[0]
        for field, cast in reversed(field_chain):
            if cast:
                for dep_type, dep_field in self.struct_graph.get(cast, []):
                    if field == dep_field:
                        declaration_type = dep_type
                        break
                    
        while True:
            changed = False
            for dep_type, dep_field in self.struct_graph.get(declaration_type, []):
                field_name, cast_name = field_chain[0]
                if field_chain and dep_field == field_name or cast_name:
                    declaration_type = dep_type if not cast_name else cast_name 
                    field_chain = field_chain[1:]
                    changed = True
                    break
                
            if not changed or not field_chain:
                break

        return declaration_type
        
    def visit_FuncCall(self, node):
        try:
            self._proceed_structcall(node)
        except Exception as ex:
            print("Error processing FuncCall:", ex)

        self.generic_visit(node)
