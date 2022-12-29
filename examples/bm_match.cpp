#include <cstdio>
#include <cstring>

char pattern[256];
char text[1024];

int max(int a, int b)
{
    if (a > b)
        return a;

    return b;
}

void computeBMBC(int bmBc[128])
{
    for (int i = 0; i < 128; i++)
    {
        bmBc[i] = 0;
    }

    int m = strlen(pattern);
    for (int i = 0; i < m; i++)
    {
        bmBc[pattern[i]] = m;
    }
    for (int i = 0; i < m - 1; i++)
    {
        bmBc[pattern[i]] = m - i - 1;
    }
}

void computeOSuff(int oSuff[256])
{
    int m = strlen(pattern);
    oSuff[m - 1] = m;

    int l = m;
    int r = m - 1;
    for (int i = m - 2; i >= 0; --i)
    {
        // Invariant: [l, r] matches the suffix of pattern
        // r > i
        if (i >= l && oSuff[m - r + i - 1] <= i - l + 1)
        {
            // [l, i] matches the suffix of P[0:m-r+i)
            // oSuff[m-r+i-1] <= i-l+1 (the same suffix is no longer than [l,i])
            // So, oSuff[i] should be oSuff[m-r+i-1]
            oSuff[i] = oSuff[m - r + i - 1];
        }
        else
        {
            r = i;
            if (l > i)
                l = i;
            while (l >= 0 && pattern[l] == pattern[m - i + l - 1])
            {
                l--;
            }
            l++;
            oSuff[i] = r - l + 1;
        }
    }
}

void computeBMGS(int bmGs[256])
{
    int m = strlen(pattern);
    int oSuff[256];
    computeOSuff(oSuff);

    for (int i = 0; i < m; i++)
    {
        bmGs[i] = m;
    }

    int j = 0;
    for (int i = m - 2; i >= 0; i--)
    {
        if (oSuff[i] == i + 1)
        {
            while (j < m - i - 1)
            {
                if (bmGs[j] == m)
                {
                    bmGs[j] = m - i - 1;
                }
                j++;
            }
        }
    }
    for (int i = 0; i < m - 1; i++)
    {
        bmGs[m - oSuff[i] - 1] = m - i - 1;
    }
}

int BMMatching(int result[128])
{
    int n = strlen(text);
    int m = strlen(pattern);

    // Preparation
    int bmBc[128];
    computeBMBC(bmBc);
    int bmGs[256];
    computeBMGS(bmGs);

    // Main algorithm
    int count = 0;
    int s = 0;
    while (s <= n - m)
    {
        int i = m - 1;
        while (pattern[i] == text[s + i])
        {
            if (i == 0)
            {
                result[count++] = s;
                break;
            }
            else
            {
                i--;
            }
        }
        s = s + max(bmGs[i], bmBc[text[s + i]] + i - m + 1);
    }
    return count;
}

int main()
{
    // Input
    char tmp[1024];
    scanf("%s", tmp);
    strcpy(text, tmp);
    scanf("%s", tmp);
    strcpy(pattern, tmp);

    // Match
    int result[128];
    int len = BMMatching(result);
    for (int i = 0; i < len; i++)
    {
        printf("%d\n", result[i]);
    }

    return 0;
}
