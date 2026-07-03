#include<stdio.h>
#include<math.h>
int prime(int n);
int countvalue(int aa[]);
int main()
{
	int i,t,a[150];
	for(i=0;i<countvalue(a);i++)
	{
		printf("%d ",a[i]);
		if((i+1)%10==0)
			printf("\n");
	}

	return 0;
}
int prime(int n)
{
	int p,t,i;
	p=sqrt(n*1.0);
	for(i=2,t=1;i<=p&t;i++)
		if(n%i==0)
			t=0;
	if(t)
		return 1;
	else
		return 0;
}
int countvalue(int aa[])
{
	int i,cnt=0;
	for(i=500;i<=800;i++)
		if(prime(i))
			aa[cnt]=i,cnt++;
	return cnt;
}