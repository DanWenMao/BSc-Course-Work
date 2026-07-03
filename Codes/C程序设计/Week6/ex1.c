#include<stdio.h>
int main()
{
	int num,a,b,c,t,max,min;
	scanf("%d",&num);
	
	do{
		printf("%d-",num);
		a=num/100;
		b=(num-a*100)/10;
		c=num-a*100-b*10;
		if(a==b&&b==c)
			printf("invaild");
		if(a<b)
			t=a,a=b,b=t;
		if(a<c)
			t=a,a=c,c=t;
		if(b<c)
			t=b,b=c,c=t;	
	//printf("%d,%d,%d",a,b,c);
		max=100*a+10*b+c;
		min=100*c+10*b+a;
		num=max-min;
	}while(num!=495);
	printf("495");
	return 0;
}