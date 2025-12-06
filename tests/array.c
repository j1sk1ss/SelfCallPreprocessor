typedef struct {
    int id;
    void (*reset)(/* processor::selfcall */);
} Item;

void test_array() {
    Item items[10];
    items[0].reset();
    
    Item* ptr = items;
    ((Item*)&ptr[5])->reset();
    
    for(int i = 0; i < 10; i++) {
        items[i].reset();
    }
}