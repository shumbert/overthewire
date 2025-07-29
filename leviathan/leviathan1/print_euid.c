#include <stdio.h>
#include <unistd.h>

int main() {
	uid_t euid = geteuid();
	printf("Effective User ID is %d\n", euid);
	return 0;
}
