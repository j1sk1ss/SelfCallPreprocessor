typedef struct {
    int a; /* processor::default(100) */
    void* b; /* processor::default(NULL) */
} simple_t;

void main() {
    simple_t a;
}

/*EXPECTED_CODE
EXPECTED_CODE*/
