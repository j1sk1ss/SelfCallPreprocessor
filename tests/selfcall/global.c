typedef struct {
    void (*init)(/* processor::selfcall */);
} Inner;

typedef struct {
    Inner inner;
    void (*process)(/* processor::selfcall */);
} Outer;

static Outer o;

void test_nested() {
    o.inner.init();
    o.process();
}

/*EXPECTED_CODE
typedef struct __anon_struct_Inner
{
  void (*init)(struct __anon_struct_Inner *);
} Inner;
typedef struct __anon_struct_Outer
{
  Inner inner;
  void (*process)(struct __anon_struct_Outer *);
} Outer;
static Outer o;
void test_nested()
{
  o.inner.init(&o.inner);
  o.process(&o);
}
EXPECTED_CODE*/
