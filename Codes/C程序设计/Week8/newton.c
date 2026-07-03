#include<stdio.h>
#include<math.h>
#define EPS 1e-7 //if add ';',then wrong!
double newton(double x,double eps,double(*p)(double),double(*q)(double));
double f(double x);
double f1(double x);
//change the f(and f1 accordingly) to meet your need
int main()
{
	double x;
	scanf("%lf",&x);//input the initial value of x
	x=newton(x,EPS,f,f1);
	printf("%lf",x);
	
	return 0;
}

double newton(double x,double eps,double(*p)(double),double(*q)(double))
{
	double x1;
	
	if(fabs(p(x))<eps)
		return x;
	do
	{
		x1=x-p(x)/q(x);
		x=x1; 
	}while(fabs(p(x))>eps);
	return x;
}
double f(double x)
{
	double y;
	y=pow(x,3)-27;
	return y;
}
double f1(double x)
{
	double y;
	y=3*pow(x,2);
	return y;
}
