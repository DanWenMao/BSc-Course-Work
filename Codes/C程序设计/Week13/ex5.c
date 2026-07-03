#include<stdio.h>
#include<string.h>
#include<math.h>
int replace_str(char *s,char *t,char *g);
int main()
{
	char s[100],t[100],g[100];
	int cnt;
	scanf("%s%s%s",s,t,g);
	cnt=replace_str(s,t,g);
	puts(s);
	printf("count=%d\n",cnt);

	return 0;
}
int replace_str(char *s,char *t,char *g)
{
	int i,j,k,m,count=0,r1,r2,r3,diat;
	r1=strlen(s);
	r2=strlen(t);
	r3=strlen(g);
	diat=abs(r2-r3);
	for(i=0;i<r1;i++)
		if(s[i]==t[0]){
			for(k=i,j=0;j<r2&&s[k]==t[j];k++,j++);
			if(t[j]=='\0'){
				count++;
				if(strcmp(t,g)>0)
					for(m=k;m<=r1;m++)
						s[m-diat]=s[m];
				else if(strcmp(t,g)<0)
					for(m=r1;m>=k;m--)
						s[m+diat]=s[m];
				for(k=i,j=0;j<r3;k++,j++)
					s[k]=g[j];
				r1=strlen(s);
			}
		}

	return count;
}