#include <cstdio>
#include <cstring>

char expression[1000];
char operations[1000];
int operations_top;
double operands[1000];
int operands_top;

double l_operand, r_operand, result;
char operation;

// calculation with '(' and ')'

void cal()
{
    operation = operations[operations_top];
    operations_top = operations_top - 1;
    r_operand = operands[operands_top];
    operands_top = operands_top - 1;
    l_operand = operands[operands_top];
    operands_top = operands_top - 1;

    if (operation == '+')
        result = l_operand + r_operand;
    else if (operation == '-')
        result = l_operand - r_operand;
    else if (operation == '*')
        result = l_operand * r_operand;
    else if (operation == '/')
        result = l_operand / r_operand;
    else
        printf("Error: Unknown operation: %d.\n", operation);

    operands_top = operands_top + 1;
    operands[operands_top] = result;
    return;
}

int main()
{
    printf("Please input the expression:\n");
    scanf("%s", expression);
    int i = 0;

    while (expression[i] != '\0')
    {
        if (expression[i] == '(')
        {
            operations_top = operations_top + 1;
            operations[operations_top] = expression[i];
        }
        else if (expression[i] == ')')
        {
            while (operations_top >= 1 && operations[operations_top] != '(')
            {
                cal();
            }
            operations_top = operations_top - 1;
        }
        else if (expression[i] == '+' || expression[i] == '-')
        {
            while (operations_top >= 1 && (operations[operations_top] == '*' || operations[operations_top] == '/'))
            {
                cal();
            }
            operations_top = operations_top + 1;
            operations[operations_top] = expression[i];
        }
        else if (expression[i] == '*' || expression[i] == '/')
        {
            operations_top = operations_top + 1;
            operations[operations_top] = expression[i];
        }
        else
        {
            operands_top = operands_top + 1;
            // operands[operands_top] = expression[i] - '0';
            char tmp[2];
            double number;
            strncpy(tmp, &expression[i], 1);
            tmp[1] = '\0';
            sscanf(tmp, "%lf", &number);
            operands[operands_top] = number;
            // printf("%d %f\n", operands_top, operands[operands_top]);
        }
        i++;
    }
    while (operations_top >= 1)
    {
        cal();
    }
    printf("The result is %f\n", result);
    return 0;
}