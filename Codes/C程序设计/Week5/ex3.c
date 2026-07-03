#include<stdio.h>
int main()
{
	int num,i;
	i=0;
	scanf("%d",&num);
	while(num!=0)
	{
		num=num/10;
		i++;
	}
	printf("正整数的位数是%d\n",i);

	return 0;
}