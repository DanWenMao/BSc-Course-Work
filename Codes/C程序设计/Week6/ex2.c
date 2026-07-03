#include<stdio.h>
int main()
{
	int num,i=1,t=1;
	scanf("%d",&num);
	printf("%d=",num);
	while(t&&i<num)
	{
		i++;
		while(t&&num%i==0)
		{
			if(i!=num)
				printf("%d*",i);
			else t=0;
			num=num/i;
		}
	}
	printf("%d",i);
	
	return 0;
}
