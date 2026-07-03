#include <graphics.h>      
#include <conio.h>
#define pi 3.1415926535
int main()
{
	char a;
    initgraph(1000,500);
    outtextxy(400,100,_T("1.圆形"));
	outtextxy(400,150,_T("2.矩形"));
	outtextxy(400,200,_T("3.椭圆"));
	outtextxy(400,250,_T("4.扇形"));
	outtextxy(400,300,_T("0.退出"));
	a=getch();
	cleardevice();
	if(a=='1'){
		circle(500,250,100);
	}else if(a=='2'){
		rectangle(400,200,600,600);
	}else if(a=='3'){
		ellipse(400,200,600,600);
	}else if(a=='4'){
		pie(400,200,600,600,0*pi/180,60*pi/180);
	}else return 0;
	_getch();
	return 0;
}