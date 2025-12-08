typedef struct {
    int (*foo1)( /* processor::selfcall */ );
} a_1_t;

typedef struct {
    a_1_t a;
} b_1_t;

typedef struct {
    void* b;
} c_1_t;

typedef struct {
    int (*foo1)( /* processor::selfcall */ );
    c_1_t c;
} d_1_t;

typedef struct {
    void* d;
} k_1_t;

typedef struct {
    int (*foo2)( /* processor::selfcall */ );
} a_2_t;

typedef struct {
    a_2_t a;
} b_2_t;

typedef struct {
    void* b;
} c_2_t;

typedef struct {
    int (*foo2)( /* processor::selfcall */ );
    c_2_t c;
} d_2_t;

typedef struct {
    void* d;
} k_2_t;

void bar1() {
    k_1_t k;
    ((b_1_t*)(((d_1_t*)(k.d))->c.b))->a.foo1();
    ((d_1_t*)(k.d))->foo1();
    ((b_1_t*)(((d_1_t*)(k.d))->c.b))->a.foo1();
    ((d_1_t*)(k.d))->foo1();
    ((b_1_t*)(((d_1_t*)(k.d))->c.b))->a.foo1();
    ((d_1_t*)(k.d))->foo1();
    ((b_1_t*)(((d_1_t*)(k.d))->c.b))->a.foo1();
    ((d_1_t*)(k.d))->foo1();
    ((b_1_t*)(((d_1_t*)(k.d))->c.b))->a.foo1();
    ((d_1_t*)(k.d))->foo1();
    ((b_1_t*)(((d_1_t*)(k.d))->c.b))->a.foo1();
    ((d_1_t*)(k.d))->foo1();
    ((b_1_t*)(((d_1_t*)(k.d))->c.b))->a.foo1();
    ((d_1_t*)(k.d))->foo1();
    ((b_1_t*)(((d_1_t*)(k.d))->c.b))->a.foo1();
    ((d_1_t*)(k.d))->foo1();
    ((b_1_t*)(((d_1_t*)(k.d))->c.b))->a.foo1();
    ((d_1_t*)(k.d))->foo1();
    ((b_1_t*)(((d_1_t*)(k.d))->c.b))->a.foo1();
    ((d_1_t*)(k.d))->foo1();
    ((b_1_t*)(((d_1_t*)(k.d))->c.b))->a.foo1();
    ((d_1_t*)(k.d))->foo1();
    ((b_1_t*)(((d_1_t*)(k.d))->c.b))->a.foo1();
    ((d_1_t*)(k.d))->foo1();
    ((b_1_t*)(((d_1_t*)(k.d))->c.b))->a.foo1();
    ((d_1_t*)(k.d))->foo1();
    ((b_1_t*)(((d_1_t*)(k.d))->c.b))->a.foo1();
    ((d_1_t*)(k.d))->foo1();
    ((b_1_t*)(((d_1_t*)(k.d))->c.b))->a.foo1();
    ((d_1_t*)(k.d))->foo1();
    ((b_1_t*)(((d_1_t*)(k.d))->c.b))->a.foo1();
    ((d_1_t*)(k.d))->foo1();
    ((b_1_t*)(((d_1_t*)(k.d))->c.b))->a.foo1();
    ((d_1_t*)(k.d))->foo1();
    ((b_1_t*)(((d_1_t*)(k.d))->c.b))->a.foo1();
    ((d_1_t*)(k.d))->foo1();
    ((b_1_t*)(((d_1_t*)(k.d))->c.b))->a.foo1();
    ((d_1_t*)(k.d))->foo1();
    ((b_1_t*)(((d_1_t*)(k.d))->c.b))->a.foo1();
    ((d_1_t*)(k.d))->foo1();
    ((b_1_t*)(((d_1_t*)(k.d))->c.b))->a.foo1();
    ((d_1_t*)(k.d))->foo1();
    ((b_1_t*)(((d_1_t*)(k.d))->c.b))->a.foo1();
    ((d_1_t*)(k.d))->foo1();
    ((b_1_t*)(((d_1_t*)(k.d))->c.b))->a.foo1();
    ((d_1_t*)(k.d))->foo1();
    ((b_1_t*)(((d_1_t*)(k.d))->c.b))->a.foo1();
    ((d_1_t*)(k.d))->foo1();
    ((b_1_t*)(((d_1_t*)(k.d))->c.b))->a.foo1();
    ((d_1_t*)(k.d))->foo1();
    ((b_1_t*)(((d_1_t*)(k.d))->c.b))->a.foo1();
    ((d_1_t*)(k.d))->foo1();
    ((b_1_t*)(((d_1_t*)(k.d))->c.b))->a.foo1();
    ((d_1_t*)(k.d))->foo1();
    ((b_1_t*)(((d_1_t*)(k.d))->c.b))->a.foo1();
    ((d_1_t*)(k.d))->foo1();
    ((b_1_t*)(((d_1_t*)(k.d))->c.b))->a.foo1();
    ((d_1_t*)(k.d))->foo1();
    ((b_1_t*)(((d_1_t*)(k.d))->c.b))->a.foo1();
    ((d_1_t*)(k.d))->foo1();
    ((b_1_t*)(((d_1_t*)(k.d))->c.b))->a.foo1();
    ((d_1_t*)(k.d))->foo1();
    ((b_1_t*)(((d_1_t*)(k.d))->c.b))->a.foo1();
    ((d_1_t*)(k.d))->foo1();
    ((b_1_t*)(((d_1_t*)(k.d))->c.b))->a.foo1();
    ((d_1_t*)(k.d))->foo1();
    ((b_1_t*)(((d_1_t*)(k.d))->c.b))->a.foo1();
    ((d_1_t*)(k.d))->foo1();
    ((b_1_t*)(((d_1_t*)(k.d))->c.b))->a.foo1();
    ((d_1_t*)(k.d))->foo1();
    ((b_1_t*)(((d_1_t*)(k.d))->c.b))->a.foo1();
    ((d_1_t*)(k.d))->foo1();
    ((b_1_t*)(((d_1_t*)(k.d))->c.b))->a.foo1();
    ((d_1_t*)(k.d))->foo1();
    ((b_1_t*)(((d_1_t*)(k.d))->c.b))->a.foo1();
    ((d_1_t*)(k.d))->foo1();
    ((b_1_t*)(((d_1_t*)(k.d))->c.b))->a.foo1();
    ((d_1_t*)(k.d))->foo1();
    ((b_1_t*)(((d_1_t*)(k.d))->c.b))->a.foo1();
    ((d_1_t*)(k.d))->foo1();
}

