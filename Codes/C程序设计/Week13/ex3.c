#include<stdio.h>
#include<string.h>
void fun(char xx[]);
int main()
{
	char s[100];
	gets(s);
	fun(s);
	puts(s);

	return 0;
}
void fun(char xx[])
{
	int i,j,t;
	t=strlen(xx);
	for(i=0;i<t;i++){
		if(xx[i]>='0'&&xx[i]<='9'){
			for(j=t;j>=i;j--)
				xx[j+1]=xx[j];
			t=strlen(xx);
			xx[i]='$';
			i++;
		}
	}
}