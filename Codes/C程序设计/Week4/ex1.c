#include<stdio.h>
int main()
{
	float a,b,c,d,e;
	printf("请输入5个实数:"); 
	scanf("%f%f%f%f%f",&a,&b,&c,&d,&e);
	if(a<=b && b<=c && c<=d && d<=e){
		printf("Yes\n");
	}else{
		printf("No\n");
	}
	
	return 0;

}
