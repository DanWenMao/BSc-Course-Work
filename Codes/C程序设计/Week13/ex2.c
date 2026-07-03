#include<stdio.h>
#include<string.h>
int fun(char a[]);
int main()
{
	char a[100];
	int cnt;
	gets(a);
	cnt=fun(a);
	printf("%d:",cnt);
	puts(a);
	return 0;
}
int fun(char a[])
{
	int i,j,t;
	t=strlen(a);
	for(i=j=0;i<=t;i++)
		if(a[i]<'0'||a[i]>'9')
			a[j++]=a[i];

	return i-j;
}