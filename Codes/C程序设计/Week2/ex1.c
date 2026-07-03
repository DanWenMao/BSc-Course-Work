#include<stdio.h>
int main()
{
	double num,deci;
	int inte;
	printf("请输入一个不为零的实数:");
	scanf("%lf",&num);
	if(num<0){
		printf("sign:-\n");
		num=-num;
	}else{
		printf("sign:+\n");
	}
	inte=num;
	deci=num-inte;
	printf("integral part:%d\ndecimal fraction part:%lf\n",inte,deci);
	
	return 0;
}
