#include<stdio.h>
int main()
{
	int a[10],i,j,t,count=0;
	for(i=0;i<10;i++)
		scanf("%d",&a[i]);
	for(i=0;i<10;i++)
	{
		t=1;
		for(j=i+1;j<10;j++)
			if(a[i]==a[j])
				t=0;
		if(t)
			count++;
	}
	printf("%d\n",count);

	return 0;
}