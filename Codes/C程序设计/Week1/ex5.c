#include<stdio.h>
int main()
{
	int x,a,b,c,d,y;
	printf("请输入一个四位正整数：");
	scanf("%d",&x);
	a=x%10;
	x/=10;
	b=x%10;
	x/=10;
	c=x%10;
	x/=10;
	d=x%10;
	y=1000*a+100*b+10*c+d;
	printf("输入数的反序数为%d\n",y);

	return 0;

}