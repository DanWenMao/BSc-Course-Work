#include<stdio.h>
void f(long n,int a);
int main()
{
	long n;
	int a;
	char i;
	scanf("%ld %d",&n,&a);
	f(n,a);
	
	return 0;
}

void f(long n,int a)
{
	char i;
	if(n>=a)
		i=n%a,f(n/a,a);
	else
		i=n;
	if(i>=10)
		i='A'+i-10;
	else i='0'+i;
	
	
	printf("%c",i);
}

