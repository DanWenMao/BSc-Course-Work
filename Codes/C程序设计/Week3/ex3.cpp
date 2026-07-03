#include <graphics.h>
#include <conio.h>
#include <stdio.h>
#define pi 3.1415926535
int main()
{
	int x1re,y1re,x2re,y2re;
	int leftpi,rightpi,toppi,botpi;
	double stpi,enpi;
	int leftel,rightel,topel,botel;
	printf("Please input the parameters of a rectangle\n");
	scanf("%d%d%d%d",&x1re,&y1re,&x2re,&y2re);
	printf("Please input the parameters of a pie\n");
	scanf("%d%d%d%d%lf%lf",&leftpi,&toppi,&rightpi,&botpi,&stpi,&enpi);
	stpi=stpi/180*pi;
	enpi=enpi/180*pi;
	printf("Please input the parameters of an ellipse\n");
	scanf("%d%d%d%d",&leftel,&topel,&rightel,&botel);
	initgraph(1024,768);
	rectangle(x1re,y1re,x2re,y2re);
	pie(leftpi,toppi,rightpi,botpi,stpi,enpi);
	ellipse(leftel,topel,rightel,botel);
    _getch();              
    closegraph();
	
	return 0;
}