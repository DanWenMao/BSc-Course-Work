#include<stdio.h>
void line_sort(int a[ ][4],int b[ ],int n);
void exchange(int a[ ][4],int i,int j);
int main()
{
	int a[5][4],b[5],i,j;
	for(i=0;i<5;i++)
		for(j=0;j<4;j++)
			scanf("%d",&a[i][j]);


	line_sort(a,b,5);
	for(i=0;i<5;i++){
		for(j=0;j<4;j++)
			printf("%d ",a[i][j]);
		printf("\n");
	}
	printf("sum\n");
	for(i=0;i<5;i++)
		printf("%d ",b[i]);
	printf("\n");

	return 0;
}
void line_sort(int a[ ][4],int b[ ],int n)
{
	int i,j,t,flag;
	for(i=0;i<n;i++)
		for(j=0,b[i]=0;j<4;j++)
			b[i]+=a[i][j];

	for(i=0;i<n-1;i++){
		flag=1;
		for(j=0;j<n-1-i;j++)
			if(b[j]>b[j+1]){
				t=b[j];
				b[j]=b[j+1];
				b[j+1]=t;
				exchange(a,j,j+1);
				flag=0;
			}
		if(flag)
				break;
	}
}
void exchange(int a[ ][4],int i,int j)
{
	int k,t;
	for(k=0;k<4;k++){
		t=a[i][k];
		a[i][k]=a[j][k];
		a[j][k]=t;
	}
}