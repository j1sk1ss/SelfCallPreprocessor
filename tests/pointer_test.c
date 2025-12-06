#include "header.h"
void foo() {
    string_t s;
    void* b = &s;

    ((string_t*)((int)b))->get_size();
    ((string_t*)((int)b))->get_size(b);

    s.get_size();
    s.get_size(&s);

    ((string_t*)b)->set_body("Hello world!");
    s.set_body("Hello world!");
}