void bar2() {
    k_2_t k;
    ((b_2_t*)(((d_2_t*)(k.d))->c.b))->a.foo2();
    ((d_2_t*)(k.d))->foo2();
    ((b_2_t*)(((d_2_t*)(k.d))->c.b))->a.foo2();
    ((d_2_t*)(k.d))->foo2();
    ((b_2_t*)(((d_2_t*)(k.d))->c.b))->a.foo2();
    ((d_2_t*)(k.d))->foo2();
    ((b_2_t*)(((d_2_t*)(k.d))->c.b))->a.foo2();
    ((d_2_t*)(k.d))->foo2();
    ((b_2_t*)(((d_2_t*)(k.d))->c.b))->a.foo2();
    ((d_2_t*)(k.d))->foo2();
    ((b_2_t*)(((d_2_t*)(k.d))->c.b))->a.foo2();
    ((d_2_t*)(k.d))->foo2();
    ((b_2_t*)(((d_2_t*)(k.d))->c.b))->a.foo2();
    ((d_2_t*)(k.d))->foo2();
    ((b_2_t*)(((d_2_t*)(k.d))->c.b))->a.foo2();
    ((d_2_t*)(k.d))->foo2();
    ((b_2_t*)(((d_2_t*)(k.d))->c.b))->a.foo2();
    ((d_2_t*)(k.d))->foo2();
    ((b_2_t*)(((d_2_t*)(k.d))->c.b))->a.foo2();
    ((d_2_t*)(k.d))->foo2();
    ((b_2_t*)(((d_2_t*)(k.d))->c.b))->a.foo2();
    ((d_2_t*)(k.d))->foo2();
    ((b_2_t*)(((d_2_t*)(k.d))->c.b))->a.foo2();
    ((d_2_t*)(k.d))->foo2();
    ((b_2_t*)(((d_2_t*)(k.d))->c.b))->a.foo2();
    ((d_2_t*)(k.d))->foo2();
    ((b_2_t*)(((d_2_t*)(k.d))->c.b))->a.foo2();
    ((d_2_t*)(k.d))->foo2();
    ((b_2_t*)(((d_2_t*)(k.d))->c.b))->a.foo2();
    ((d_2_t*)(k.d))->foo2();
    ((b_2_t*)(((d_2_t*)(k.d))->c.b))->a.foo2();
    ((d_2_t*)(k.d))->foo2();
    ((b_2_t*)(((d_2_t*)(k.d))->c.b))->a.foo2();
    ((d_2_t*)(k.d))->foo2();
    ((b_2_t*)(((d_2_t*)(k.d))->c.b))->a.foo2();
    ((d_2_t*)(k.d))->foo2();
    ((b_2_t*)(((d_2_t*)(k.d))->c.b))->a.foo2();
    ((d_2_t*)(k.d))->foo2();
    ((b_2_t*)(((d_2_t*)(k.d))->c.b))->a.foo2();
    ((d_2_t*)(k.d))->foo2();
    ((b_2_t*)(((d_2_t*)(k.d))->c.b))->a.foo2();
    ((d_2_t*)(k.d))->foo2();
    ((b_2_t*)(((d_2_t*)(k.d))->c.b))->a.foo2();
    ((d_2_t*)(k.d))->foo2();
    ((b_2_t*)(((d_2_t*)(k.d))->c.b))->a.foo2();
    ((d_2_t*)(k.d))->foo2();
    ((b_2_t*)(((d_2_t*)(k.d))->c.b))->a.foo2();
    ((d_2_t*)(k.d))->foo2();
    ((b_2_t*)(((d_2_t*)(k.d))->c.b))->a.foo2();
    ((d_2_t*)(k.d))->foo2();
    ((b_2_t*)(((d_2_t*)(k.d))->c.b))->a.foo2();
    ((d_2_t*)(k.d))->foo2();
    ((b_2_t*)(((d_2_t*)(k.d))->c.b))->a.foo2();
    ((d_2_t*)(k.d))->foo2();
    ((b_2_t*)(((d_2_t*)(k.d))->c.b))->a.foo2();
    ((d_2_t*)(k.d))->foo2();
    ((b_2_t*)(((d_2_t*)(k.d))->c.b))->a.foo2();
    ((d_2_t*)(k.d))->foo2();
    ((b_2_t*)(((d_2_t*)(k.d))->c.b))->a.foo2();
    ((d_2_t*)(k.d))->foo2();
    ((b_2_t*)(((d_2_t*)(k.d))->c.b))->a.foo2();
    ((d_2_t*)(k.d))->foo2();
    ((b_2_t*)(((d_2_t*)(k.d))->c.b))->a.foo2();
    ((d_2_t*)(k.d))->foo2();
    ((b_2_t*)(((d_2_t*)(k.d))->c.b))->a.foo2();
    ((d_2_t*)(k.d))->foo2();
    ((b_2_t*)(((d_2_t*)(k.d))->c.b))->a.foo2();
    ((d_2_t*)(k.d))->foo2();
    ((b_2_t*)(((d_2_t*)(k.d))->c.b))->a.foo2();
    ((d_2_t*)(k.d))->foo2();
    ((b_2_t*)(((d_2_t*)(k.d))->c.b))->a.foo2();
    ((d_2_t*)(k.d))->foo2();
    ((b_2_t*)(((d_2_t*)(k.d))->c.b))->a.foo2();
    ((d_2_t*)(k.d))->foo2();
    ((b_2_t*)(((d_2_t*)(k.d))->c.b))->a.foo2();
    ((d_2_t*)(k.d))->foo2();
    ((b_2_t*)(((d_2_t*)(k.d))->c.b))->a.foo2();
    ((d_2_t*)(k.d))->foo2();
    ((b_2_t*)(((d_2_t*)(k.d))->c.b))->a.foo2();
    ((d_2_t*)(k.d))->foo2();
}

