#include <cstdio>

int main()
{
    int m;
    scanf("%d", &m);
    int i = 0;
    do
    {
        printf("%d\n", ++i);
    } while (i < m);
    return 0;
}