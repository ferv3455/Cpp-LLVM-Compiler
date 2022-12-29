#include <cstdio>

int input_number[100];
int count = 0;

int main()
{
    int temp_number = 0;

    scanf("%d", &count);
    for (int i = 0; i < count; i++)
    {
        scanf("%d", &input_number[i]);
    }

    for (int i = 0; i < count; i++)
    {
        for (int j = 0; j < count - i - 1; j++)
        {
            if (input_number[j] > input_number[j + 1])
            {
                int temp = input_number[j];
                input_number[j] = input_number[j + 1];
                input_number[j + 1] = temp;
            }
        }
    }

    for (int i = 0; i < count; i++)
    {
        printf("%d ", input_number[i]);
    }
    printf("\n");
    return 0;
}
