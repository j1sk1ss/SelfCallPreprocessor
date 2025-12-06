from pycparser import c_ast

def _get_base_type_from_decl(node) -> str | None:
    """AST help function.
        Primarily works with declaration node.

    Args:
        node (c_ast.Decl): Declaration node.

    Returns:
        str | None: The base type of the node.
    """
    if isinstance(node, c_ast.Decl):
        return _get_base_type_from_decl(node.type)
    elif isinstance(node, c_ast.PtrDecl):
        return _get_base_type_from_decl(node.type)
    elif isinstance(node, c_ast.TypeDecl):
        return _get_base_type_from_decl(node.type)
    elif isinstance(node, c_ast.IdentifierType):
        return node.names[0]
    
    return None
    
def _get_base_type_from_cast(node: c_ast.Cast | c_ast.ID) -> str | None:
    """Return type from the cast AST node.

    Args:
        node (c_ast.Cast | c_ast.ID): Cast node.

    Returns:
        str | None: Variable's name that is casted.
    """
    if isinstance(node, c_ast.Cast):
        return node.to_type.type.type.type.names[0]
    elif isinstance(node, c_ast.StructRef):
        return _get_base_type_from_cast(node.name)
    elif isinstance(node, c_ast.ID):
        return node.name
    
    return None

def _has_self_argument(name: str, args: list | None) -> bool:
    """Check if argument's list already contains the self name.

    Args:
        name (str): Self name.
        args (list | None): Argument' list.

    Returns:
        bool: Self already in arguments?
    """
    if not args:
        return False
    
    for arg in args:
        if isinstance(arg, c_ast.ID):
            if arg.name == name:
                return True
        elif isinstance(arg, c_ast.UnaryOp):
            if arg.expr.name == name:
                return True
    
    return False

def _find_self_for_call(node) -> c_ast.UnaryOp | c_ast.StructRef | c_ast.ID:
    """Find a root of function call

    Args:
        node (_type_): Function call node

    Returns:
        c_ast.UnaryOp | c_ast.StructRef | c_ast.ID: Root of the function call
    """
    if not isinstance(node.name, c_ast.StructRef):
        return None

    chain = []
    ref = node.name
    while isinstance(ref, c_ast.StructRef) or isinstance(ref, c_ast.ArrayRef):
        chain.append(ref)
        ref = ref.name
    
    if isinstance(ref, (c_ast.ID, c_ast.Cast)):
        base = ref
    else:
        return None

    for struct_ref in reversed(chain[1:]):
        if isinstance(struct_ref, c_ast.StructRef):
            base = c_ast.StructRef(name=base, type=struct_ref.type, field=struct_ref.field)
        elif isinstance(struct_ref, c_ast.ArrayRef):
            base = c_ast.ArrayRef(name=base, subscript=struct_ref.subscript)

    last_op = chain[0].type if chain else '.'
    if last_op == '.':
        base = c_ast.UnaryOp(op='&', expr=base)

    return base

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
                struct_node, field_chain = self._resolve_structref(node.name)
                base_struct_type: str | None = None
                
                if isinstance(struct_node, c_ast.ID) or isinstance(struct_node, c_ast.ArrayRef):
                    base_struct_type = self._resolve_base_struct_type(struct_node=struct_node, field_chain=field_chain)
                elif isinstance(struct_node, c_ast.Cast): # Access via casting
                    base_struct_type = _get_base_type_from_cast(struct_node)
                
                func_name = field_chain[-1]
                args = node.args.exprs if node.args else []
                if (
                    base_struct_type and
                    func_name in self.symtab.get(base_struct_type, []) and
                    not _has_self_argument(base_struct_type, args)
                ):
                    self_node = _find_self_for_call(node)
                    if self_node:
                        if node.args:
                            node.args.exprs.insert(0, self_node)
                        else:
                            node.args = c_ast.ParamList(params=[self_node])

        elif isinstance(node, c_ast.StructRef):
            self._proceed_structcall(node.name)

    def _resolve_base_struct_type(self, struct_node, field_chain: list[str]) -> str:
        def _get_name(node) -> str:
            while not isinstance(node, str):
                node = node.name
        
            return node
        
        base_struct_type = self.lookup(_get_name(struct_node))
        while not isinstance(base_struct_type, c_ast.IdentifierType):
            base_struct_type = base_struct_type.type
            
        base_struct_type = base_struct_type.names[0]
        while True:
            changed = False
            for dep_type, dep_field in self.struct_graph.get(base_struct_type, []):
                if field_chain and dep_field == field_chain[0]:
                    base_struct_type = dep_type
                    field_chain = field_chain[1:]
                    changed = True
                    break
                
            if not changed or not field_chain:
                break

        return base_struct_type

    def _resolve_structref(self, structref):
        fields = []
        node = structref
        while isinstance(node, c_ast.StructRef):
            fields.insert(0, node.field.name)
            node = node.name
            
        return node, fields
        
    def visit_FuncCall(self, node):
        try:
            self._proceed_structcall(node)
        except Exception as ex:
            print("Error processing FuncCall:", ex)

        self.generic_visit(node)
