#include <cstdio>
#include <stdlib.h>

#define dfsd 5 + 6

int main()
{
	for (int i = 0; i < 10.5; i++)
	{
		if (i && '\0')
		{
			// print here
			printf("Hello 'world'!\n");
		}
		else if (i % 5 == 0)
		{
			printf("?\n");
		}
	}
	return 0;
}
