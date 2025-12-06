# SelfCall preprocessing
This repository contains a preprocessor for C language. The main idea is the `selfcall` attribute implementation.

## Repository
- `misc`:
    - `preprocessor.py` - Python attribute preprocessor. See `misc/README.md` for details.
    - `selfcaller.py` - Python the `C language AST-walker `. See `misc/README.md` for details.
- `tests` - C source files for a test purpose.
- `vscode` - Preprocessor's extention to supress warnings from a canonical C-extention.
- `main.py` - Entry point.

## SelfCall idea
The idea is simple. I love C language, and I want to improve it with the next attribute:
```c
__attribute__((selfcall))
```

This attribute allows us to build and use structures in a completly new way:
```c
// foo.h
#define str_self struct string*
typedef struct string {
    int   size;
    char* body;
    int   __attribute__((selfcall)) (*get_size)(str_self);
    char* __attribute__((selfcall)) (*get_body)(str_self);
} string_t;

// foo.c
#include "foo.h"
static int string_get_size(str_self self) {
    return self->size;
}

static int string_get_body(str_self self) {
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

As you mentioned above, the string structure has addtional attributes before an every function defenition. This attribute used for a self argument passing to function calls, that are called from structures. In nutshell, we can use an aforementioned structure in the next way:
```c
int main() {
    string_t s;
    printf("Size=%i\n", s.get_size());
    printf("Body=%s\n", s.get_body());
    return 0;
}
```

This tool allows us to ignore the first `self` parameter when we invoke function with the `selfcall` attribute from a structure. 

# How it works?


