#include<stdio.h>
int fbnq(int n);
int main()
{
	int n;
	scanf("%d",&n);
	printf("%d\n",fbnq(n));

	return 0;
}

int fbnq(int n)
{
	if(n>2)
		return fbnq(n-2)+fbnq(n-1);
	else
		return 1;
}