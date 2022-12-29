#include <cstdio>

int n[10];
int m = 6, t = 4;

int input(int a[10])
{
    scanf("%d", &a[0]);
    return 6;
}

int main()
{
    // printf("%d\n", input(n));
    printf("%d\n", t);
    // scanf("%d", &n[2]);
    for (int i = 0; i < m; i++)
    {
        for (int j = 0; j <= i; ++j)
            n[i] = n[i] + j;
    }
    for (int i = 0; i < m; i++)
    {
        printf("Hello world %d!\n", n[i]);
    }
    return 0;
}