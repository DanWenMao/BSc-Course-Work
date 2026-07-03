#include<stdio.h>
#include<string.h>
void num(char a[],char alpha[],int beta[]);
int main()
{
	char a[100],alpha[26];
	int beta[26]={0},i;
	for(i=0;i<26;i++)
		alpha[i]='a'+i;
	gets(a);
	num(a,alpha,beta);
	for(i=0;i<26;i++)
		if(beta[i]>0)
			printf("%c:%d ",alpha[i],beta[i]);

	return 0;
}
void num(char a[],char alpha[],int beta[])
{
	int i,j,t;
	t=strlen(a);
	for(i=0;i<t;i++)
		for(j=0;j<26;j++)
			if(a[i]==alpha[j])
				beta[j]++;
}