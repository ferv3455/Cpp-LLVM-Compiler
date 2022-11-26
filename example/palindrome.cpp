#include <iostream>
#include <cstring>
using namespace std;

bool palindrome(string str)
{
    int len = str.length();
    for(int i = 0; i < len / 2; i++)
    {
        if(str[i] != str[len - i - 1])
        {
            return false;
        }
    }
    return true;
}

int main()
{
    string str;
    cin >> str;
    if(palindrome(str)) cout << "True" << endl;
    else cout << "False" << endl;
    return 0;
}
