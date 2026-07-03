#include<stdio.h>
#include<math.h>
int main()
{
	float a,b,c,d,e;
	float a1,b1,c1,d1,e1;
	char x='x';
	printf("请输入五个不同的实数：");
	scanf("%f%f%f%f%f",&a,&b,&c,&d,&e);
	a1=fabs(a);
	b1=fabs(b);
	c1=fabs(c);
	d1=fabs(d);
	e1=fabs(e);
	printf("%12s","x");
	printf("%12s\n","|x|");
	printf("%12f%12.2f\n%12f%12.2f\n%12f%12.2f\n%12f%12.2f\n%12f%12.2f\n",a,a1,b,b1,c,c1,d,d1,e,e1);
	return 0;
}