#include <strobj.h>

int main() {
    string_t* str = create_string("Hello world!");
    if (!str) return 1;

    printf("String len=%i\n", str->length());
    str->print();

    destroy_string(str);
    return 0;
}
