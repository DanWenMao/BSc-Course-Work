#include <graphics.h>
#include <conio.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#define x1 110
#define x2 310
#define x3 510
#define y1 110
#define y2 310
#define y3 510
#define R 81
#define L 55
void pgo(int (*a)[3],int i,int j){		//ÁúãåÑô
	if(a[i-1][j-1]){
		return;
	}
	a[i-1][j-1]=1;
	switch(i){
	case 1: i=x1;break;
	case 2: i=x2;break;
	case 3: i=x3;break;
	}
	switch(j){
	case 1: j=y1;break;
	case 2: j=y2;break;
	case 3: j=y3;break;
	}
	circle(i,j,R);
	_getch();
}
void cgo(int (*a)[3]){		//ÁúãåÑô
	int i=2,j=2;
	do{
		srand((unsigned int)time(NULL));
		i=1+rand()%(3);
		j=1+rand()%(3);
	}while(a[i-1][j-1]);
	a[i-1][j-1]=-1;
	switch(i){
	case 1: i=x1;break;
	case 2: i=x2;break;
	case 3: i=x3;break;
	}
	switch(j){
	case 1: j=y1;break;
	case 2: j=y2;break;
	case 3: j=y3;break;
	}
	line(i-L,j+L,i+L,j-L);
	line(i+L,j+L,i-L,j-L);
	_getch();
}
int win(int a[3][3]){		//ÁúãåÑô
	int b,c,d=1,i;
	b=a[0][0]+a[1][1]+a[2][2];
	c=a[2][0]+a[1][1]+a[0][2];
	if(b==3||c==3){
		return 1;
	}
	if(b==-3||c==-3){
		return -1;
	}
	for(i=1;i<=3;i++){
		b=a[i-1][0]+a[i-1][1]+a[i-1][2];
		c=a[0][i-1]+a[1][i-1]+a[2][i-1];
		d*=a[i-1][0]*a[i-1][1]*a[i-1][2];
		if(b==3||c==3){
			return 1;
		}
		if(b==-3||c==-3){
			return -1;
		}
	}
	if(d){
		return 114514;
	}
	return 0;
}
int choose(){		//ÁúãåÑô
	int a;
    initgraph(300, 100);
	setbkcolor(YELLOW);
	settextcolor(BLACK);
	RECT r = {0, 0, 300, 100};
	drawtext(_T(" 1.You GO First    2.Computer GO First "),&r,DT_CENTER | DT_VCENTER | DT_SINGLELINE);
    a=_getch();
	closegraph();
	if(a=='1'){
		return 1;
	}
	if(a=='2'){
		return -1;
	}
	else{
		return 0;
	}
}
void pic(){		//Ã©µ¥ÎÄ
	wchar_t insen[]=L"Up  W; Down  S; Left  A; Right  D; Comfirm  Enter";
	initgraph(620,650);
	line(10,10,10,610);
	line(210,10,210,610);
	line(410,10,410,610);
	line(610,10,610,610);
	line(10,10,610,10);
	line(10,210,610,210);
	line(10,410,610,410);
	line(10,610,610,610);
	outtextxy(10,625,insen);
}
void high(int i,int j){		//Ã©µ¥ÎÄ
	setfillcolor(BLUE);
	floodfill(100+200*i,100+200*j,WHITE);
	floodfill(15+200*i,15+200*j,WHITE);
}
void dehigh(int i,int j){		//Ã©µ¥ÎÄ
	setfillcolor(BLACK);
	floodfill(100+200*i,100+200*j,WHITE);
	floodfill(15+200*i,15+200*j,WHITE);
}
int main()		//Ã©µ¥ÎÄ
{
	int a_array[3][3]={0},i,j,cho,r,t;
	char c;
	wchar_t sen1[]=L"You win!";
	wchar_t sen2[]=L"Computer wins!";
	wchar_t sen3[]=L"Draw!";
	i=j=1;
	do{
		cho=choose();
	}while(cho==0);
	pic();
	if(cho==-1){
		cgo(a_array);
	}
	do
	{
		do{
			r=0;
			high(i,j);
			c=_getch();
			if(c!='\r'){
				dehigh(i,j);
				switch (c){
					case 'W':
					case 'w':if(j>0) j--;break;
					case 'A':
					case 'a':if(i>0) i--;break;
					case 'S':
					case 's':if(j<2) j++;break;
					case 'D':
					case 'd':if(i<2) i++;break;
				}
				high(i,j);
			}
			if(c=='\r'&&!(a_array[i][j])){
				dehigh(i,j);
				pgo(a_array,i+1,j+1);
				r=1;
			}
			if(c=='\r'&&a_array[i][j])
				continue;
		}while(r==0);
		t=win(a_array);
		if(t!=0)
			break;
		cgo(a_array);
		t=win(a_array);
		}while(t==0);
	switch(t){
	case 1:outtextxy(500,625,sen1);break;
	case -1:outtextxy(500,625,sen2);break;
	case 114514:outtextxy(500,625,sen3);break;
	}
	_getch();
	closegraph();

	return 0;
}