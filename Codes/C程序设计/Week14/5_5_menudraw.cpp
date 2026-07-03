#include <graphics.h> 
#include <conio.h>
#include <stdio.h>
#include<stdlib.h>
#include <windows.h>
#include <mmsystem.h>

#pragma comment(lib,"winmm.lib")

void draw_menu(int index);
void do_user_choice(int choice);
void function_1();
void function_2();
void function_3();
void function_4();
void draw_music_menu(int index);
void function_music();

int main(void)
{
	int choice=-1,prechoice=-1;	
	MOUSEMSG m;			
	
	initgraph(640,480);  
	draw_menu(choice);

	while(1)
	{
		if(MouseHit()){
			m = GetMouseMsg();
			if(m.x>=300 && m.x<=400 && m.y>=20 && m.y<=320)  /* 鼠标位置在菜单范围内 */
			{
				choice = (m.y-20)/50;  /* 通过鼠标位置计算位于第几个菜单选项中 */
				switch(m.uMsg){
					case WM_MOUSEMOVE:
						if(choice!=prechoice){
							draw_menu(choice);
							prechoice=choice;
						}
						break;

					case WM_LBUTTONDOWN:
						do_user_choice(choice);
						draw_menu(choice);
						break;
				}
			}

		}

	}
	
	
	closegraph();
}

void draw_menu(int index)
{
	int x=300,y=20,i;
	TCHAR menu_text[6][20]={_T("1.圆形"),_T("2,矩形"),_T("3.椭圆"),_T("4.扇形"),_T("5.背景音乐"),_T("0.退出")};

	cleardevice();
	outtextxy(100,450,menu_text[index]);

	setlinecolor(WHITE);
	setfillcolor(LIGHTGRAY);
	settextcolor(YELLOW);
	setbkcolor(LIGHTGRAY);
	for(i=0;i<6;i++){
		if(i==index){
			setbkcolor(LIGHTGRAY);
			fillrectangle(x,y,x+120,y+50);
		}
		else
			setbkcolor(BLACK);
		rectangle(x,y,x+120,y+50);
		outtextxy(x+25,y+20,menu_text[i]);
		y=y+50;
	}
	setbkcolor(BLACK);
}

void do_user_choice(int choice)
{
		switch(choice){
			case 0:	function_1(); break;
			case 1:	function_2(); break;
			case 2:	function_3(); break;
			case 3:	function_4(); break;
			case 4: function_music(); break;
			case 5: exit(0);  /* 选最后一个菜单项，就是退出 */
		}
		
}

void function_1()
{
	MOUSEMSG m;						// 定义鼠标消息

	cleardevice();
	outtextxy(100,450,_T("按鼠标右键继续。。。"));

	while(true)
	{
		// 获取一条鼠标消息
		m = GetMouseMsg();

		switch(m.uMsg)
		{
			case WM_MOUSEMOVE:		// 鼠标移动的时候画圆圈
				circle(m.x,m.y,5);;
				break;

			case WM_RBUTTONUP:
				return;				// 按鼠标右键退出
		}
	}
}

void function_2()
{
	MOUSEMSG m;						// 定义鼠标消息

	cleardevice();
	outtextxy(100,450,_T("按鼠标右键继续。。。"));

	while(true)
	{
		// 获取一条鼠标消息
		m = GetMouseMsg();

		switch(m.uMsg)
		{
			case WM_MOUSEMOVE:		// 鼠标移动的时候画矩形
				rectangle(m.x,m.y,m.x+5,m.y+5);;
				break;

			case WM_RBUTTONUP:
				return;				// 按鼠标右键退出
		}
	}
}

void function_3()
{
	MOUSEMSG m;						// 定义鼠标消息

	cleardevice();
	outtextxy(100,450,_T("按鼠标右键继续。。。"));

	while(true)
	{
		// 获取一条鼠标消息
		m = GetMouseMsg();

		switch(m.uMsg)
		{
			case WM_MOUSEMOVE:		// 鼠标移动的时候画椭圆
				ellipse(m.x,m.y,m.x+10,m.y+10);;
				break;

			case WM_RBUTTONUP:
				return;				// 按鼠标右键退出
		}
	}
}

