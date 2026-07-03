#include<stdio.h>
void change(int x[],int n,int m);
int main()
{
	int a[100],i,n,m;
	scanf("%d",&n);
	for(i=0;i<n;i++)
		scanf("%d",&a[i]);
	scanf("%d",&m);
	change(a,n,m);
	for(i=0;i<n-1;i++)
		printf("%d ",a[i]);
	printf("%d\n",a[n-1]);

	return 0;
}
void change(int x[],int n,int m)
{
	int y[100],i;
	for(i=0;i<m;i++)
		y[i]=x[n-m+i];
	for(i=0;i<n-m;i++)
		x[n-1-i]=x[n-m-i-1];
	for(i=0;i<m;i++)
		x[i]=y[i];
}