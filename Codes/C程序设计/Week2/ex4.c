#include<stdio.h>
#define price 30
int main()
{
	double r,h,dens,V,value;
	scanf("%lf%lf%lf",&r,&h,&dens);
	V=3.1415926*r*r*h;
	value=V*dens*price;
	printf("总体积=%lf\n总价值=%lf",V,value);
	
	return 0;
}
