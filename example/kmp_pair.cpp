#include<iostream>
#include<cstdio>
#include<cstring>

#define maxn 100005
using namespace std;
string pattern;
string text;
int pi[maxn];

void pi_cal(int len_p){
    pi[1] = 0;
    int k = 0;

    for(int q = 2; q <= len_p; q++){
        while(k > 0 && k + 1 < len_p && pattern[k + 1] != pattern[q])
        {
            k = pi[k];
        }
        if(k + 1 < len_p && pattern[k + 1] == pattern[q]){
            k++;
        }
        pi[q] = k;
    }
    return;
}


void knuth_morris_pratt(){

    int len_p = pattern.length();
    int len_t = text.length();

    text = " " + text;
    pattern = " " + pattern;
    
    pi_cal(len_p);

    int q = 0;
    for(int i = 1 ;i <= len_t; i++){
        while(q > 0 && pattern[q + 1] != text[i]){
            q = pi[q];
        }
        if(pattern[q + 1] == text[i]){
            q++;
        }
        if(q == len_p){
            printf("Shift at %d.\n", i-len_p);
            q = pi[q];
        }
    }
    
    return;
}

int main(){
    cin >> text;
    cin >> pattern;
    
    knuth_morris_pratt();

    return 0;
}