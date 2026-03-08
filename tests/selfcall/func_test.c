typedef struct {
    int (*get_size)( /* processor::selfcall */ );
    int (*set_size)( /* processor::selfcall */ int );
} string_t;

void foo(string_t* a) {
    a->set_size(a->get_size());
}

/*EXPECTED_CODE
typedef struct __anon_struct_string_t
{
  int (*get_size)(struct __anon_struct_string_t *);
  int (*set_size)(struct __anon_struct_string_t *, int);
} string_t;
void foo(string_t *a)
{
  a->set_size(a, a->get_size(a));
}

EXPECTED_CODE*/
