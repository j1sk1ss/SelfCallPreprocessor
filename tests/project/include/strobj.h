#ifndef STRING_H_
#define STRING_H_

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct string {
    unsigned int size;
    const char*  body;
    unsigned int (*length)( /* processor::selfcall */ );
    int          (*print)( /* processor::selfcall */ );
} string_t;

string_t* create_string(const char* s);
int destroy_string(string_t* s);

#endif