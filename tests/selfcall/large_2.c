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

typedef struct {
    int (*bar)( /* processor::selfcall */ );
    k_t* k;
    void* next;
} e_t;

typedef struct {
    e_t e1;
    e_t e2;
    e_t e3;
    int (*test1)( /* processor::selfcall */ );
    int (*test2)( /* processor::selfcall */ );
    int (*test3)( /* processor::selfcall */ );
} f_t;

typedef struct {
    f_t f;
    d_t* d_array[10];
    b_t b_nested[5];
    void* complex_ptr;
} g_t;

typedef struct {
    g_t* g;
    k_t k_matrix[3][3];
    int (*matrix_func[2][2])( /* processor::selfcall */ );
} h_t;

typedef struct {
    h_t* h1;
    h_t* h2;
    h_t h3;
    f_t f_instances[4];
    int (*deep_call)( /* processor::selfcall */ );
} i_t;

typedef struct {
    i_t** i_ptrs;
    void* volatile_ptr;
    const void* const_ptr;
    int (*volatile_func)( /* processor::selfcall */ );
} j_t;

typedef struct {
    j_t j;
    a_t a_array[20];
    d_t d_complex;
    struct {
        k_t* inner_k;
        int (*inner_func)( /* processor::selfcall */ );
        struct {
            b_t* deep_b;
            int (*deeper_func)( /* processor::selfcall */ );
            struct {
                c_t deepest_c;
                int (*deepest_func)( /* processor::selfcall */ );
            } nested;
        } deeper;
    } anonymous;
} l_t;

typedef struct {
    l_t l_items[8];
    k_t* k_ptrs[16];
    void* void_matrix[4][4];
    int (*func_array[8])( /* processor::selfcall */ );
} m_t;

typedef struct {
    m_t m;
    union {
        a_t a_union;
        b_t b_union;
        struct {
            d_t* d_in_union;
            int (*union_func)( /* processor::selfcall */ );
        } u_nested;
    } u;
} n_t;

typedef struct {
    n_t n_recursive[2];
    volatile int counter;
    const char* name;
    int (*recursive_func)( /* processor::selfcall */ );
    struct o_t* next_o;
} o_t;

typedef struct {
    o_t* o_tree[7];
    k_t*** k_3d[2][2][2];
    int (**complex_func_ptr)( /* processor::selfcall */ );
    struct {
        b_t* b_chain;
        struct {
            c_t* c_chain;
            struct {
                d_t* d_chain;
                int (*chain_func)( /* processor::selfcall */ );
            } level3;
        } level2;
    } level1;
} p_t;

typedef struct {
    p_t p_main;
    p_t p_backup;
    p_t* p_alternates[3];
    void* void_ptrs[10];
    int (*alternate_funcs[5])( /* processor::selfcall */ );
} q_t;

typedef struct {
    q_t q;
    a_t* a_ptr_grid[6][6];
    b_t b_grid[4][4];
    c_t c_volatile;
    volatile d_t* volatile_d;
    const k_t* const_k;
} r_t;

typedef struct {
    r_t r;
    struct s_t* self_ref;
    union {
        int x;
        struct {
            long y;
            int (*union_nested_func)( /* processor::selfcall */ );
        } data;
    } value;
    enum {
        STATE_A,
        STATE_B,
        STATE_C
    } state;
} s_t;

typedef struct {
    s_t s_array[3];
    t_t* t_link;
    u_t* u_link;
    int (*link_func)( /* processor::selfcall */ );
} t_t;

typedef struct {
    t_t* t;
    void** void_double_ptr;
    int (*double_func)( /* processor::selfcall */ );
    struct {
        a_t** a_double_ptr;
        int (**double_func_ptr)( /* processor::selfcall */ );
    } inner;
} u_t;

typedef struct {
    u_t u;
    v_t* v_next;
    w_t* w_branch;
    x_t* x_leaf;
    y_t* y_root;
    z_t* z_final;
    int (*final_func)( /* processor::selfcall */ );
} v_t;

