#include <stdio.h>

int main(){
	int a,i;
	scanf("%d",&a);
	printf("%d=",a);
	for(i=2;i<=a;i++){
		while(a%i==0&&a!=i){
			printf("%d*",i);
			a=a/i;
		}
		if(a==i){
			printf("%d",i);
			break;
		}
	}
	return 0;
}
