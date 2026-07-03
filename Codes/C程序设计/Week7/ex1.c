#include<stdio.h>
int palindrome(long n);
int main()
{
	long num;
	for(num=1;num<=300;num++)
	{
		if(palindrome(num))	printf("%ld\n",num);
	}
	return 0;
}
int palindrome(long n)
{
	int a,b,c,a1,b1,c1,d1,e1,i,j;
	long squ,t1,t2;
	squ=n*n;
	t1=n;
	t2=squ;
	for(i=0;t1>0;i++)
		t1=t1/10;
	for(j=0;t2>0;j++)
		t2=t2/10;
	switch(i)
	{
	case 1:switch(j)
		   {
			case 1:return 1;break;
			case 2:return 0;break;
		   }
	case 2:	a=n%10;b=(n-a)/10;
			if(a!=b) return 0;
			else
			{
				switch(j)
				{
				case 2:	a1=squ%10;b1=(squ-a1)/10;
						if(a1==b1)	return 1;
						else	return 0;
				case 3:	a1=squ%10;b1=(squ-a1)%100/10;c1=(squ-10*b1-a1)/100;
						if(a1==c1)	return 1;
						else	return 0;
				case 4:	a1=squ%10;b1=(squ-a1)%100/10;
						c1=(squ-10*b1-a1)%1000/100;d1=(squ-100*c1-10*b1-a1)/1000;
						if(a1==d1&&b1==c1)	return 1;
						else	return 0;
				}
			}
	case 3:	a=n%10;b=(n-a)%100/10;c=(n-10*b-a)/100;
			if(a!=c)	return 0;
			else
			{	a1=squ%10;b1=(squ-a1)%100/10;
				c1=(squ-10*b1-a1)%1000/100;d1=(squ-100*c1-10*b1-a1)%10000/1000;
				e1=(squ-1000*d1-100*c1-10*b1-a1)/10000;
				if(a1==e1&&b1==d1)	return 1;
				else	return 0;
			}
	}
}