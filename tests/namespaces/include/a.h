#ifndef A_H_
#define A_H_

typedef struct {
    void (*foo)( /* processor::selfcall */ );
    void (*bar)( /* processor::selfcall */ );
    void (*baz)( /* processor::selfcall */ );
} a_namespace_t;

#endif