typedef struct {
    char* data;
    void (*clear)(/* processor::selfcall */);
    void (*append)(/* processor::selfcall */ const char* str);
} Buffer;

void test_pointers() {
    Buffer* buf = malloc(sizeof(Buffer));
    buf->clear();
    buf->append("test");
    
    Buffer b;
    Buffer* ptr = &b;
    ptr->clear();
}