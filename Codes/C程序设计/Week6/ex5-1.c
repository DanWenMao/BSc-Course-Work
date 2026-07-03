#include<stdio.h>
#include<math.h>
int main()
{
	double x, eps=1e-8,t,m,s;
	int n, sign;
	scanf_s("%lf", &x);
	s = x;
	t = x;
	n = 2;
	sign = -1;
	do {
		//sign = -sign;
		m = (2 * n - 1) * (2 * n - 2);
		t = t*sign* x * x / m;
		s = s + t;
		n = n + 1;
	} while (fabs(t) > eps);
	printf("%.1lf", s);
	
	return 0;
}
