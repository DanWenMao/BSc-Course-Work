#include<stdio.h>
#include<string.h>
#define NUM 10
int FindNoVowel(char *str[],int num,char res[][20]);
int main()
{
	char *words[NUM],get[NUM][20],res[NUM][20];
	int i,num;
	for(i=0;i<NUM;i++){
		scanf("%s",get+i);
		//strcpy(get[0],"y");
		words[i]=get[i];
	}
	num=FindNoVowel(words,NUM,res);
	for(i=0;i<num;i++)
		printf("%s ",res[i]);
	//printf("%d",num);

	return 0;
}
int FindNoVowel(char *str[],int num,char res[][20])
{
	int i,j,k,t,cnt;
	char vowel[5]={'a','e','i','o','u'},tran[20];
	for(i=0,cnt=0;i<num;i++){
		for(j=0,t=1;t&&str[i][j]!='\0';j++)
			for(k=0;k<5;k++)
				if(str[i][j]==vowel[k]){
					t=0;
					break;
				}
		if(t)
			strcpy(res[cnt++],str[i]);
	}
	for(i=0;i<cnt;i++)
		for(j=i+1;j<cnt;j++)
			if(strcmp(res[i],res[j])>0){
				strcpy(tran,res[i]);
				strcpy(res[i],res[j]);
				strcpy(res[j],tran);
			}

	return cnt;
}