#include<stdio.h>
#include<math.h>
int prime(int x);
int main()
{
	int a_1[10],a_2[10],i,j=0;
	for(i=0;i<10;i++)
	{
		scanf("%d",&a_1[i]);
		if(prime(a_1[i]))
			a_2[j]=a_1[i],j++;
	}
	for(i=0;i<10;i++)
	{
		if(prime(a_1[i]))
			a_1[i]=a_2[j-1],j--;
	}
	for(i=0;i<9;i++)
		printf("%d ",a_1[i]);
	printf("%d\n",a_1[9]);

	return 0;
}

int prime(int x)
{
	int n,i,t=1;
	n=sqrt(x*1.0);
	for(i=2;i<=n&&t;i++)
		if(x%i==0)
			t=0;
	if(t)
		return 1;
	else
		return 0;
}