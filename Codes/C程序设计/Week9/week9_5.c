#include<stdio.h>
#define NUM 5
int peach(int n,int s);
int main()
{
	int n,s;
	s=NUM;
	for(n=6;;n++)
	{
		if(!peach(n,s))
			continue;
		else
		{
			printf("%d\n",n);
			return 0;
		}
	}
}

int peach(int n,int s)
{
	if(s==0)
		return 1;
	if((n-1)%5!=0)
		return 0;
	else
		return peach((n-1)/5*4,s-1);
}
