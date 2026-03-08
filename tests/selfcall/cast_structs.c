typedef struct {
    int a;
    int (*get_a)( /* processor::selfcall */ );
} a_t;

typedef struct {
    void* field;
} b_t;

void foo(b_t* b) {
    ((a_t*)b->field)->get_a();
}

/*EXPECTED_CODE
typedef struct __anon_struct_a_t
{
  int a;
  int (*get_a)(struct __anon_struct_a_t *);
} a_t;
typedef struct 
{
  void *field;
} b_t;
void foo(b_t *b)
{
  ((a_t *) b->field)->get_a((a_t *) b->field);
}
EXPECTED_CODE*/
