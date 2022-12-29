#include <cstdio>

int n = 1;

class Test
{
public:
    int a;
    int d;
};

int main()
{
    Test t;
    t.a = 3;
    t.d = 7;
    printf("%d\n", t.a);
    printf("%d\n", t.d);
    return 0;
}