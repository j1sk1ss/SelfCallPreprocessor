typedef struct {
    int x, y;
    void (*move)(/* processor::selfcall */ int dx, int dy);
    void (*scale)(/* processor::selfcall */ float factor);
} Point;

void test_params() {
    Point p;
    p.move(10, 20);
    p.scale(2.5);
}