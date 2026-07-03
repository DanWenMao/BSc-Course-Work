#include<stdio.h>
int main()
{
	int x,y,i;
	scanf("%d%d",&x,&y);
	while((i=x%y)!=0)
	{
		x=y;
		y=i;
	}
	printf("%d",y);
	
	return 0;

}
