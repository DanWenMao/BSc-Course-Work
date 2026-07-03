#include<stdio.h>
int reverse(long *p);
int main()
{
	long num;
	int digit;
	scanf("%ld",&num);
	digit=reverse(&num);
	printf("%ld\n",num);
	printf("%d\n",digit);
	//which can output the digit of the input number 
	
	return 0;
}

int reverse(long *p)
{
	int i;
	long re_n=0;
	for(i=0;*p!=0;i++)
	{
		re_n=re_n*10+*p%10;
		*p/=10;
	}
	*p=re_n;
		
	return i;
}
