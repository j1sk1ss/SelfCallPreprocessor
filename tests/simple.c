typedef struct {
    int value;
    void (*print)(/* processor::selfcall */);
    void (*increment)(/* processor::selfcall */);
} Counter;

void test_simple() {
    Counter c;
    c.print();
    c.increment();
}

/*EXPECTED_CODE
typedef struct __anon_struct_Counter
{
  int value;
  void (*print)(struct __anon_struct_Counter *);
  void (*increment)(struct __anon_struct_Counter *);
} Counter;
void test_simple()
{
  Counter c;
  c.print(&c);
  c.increment(&c);
}
EXPECTED_CODE*/
