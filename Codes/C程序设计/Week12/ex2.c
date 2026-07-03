#include<stdio.h>
void sort(int x[],int n);
int main()
{
	int a[5][5],b[5],i,j,t,r,count=0,num=0,*p,*q;
	for(i=0;i<5;i++)
		for(j=0;j<5;j++)
			scanf("%d",&a[i][j]);
	p=a[0];
	for(r=0;r<5;r++){
		for(i=1;i<5;i++){
			q=a[i];
			for(j=0,t=1;j<5&&t;j++){
				if(q[j]==p[r]){
					count++,t=0;
					break;
				}
			}
			if(t)
				break;
		}
		if(count==4)
			b[num]=p[r],num++;
		count=0;
	}
	sort(b,num);
	for(i=0;i<num;i++)
		printf("%d ",b[i]);

	return 0;           
}
void sort(int x[],int n)
{
	int i,j,t;
	for(i=0;i<n;i++){
		t=x[i];
		for(j=i-1;j>=0&&t<x[j];j--)
			x[j+1]=x[j];
		x[j+1]=t;
	}
}