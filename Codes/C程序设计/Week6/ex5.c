#include<stdio.h>
#include<math.h>
#define EXP 1e-8
int main()
{
	double x,s=0,a;
	int n=1;
	scanf("%lf",&x);
	a=x/n;
	while(fabs(a)>EXP){
		s+=a;
		n+=2;
		a=a*x*x/(n*(n-1))*(-1);
	}
	printf("%.1lf",s);
	
	return 0;
}
