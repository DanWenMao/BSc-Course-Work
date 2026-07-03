#include<stdio.h>
int main()
{
	int a1=2,a2=3,i;
	for(i=1;i<=10;i++)
	{
		printf("%d %d ",a1,a2);
		a1=a1+a2;
		a2=a2-a1;
	}
	return 0;
}