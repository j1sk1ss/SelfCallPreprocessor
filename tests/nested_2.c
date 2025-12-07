typedef struct {
    int (*foo)( /* processor::selfcall */ );
} a_t;

typedef struct {
    a_t a;
} b_t;

typedef struct {
    void* b;
} c_t;

int bar() {
    c_t c2;
    ((b_t*)(c2.b))->a.foo();
}

/*EXPECTED_CODE
typedef struct __anon_struct_a_t
{
  int (*foo)(struct __anon_struct_a_t *);
} a_t;
typedef struct 
{
  a_t a;
} b_t;
typedef struct 
{
  void *b;
} c_t;
int bar()
{
  c_t c2;
  ((b_t *) c2.b)->a.foo(((b_t *) c2.b)->a);
}
EXPECTED_CODE*/

