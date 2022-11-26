#include <cstdio>
#include <iostream>
#include <stdlib.h>

#define dfsd 5 + 6

using namespace std;

int main()
{
	for (int i = 0x1; i < -10.5F; i += 02)
	{
		// try error: @
		if (i && '\0')
		{
			float a = -.4e010L;
			// print here
			printf(u8"Hello 'world'!\n");
		}
		else if (i % 5 == 0)
		{
			std::cout << U'?' << std::endl;
		}
	}
	return 0;
}
