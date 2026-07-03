#include<stdio.h>
#include<math.h>
double f(double x);
int main()
{
	int n=20000,i;
	double x=1,s,S,y;
	s=(f(1)+f(3))/2;
	for(i=1;i<20000;i++)
	{
		x+=2.0/n;
		s+=f(x);
	}
	S=s*2.0/n;
	printf("%.3lf\n",S);
	return 0;
}
double f(double x)
{
	double y;
	y=exp(3*x)+pow(x,7);
	return y;
}