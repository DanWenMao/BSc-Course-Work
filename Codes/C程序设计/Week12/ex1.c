#include<stdio.h>
#include<math.h>
int prime(int x);
int main()
{
	int a[4][4],i,j,k,count=0,t;
	for(i=0;i<4;i++)
		for(j=0;j<4;j++)
			scanf("%d",&a[i][j]);
	for(i=0;i<4;i++)
		for(j=0;j<=i;j++){
			if(prime(a[i][j])){
				count++;
				for(k=(a[i][j]+1),t=1;t;k++)
					if(prime(k))
						t=0;
				a[i][j]=k-1;
			}
			else
				a[i][j]=0;
		}
	for(i=0;i<4;i++){
		for(j=0;j<4;j++)
			printf("%d ",a[i][j]);
		printf("\n");
	}
	printf("count=%d\n",count);

	return 0;
}
int prime(int x)
{
	int p,t=1,i;
	if(x==1)
		return 0;
	p=sqrt(x*1.0);
	for(i=2;i<=p&&t;i++)
		if(x%i==0)
			t=0;
	if(t)
		return 1;
	else
		return 0;
}