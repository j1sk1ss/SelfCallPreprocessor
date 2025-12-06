typedef struct {
    void (*init)(/* processor::selfcall */);
} Inner;

typedef struct {
    Inner inner;
    void (*process)(/* processor::selfcall */);
} Outer;

void test_nested() {
    Outer o;
    o.inner.init();
    o.process();
    
    Outer* op = &o;
    op->inner.init();
}