from pycparser import c_ast
from misc.ast import ASTool, CallElement

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

    def _resolve_base_struct_type(self, struct_node: c_ast.Node, call_chain: list[CallElement]) -> str:
        def _get_name(node: c_ast.Node) -> str:
            while not isinstance(node, str):
                node = node.name
            return node
        
        def _get_identifier(node: c_ast.Node) -> c_ast.Node:
            while not isinstance(node, c_ast.IdentifierType):
                node = node.type
            return node
        
        # Find closest declaration node from the symtble
        # It isn't suppose to be a correct declaration. We need to figure out where is a start point
        declaration_name: str = _get_name(struct_node)
        struct_declaration: c_ast.Node = _get_identifier(self.lookup(declaration_name))
        declaration_type: str = struct_declaration.names[0]
        
        # Add redundant the first cast-call
        call_chain.insert(0, CallElement(name=declaration_name, cast=declaration_type, call=call_chain[0].name))
        
        # Select the last defined structure type
        # We do such an action given the C-logic, where a last accessed structure has
        # a same type with the last cast type 
        for call in reversed(call_chain):
            if call.cast:
                declaration_type = call.cast
                break
        
        # Remove redundant the first cast-call
        call_chain = call_chain[1:]

        # Figure out the basic structure type with the symtable usage
        # The main idea is to find a source structure of the field chain
        while True:
            changed = False
            for dep_type, dep_field in self.struct_graph.get(declaration_type, []):
                call = call_chain[0]
                
                # This is the 'cast operation'. Given that it isn't a call,
                # we'll skip it.
                if call.cast:
                    continue
                
                presented: int = -1
                for i in range(len(call_chain)):
                    if call_chain[i].name == dep_field:
                        presented = i
                        break
                
                if presented < 0:
                    continue
                else:
                    call_chain = call_chain[presented:]
                    call = call_chain[0]
                
                # If there is at least one call in the 'field_chain'
                # If the current call uses a field from this structure
                if call_chain and call.name == dep_field:
                    declaration_type = dep_type
                    call_chain = call_chain[1:]
                    changed = True
                    break
                
            if not changed or not call_chain:
                break

        return declaration_type
        
    def _proceed_structcall(self, node) -> None:
        if isinstance(node, c_ast.FuncCall):
            if isinstance(node.name, c_ast.StructRef):
                struct_node, call_chain = ASTool.resolve_structref(node.name)
                base_struct_type: str | None = None
                
                if isinstance(struct_node, c_ast.ID) or isinstance(struct_node, c_ast.ArrayRef):
                    base_struct_type = self._resolve_base_struct_type(struct_node=struct_node, call_chain=call_chain)
                elif isinstance(struct_node, c_ast.Cast):
                    base_struct_type = ASTool.get_base_type_from_cast(struct_node)
                
                func_name = call_chain[-1].name
                args = node.args.exprs if node.args else []
                if (
                    base_struct_type and
                    func_name in self.symtab.get(base_struct_type, []) and
                    not ASTool.has_self_argument(base_struct_type, args)
                ):
                    self_node = ASTool.find_self_for_call(node, call_chain)
                    if self_node:
                        if node.args:
                            node.args.exprs.insert(0, self_node)
                        else:
                            node.args = c_ast.ParamList(params=[ self_node ])

        elif isinstance(node, c_ast.StructRef):
            self._proceed_structcall(node.name)
        
    def visit_FuncCall(self, node):
        try:
            self._proceed_structcall(node)
        except Exception as ex:
            print("Error processing FuncCall:", ex)

        self.generic_visit(node)
