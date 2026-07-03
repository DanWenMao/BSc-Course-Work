#include<stdio.h>
int main()
{
	int a1=0,a2=0,a3=0,t=1,score;
	while(t)
	{
		scanf("%d",&score);
		if(score<=0)
			t=0;
		else if(score<60)
			a1++;
		else if(score<85)
			a2++;
		else
			a3++;
	}
	printf(">=85:%d\n60-84:%d\n<60:%d\n",a3,a2,a1);

	return 0;
}