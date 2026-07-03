#include<stdio.h>
#include<math.h>
double integral(double a,double b,long n,double (*p)(double));
double f(double x);

int main()
{
	double a,b,s1,s2,s3;
	long n;
	scanf("a=%lf,b=%lf,n=%ld",&a,&b,&n);
	s1=integral(a,b,n,cos);
	s2=integral(a,b,n,sin);
	s3=integral(a,b,n,f);
	printf("integral cos:%.6lf\nintegral sin:%.6lf\nintegral 2x+1:%.6lf\n",s1,s2,s3);

	return 0;
}

double integral(double a,double b,long n,double (*p)(double))
{
	double f,s,h,i;
	h=(b-a)/n;
	s=(p(a)+p(b))/2;
	for(i=1;i<n;i++)
	{
		f=p(a+h*i);
		s+=f;
	}
	s*=h;

	return s;
}
double f(double x)
{
	double y;
	y=2*x+1;

	return y;
}