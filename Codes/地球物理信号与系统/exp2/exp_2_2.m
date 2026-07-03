clear all
N=100; k=0:N;
a=[1.0 -0.0494 0.334 -0.0045];
b=[0.16 0.48 0.48 0.16];
% 单位冲激响应
r_h=impz(b,a,k);
% 单位阶跃响应
u=ones(size(k)); % 单位阶跃函数
r_step1=filter(b,a,u);
r_step2=conv(r_h,u,"full");

% 输入cos()
e1=cos(5*pi*k/6);
e2=cos(pi*k/6);
e3=cos(pi*k/6)+cos(5*pi*k/6);
r1=conv(r_h,e1,"full");
r2=conv(r_h,e2,"full");
r3=conv(r_h,e3,"full");

%% 可视化
% fig1
figure('Name','离散时间系统求解','NumberTitle','off');

subplot(3,1,1);
stem(k,r_h,'filled','MarkerSize',3);
title('单位脉冲响应h[n]: impz(b,a,n)');
xlabel('n');ylabel('h[n]');

subplot(3,1,2);
stem(k,r_step1,'filled','MarkerSize',3);
title('单位阶跃响应g[n]: filter(b,a,n)');
xlabel('n');ylabel('g[n]');

subplot(3,1,3);
stem(k,r_step2(1:N+1),'filled','MarkerSize',3);
title('单位阶跃响应g[n]: conv(h[n],u[n])');
xlabel('n');ylabel('g[n]');

% 输入cos()
% fig2
figure('Name','离散时间系统求解','NumberTitle','off');

subplot(2,1,1);
stem(k,e1,'filled','MarkerSize',3);
title('激励函数E[n]: cos(5*pi*k/6)');
xlabel('n');ylabel('E[n]');

subplot(2,1,2);
stem(k,r1(1:N+1),'filled','MarkerSize',3);
title('零状态响应R[n]: conv(h[n],E[n])');
xlabel('n');ylabel('R[n]');

% fig3
figure('Name','离散时间系统求解','NumberTitle','off');

subplot(2,1,1);
stem(k,e2,'filled','MarkerSize',3);
title('激励函数E[n]: cos(pi*k/6)');
xlabel('n');ylabel('E[n]');

subplot(2,1,2);
stem(k,r2(1:N+1),'filled','MarkerSize',3);
title('零状态响应R[n]: conv(h[n],E[n])');
xlabel('n');ylabel('R[n]');

% fig4
figure('Name','离散时间系统求解','NumberTitle','off');

subplot(2,1,1);
stem(k,e3,'filled','MarkerSize',3);
title('激励函数E[n]: cos(pi*k/6)+cos(5*pi*k/6)');
xlabel('n');ylabel('E[n]');

subplot(2,1,2);
stem(k,r3(1:N+1),'filled','MarkerSize',3);
title('零状态响应R[n]: conv(h[n],E[n])');
xlabel('n');ylabel('R[n]');