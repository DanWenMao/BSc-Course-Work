#include<stdio.h>
float a_max(float x[],int n);
float a_min(float x[],int n);
int main()
{
	float a[100],t;
	int n,i;
	scanf("%d",&n);
	for(i=0;i<n;i++)
		scanf("%f",&a[i]);
	t=a[0];
	printf("%.2f ",a_max(a,n));
	a[0]=t;
	printf("%.2f",a_min(a,n));

	return 0;
}
float a_max(float x[],int n)
{
	int i;
	for(i=0;i<n;i++)
		if(x[0]<x[i])
			x[0]=x[i];

	return x[0];
}
float a_min(float x[],int n)
{
	int i;
	for(i=0;i<n;i++)
		if(x[n-1]>x[i])
			x[n-1]=x[i];

	return x[n-1];
}