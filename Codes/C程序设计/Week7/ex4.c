#include<stdio.h>
#include<math.h>
double f(double x);
int main()
{
	double y,a=-1,b=1,x,eps=1e-7;
	do{
		x=(a+b)/2;
		if(f(a)*f(x)<0)
			b=x;
		else a=x;
	}while(fabs(f(x))>eps);
	printf("x=%.6lf\n",x);
	return 0;
}
double f(double x)
{
	double y;
	y=exp(x)+x;
	return y;
}
