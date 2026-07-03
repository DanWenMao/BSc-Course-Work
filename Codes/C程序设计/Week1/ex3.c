#include<stdio.h>
int main()
{
	int a,b,c,V;
	printf("请输入长方体的长、宽、高：");
	scanf("%d%d%d",&a,&b,&c);
	V=a*b*c;
	printf("长方体的体积=%d\n",V);
	
	return 0;
}
