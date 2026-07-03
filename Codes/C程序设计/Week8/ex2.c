#include<stdio.h>
int fun(long n,long *hw);
long reverse(long n);
int main()
{
	long a,b;
	int c;
	scanf("%ld",&a);
	c=fun(a,&b);
	printf("%ld,%d",b,c);
	return 0;
}

int fun(long n,long *hw)
{
	int n1,i,j;
	n1=reverse(n);
	for(j=0;n1!=n&&j<=9999;j++)
	{
		n=n+n1;
		n1=reverse(n);
	}
	if(j==10000)
		return -1;
	else
	{
		*hw=n;
		return j;
	}
}

long reverse(long n)
{
	long d;
	for(d=0;n!=0;n=n/10)
		d=d*10+n%10;
	return d;
}