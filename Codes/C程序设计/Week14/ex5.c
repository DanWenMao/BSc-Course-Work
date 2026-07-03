#include<stdio.h>
#include<string.h>
#include<ctype.h>
#define NUM 2
void count(char a[], char w[][10], int n,int b[]);
int seperate(char a[],char store[][10]);
int main()
{
	int i;
	char w[NUM][10],a[100],store[10][10];
	int b[NUM]={0};
	gets(a);
	//strcpy(a,"this is a book,that is an apple");
	seperate(a,store);
	for(i=0;i<NUM;i++)
		strcpy(w[i],store[i]);
	count(a,w,NUM,b);
	for(i=0;i<NUM;i++)
		printf("%s:%d ",w+i,b[i]);

	return 0;
}
void count(char a[], char w[][10], int n,int b[])
{
	char store[10][10];
	int i,j,cnt2;
	cnt2=seperate(a,store);
	for(i=0;i<cnt2;i++)
		for(j=0;j<NUM;j++)
			if(strcmp(store[i],w[j])==0)
				b[j]++;
}
int seperate(char a[],char store[][10])
{
	int i,j,t,cnt1=0;
	t=strlen(a);
	for(i=0;i<t;i++)
	{
		if(isalpha(a[i])){
			j=0;
			while(isalpha(a[i])){
				store[cnt1][j]=a[i];
				j++,i++;
		}
			store[cnt1][j]='\0';
			cnt1++;
		}
	}
	return cnt1;
}
