#include<stdio.h>
int main()
{
	double num=100.453627;
	int a1,b1,c1,d1;
	float a2,b2,c2,d2;
	a1=num*10+0.5;
	a2=a1/10.0;
	b1=num*100+0.5;
	b2=b1/100.0;
	c1=num*1000+0.5;
	c2=c1/1000.0;
	d1=num*10000+0.5;
	d2=d1/10000.0;
	printf("%.1f\n%.2f\n%.3f\n%.4f\n",a2,b2,c2,d2);
	
	return 0;
	
	 
}
