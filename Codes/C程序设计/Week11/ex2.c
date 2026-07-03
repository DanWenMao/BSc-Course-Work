#include<stdio.h>
int Del_findgcd(int a[],int n,int *f);
int gcd(int x,int y);
#define NUM 10
int main()
{
	int a[NUM],i,r,num;
	for(i=0;i<NUM;i++)
		scanf("%d",&a[i]);
	num=Del_findgcd(a,NUM,&r);
	for(i=0;i<num;i++)
		printf("%d ",a[i]);
	printf(",max common divisor is %d\n",r);

	return 0;
}
int Del_findgcd(int a[],int n,int *f)
{
	int i,j,k,r;
	for(i=j=0;i<n;i++)
		if(i%2==0)
			a[j++]=a[i];
	
	r=a[0];
	k=1;
	while(k<j)
	{
		r=gcd(r,a[k]);
		k++;
	}
	*f=r;
	return j;
}
int gcd(int x,int y)
{
	int r;
	while((r=x%y)!=0)
		x=y,y=r;

	return y;
}