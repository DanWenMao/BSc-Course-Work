#include<stdio.h>
int main()
{
	char name1,name2;
	float math1,math2,phy1,phy2,chem1,chem2,sum1,sum2,aver1,aver2;
	printf("请输入两个学生的姓名、数学成绩、物理成绩、化学成绩:");
	scanf("%c%f%f%f",&name1,&math1,&phy1,&chem1);
	scanf(" %c%f%f%f",&name2,&math2,&phy2,&chem2);
	sum1=math1+phy1+chem1;
	sum2=math2+phy2+chem2;
	aver1=sum1/3;
	aver2=sum2/3;
	printf("%12s%12s%12s%12s%12s%12s\n","NAME","MATH","PHYSICS","CHEMISTRY","SUM","AVERAGE");
	printf("%12c%12.1f%12.1f%12.1f%12.1f%12.1f\n",name1,math1,phy1,chem1,sum1,aver1);
	printf("%12c%12.1f%12.1f%12.1f%12.1f%12.1f\n",name2,math2,phy2,chem2,sum2,aver2);

	return 0;

}