typedef struct {
    v_t* v;
    k_t k_complex;
    d_t d_nested;
    b_t b_multi[3];
    int (*multi_func[3])( /* processor::selfcall */ );
} w_t;

typedef struct {
    w_t w;
    a_t* a_ptrs[10];
    void* complex_void;
    struct xx_t {
        b_t* b_in_struct;
        int (*struct_func)( /* processor::selfcall */ );
    } xx;
} x_t;

typedef struct {
    x_t x;
    y_t* y_recursive;
    z_t* z_related;
    int (*recursive_self_func)( /* processor::selfcall */ );
} y_t;

typedef struct {
    y_t y;
    z_t* z_loop;
    k_t final_k;
    d_t final_d;
    int (*ultimate_func)( /* processor::selfcall */ );
} z_t;

k_t global_k;
d_t global_d;
b_t global_b;
a_t global_a;
c_t global_c;

v_t* global_v;
w_t global_w_array[5];
x_t*** global_x_3d;
y_t* global_y_chain;
z_t global_z_complex;

void complex_access_1() {
    k_t k;
    ((b_t*)(((d_t*)(k.d))->c.b))->a.foo();
    ((d_t*)(k.d))->foo();
    ((e_t*)(((f_t*)(((g_t*)(((h_t*)(((i_t*)(((j_t*)(((l_t*)(((m_t*)(((n_t*)(((o_t*)(((p_t*)(((q_t*)(((r_t*)(((s_t*)(((t_t*)(((u_t*)(((v_t*)(((w_t*)(((x_t*)(((y_t*)(((z_t*)global_z_complex.z_loop)->y.y_recursive))->x.w.v))->u.t.t_link))->s_array[0].r.q.p_main.o_tree[0]->n_recursive[0].m.l_items[0].anonymous.deeper.deep_b))->c.b))->a.foo();
}

void complex_access_2() {
    global_w_array[2].multi_func[1]();
    global_x_3d[1][2][3]->xx.struct_func();
    (*(*(*(global_x_3d[0])))).w.v->u.t.t_link->s_array[1].r.q.p_alternates[0]->level1.level2.level3.chain_func();
}

void complex_access_3() {
    for (int i = 0; i < 10; i++) {
        for (int j = 0; j < 10; j++) {
            global_w_array[i].v->u.t.t_link->s_array[j].r.q.p_main.o_tree[i]->n_recursive[j].m.func_array[i+j]();
        }
    }
}

void complex_access_4() {
    ((b_t*)(((d_t*)(((k_t*)(((e_t*)(((f_t*)(((g_t*)(((h_t*)(((i_t*)(((j_t*)(((l_t*)(((m_t*)(((n_t*)(((o_t*)(((p_t*)(((q_t*)(((r_t*)(((s_t*)(((t_t*)(((u_t*)(((v_t*)(((w_t*)(((x_t*)(((y_t*)(((z_t*)global_z_complex.z_loop)->y.y_recursive))->x.w.v))->u.t.t_link))->s_array[2].r.q.p_backup.level1.level2.level3.d_chain))->c.b))->a.foo();   
    global_z_complex.y.x.w.v->u.t.t_link->s_array[0].r.q.p_alternates[1]->level1.b_chain->a.foo();
}

void multi_line_complex() {
    k_t k1, k2, k3;
    d_t d1, d2, d3;
    b_t b1, b2, b3;
    
    ((b_t*)(((d_t*)(k1.d))->c.b))->a.foo();
    ((d_t*)(k2.d))->foo();
    ((b_t*)(((d_t*)(k3.d))->c.b))->a.foo();
    
    ((d_t*)(((k_t*)(((b_t*)(((d_t*)(k1.d))->c.b))->a.foo))->d))->foo();
}

void ternary_complex() {
    k_t k;
    int condition = 1;
    
    (condition ? 
        ((b_t*)(((d_t*)(k.d))->c.b))->a.foo() : 
        ((d_t*)(k.d))->foo()
    );
    
    (condition ? 
        (condition ? 
            ((b_t*)(((d_t*)(k.d))->c.b))->a.foo() : 
            ((d_t*)(k.d))->foo()
        ) : 
        (condition ? 
            ((d_t*)(k.d))->foo() : 
            ((b_t*)(((d_t*)(k.d))->c.b))->a.foo()
        )
    );
}

void loop_complex_access() {
    k_t k_array[100];
    d_t d_array[100];
    
    for (int i = 0; i < 100; i++) {
        for (int j = 0; j < 100; j++) {
            ((b_t*)(((d_t*)(k_array[i].d))->c.b))->a.foo();
            ((d_t*)(d_array[j].d))->foo();
            for (int k = 0; k < 10; k++) {
                ((b_t*)(((d_t*)(k_array[k].d))->c.b))->a.foo();
            }
        }
    }
}

void conditional_complex_access() {
    k_t k;
    d_t d;
    
    if (((b_t*)(((d_t*)(k.d))->c.b))->a.foo) {
        ((d_t*)(d.d))->foo();
    }
    
    while (((b_t*)(((d_t*)(k.d))->c.b))->a.foo) {
        ((d_t*)(k.d))->foo();
    }
    
    do {
        ((b_t*)(((d_t*)(k.d))->c.b))->a.foo();
    } while (((d_t*)(d.d))->foo);
    
    switch (((b_t*)(((d_t*)(k.d))->c.b))->a.foo()) {
        case 1:
            ((d_t*)(k.d))->foo();
            break;
        case 2:
            ((b_t*)(((d_t*)(k.d))->c.b))->a.foo();
            break;
        default:
            ((d_t*)(d.d))->foo();
    }
}

void multi_param_access(
    k_t* k1, k_t* k2, k_t* k3,
    d_t* d1, d_t* d2, d_t* d3,
    b_t* b1, b_t* b2, b_t* b3
) {
    ((b_t*)(((d_t*)(k1->d))->c.b))->a.foo();
    ((d_t*)(k2->d))->foo();
    ((b_t*)(((d_t*)(k3->d))->c.b))->a.foo();
    
    d1->foo();
    d2->foo();
    d3->foo();
    
    b1->a.foo();
    b2->a.foo();
    b3->a.foo();
}

void complex_casting() {
    k_t k;
    
    ((b_t*)(((d_t*)((void**)((intptr_t)(k.d)))))->c.b))->a.foo();
    ((d_t*)((char*)k.d + sizeof(void*)))->foo();
    
    union {
        void* ptr;
        d_t* d_ptr;
    } u;
    u.ptr = k.d;
    u.d_ptr->foo();
}

void extreme_nested_access() {
    ((b_t*)(((d_t*)(((k_t*)(((e_t*)(((f_t*)(((g_t*)(((h_t*)(((i_t*)(((j_t*)(((l_t*)(((m_t*)(((n_t*)(((o_t*)(((p_t*)(((q_t*)(((r_t*)(((s_t*)(((t_t*)(((u_t*)(((v_t*)(((w_t*)(((x_t*)(((y_t*)(((z_t*)global_z_complex.z_loop)->y.y_recursive))->x.w.v))->u.t.t_link))->s_array[0].r.q.p_main.o_tree[0]->n_recursive[0].m.l_items[0].anonymous.deeper.deep_b))->c.b))->a.foo();
}

void final_complex_function() {
    k_t local_k;
    d_t* d_ptr = (d_t*)local_k.d;
    b_t* b_ptr = (b_t*)d_ptr->c.b;
    
    b_ptr->a.foo();
    d_ptr->foo();
    
    ((b_t*)(((d_t*)(local_k.d))->c.b))->a.foo();
    ((d_t*)(local_k.d))->foo();
    
    k_t** k_ptr_ptr;
    ((b_t*)(((d_t*)((*k_ptr_ptr)->d))->c.b))->a.foo();
    
    int result = ((b_t*)(((d_t*)(local_k.d))->c.b))->a.foo() + 
                 ((d_t*)(local_k.d))->foo() * 
                 ((b_t*)(((d_t*)(global_k.d))->c.b))->a.foo();
    
    if (result > 0) {
        ((d_t*)(global_k.d))->foo();
    }
}