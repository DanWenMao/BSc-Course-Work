#include<stdio.h>
#define NUM 10
int com(int *a,int *b,int *c);
int main()
{
	int c[2*NUM],n,i;
	int a[NUM]={3,6,7,18,23,33,35,43,48,78};
	int b[NUM]={2,7,13,21,33,37,48,50,58,67};
	n=com(a,b,c);
	for(i=0;i<2*NUM-2*n;i++)
		printf("%d ",c[i]);
	printf("\ncount=%d\n",n);

	return 0;
}
int com(int *a,int *b,int *c)
{
	int i=0,j=0,k=0,count=0;
	while(i<NUM&&j<NUM)
	{
		if(a[i]<b[j])
			c[k]=a[i],i++,k++;
		else if(a[i]==b[j])
			count++,i++,j++;
		else
			c[k]=b[j],j++,k++;
	}
	while(j<NUM)
		c[k]=b[j],k++,j++;
	while(i<NUM)
		c[k]=a[i],k++,i++;
	return count;
}