#ifndef HEADER_H_
#define HEADER_H_

typedef struct string {
    int   __attribute__((selfcall)) (*get_size)(struct string*);
    char* __attribute__((selfcall)) (*get_body)(struct string*);
    int   __attribute__((selfcall)) (*set_body)(struct string*, char*);
} string_t;

#endif