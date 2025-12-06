# SelfCall preprocessing
This repository contains a preprocessor for C language. The main idea is the `selfcall` attribute implementation.

## Repository
- `tests` - C source files for a test purpose.
- `vscode` - Preprocessor's extention to supress warnings from a canonical C-extention.
- `selfcall.py` - Python sandbox script tool.

## SelfCall idea
The idea is simple. I love C language, and I want to improve it with next attributes:
```c
__attribute__((selfcall))
__attribute__((selfcall,pubcall))
```

This attributes allow us to build and use structures in a completly new way:
```c
// foo.h
#define str_self struct string*
typedef struct string {
    int   size;
    char* body;
    int   __attribute__((selfcall,pubcall)) (*get_size)(str_self);
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
```

As you menioned above, the string structure has addtional attributes before the every function defenition.

# How it works?
