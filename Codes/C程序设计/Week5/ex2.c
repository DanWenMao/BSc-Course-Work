#include<stdio.h>
int main()
{
	int pro;
	double bon;
	scanf("%d",&pro);
	switch(pro/100000){
	case 0:bon=pro*0.1;break;
	case 1:bon=100000*0.1+(pro-100000)*0.075;break;
	case 2:
	case 3:bon=100000*0.1+100000*0.075+(pro-200000)*0.05;break;
	case 4:
	case 5:bon=100000*0.1+100000*0.075+200000*0.05+(pro-400000)*0.03;break;
	case 6:
	case 7:
	case 8:
	case 9:bon=100000*0.1+100000*0.075+200000*0.05+200000*0.03+(pro-600000)*0.015;break;
	default:bon=100000*0.1+100000*0.075+200000*0.05+200000*0.03+400000*0.015+(pro-1000000)*0.01;
	}
	printf("%f\n",bon);

	return 0;
}