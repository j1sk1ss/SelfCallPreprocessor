typedef struct {
    int id;
    void (*reset)(/* processor::selfcall */);
} Item;

void test_array() {
    Item items[10];
    items[0].reset();
    
    Item* ptr = items;
    ((Item*)&ptr[5])->reset();
    ptr->reset();

    for(int i = 0; i < 10; i++) {
        items[i].reset();
    }
}

/*EXPECTED_CODE
typedef struct __anon_struct_Item
{
  int id;
  void (*reset)(struct __anon_struct_Item *);
} Item;
void test_array()
{
  Item items[10];
  items[0].reset(&items[0]);
  Item *ptr = items;
  ((Item *) (&ptr[5]))->reset((Item *) (&ptr[5]));
  ptr->reset(ptr);
  for (int i = 0; i < 10; i++)
  {
    items[i].reset(&items[i]);
  }

}
EXPECTED_CODE*/
