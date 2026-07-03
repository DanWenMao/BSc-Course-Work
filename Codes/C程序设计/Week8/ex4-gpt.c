#include<stdio.h>

void convert(long n, int a);

int main() {
    long n;
    int a;
    scanf("%ld %d", &n,&a);
    convert(n, a);
    
    return 0;
}

void convert(long n, int a) {
    char c;
    
    if (n == 0) {
        return;
    }

    int remainder = n % a;
    
    if (remainder < 10) {
        c = remainder + '0';
    } else {
        c = remainder - 10 + 'A';
    }
    
    convert(n / a, a);
    
    printf("%c", c);
}
