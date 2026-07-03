#include<graphics.h>
#include<conio.h>
#include<stdio.h>
#include<math.h>
#include<time.h>
#include<stdlib.h>
#include<Windows.h>
#define NUM 5
#define ME '1'
#define ENE '2'
#define B_ME '6'
#define B_ENE1 '3'
#define B_ENE2 '7'
#define B_ENE3 '8'
#define B_ENE4 '9'
#define B_ENE11 40
#define B_ENE21 41
#define B_ENE31 42
#define B_ENE41 43
#define MYSPEED 5
#define ENESPEED 1
#define BUSPEED_ENE 5
//以下部分由朱泽磐完成
int nandu;
int myplanex = 220;
int myplaney = 135;
void me_pldr(int* mpx, int* mpy, char x[][300]);
void me_plmove(int* mpx, int* mpy, char c);
void ene_gen(int y[NUM][4]);
void ene_dr(int y[NUM][4], char x[][300]);
void ene_move(int y[NUM][4]);
void me_bushoot(int* mpx, int* mpy, char x[][300]);
void ene_bushoot(int y[NUM][4], char x[][300]);
void me_pldr(int* mpx, int* mpy, char x[][300])
{
	for (int i = 0; i < 300; i++) {
		for (int j = 0; j < 300; j++) {
			switch (x[i][j]) {
			case ME:
				x[i][j] = 0; break;
			}
		}
	}
	int i, j;
	char me_pldr[30][30] = { {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},
	{0,0,0,0,0,0,0,0,0,0,0,0,0,0,ME,ME,0,0,0,0,0,0,0,0,0,0,0,0,0,0},{0,0,0,0,0,0,0,0,0,0,0,0,0,0,ME,ME,0,0,0,0,0,0,0,0,0,0,0,0,0,0},
	{0,0,0,0,0,0,0,0,0,0,0,0,0,0,ME,ME,0,0,0,0,0,0,0,0,0,0,0,0,0,0},{0,0,0,0,0,0,0,0,0,0,0,0,0,0,ME,ME,0,0,0,0,0,0,0,0,0,0,0,0,0,0},
	{0,0,0,0,0,0,0,0,0,0,0,0,0,0,ME,ME,0,0,0,0,0,0,0,0,0,0,0,0,0,0},{0,0,0,0,0,0,0,0,0,0,0,0,0,ME,ME,ME,ME,0,0,0,0,0,0,0,0,0,0,0,0,0},
	{0,0,0,0,0,0,0,0,0,0,0,0,ME,ME,ME,ME,ME,ME,0,0,0,0,0,0,0,0,0,0,0,0},{0,0,0,0,0,0,0,0,0,0,0,0,ME,ME,ME,ME,ME,ME,0,0,0,0,0,0,0,0,0,0,0,0},
	{0,0,0,0,0,0,0,0,0,0,0,ME,ME,ME,ME,ME,ME,ME,ME,0,0,0,0,0,0,0,0,0,0,0},{0,0,0,0,0,0,0,0,0,0,0,ME,ME,ME,ME,ME,ME,ME,ME,0,0,0,0,0,0,0,0,0,0,0},
	{0,0,0,0,0,0,0,0,0,0,0,ME,ME,ME,ME,ME,ME,ME,ME,0,0,0,0,0,0,0,0,0,0,0},{0,0,0,0,0,0,0,0,0,0,0,ME,ME,ME,ME,ME,ME,ME,ME,0,0,0,0,0,0,0,0,0,0,0},
	{0,0,0,0,0,0,0,0,0,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,0,0,0,0,0,0,0,0,0},{0,0,0,0,0,0,0,0,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,0,0,0,0,0,0,0,0},
	{0,0,0,0,0,0,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,0,0,0,0,0,0},{0,0,0,0,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,0,0,0,0},
	{0,0,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,0,0},{ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME},
	{ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME},{0,0,0,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,0,0,0},
	{0,0,0,0,0,0,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,0,0,0,0,0,0},{0,0,0,0,0,0,0,0,0,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,0,0,0,0,0,0,0,0,0},
	{0,0,0,0,0,0,0,0,0,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,0,0,0,0,0,0,0,0,0},{0,0,0,0,0,0,0,0,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,0,0,0,0,0,0,0,0},
	{0,0,0,0,0,0,0,0,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,ME,0,0,0,0,0,0,0,0},{0,0,0,0,0,0,ME,ME,ME,ME,ME,ME,ME,ME,0,0,ME,ME,ME,ME,ME,ME,ME,ME,0,0,0,0,0,0},
	{0,0,0,0,ME,ME,ME,ME,ME,ME,ME,ME,ME,0,0,0,0,ME,ME,ME,ME,ME,ME,ME,ME,ME,0,0,0,0},{0,0,0,0,ME,ME,ME,ME,ME,ME,ME,ME,0,0,0,0,0,0,ME,ME,ME,ME,ME,ME,ME,ME,0,0,0,0} };
	for (i = 0; i <= 29; i++) {
		for (j = 0; j <= 29; j++) {
			if(x[i + *mpy][j + *mpx] != B_ENE1 && x[i + *mpy][j + *mpx] != B_ENE2 && x[i + *mpy][j + *mpx] != B_ENE3 && x[i + *mpy][j + *mpx] != B_ENE4) {
				x[i + *mpy][j + *mpx] = me_pldr[i][j];
			}
		}
	}
}
void me_plmove(int* mpx, int* mpy, char c)
{
	if (c == 72 && *mpy > 10) {
		*mpy = *mpy - MYSPEED;
	}
	if (c == 80 && *mpy < 260) {
		*mpy = *mpy + MYSPEED;
	}
	if (c == 75 && *mpx > 10) {
		*mpx = *mpx - MYSPEED;
	}
	if (c == 77 && *mpx < 260) {
		*mpx = *mpx + MYSPEED;
	}
}
void ene_gen(int y[NUM][4])
{
	int i,j;
	unsigned int seed = static_cast<unsigned int>(GetTickCount());
	int rannum1;
	srand(seed);
	rannum1 = rand();
	if (rannum1 % (4 / nandu) == 0) {
		for (i = 0; i < NUM; i++) {
			if (y[i][0] == 0) {
				y[i][0] = 1;
				y[i][1] = rannum1 % 50 + 25;
				y[i][2] = rannum1 % 260+10;
				y[i][3] = rannum1 % 4 + 1;
				break;
			}
		}
	}
}
void ene_dr(int y[NUM][4], char x[][300])
{
	for (int i = 0; i < 300; i++) {
		for (int j = 0; j < 300; j++) {
			switch (x[i][j]) {
			case 33:
			case 34:
			case 35:
			case 36:
			case 37: 
				x[i][j] = 0; break;
			}
		}
	}
	char ene_pldr[30][30] = { {0,0,0,0,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,0,0,0,0,0,0,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,0,0,0,0},{0,0,0,0,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,0,0,0,0,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,0,0,0,0},
	{0,0,0,0,0,0,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,0,0,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,0,0,0,0,0,0},{0,0,0,0,0,0,0,0,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,0,0,0,0,0,0,0,0},
	{0,0,0,0,0,0,0,0,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,0,0,0,0,0,0,0,0},{0,0,0,0,0,0,0,0,0,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,0,0,0,0,0,0,0,0,0},
	{0,0,0,0,0,0,0,0,0,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,0,0,0,0,0,0,0,0,0},{0,0,0,0,0,0,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,0,0,0,0,0,0},
	{0,0,0,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,0,0,0},{ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE},
	{ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE},{0,0,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,0,0},
	{0,0,0,0,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,0,0,0,0},{0,0,0,0,0,0,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,0,0,0,0,0,0},
	{0,0,0,0,0,0,0,0,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,0,0,0,0,0,0,0,0},{0,0,0,0,0,0,0,0,0,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,0,0,0,0,0,0,0,0,0},
	{0,0,0,0,0,0,0,0,0,0,0,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,0,0,0,0,0,0,0,0,0,0,0},{0,0,0,0,0,0,0,0,0,0,0,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,0,0,0,0,0,0,0,0,0,0,0},
	{0,0,0,0,0,0,0,0,0,0,0,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,0,0,0,0,0,0,0,0,0,0,0},{0,0,0,0,0,0,0,0,0,0,0,ENE,ENE,ENE,ENE,ENE,ENE,ENE,ENE,0,0,0,0,0,0,0,0,0,0,0},
	{0,0,0,0,0,0,0,0,0,0,0,0,ENE,ENE,ENE,ENE,ENE,ENE,0,0,0,0,0,0,0,0,0,0,0,0},{0,0,0,0,0,0,0,0,0,0,0,0,ENE,ENE,ENE,ENE,ENE,ENE,0,0,0,0,0,0,0,0,0,0,0,0},
	{0,0,0,0,0,0,0,0,0,0,0,0,0,ENE,ENE,ENE,ENE,0,0,0,0,0,0,0,0,0,0,0,0,0},{0,0,0,0,0,0,0,0,0,0,0,0,0,0,ENE,ENE,0,0,0,0,0,0,0,0,0,0,0,0,0,0},
	{0,0,0,0,0,0,0,0,0,0,0,0,0,0,ENE,ENE,0,0,0,0,0,0,0,0,0,0,0,0,0,0},{0,0,0,0,0,0,0,0,0,0,0,0,0,0,ENE,ENE,0,0,0,0,0,0,0,0,0,0,0,0,0,0},
	{0,0,0,0,0,0,0,0,0,0,0,0,0,0,ENE,ENE,0,0,0,0,0,0,0,0,0,0,0,0,0,0},{0,0,0,0,0,0,0,0,0,0,0,0,0,0,ENE,ENE,0,0,0,0,0,0,0,0,0,0,0,0,0,0},
	{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0} };
	for (int i = 0; i < NUM; i++) {
		if (y[i][0] == 1) {
			for (int k = 0; k <= 29; k++) {
				for (int l = 0; l <= 29; l++) {
					if (ene_pldr[k][l] == ENE) {
						if (x[k + y[i][1]][l + y[i][2]] != B_ME) {
							x[k + y[i][1]][l + y[i][2]] = i + 33;
						}
					}
				}
			}
		}
	}
}
void ene_move(int y[NUM][4], char x[][300])
{
	for (int i = 0; i < NUM; i++) {
		if (y[i][0] == 1) {
			switch (y[i][3])
			{
			case 1:y[i][1] += (ENESPEED * nandu);
				if (y[i][1] > 260) {
					y[i][0] = 0;
				}; break;
			case 2: {
				y[i][2] += (ENESPEED * nandu);
				if (y[i][2] > 270) {
					y[i][0] = 0 ;
				}
				break;
			case 3: {
				y[i][1] += (ENESPEED * nandu);
				y[i][2] += (ENESPEED * nandu);
				if (y[i][2] > 270) {
					y[i][3] = 4;
				}
				if (y[i][1] > 260) {
					y[i][0] = 0;
				}
				break;
			}
			case 4: {
				y[i][1] += (ENESPEED * nandu);
				y[i][2] -= (ENESPEED * nandu);
				if (y[i][2] < 10) {
					y[i][3] = 3;
				}
				if (y[i][1] > 260) {
					y[i][0] = 0;
				}
				break;
			}
			}

			}
		}
	}
}
void me_bushoot(int* mpy,int* mpx, char x[][300])
{
	x[*mpx -1][*mpy +9] = B_ME;
	x[*mpx -1][*mpy +20] = B_ME;
}
void ene_bushoot(int y[NUM][4], char x[][300])
{
	for (int i = 0; i < NUM; i++) {
		if (y[i][0] == 1) {
			switch ((y[i][3] + 3 * i) % 4 + 1)
			{
			case 1:x[y[i][1] + 31][y[i][2] + 12] = B_ENE1;
				x[y[i][1] + 31][y[i][2] + 18] = B_ENE1;
				break;
			case 2:x[y[i][1] + 31][y[i][2] + 12] = B_ENE2;
				x[y[i][1] + 31][y[i][2] + 18] = B_ENE2;
				break;
			case 3:x[y[i][1] + 31][y[i][2] + 12] = B_ENE3;
				x[y[i][1] + 31][y[i][2] + 18] = B_ENE3;
				break;
			case 4:x[y[i][1] + 31][y[i][2] + 12] = B_ENE4;
				x[y[i][1] + 31][y[i][2] + 18] = B_ENE4;
				break;
			}
		}
	}
}
//以下部分由茅单文完成
int me_bumove(char x[300][300], int y[NUM][4]);
int ene_bumove(char x[300][300], int y[NUM][4]);
static int fdig(int y, int indi);
static int fsmallcyc(int x, int y);
static int random();
int me_bumove(char x[300][300], int y[NUM][4])
{
	int i, j, marker, t, m, cnt = 0;
	for (i = 0; i < 300; i++)
		for (j = 0; j < 300; j++)
			if (x[i][j] == B_ME)
			{
				x[i][j] = 0;
				if (i < 3)
					continue;
				marker = i - 3;
				x[marker][j] = B_ME;
				for (t = i; t > marker; t--) {
					if (x[t][j] > 32 && x[t][j] <= 38)
					{
						y[x[t][j] - 33][0] = 0;
						x[t][j] = 0;
						x[marker][j] = 0;
						cnt++;
					}
				}
			}
	return cnt;
}
int ene_bumove(char x[300][300], int y[NUM][4])
{
	int i, j, m, n;
	for (i = 0; i < 300; i++)
		for (j = 0; j < 300; j++)
		{
			if (x[i][j] == B_ENE1)
			{
				int marker1 = j % 5, marker2 = i % 8, marker3;
				m = i + BUSPEED_ENE;
				x[i][j] = 0;
				switch (marker1) {	//求出y坐标，子弹的轨迹是曲折的，周期大
				case 0: n = j + 2;
					marker3 = 2;
					break;
				case 1:
					switch (marker2) {
					case 0:
					case 1:
					case 2:
					case 3:
					case 4:
					case 5:
						n = j - 2;
						marker3 = -2;
						break;
					case 6:
					case 7:
						n = j + 2;
						marker3 = 2;
						break;
					}
					break;
				case 2:
					switch (marker2) {
					case 0:
						n = j + 2;
						marker3 = 2;
						break;
					case 1:
					case 2:
					case 3:
					case 4:
					case 5:
					case 6:
					case 7:
						n = j - 2;
						marker3 = -2;
						break;
					}
					break;
				case 3:
					switch (marker2) {
					case 0:
					case 1:
						n = j + 2;
						marker3 = 2;
						break;
					case 2:
					case 3:
					case 4:
					case 5:
					case 6:
					case 7:
						n = j - 2;
						marker3 = -2;
						break;
					}
					break;
				case 4: n = j - 2;
					marker3 = -2;
					break;
				}
				if (m > 0 && m < 300 && n >= 1 && n < 299) {//移动子弹
					switch (marker3) {
					case -2:
						if (x[m][n] == ME || x[m - 1][n + 1] == ME)	
						{
							return 0;
						}
						if (x[m][n] == B_ME) { x[m][n] = 0; break; }
						if (x[m - 1][n + 1] == B_ME) { x[m][n] = 0; x[m - 1][n + 1] = 0; break; }
						x[m][n] = B_ENE11;
						break;
					case 2:
						if (x[m][n] == ME || x[m - 1][n - 1] == ME)	
						{
							return 0;
						}
						if (x[m][n] == B_ME) { x[m][n] = 0; break; }
						if (x[m - 1][n - 1] == B_ME) { x[m][n] = 0; x[m - 1][n - 1] = 0; break; }
						x[m][n] = B_ENE11;
						break;
					}
				}
				continue;
			}
			if (x[i][j] == B_ENE2 )
			{
				int t = random() % 30 - 15;
				int s = 1;
				m = i + 2;
				n = fdig(j, t);//求y方向的移动，子弹在y方向的移动方向是随机的
				x[i][j] = 0;
				if (n < 0 || n >= 300)//当n超出了边界时，则反方向移动
					n = fdig(j, -t);
				if (m > 0 && m < 300 && n>2 && n < 298) {//移动子弹
					switch (t)
					{
					case -1:
						if (x[m][n] == ME || x[m - 1][n + 1] == ME || x[m - 1][n + 2] == ME)
							return 0;
						if (x[m][n] == B_ME) {
							x[m][n] = 0; s = 0;
							break;
						}
						if (x[m - 1][n + 1] == B_ME) {
							x[m - 1][n + 1] = 0;
							x[m][n] = 0; s = 0;
							break;
						}
						if (x[m - 1][n + 2] == B_ME) {
							x[m - 1][n + 2] = 0;
							x[m][n] = 0; s = 0;
							break;
						}
					case 0:
						if (x[m][n] == ME || x[m - 1][n] == ME)
							return 0;
						if (x[m][n] == B_ME) {
							x[m][n] = 0; s = 0;
							break;
						}
						if (x[m - 1][n] == B_ME) {
							x[m - 1][n] = 0;
							x[m][n] = 0; s = 0;
							break;
						}
					case 1:
						if (x[m][n] == ME || x[m - 1][n - 1] == ME || x[m - 1][n - 2] == ME)
							return 0;
						if (x[m][n] == B_ME) {
							x[m][n] = 0; s = 0;
							break;
						}
						if (x[m - 1][n - 1] == B_ME) {
							x[m - 1][n - 1] = 0;
							x[m][n] = 0; s = 0;
							break;
						}
						if (x[m - 1][n - 2] == B_ME) {
							x[m - 1][n - 2] = 0;
							x[m][n] = 0; s = 0;
							break;
						}
					}
					if (s)
						x[m][n] = B_ENE21;
				}
				continue;
			}
			if (x[i][j] == B_ENE3)
			{
				int s = 1;
				m = i + 1;
				n = fsmallcyc(i, j);//子弹的轨迹是曲折的，周期小
				x[i][j] = 0;
				if (m < 300 && n >= 0 && n < 300) {
					if (x[m][n] == ME)
					{
						return 0;
					}
					if (x[m][n] == B_ME)
						x[m][n] = 0, s = 0;
					if (s)
						x[m][n] = B_ENE31;
					continue;
				}
			}
			if (x[i][j] == B_ENE4)
			{
				int t = random() % 10, mn, s = 1;
				x[i][j] = 0;
				if (i < 295) {
					if (t != 0) {
						m = i + BUSPEED_ENE;//当t不是10的倍数时，子弹平凡地移动
						n = j;
						if (m < 300 && n >= 0 && n < 300) {
							for (mn = i; mn < m; mn++) {
								if (x[mn][n] == ME)
								{
									return 0;
								}
							}
							if (x[m][n] == B_ME) {
								x[m][n] = 0; s = 0;
							}
							else if (s)
								x[m][n] = B_ENE41;
						}
					}
					else {
						int s1, s2, s3;
						s1 = s2 = s3 = 0;
						if (j > 3 && j < 297) {
							if (x[i + 1][j] == ME || x[i + 1][j + 1] == ME || x[i + 1][j - 1] == ME)//当t是10的倍数时，子弹分裂
							{
								return 0;
							}
							if (x[i + 1][j] == B_ME) {
								x[i + 1][j] = 0; s2 = 0;
							}
							if (x[i + 1][j + 3] == B_ME) {
								x[i + 1][j + 3] = 0; s1 = 0;
							}
							if (x[i + 1][j - 3] == B_ME) {
								x[i + 1][j - 3] = 0; s3 = 0;
							}
							if (s1)	x[i + 1][j + 3] = B_ENE31;
							if (s2)	x[i + 1][j] = B_ENE11;
							if (s3)	x[i + 1][j - 3] = B_ENE31;
						}
					}
				}
			}
		}
	for (i = 0; i < 300; i++) {
		for (j = 0; j < 300; j++) {
			switch (x[i][j]) {
			case B_ENE11:x[i][j] = B_ENE1; break;
			case B_ENE21:x[i][j] = B_ENE2; break;
			case B_ENE31:x[i][j] = B_ENE3; break;
			case B_ENE41:x[i][j] = B_ENE4; break;
			}
		}
	}
	return 1;
}
static int fsmallcyc(int x, int y)
{
	int marker1 = y % 3, marker2 = x % 4;
	switch (marker1) {
	case 0:return y + 1;
	case 1:
		switch (marker2) {
		case 0:
		case 1:return y + 1;
		case 2:
		case 3:return y - 1;
		}
	case 2:return y - 1;
	}
}
static int fdig(int y, int indi)
{
	if (indi < 0)
		return y - 3;
	else if (indi > 0)
		return y + 3;
	else
		return y;
}
static int random()
{
	unsigned int seed = static_cast<unsigned int>(GetTickCount());
	srand(seed);
	return rand();
}
//以下部分由杨甲珅完成
IMAGE plane_img,plane_img_small;
void KeyBoardInput(int* mpx, int* mpy, char c[][300])
{
	if (GetAsyncKeyState(VK_UP) || GetAsyncKeyState('W'))
		me_plmove(mpx, mpy, 72);
	if (GetAsyncKeyState(VK_DOWN) || GetAsyncKeyState('S'))
		me_plmove(mpx, mpy, 80);
	if (GetAsyncKeyState(VK_LEFT) || GetAsyncKeyState('A'))
		me_plmove(mpx, mpy, 75);
	if (GetAsyncKeyState(VK_RIGHT) || GetAsyncKeyState('D'))
		me_plmove(mpx, mpy, 77);
}
void drawSTAT(DWORD t,int score)
{
	settextstyle(45, 0, "微软雅黑"); 
	setbkmode(TRANSPARENT);
	settextcolor(BROWN);
	char str1[20],str2[20];
	DWORD t2 = GetTickCount();
	int totalsec = (t2 - t)/1000, min = totalsec / 60, sec = totalsec % 60;
	sprintf_s(str1, "Time: %02d:%02d", min,sec); 
	sprintf_s(str2, "Score:%2d",score);
	outtextxy(600,100,str1); 
	outtextxy(600, 200, str2);
	outtextxy(600, 300, "作者：");
	settextstyle(11, 0, "宋体");
	settextcolor(BLUE);
	outtextxy(600, 350, "地球科学与工程学院 茅单文 231830128");
	outtextxy(600, 370, "安邦书院化生大类 杨甲珅 231850008");
	outtextxy(600, 390, "有训书院数理大类 朱泽磐 231840004");
	settextstyle(20, 0, "微软雅黑");
	outtextxy(600, 410, "WSAD或方向键移动飞机");
	outtextxy(600, 440, "被敌方子弹射到游戏结束！");
}
void drawbackground(void)
{
	setfillcolor(RGB(128, 128, 128));
	setlinecolor(RGB(128, 128, 128));
	fillrectangle(600, 0, 800, 600);
}
void drawGame(char a[][300])
{
		putimage(2 * myplaney, 2 * myplanex, &plane_img_small);
	for(int i=0;i<300;++i)
		for (int j = 0; j < 300; ++j)
			switch (a[i][j])
			{
			case B_ME:
				setfillcolor(WHITE);
				setlinecolor(WHITE);
				fillcircle(2 * j+ 1, 2 * i + 1, 2);
				break;
			case	B_ENE1:
			case	B_ENE2:
			case	B_ENE3:
			case	B_ENE4:
				setfillcolor(GREEN);
				setlinecolor(GREEN);
				fillcircle(2 * j + 1, 2 * i + 1, 2);
				break;
			case 33:
			case 34:
			case 35:
			case 36:
			case 37:
				setfillcolor(RED);
				setlinecolor(RED);
				fillrectangle(2 * j, 2 * i, 2 * j + 2, 2 * i + 2);
				break;
			}
	
}
void drawMenu(int* p,bool*i)
{
	setlinecolor(BLACK);
	putimage(100, 76,&plane_img);
	rectangle(600, 200, 800, 300);
	rectangle(600, 300, 800, 400);
	rectangle(600, 400, 800, 500);
	settextstyle(48, 0, "微软雅黑");
	setbkmode(TRANSPARENT);
	settextcolor(BLACK);
	setfillcolor(YELLOW);
	fillrectangle(600, 100+100 * (*p), 800, 200 + 100 * (*p));
	outtextxy(615, 200, "Easy");
	outtextxy(615, 300, "Normal");
	outtextxy(615, 400, "Hard");
	outtextxy(615, 50, "飞机大战");
	settextstyle(24, 0, "微软雅黑");
	outtextxy(600, 100, "By 杨甲珅 朱泽磐 茅单文");
	settextstyle(20, 0, "微软雅黑");
	outtextxy(615, 500, "WS或上下方向键选择");
	outtextxy(615, 530, "回车键确定");
	FlushBatchDraw();
	if (GetAsyncKeyState(VK_UP) || GetAsyncKeyState('W'))
		if (*p > 1)
			(*p)--;
	if (GetAsyncKeyState(VK_DOWN) || GetAsyncKeyState('S'))
		if (*p < 3)
			(*p)++;
	if(GetAsyncKeyState(VK_RETURN))
		*i = false;
}
void drawName(void);
void importIMG(void)
{
	loadimage(&plane_img, "./image/image (1).png");
	loadimage(&plane_img_small, "./image/image_small.png");
}
int main(void)
{
	int x=1;
	int* mpx;
	int* mpy;
	mpx = &myplanex;
	mpy = &myplaney;
	bool i = true;
	char a[300][300] = {0};
	char move;
	int y[NUM][4] = { 0 };
	initgraph(800, 600);
	BeginBatchDraw();
	importIMG();
	while (i)
	{
		drawbackground();
		drawMenu(&x,&i);
		cleardevice();
		Sleep(100);
	}
	DWORD t = GetTickCount();
	if (x == 3)
		x = 4;
	nandu = x;
	i = true;
	int score = 0;
	while(i)
	{

		drawbackground();
		drawSTAT(t,score);
		KeyBoardInput(mpy, mpx, a);
		me_bushoot(mpy, mpx, a);
		DWORD t1 = GetTickCount();
		if ((t1 - t) % 100 == 0)
		{
			ene_gen(y);
			ene_move(y, a);
		}
		score+=me_bumove(a, y);
		ene_dr(y, a);
		if((t1-t)%500==0)
			ene_bushoot(y, a);
		i=ene_bumove(a, y);
		drawGame(a);
		FlushBatchDraw();
		me_pldr(mpy, mpx, a);
		cleardevice();
		Sleep(30);
	}
	EndBatchDraw();
	char str[50];
	DWORD t2 = GetTickCount();
	int totalsec = (t2 - t) / 1000, min = totalsec / 60, sec = totalsec % 60;
	sprintf_s(str,"游戏结束!您的分数是:%2d,您坚持了%02d分%02d秒", score,min,sec);
	MessageBox(NULL, str, "游戏分数", MB_OK);
}