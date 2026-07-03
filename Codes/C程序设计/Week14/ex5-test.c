#include<stdio.h>
#include<ctype.h>
#include<string.h>
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
int main()
{
	char a[100],s[10][10];
	int i,t;
	strcpy(a,"this is a book,that is an apple");
	t=seperate(a,s);
	for(i=0;i<t;i++)
		puts(s[i]);

	return 0;
}
