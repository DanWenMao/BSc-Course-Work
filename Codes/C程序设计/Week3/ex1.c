#include<stdio.h>
int main()
{
	int x,y,c;
	scanf("%d%d",&x,&y);
	if(x>y)
	{
		c=x%y;
	}else{
		c=y%x;	
	}
	if(c==0)
	{
		printf("Õû³ı");
	}else{
		printf("²»Õû³ı");
	}
	return 0;
}
