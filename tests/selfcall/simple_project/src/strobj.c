#include <strobj.h>

static int string_print(string_t* self) {
    printf("%s\n", self->body);
    return 1;
}

static unsigned int string_length(string_t* self) {
    return self->size;
}

string_t* create_string(const char* s) {
    string_t* str = (string_t*)malloc(sizeof(string_t));
    if (!str) return NULL;

    str->body = (char*)malloc(strlen(s) + 1);
    if (!str->body) {
        free(str);
        return NULL;
    }

    strcpy(str->body, s);
    str->print  = string_print;
    str->length = string_length;

    return str;
}

int destroy_string(string_t* s) {
    if (!s) return 0;
    free(s->body);
    free(s);
    return 1;
}
