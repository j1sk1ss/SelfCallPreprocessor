typedef struct {
    void (*method)(/* processor::selfcall */);
} Obj;

Obj* get_obj(int idx);
Obj global_obj;

void test_complex() {
    Obj* o = get_obj(0);
    o->method();
    (o + 1)->method();
    (global_obj.method ? &global_obj : o)->method(); 
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
  (o + 1)->method(o + 1);
  ((global_obj.method) ? (&global_obj) : (o))->method(((global_obj.method) ? (&global_obj) : (o)));
  ((Obj *) 0x1000)->method((Obj *) 0x1000);
}
EXPECTED_CODE*/
