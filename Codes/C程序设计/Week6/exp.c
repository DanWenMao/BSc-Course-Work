#include<stdio.h>
#include<math.h>
#define EXP 1e-8
int main()
{
	double x,a,s=0;
	int n=0;
	scanf("%lf",&x);
	a=1;
	while(fabs(a)>EXP){
		s+=a;
		//printf("%lf\n",s);
		n++;
		a=a*x/n;
	}	
	printf("e^%.1lf=%.7lf",x,s);
	
	return 0;
}
