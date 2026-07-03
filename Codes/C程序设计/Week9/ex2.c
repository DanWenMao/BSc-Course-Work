#include<stdio.h>
#include<math.h>
int ifpo(int n);
int main()
{
	int n;
	scanf("%d",&n);
	printf("%d\n",ifpo(n));

	return 0;
}

int ifpo(int n)
{
	static int s=2;
	int sq;
	//sq=sqrt(n);
	if(n%s==0)
		return 0;
	else
	{
		s++;
		if(s>=n)
			return 1;
		ifpo(n);
	}
}