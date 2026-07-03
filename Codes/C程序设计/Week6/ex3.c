#include<stdio.h>
#include<math.h>
int main()
{
	int num,sq,a,b,c,d,e,f;
	for(num=100000;num<=999999;num++)
	{
		sq=sqrt(num);
		if(sq*sq==num)
		{
			a=num/100000;
			b=(num-100000*a)/10000;
			c=(num-100000*a-10000*b)/1000;
			d=(num-100000*a-10000*b-1000*c)/100;
			e=(num-100000*a-10000*b-1000*c-100*d)/10;
			f=(num-100000*a-10000*b-1000*c-100*d-10*e);
			if(a==f&&b==e&&c==d){
				//printf("%d%d%d%d%d%d\n",a,b,c,d,e,f);
				printf("%d",num);
			}
		}
	
	}

	return 0;
}