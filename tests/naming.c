typedef struct {
    int (*foo)( /* processor::selfcall */ );
} allias1_t;

typedef struct allias2 {
    int (*foo)( /* processor::selfcall */ );
};

typedef struct {
    int (*foo)();
} allias3_t;

/*EXPECTED_CODE
typedef struct __anon_struct_allias1_t
{
  int (*foo)(struct __anon_struct_allias1_t *);
} allias1_t;
typedef struct allias2
{
  int (*foo)(struct allias2 *);
};
typedef struct 
{
  int (*foo)();
} allias3_t;
EXPECTED_CODE*/
