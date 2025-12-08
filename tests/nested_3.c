typedef struct {
    int (*foo)( /* processor::selfcall */ );
} a_t;

typedef struct {
    a_t a;
} b_t;

typedef struct {
    void* b;
} c_t;

typedef struct {
    int (*foo)( /* processor::selfcall */ );
    c_t c;
} d_t;

typedef struct {
    void* d;
} k_t;

void bar(k_t* k) {
    ((b_t*)(((d_t*)(k->d))->c.b))->a.foo();
    ((d_t*)(k->d))->foo();
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
typedef struct __anon_struct_d_t
{
  int (*foo)(struct __anon_struct_d_t *);
  c_t c;
} d_t;
typedef struct 
{
  void *d;
} k_t;
void bar(k_t *k)
{
  ((b_t *) ((d_t *) k->d)->c.b)->a.foo(&((b_t *) ((d_t *) k->d)->c.b)->a);
  ((d_t *) k->d)->foo((d_t *) k->d);
}
EXPECTED_CODE*/
