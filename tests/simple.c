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