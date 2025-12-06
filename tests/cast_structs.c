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
