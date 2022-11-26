#include <cstdio>
#include <iostream>
#include <stdlib.h>

#define dfsd 5 + 6

using namespace std;

int main()
{
	for (int i = 0; i < -10.5; i++)
	{
		if (i && '\0')
		{
			// print here
			printf("Hello 'world'!\n");
		}
		else if (i % 5 == 0)
		{
			std::cout << "?" << std::endl;
		}
	}
	return 0;
}
