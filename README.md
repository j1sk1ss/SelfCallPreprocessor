# SelfCall preprocessing
This repository contains a preprocessor for C language. The main idea is the `selfcall` attribute implementation.

## Repository
- `misc`:
    - `preprocessor.py` - Python attribute preprocessor. See `misc/README.md` for details.
    - `selfcaller.py` - Python the `C language AST-walker `. See `misc/README.md` for details.
- `tests` - C source files for a test purpose.
- `vscode` - Preprocessor's extention to supress warnings from a canonical C-extention.
- `main.py` - Entry point.

## Requier tools & Usage
### Resuired tools
There is a few things that are needed before we can proceed any further:
- [gcc](https://gcc.gnu.org/) - GCC or Clang compilers are essential for a basic C-preprocessing.
- [pycparcer](https://github.com/eliben/pycparser) - Basic library for AST operations.
- [loguru](https://github.com/Delgan/loguru) - Fancy-looking logg messages. 

### Usage

## SelfCall idea
The idea is simple. I love C language, and I want to improve it with the next annotation:
```
processor::selfcall
```

This annotation allows us to build and use structures in a completly new way:
```c
// foo.h
typedef struct string {
    int   size;
    char* body;
    int   (*get_size)( /* processor::selfcall */ );
    char* (*get_body)( /* processor::selfcall */ );
} string_t;

// foo.c
#include "foo.h"
static int string_get_size(struct string* self) {
    return self->size;
}

static int string_get_body(struct string* self) {
    return self->body;
}

int main() {
    string_t s = {
        .size = 13,
        .body = "Hello world!",
        .get_size = string_get_size,
        .get_body = string_get_body
    };

    return 0;
}
```

As you mentioned above, the string structure has addtional annotation in argument' list in every function defenition. This annotation is used for a self argument passing to function calls, that are called from structures. In nutshell, we can use an aforementioned structure in the next new way:
```c
int main() {
    string_t s;
    printf("Size=%i\n", s.get_size());
    printf("Body=%s\n", s.get_body());
    return 0;
}
```

This tool allows us to ignore the first `self` parameter when we invoke a function with the `selfcall` attribute from a structure. 

# How it works?
## Summary
Let's consider the next code snippet:
```c
typedef struct {
    int (*get_size)( /* processor::selfcall */ );
    int (*set_size)( /* processor::selfcall */ int );
} string_t;

void foo(string_t* a) {
    a->set_size(a->get_size());
}
```

This is a very simple example of the `selfcall` annotation. With the `processor::selfcall` usage, an user can "reserve" the first argument for the `self` pointer. Aforementioned code snippet, after such a transformation becames a less-readeble, but at least, a correct version of C-code.
```c
typedef struct __anon_struct_string_t
{
  int (*get_size)(struct __anon_struct_string_t *);
  int (*set_size)(struct __anon_struct_string_t *, int);
} string_t;
void foo(string_t *a)
{
  a->set_size(a, a->get_size(a));
}
```

## C-preprocessor part
## Layout part
## AST part
