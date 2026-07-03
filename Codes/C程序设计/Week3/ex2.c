#include<stdio.h>
int main()
{
	int re1,re2,re3,re4,re5,im1,im2,im3,im4,im5;
	printf("Please input complex number one\nrealpart:");
	scanf("%d",&re1);
	printf("imagpart:");
	scanf("%d",&im1);
	printf("Please input complex number two\nrealpart:");
	scanf("%d",&re2);
	printf("imagpart:");
	scanf("%d",&im2);
	re3=re1+re2;
	im3=im1+im2;
	re4=re1-re2;
	im4=im1-im2;
	re5=re1*re2-im1*im2;
	im5=re1*im2+re2*im1;
	printf("sum:%d+%di\ndifference:%d+%di\nproduct:%d+%di",re3,im3,re4,im4,re5,im5);
	
	return 0;
}
