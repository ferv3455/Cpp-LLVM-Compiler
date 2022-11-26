#include<iostream>
#include <stack>
#include <cstring>
using namespace std;

stack <char> operations;
stack <float> operands;

float l_operand, r_operand, result;
char operation;

// calculation with '(' and ')'

void cal(){
    operation = operations.top();
    operations.pop();
    r_operand = operands.top();
    operands.pop();
    l_operand = operands.top();
    operands.pop();
    switch (operation)
    {
        case '+':
            result = l_operand + r_operand;
            break;
        case '-':
            result = l_operand - r_operand;
            break;
        case '*':
            result = l_operand * r_operand;
            break;
        case '/':
            result = l_operand / r_operand;
            break;
    }
    operands.push(result);
    return;
}

int main()
{
    char expression[100];
    cout << "Enter the expression: ";
    cin >> expression;
    int i = 0;

    while (expression[i] != '\0')
    {
        switch (expression[i])
        {
            case '(':
                operations.push(expression[i]);
                break;
            case ')':
                while (!operations.empty() &&operations.top() != '(')
                {
                    cal();
                }
                operations.pop();
                break;
            case '+': case '-':
                while (!operations.empty() && (operations.top() == '*' || operations.top() == '/'))
                {
                    cal();
                }
                operations.push(expression[i]);
                break;
            case '*': case '/':
                operations.push(expression[i]);
                break;
            default:
                operands.push(expression[i] - '0');
                break;
        }
        i++;
    }
    while (!operations.empty())
        cal();

    cout << "Result: " << result << endl;
    return 0;
}
