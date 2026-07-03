#include<stdio.h>
int half_search(int a[],int n,int x);
#define NUM 10
int main()
{
	int a[]={5,23,28,34,43,45,56,60,67,90},x,r;
	scanf("%d",&x);
	r=half_search(a,NUM,x);
	if(r!=-1)
		printf("%d\n",r);
	else
		printf("not found\n",r);

	return 0;
}
int half_search(int a[],int n,int x)
{
	int min,max,mid;
	min=0,max=n-1;
	while(min<=max)
	{
		mid=(min+max)/2;
		if(a[mid]==x)
			return mid;
		if(a[mid]>x)
			max=mid-1;
		else
			min=mid+1;
	}
	return -1;
}