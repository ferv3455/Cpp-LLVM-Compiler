#include <cstdio>

int n;
int fib[101];

void calFib(int n)
{
    fib[0] = 0;
    fib[1] = 1;
    for (int i = 2; i <= n; i++)
    {
        fib[i] = fib[i - 1] + fib[i - 2];
    }
    printf("fib(%d) = %lld\n", n, fib[n]);
    return;
}

int main()
{
    printf("Please input n and then get fib(n), n <= 100:\n");
    scanf("%d", &n);

    calFib(n);
    return 0;
}