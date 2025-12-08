from pycparser import c_ast

class CallElement:
    def __init__(
        self, 
        name: str | None, cast: str | None, call: str | None, isref: bool = False
    ) -> None:
        self.name: str | None = name
        self.cast: str | None = cast
        self.call: str | None = call
        self.isref: bool = isref

    def __repr__(self) -> str:
        return f"[name={self.name}{'->' if self.isref else '.'}call={self.call}, cast={self.cast}]"

class ASTool:
    @staticmethod
    def resolve_structref(node) -> tuple[c_ast.Node, list[CallElement]]:
        """Extract essential information from StructRef node

        Args:
            node (_type_): StructRef node

        Returns:
            tuple: Return base structure node and call sequence
        """
        call_chain: list[CallElement] = []
        while True:
            if isinstance(node, c_ast.StructRef):
                call_chain.insert(
                    0, CallElement(name=node.field.name, cast=None, call=None, isref=node.type != '.')
                )
                
                node = node.name
            elif isinstance(node, c_ast.Cast) and isinstance(node.expr, c_ast.StructRef):
                call_chain.insert(
                    0, CallElement(
                        name=node.expr.field.name, 
                        cast=node.to_type.type.type.type.names[0], 
                        call=None,
                        isref=node.expr.type != '.'
                    )
                )
                
                node = node.expr
            else:
                break
            
        for i in range(len(call_chain)):
            for j in range(i + 1, len(call_chain)):
                if not call_chain[j].cast:
                    call_chain[i].call = call_chain[j].name
                    call_chain[i].isref = call_chain[j].isref
                    break
        
        return node, call_chain
    
    @staticmethod
    def get_base_type_from_decl(node) -> str | None:
        """AST help function.
            Primarily works with declaration node.

        Args:
            node (c_ast.Decl): Declaration node.

        Returns:
            str | None: The base type of the node.
        """
        if isinstance(node, c_ast.Decl):
            return ASTool.get_base_type_from_decl(node.type)
        elif isinstance(node, c_ast.PtrDecl):
            return ASTool.get_base_type_from_decl(node.type)
        elif isinstance(node, c_ast.TypeDecl):
            return ASTool.get_base_type_from_decl(node.type)
        elif isinstance(node, c_ast.IdentifierType):
            return node.names[0]
        
        return None
        
    @staticmethod
    def get_base_type_from_cast(node: c_ast.Cast | c_ast.ID) -> str | None:
        """Return type from the cast AST node.

        Args:
            node (c_ast.Cast | c_ast.ID): Cast node.

        Returns:
            str | None: Variable's name that is casted.
        """
        if isinstance(node, c_ast.Cast):
            return node.to_type.type.type.type.names[0]
        elif isinstance(node, c_ast.StructRef):
            return ASTool.get_base_type_from_cast(node.name)
        elif isinstance(node, c_ast.ID):
            return node.name
        
        return None

    @staticmethod
    def has_self_argument(name: str, args: list | None) -> bool:
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

    @staticmethod
    def find_self_for_call(
        node: c_ast.Cast, call_chain: list[CallElement]
    ) -> c_ast.UnaryOp | c_ast.StructRef | c_ast.ID:
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

        if not call_chain[-1].isref:
            base = c_ast.UnaryOp(op='&', expr=base)

        return base
