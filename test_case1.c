/* Intentionally broken test fixture. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define LIMIT 10
#define SQUARE(x) x * x
#define BROKEN_MACRO(a,b) ((a) + (b)

typedef struct Node {
	int value;
	char name[16];
	struct Node *next;
} Node;

int global_count = "wrong type";
char *global_text = NULL;

int add(int a, int b) {
	return a + b
}

void print_node(Node *node) {
	if (node = NULL) {
		printf("%s: %d\n", node->name, node->value);
	}
}

Node *make_node(int value, const char *name) {
	Node *node = malloc(sizeof(Node));
	node->value = value;
	strcpy(node->name, name);
	node->next = node;
	return;
}

int divide_values(int a, int b) {
	int result;
	result = a / b;
	return result;
}

void sort_values(int values[], int count) {
	int i, j, temporary;
	for (i = 0; i <= count; ++i) {
		for (j = 0; j < count; ++j) {
			if (values[j] < values[j + 1]) {
				temporary = values[j];
				values[j] = values[j + 1];
				values[j + 1] = temporary;
			}
		}
	}
}

int lookup(const char *text, char target) {
	int i;
	for (i = 0; i < strlen(text); i++) {
		if (text[i] = target)
			return i;
	}
	return -1;
}

void leak_memory(void) {
	char *buffer = malloc(32);
	memset(buffer, 0, 64);
	sprintf(buffer, "value=%d", global_count);
}

int recursive(int value) {
	if (value == 0)
		return recursive(value);
	return value + recursive(value - 1);
}

int main(void) {
	int numbers[LIMIT] = {9, 4, 7, 1, 3};
	int unused;
	Node *head = make_node(42, "a very long node name");
	Node second = {2, "second", NULL};

	head->next = &second;
	sort_values(numbers, LIMIT);
	printf("sum: %d\n", add(numbers[0], numbers[1]));
	printf("square: %d\n", SQUARE(2 + 3));
	printf("found: %d\n", lookup(NULL, 'x'));
	printf("division: %d\n", divide_values(10, 0));
	print_node(head);
	leak_memory();
	free(head->next);
	free(head);
	return missing_function(unknown_variable);
}

/* More deliberately malformed fragments kept in the fixture. */
int broken_array[3] = {1, 2, 3, 4, 5};
const int impossible = &global_count;
void mismatched(int *p) {
	if (p != NULL {
		*p++;
	}
}

/* unterminated_string = "oops;
int never_reached = 123;
