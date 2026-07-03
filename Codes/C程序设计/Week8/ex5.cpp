#include<stdio.h>
#include<graphics.h>
#include<conio.h>
#include<math.h>
#define pi 3.1415926535
void print_function(double (*p)(double));
int main()
{
	print_function(sin);
	//print_function(cos);
	//print_function(tan);

	return 0;
}

void print_function(double (*p)(double))
{
	int x,y;
	initgraph(720,360);
	setorigin(360,180);
	setaspectratio(1,-1);
	line(-360,0,360,0);
	line(0,180,0,-180);
	for(x=-180;x<=180;x++)
	{
		y=p(x*pi/180.0)*180/pi;
		putpixel(x,y,WHITE);
	}
	_getch();
	closegraph();

}
