#include <iostream>
#include <cstdio>
using namespace std;

int input_number[100];
int count = 0;

int main()
{
    int temp_number = 0;

    cin >> count;
    for(int i = 0; i < count; i++)
    {
        cin >> input_number[i];
    }

    for(int i = 0; i < count; i++){
        for(int j = 0; j < count - i - 1; j++){
            if(input_number[j] > input_number[j+1]){
                int temp = input_number[j];
                input_number[j] = input_number[j+1];
                input_number[j+1] = temp;
            }
        }
    }

    for(int i = 0; i < count; i++){
        cout << input_number[i] << " ";
    }
    cout << endl;
    return 0;
}
