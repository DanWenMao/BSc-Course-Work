#include<stdio.h>
#include<math.h>
int prime(int n);
int main()
{
	int m,n,r,i,t;
	scanf("%d%d",&m,&n);
	if(m>n)
		r=m,m=n,n=r;
	if(m==1)
		m++;
	for(i=m,t=0;i<=n;i++)
	{
		if(prime(i)&&prime(i+2))
			printf("(%d,%d)\n",i,i+2),t++;
	}
	if(!t)
		printf("该区间内无孪生素数\n");
	else printf("t=%d\n",t);

	return 0;
}
int prime(int n)
{
	int r,i,t;
	r=sqrt(n);
	for(t=1,i=2;t&&i<=r;i++)
	{
		if(n%i==0)
			t=0;
	}
	return t;
}