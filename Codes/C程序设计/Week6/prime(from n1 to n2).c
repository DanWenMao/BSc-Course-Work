#include<stdio.h>
int main()
{
	int num1,num2,t,i,j,r,m;
	scanf("%d%d",&num1,&num2);
	t=num1;
	num1=num1>=num2?num2:num1;
	num2=t>=num2?t:num2;
	//printf("%d%d",num1,num2);
	if(num1==1)
		num1++;
	for(i=num1;i<=num2;i++)
	{
		r=sqrt(i);
		for(m=1,j=2;j<=r;j++)
		{
			if(i%j==0)
				m=0;
		}
		if(m)
			printf("%d\n",i);
	}
	
	return 0;
}
