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

/*EXPECTED_CODE
typedef struct __anon_struct_Point
{
  int x;
  int y;
  void (*move)(struct __anon_struct_Point *, int dx, int dy);
  void (*scale)(struct __anon_struct_Point *, float factor);
} Point;
void test_params()
{
  Point p;
  p.move(&p, 10, 20);
  p.scale(&p, 2.5);
}
EXPECTED_CODE*/
