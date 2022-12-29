#include <cstdio>

int main()
{
    int m;
    scanf("%d", &m);
    int i = 0;
    while (true)
    {
        printf("%d\n", i);
        for (int j = 0; j <= i; j++)
        {
            printf("   %d\n", j);
            if (j >= i / 2)
            {
                break;
            }
            continue;
        }
        if (i >= m)
        {
            break;
        }
        i++;
    }
    return 0;
}