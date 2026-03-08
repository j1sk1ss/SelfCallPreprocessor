typedef struct {
    int (*foo)( /* processor::selfcall */ );
} a_t;

typedef struct {
    void* b;
} b_t;

typedef struct {
    void* c;
} c_t;

int bar() {
    c_t c2; (
        (a_t*)(
            (b_t*)c2.c
        )->b
    )->foo();
}

/*EXPECTED_CODE
typedef struct __anon_struct_a_t
{
  int (*foo)(struct __anon_struct_a_t *);
} a_t;
typedef struct 
{
  void *b;
} b_t;
typedef struct 
{
  void *c;
} c_t;
int bar()
{
  c_t c2;
  ((a_t *) ((b_t *) c2.c)->b)->foo((a_t *) ((b_t *) c2.c)->b);
}
EXPECTED_CODE*/
