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