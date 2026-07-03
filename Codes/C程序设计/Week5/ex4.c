#include<stdio.h>
int main()
{
	int num=100;
	int num2,num3;
	int a1,a2,a3;
	while(num<=999)
	{
		if(0==num%37)
		{
			a1=num%10;
			a2=(num-a1)%100/10;
			a3=(num-10*a2-a1)%1000/100;
			num2=a2*100+a1*10+a3;
			num3=a1*100+a3*10+a2;
			if(0==num2%37&&0==num3%37)
				printf("%d\n",num);
			else
				printf("wrong");
		}
		num=num+1;
	}

	return 0;
}