#include<stdio.h>
int main()
{
	char ch1,ch2;
	printf("please input the first character ");
	scanf("%c",&ch1);
	switch(ch1){
	case 'm':
	case 'M':printf("Monday\n");break;
	case 'w':
	case 'W':printf("Wednesday\n");break;
	case 'f':
	case 'F':printf("Friday\n");break;
	case 't':
	case 'T':printf("please input the second character ");
			 scanf(" %c",&ch2);
			 switch(ch2){
			 case 'U':
			 case 'u':printf("Tuesday\n");break;
			 case 'H':
			 case 'h':printf("Thursday\n");break;
			 default:printf("invaild\n");
			 }
			 break;
	case 's':
	case 'S':printf("please input the second character ");
			 scanf(" %c",&ch2);
			 switch(ch2){
			 case 'U':
			 case 'u':printf("Sunday\n");break;
			 case 'a':
			 case 'A':printf("Saturday\n");break;
			 default:printf("invaild\n");
			 }
			 break;
	default:printf("invaild\n");
	}

	return 0;
}