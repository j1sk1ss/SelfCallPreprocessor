typedef struct {
    int (*foo)( /* processor::selfcall */ );
} a_t;

typedef struct {
    a_t a;
} b_t;

typedef struct {
    b_t b;
} c_t;

int bar() {
    c_t c2;
    c2.b.a.foo();
}