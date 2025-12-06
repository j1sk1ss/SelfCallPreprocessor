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

/*EXPECTED_CODE
typedef struct __anon_struct_Buffer
{
  char *data;
  void (*clear)(struct __anon_struct_Buffer *);
  void (*append)(struct __anon_struct_Buffer *, const char *str);
} Buffer;
void test_pointers()
{
  Buffer *buf = malloc(sizeof(Buffer));
  buf->clear(buf);
  buf->append(buf, "test");
  Buffer b;
  Buffer *ptr = &b;
  ptr->clear(ptr);
}
EXPECTED_CODE*/
