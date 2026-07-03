#include<stdio.h>
#include<math.h>
int main()
{
	float x,y,s,c,a,e,p;
	printf("请输入两个实数:"); 
	scanf("%f%f",&x,&y);
	s=sin(x);
	c=cos(x);
	a=fabs(x);
	e=exp(x);
	p=pow(x,y);
	printf("sinx=%f\ncosx=%f\n|x|=%f\ne^x=%f\nx^y=%f\n",s,c,a,e,p);

	return 0;
}
