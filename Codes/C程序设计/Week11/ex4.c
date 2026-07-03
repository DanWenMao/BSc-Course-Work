#include<stdio.h>
#include<math.h>
void sort(int x[],int n);
int mpsort(int x[],int n);
int prime(int n);
#define NUM 10
int main()
{
	int a[NUM],i,n;
	for(i=0;i<NUM;i++)
		scanf("%d",&a[i]);
	n=mpsort(a,NUM);
	for(i=0;i<NUM;i++)
		printf("%d ",a[i]);
	printf("\nt=%d\n",n);

	return 0;
}
int mpsort(int x[],int n)
{
	int i,pri,even,n_even=0,max,min,t=1;
	for(i=n-1;i>=0;i--)
		if(prime(x[i])&&t)
			pri=i,t=0;
	for(i=0;i<n;i++)
		if(x[i]%2==0&&x[i]>n_even)
			n_even=x[i],even=i;
	//printf("%d %d\n",pri,even);
	max=even>pri?even:pri;
	min=even>pri?pri:even;
	sort(x+min,max-min+1);
	return max-min+1;
}
void sort(int x[],int n)
{
	int i,j,t;
	for(i=1;i<n;i++)
	{
		t=x[i];
		for(j=i-1;t<x[j]&&j>=0;j--)
			x[j+1]=x[j];
		x[j+1]=t;
	}
}
int prime(int n)
{
	int p=sqrt(n*1.0),i,t=1;
	for(i=2;i<=p&&t;i++)
		if(n%i==0)
			t=0;
	if(t)
		return 1;
	else
		return 0;
}