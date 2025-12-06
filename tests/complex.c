typedef struct {
    void (*method)(/* processor::selfcall */);
} Obj;

Obj* get_obj(int idx);
Obj global_obj;

void test_complex() {
    Obj* o = get_obj(0);
    o->method();
    ((Obj*)(o + 1))->method();
    ((Obj*)(global_obj.method ? &global_obj : o))->method(); 
    ((Obj*)0x1000)->method();
}

/*EXPECTED_CODE
typedef struct __anon_struct_Obj
{
  void (*method)(struct __anon_struct_Obj *);
} Obj;
Obj *get_obj(int idx);
Obj global_obj;
void test_complex()
{
  Obj *o = get_obj(0);
  o->method(o);
  ((Obj *) (o + 1))->method((Obj *) (o + 1));
  ((Obj *) ((global_obj.method) ? (&global_obj) : (o)))->method((Obj *) ((global_obj.method) ? (&global_obj) : (o)));
  ((Obj *) 0x1000)->method((Obj *) 0x1000);
}
EXPECTED_CODE*/
