#include<stdio.h>
#include<math.h>
int main()
{
	int num,a,b,c,i,t,r;
	for(num=100;num<=999;num++)
	{
		a=num/100;
		b=(num-a*100)/10;
		c=num-a*100-b*10;
		if(a==(b+c)%10)
		{
			r=sqrt(num);
		for(t=1,i=2;i<=r&&t;i++)
		{
			if(num%i==0)
				t=0;
		}
		if(t)
			printf("%d\n",num);
		}
	}
	return 0;
}
