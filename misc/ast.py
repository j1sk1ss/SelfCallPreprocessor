from pycparser import c_ast

class ASTool:
    @staticmethod
    def resolve_structref(node) -> tuple:
        """Extract essential information from StructRef node

        Args:
            node (_type_): StructRef node

        Returns:
            tuple: Return base structure node and call sequence
        """
        fields: list = []
        casts: list = []
        
        while True:
            if isinstance(node, c_ast.StructRef):
                casts.append(None)
                fields.insert(0, node.field.name)
                node = node.name # TODO
            # elif isinstance(node, c_ast.Cast) and isinstance(node.expr, c_ast.StructRef):
            #     # casts.append(node.to_type.type.type.type.names[0])
            #     casts.append(None)
            #     fields.insert(0, node.expr.name.name)
            #     node = node.expr
            else:
                break
            
        # print(node)
        return node, list(zip(fields, casts))
    
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
    def find_self_for_call(node) -> c_ast.UnaryOp | c_ast.StructRef | c_ast.ID:
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
