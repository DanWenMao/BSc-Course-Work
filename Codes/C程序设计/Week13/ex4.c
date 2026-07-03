#include<stdio.h>
#include<string.h>
int main()
{
	int i,j,count=0,t,k,biggest,nbiggest;
	char a[100][100],s[100];
	int num[100];
	gets(s);
	t=strlen(s);
	for(i=0;i<t;i++)
	{
		if((s[i]>='a'&&s[i]<='z')||(s[i]>='A'&&s[i]<='Z')){
			j=0;
			while((s[i+j]>='a'&&s[i+j]<='z')||(s[i+j]>='A'&&s[i+j]<='Z')){
				a[count][j]=s[i+j];
				j++;
		}
			a[count][j]='\0';
			num[count]=j;
			count++;
		}
	}
	biggest=num[0];
	nbiggest=0;
	for(k=0;k<count;k++){
		if(num[k]>biggest)
			biggest=num[k],nbiggest=k;
	}
	puts(a[nbiggest]);

	return 0;
}