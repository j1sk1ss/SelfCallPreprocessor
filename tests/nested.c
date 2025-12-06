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

/*EXPECTED_CODE
typedef struct __anon_struct_Inner
{
  void (*init)(struct __anon_struct_Inner *);
} Inner;
typedef struct 
{
  Inner inner;
  void (*process)(struct __anon_struct_Inner *);
} Outer;
void test_nested()
{
  Outer o;
  o.inner.init(&o.inner);
  o.process(&o);
  Outer *op = &o;
  op->inner.init(&op->inner);
}
EXPECTED_CODE*/
