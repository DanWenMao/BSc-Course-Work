#include<stdio.h>
#include<math.h>
#define EPS 1e-6
double root(double a,double b);
double f(double x);
int main()
{
	double a=1,b=2;
	if(f(a)*f(b)>0)
		printf("no root\n");
	else
		printf("x=%lf\n",root(a,b));

	return 0;
}

double root(double a,double b)
{
	double c=(a+b)/2;
	if(fabs(f(a))<EPS)
		return a;
	if(fabs(f(b))<EPS)
		return b;
	if(f(a)*f(c)<0)
		return root(a,c);
	else
		return root(c,b);
}

double f(double x)
{
	double y;
	y=x*x/4-sin(x);
	
	return y;
}