/*EXPECTED_CODE
typedef struct __anon_struct_a_1_t
{
  int (*foo1)(struct __anon_struct_a_1_t *);
} a_1_t;
typedef struct 
{
  a_1_t a;
} b_1_t;
typedef struct 
{
  void *b;
} c_1_t;
typedef struct __anon_struct_d_1_t
{
  int (*foo1)(struct __anon_struct_d_1_t *);
  c_1_t c;
} d_1_t;
typedef struct 
{
  void *d;
} k_1_t;
typedef struct __anon_struct_a_2_t
{
  int (*foo2)(struct __anon_struct_a_2_t *);
} a_2_t;
typedef struct 
{
  a_2_t a;
} b_2_t;
typedef struct 
{
  void *b;
} c_2_t;
typedef struct __anon_struct_d_2_t
{
  int (*foo2)(struct __anon_struct_d_2_t *);
  c_2_t c;
} d_2_t;
typedef struct 
{
  void *d;
} k_2_t;
void bar1()
{
  k_1_t k;
  ((b_1_t *) ((d_1_t *) k.d)->c.b)->a.foo1(&((b_1_t *) ((d_1_t *) k.d)->c.b)->a);
  ((d_1_t *) k.d)->foo1((d_1_t *) k.d);
  ((b_1_t *) ((d_1_t *) k.d)->c.b)->a.foo1(&((b_1_t *) ((d_1_t *) k.d)->c.b)->a);
  ((d_1_t *) k.d)->foo1((d_1_t *) k.d);
  ((b_1_t *) ((d_1_t *) k.d)->c.b)->a.foo1(&((b_1_t *) ((d_1_t *) k.d)->c.b)->a);
  ((d_1_t *) k.d)->foo1((d_1_t *) k.d);
  ((b_1_t *) ((d_1_t *) k.d)->c.b)->a.foo1(&((b_1_t *) ((d_1_t *) k.d)->c.b)->a);
  ((d_1_t *) k.d)->foo1((d_1_t *) k.d);
  ((b_1_t *) ((d_1_t *) k.d)->c.b)->a.foo1(&((b_1_t *) ((d_1_t *) k.d)->c.b)->a);
  ((d_1_t *) k.d)->foo1((d_1_t *) k.d);
  ((b_1_t *) ((d_1_t *) k.d)->c.b)->a.foo1(&((b_1_t *) ((d_1_t *) k.d)->c.b)->a);
  ((d_1_t *) k.d)->foo1((d_1_t *) k.d);
  ((b_1_t *) ((d_1_t *) k.d)->c.b)->a.foo1(&((b_1_t *) ((d_1_t *) k.d)->c.b)->a);
  ((d_1_t *) k.d)->foo1((d_1_t *) k.d);
  ((b_1_t *) ((d_1_t *) k.d)->c.b)->a.foo1(&((b_1_t *) ((d_1_t *) k.d)->c.b)->a);
  ((d_1_t *) k.d)->foo1((d_1_t *) k.d);
  ((b_1_t *) ((d_1_t *) k.d)->c.b)->a.foo1(&((b_1_t *) ((d_1_t *) k.d)->c.b)->a);
  ((d_1_t *) k.d)->foo1((d_1_t *) k.d);
  ((b_1_t *) ((d_1_t *) k.d)->c.b)->a.foo1(&((b_1_t *) ((d_1_t *) k.d)->c.b)->a);
  ((d_1_t *) k.d)->foo1((d_1_t *) k.d);
  ((b_1_t *) ((d_1_t *) k.d)->c.b)->a.foo1(&((b_1_t *) ((d_1_t *) k.d)->c.b)->a);
  ((d_1_t *) k.d)->foo1((d_1_t *) k.d);
  ((b_1_t *) ((d_1_t *) k.d)->c.b)->a.foo1(&((b_1_t *) ((d_1_t *) k.d)->c.b)->a);
  ((d_1_t *) k.d)->foo1((d_1_t *) k.d);
  ((b_1_t *) ((d_1_t *) k.d)->c.b)->a.foo1(&((b_1_t *) ((d_1_t *) k.d)->c.b)->a);
  ((d_1_t *) k.d)->foo1((d_1_t *) k.d);
  ((b_1_t *) ((d_1_t *) k.d)->c.b)->a.foo1(&((b_1_t *) ((d_1_t *) k.d)->c.b)->a);
  ((d_1_t *) k.d)->foo1((d_1_t *) k.d);
  ((b_1_t *) ((d_1_t *) k.d)->c.b)->a.foo1(&((b_1_t *) ((d_1_t *) k.d)->c.b)->a);
  ((d_1_t *) k.d)->foo1((d_1_t *) k.d);
  ((b_1_t *) ((d_1_t *) k.d)->c.b)->a.foo1(&((b_1_t *) ((d_1_t *) k.d)->c.b)->a);
  ((d_1_t *) k.d)->foo1((d_1_t *) k.d);
  ((b_1_t *) ((d_1_t *) k.d)->c.b)->a.foo1(&((b_1_t *) ((d_1_t *) k.d)->c.b)->a);
  ((d_1_t *) k.d)->foo1((d_1_t *) k.d);
  ((b_1_t *) ((d_1_t *) k.d)->c.b)->a.foo1(&((b_1_t *) ((d_1_t *) k.d)->c.b)->a);
  ((d_1_t *) k.d)->foo1((d_1_t *) k.d);
  ((b_1_t *) ((d_1_t *) k.d)->c.b)->a.foo1(&((b_1_t *) ((d_1_t *) k.d)->c.b)->a);
  ((d_1_t *) k.d)->foo1((d_1_t *) k.d);
  ((b_1_t *) ((d_1_t *) k.d)->c.b)->a.foo1(&((b_1_t *) ((d_1_t *) k.d)->c.b)->a);
  ((d_1_t *) k.d)->foo1((d_1_t *) k.d);
  ((b_1_t *) ((d_1_t *) k.d)->c.b)->a.foo1(&((b_1_t *) ((d_1_t *) k.d)->c.b)->a);
  ((d_1_t *) k.d)->foo1((d_1_t *) k.d);
  ((b_1_t *) ((d_1_t *) k.d)->c.b)->a.foo1(&((b_1_t *) ((d_1_t *) k.d)->c.b)->a);
  ((d_1_t *) k.d)->foo1((d_1_t *) k.d);
  ((b_1_t *) ((d_1_t *) k.d)->c.b)->a.foo1(&((b_1_t *) ((d_1_t *) k.d)->c.b)->a);
  ((d_1_t *) k.d)->foo1((d_1_t *) k.d);
  ((b_1_t *) ((d_1_t *) k.d)->c.b)->a.foo1(&((b_1_t *) ((d_1_t *) k.d)->c.b)->a);
  ((d_1_t *) k.d)->foo1((d_1_t *) k.d);
  ((b_1_t *) ((d_1_t *) k.d)->c.b)->a.foo1(&((b_1_t *) ((d_1_t *) k.d)->c.b)->a);
  ((d_1_t *) k.d)->foo1((d_1_t *) k.d);
  ((b_1_t *) ((d_1_t *) k.d)->c.b)->a.foo1(&((b_1_t *) ((d_1_t *) k.d)->c.b)->a);
  ((d_1_t *) k.d)->foo1((d_1_t *) k.d);
  ((b_1_t *) ((d_1_t *) k.d)->c.b)->a.foo1(&((b_1_t *) ((d_1_t *) k.d)->c.b)->a);
  ((d_1_t *) k.d)->foo1((d_1_t *) k.d);
  ((b_1_t *) ((d_1_t *) k.d)->c.b)->a.foo1(&((b_1_t *) ((d_1_t *) k.d)->c.b)->a);
  ((d_1_t *) k.d)->foo1((d_1_t *) k.d);
  ((b_1_t *) ((d_1_t *) k.d)->c.b)->a.foo1(&((b_1_t *) ((d_1_t *) k.d)->c.b)->a);
  ((d_1_t *) k.d)->foo1((d_1_t *) k.d);
  ((b_1_t *) ((d_1_t *) k.d)->c.b)->a.foo1(&((b_1_t *) ((d_1_t *) k.d)->c.b)->a);
  ((d_1_t *) k.d)->foo1((d_1_t *) k.d);
  ((b_1_t *) ((d_1_t *) k.d)->c.b)->a.foo1(&((b_1_t *) ((d_1_t *) k.d)->c.b)->a);
  ((d_1_t *) k.d)->foo1((d_1_t *) k.d);
  ((b_1_t *) ((d_1_t *) k.d)->c.b)->a.foo1(&((b_1_t *) ((d_1_t *) k.d)->c.b)->a);
  ((d_1_t *) k.d)->foo1((d_1_t *) k.d);
  ((b_1_t *) ((d_1_t *) k.d)->c.b)->a.foo1(&((b_1_t *) ((d_1_t *) k.d)->c.b)->a);
  ((d_1_t *) k.d)->foo1((d_1_t *) k.d);
  ((b_1_t *) ((d_1_t *) k.d)->c.b)->a.foo1(&((b_1_t *) ((d_1_t *) k.d)->c.b)->a);
  ((d_1_t *) k.d)->foo1((d_1_t *) k.d);
  ((b_1_t *) ((d_1_t *) k.d)->c.b)->a.foo1(&((b_1_t *) ((d_1_t *) k.d)->c.b)->a);
  ((d_1_t *) k.d)->foo1((d_1_t *) k.d);
  ((b_1_t *) ((d_1_t *) k.d)->c.b)->a.foo1(&((b_1_t *) ((d_1_t *) k.d)->c.b)->a);
  ((d_1_t *) k.d)->foo1((d_1_t *) k.d);
  ((b_1_t *) ((d_1_t *) k.d)->c.b)->a.foo1(&((b_1_t *) ((d_1_t *) k.d)->c.b)->a);
  ((d_1_t *) k.d)->foo1((d_1_t *) k.d);
  ((b_1_t *) ((d_1_t *) k.d)->c.b)->a.foo1(&((b_1_t *) ((d_1_t *) k.d)->c.b)->a);
  ((d_1_t *) k.d)->foo1((d_1_t *) k.d);
  ((b_1_t *) ((d_1_t *) k.d)->c.b)->a.foo1(&((b_1_t *) ((d_1_t *) k.d)->c.b)->a);
  ((d_1_t *) k.d)->foo1((d_1_t *) k.d);
  ((b_1_t *) ((d_1_t *) k.d)->c.b)->a.foo1(&((b_1_t *) ((d_1_t *) k.d)->c.b)->a);
  ((d_1_t *) k.d)->foo1((d_1_t *) k.d);
}

void bar2()
{
  k_2_t k;
  ((b_2_t *) ((d_2_t *) k.d)->c.b)->a.foo2(&((b_2_t *) ((d_2_t *) k.d)->c.b)->a);
  ((d_2_t *) k.d)->foo2((d_2_t *) k.d);
  ((b_2_t *) ((d_2_t *) k.d)->c.b)->a.foo2(&((b_2_t *) ((d_2_t *) k.d)->c.b)->a);
  ((d_2_t *) k.d)->foo2((d_2_t *) k.d);
  ((b_2_t *) ((d_2_t *) k.d)->c.b)->a.foo2(&((b_2_t *) ((d_2_t *) k.d)->c.b)->a);
  ((d_2_t *) k.d)->foo2((d_2_t *) k.d);
  ((b_2_t *) ((d_2_t *) k.d)->c.b)->a.foo2(&((b_2_t *) ((d_2_t *) k.d)->c.b)->a);
  ((d_2_t *) k.d)->foo2((d_2_t *) k.d);
  ((b_2_t *) ((d_2_t *) k.d)->c.b)->a.foo2(&((b_2_t *) ((d_2_t *) k.d)->c.b)->a);
  ((d_2_t *) k.d)->foo2((d_2_t *) k.d);
  ((b_2_t *) ((d_2_t *) k.d)->c.b)->a.foo2(&((b_2_t *) ((d_2_t *) k.d)->c.b)->a);
  ((d_2_t *) k.d)->foo2((d_2_t *) k.d);
  ((b_2_t *) ((d_2_t *) k.d)->c.b)->a.foo2(&((b_2_t *) ((d_2_t *) k.d)->c.b)->a);
  ((d_2_t *) k.d)->foo2((d_2_t *) k.d);
  ((b_2_t *) ((d_2_t *) k.d)->c.b)->a.foo2(&((b_2_t *) ((d_2_t *) k.d)->c.b)->a);
  ((d_2_t *) k.d)->foo2((d_2_t *) k.d);
  ((b_2_t *) ((d_2_t *) k.d)->c.b)->a.foo2(&((b_2_t *) ((d_2_t *) k.d)->c.b)->a);
  ((d_2_t *) k.d)->foo2((d_2_t *) k.d);
  ((b_2_t *) ((d_2_t *) k.d)->c.b)->a.foo2(&((b_2_t *) ((d_2_t *) k.d)->c.b)->a);
  ((d_2_t *) k.d)->foo2((d_2_t *) k.d);
  ((b_2_t *) ((d_2_t *) k.d)->c.b)->a.foo2(&((b_2_t *) ((d_2_t *) k.d)->c.b)->a);
  ((d_2_t *) k.d)->foo2((d_2_t *) k.d);
  ((b_2_t *) ((d_2_t *) k.d)->c.b)->a.foo2(&((b_2_t *) ((d_2_t *) k.d)->c.b)->a);
  ((d_2_t *) k.d)->foo2((d_2_t *) k.d);
  ((b_2_t *) ((d_2_t *) k.d)->c.b)->a.foo2(&((b_2_t *) ((d_2_t *) k.d)->c.b)->a);
  ((d_2_t *) k.d)->foo2((d_2_t *) k.d);
  ((b_2_t *) ((d_2_t *) k.d)->c.b)->a.foo2(&((b_2_t *) ((d_2_t *) k.d)->c.b)->a);
  ((d_2_t *) k.d)->foo2((d_2_t *) k.d);
  ((b_2_t *) ((d_2_t *) k.d)->c.b)->a.foo2(&((b_2_t *) ((d_2_t *) k.d)->c.b)->a);
  ((d_2_t *) k.d)->foo2((d_2_t *) k.d);
  ((b_2_t *) ((d_2_t *) k.d)->c.b)->a.foo2(&((b_2_t *) ((d_2_t *) k.d)->c.b)->a);
  ((d_2_t *) k.d)->foo2((d_2_t *) k.d);
  ((b_2_t *) ((d_2_t *) k.d)->c.b)->a.foo2(&((b_2_t *) ((d_2_t *) k.d)->c.b)->a);
  ((d_2_t *) k.d)->foo2((d_2_t *) k.d);
  ((b_2_t *) ((d_2_t *) k.d)->c.b)->a.foo2(&((b_2_t *) ((d_2_t *) k.d)->c.b)->a);
  ((d_2_t *) k.d)->foo2((d_2_t *) k.d);
  ((b_2_t *) ((d_2_t *) k.d)->c.b)->a.foo2(&((b_2_t *) ((d_2_t *) k.d)->c.b)->a);
  ((d_2_t *) k.d)->foo2((d_2_t *) k.d);
  ((b_2_t *) ((d_2_t *) k.d)->c.b)->a.foo2(&((b_2_t *) ((d_2_t *) k.d)->c.b)->a);
  ((d_2_t *) k.d)->foo2((d_2_t *) k.d);
  ((b_2_t *) ((d_2_t *) k.d)->c.b)->a.foo2(&((b_2_t *) ((d_2_t *) k.d)->c.b)->a);
  ((d_2_t *) k.d)->foo2((d_2_t *) k.d);
  ((b_2_t *) ((d_2_t *) k.d)->c.b)->a.foo2(&((b_2_t *) ((d_2_t *) k.d)->c.b)->a);
  ((d_2_t *) k.d)->foo2((d_2_t *) k.d);
  ((b_2_t *) ((d_2_t *) k.d)->c.b)->a.foo2(&((b_2_t *) ((d_2_t *) k.d)->c.b)->a);
  ((d_2_t *) k.d)->foo2((d_2_t *) k.d);
  ((b_2_t *) ((d_2_t *) k.d)->c.b)->a.foo2(&((b_2_t *) ((d_2_t *) k.d)->c.b)->a);
  ((d_2_t *) k.d)->foo2((d_2_t *) k.d);
  ((b_2_t *) ((d_2_t *) k.d)->c.b)->a.foo2(&((b_2_t *) ((d_2_t *) k.d)->c.b)->a);
  ((d_2_t *) k.d)->foo2((d_2_t *) k.d);
  ((b_2_t *) ((d_2_t *) k.d)->c.b)->a.foo2(&((b_2_t *) ((d_2_t *) k.d)->c.b)->a);
  ((d_2_t *) k.d)->foo2((d_2_t *) k.d);
  ((b_2_t *) ((d_2_t *) k.d)->c.b)->a.foo2(&((b_2_t *) ((d_2_t *) k.d)->c.b)->a);
  ((d_2_t *) k.d)->foo2((d_2_t *) k.d);
  ((b_2_t *) ((d_2_t *) k.d)->c.b)->a.foo2(&((b_2_t *) ((d_2_t *) k.d)->c.b)->a);
  ((d_2_t *) k.d)->foo2((d_2_t *) k.d);
  ((b_2_t *) ((d_2_t *) k.d)->c.b)->a.foo2(&((b_2_t *) ((d_2_t *) k.d)->c.b)->a);
  ((d_2_t *) k.d)->foo2((d_2_t *) k.d);
  ((b_2_t *) ((d_2_t *) k.d)->c.b)->a.foo2(&((b_2_t *) ((d_2_t *) k.d)->c.b)->a);
  ((d_2_t *) k.d)->foo2((d_2_t *) k.d);
  ((b_2_t *) ((d_2_t *) k.d)->c.b)->a.foo2(&((b_2_t *) ((d_2_t *) k.d)->c.b)->a);
  ((d_2_t *) k.d)->foo2((d_2_t *) k.d);
  ((b_2_t *) ((d_2_t *) k.d)->c.b)->a.foo2(&((b_2_t *) ((d_2_t *) k.d)->c.b)->a);
  ((d_2_t *) k.d)->foo2((d_2_t *) k.d);
  ((b_2_t *) ((d_2_t *) k.d)->c.b)->a.foo2(&((b_2_t *) ((d_2_t *) k.d)->c.b)->a);
  ((d_2_t *) k.d)->foo2((d_2_t *) k.d);
  ((b_2_t *) ((d_2_t *) k.d)->c.b)->a.foo2(&((b_2_t *) ((d_2_t *) k.d)->c.b)->a);
  ((d_2_t *) k.d)->foo2((d_2_t *) k.d);
  ((b_2_t *) ((d_2_t *) k.d)->c.b)->a.foo2(&((b_2_t *) ((d_2_t *) k.d)->c.b)->a);
  ((d_2_t *) k.d)->foo2((d_2_t *) k.d);
  ((b_2_t *) ((d_2_t *) k.d)->c.b)->a.foo2(&((b_2_t *) ((d_2_t *) k.d)->c.b)->a);
  ((d_2_t *) k.d)->foo2((d_2_t *) k.d);
  ((b_2_t *) ((d_2_t *) k.d)->c.b)->a.foo2(&((b_2_t *) ((d_2_t *) k.d)->c.b)->a);
  ((d_2_t *) k.d)->foo2((d_2_t *) k.d);
  ((b_2_t *) ((d_2_t *) k.d)->c.b)->a.foo2(&((b_2_t *) ((d_2_t *) k.d)->c.b)->a);
  ((d_2_t *) k.d)->foo2((d_2_t *) k.d);
  ((b_2_t *) ((d_2_t *) k.d)->c.b)->a.foo2(&((b_2_t *) ((d_2_t *) k.d)->c.b)->a);
  ((d_2_t *) k.d)->foo2((d_2_t *) k.d);
  ((b_2_t *) ((d_2_t *) k.d)->c.b)->a.foo2(&((b_2_t *) ((d_2_t *) k.d)->c.b)->a);
  ((d_2_t *) k.d)->foo2((d_2_t *) k.d);
}
EXPECTED_CODE*/
