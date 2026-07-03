#include<stdio.h>
int main()
{
	int a_1[10],a_2[10],i,j,k;
	for(i=0;i<10;i++)
		scanf("%d",&a_1[i]);
	a_2[0]=a_1[0];
	for(i=1,j=1;i<10;i++)
	{
		int t=1;
		for(k=0;k<j;k++)
			if(a_1[i]==a_2[k])
				t=0;
		if(t)
			a_2[j]=a_1[i],j++;
	}
	for(k=0;k<j-1;k++)
		printf("%d ",a_2[k]);
	printf("%d\n",a_2[j-1]);

	return 0;
}