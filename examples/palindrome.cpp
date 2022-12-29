#include <cstdio>
#include <cstring>

bool palindrome(char str[256])
{
    int len = strlen(str);
    for (int i = 0; i < len / 2; i++)
    {
        if (str[i] != str[len - i - 1])
        {
            return false;
        }
    }
    return true;
}

int main()
{
    char str[256];
    scanf("%s", str);
    if (palindrome(str))
        printf("True\n");
    else
        printf("False\n");
    return 0;
}
