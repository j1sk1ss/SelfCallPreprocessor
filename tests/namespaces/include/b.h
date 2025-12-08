#ifndef B_H_
#define B_H_

typedef struct {
    void (*foo)( /* processor::selfcall */ );
    void (*bar)( /* processor::selfcall */ );
    void (*baz)( /* processor::selfcall */ );
} b_namespace_t;

#endif