void function_4()
{
	MOUSEMSG m;						// 定义鼠标消息

	cleardevice();
	outtextxy(100,450,_T("按鼠标右键继续。。。"));

	while(true)
	{
		// 获取一条鼠标消息
		m = GetMouseMsg();

		switch(m.uMsg)
		{
			case WM_MOUSEMOVE:		// 鼠标移动的时候画扇形
				pie(m.x,m.y,m.x+20,m.y+20,0,3.14);;
				break;

			case WM_RBUTTONUP:
				return;				// 按鼠标右键退出
		}
	}
}

void draw_music_menu(int index)
{
	int x=300,y=20,i;
	TCHAR menu_text[6][20]={_T("1.播放"),_T("2,暂停"),_T("3.继续"),_T("4.增大音量"),_T("5.减小音量"),_T("0.返回")};

	cleardevice();
	outtextxy(100,450,menu_text[index]);

	setlinecolor(WHITE);
	setfillcolor(LIGHTGRAY);
	settextcolor(YELLOW);
	setbkcolor(LIGHTGRAY);
	for(i=0;i<6;i++){
		if(i==index){
			setbkcolor(LIGHTGRAY);
			fillrectangle(x,y,x+150,y+50);
		}
		else
			setbkcolor(BLACK);
		rectangle(x,y,x+150,y+50);
		outtextxy(x+25,y+20,menu_text[i]);
		y=y+50;
	}
	setbkcolor(BLACK);
}

void function_music()
{
	int choice=-1,prechoice=-1;	
	char *mp3list[]={"天才白痴梦.mp3","光阴的故事.mp3"};
	int musicid=1;
	MOUSEMSG m;		
	char msgbuf[128]={0};
	long volumn;
	
	draw_music_menu(choice);

	while(1)
	{
		if(MouseHit()){
			m = GetMouseMsg();
			if(m.x>=300 && m.x<=400 && m.y>=20 && m.y<=320)  /* 鼠标位置在菜单范围内 */
			{
				choice = (m.y-20)/50;  /* 通过鼠标位置计算位于第几个菜单选项中 */
				switch(m.uMsg){
					case WM_MOUSEMOVE:
						if(choice!=prechoice){
							draw_music_menu(choice);
							prechoice=choice;
						}
						break;

					case WM_LBUTTONDOWN:
						switch(choice)
						{
							case 0: mciSendString("stop mci",0,0,0);
									mciSendString("close mci",0,0,0);
									sprintf(msgbuf,"open %s alias mci",mp3list[musicid]);
									printf("%s\n",msgbuf);
									mciSendString(msgbuf,0,0,0);
									mciSendString("play mci",0,0,0);
									break;
							case 1:	mciSendString("pause mci",0,0,0);
									break;
							case 2:	mciSendString("play mci",0,0,0);
									break;
							case 3: mciSendString("status mci volume", msgbuf, 128, 0 );
									volumn=atoi(msgbuf);
									printf("当前音量：%s,%ld\n",msgbuf,volumn);
									if(volumn<1000){
										volumn+=50;
										sprintf(msgbuf,"setaudio mci volume to %ld",volumn);
										printf("当前音量：%s,%ld\n",msgbuf,volumn);
										mciSendString(msgbuf,0,0,0);
									}
									break;
							case 4: mciSendString("status mci volume", msgbuf, 128, 0 );
									volumn=atoi(msgbuf);
									printf("当前音量：%s,%ld\n",msgbuf,volumn);
									if(volumn>0){
										volumn-=50;
										sprintf(msgbuf,"setaudio mci volume to %ld",volumn);
										printf("当前音量：%s,%ld\n",msgbuf,volumn);
										mciSendString(msgbuf,0,0,0);
									}
									break;
							case 5: return;  /* 结束当前函数，返回上一级菜单*/
						
						}
						draw_music_menu(choice);
						break;
				}
			}

		}

	}
	
}