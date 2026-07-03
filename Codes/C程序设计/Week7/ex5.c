#include<stdio.h>
#include<math.h>
double f(double x);
double f1(double x);
int main()
{
	double x=1,x1,eps=1e-8;
	do
	{
		x1=-f(x)/f1(x)+x;
		x=x1;
	}while(fabs(f(x))>eps);
	printf("x=%.6lf\nf(x)=%.6lf\n",x,fabs(f(x)));
	return 0;
}
double f(double x)
{
	double y;
	y=cos(x)-x;
	return y;
}
double f1(double x)
{
	double y;
	y=-sin(x)-1;
	return y;
}