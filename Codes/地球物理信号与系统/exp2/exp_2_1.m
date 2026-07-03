clear all;
t0=0;t1=10;dt=0.01;
t=t0:dt:t1;
t_l=t0:10*dt:10*t1; %更长的时间序列，更稀疏的采样
t_l_dt1=t0:dt:10*t1; %更长的时间序列，采样密度不变

% a:output coeffi,b:input coeffi
a=[1 3 2];
b=2;

% 经典法求解结果
r_step0=exp(-2*t)-2*exp(-t)+1;
r_h0=-2*exp(-2*t)+2*exp(-t);

% LTI系统
sys=tf(b,a);
% 冲激响应
r_h=impulse(sys,t);
% 阶跃响应
r_step1=step(sys,t);
% 零状态-阶跃响应
u=ones(size(t));
r_step2=lsim(sys,u,t);
% 零状态响应
E=sin(t)+sin(20*t);
R=lsim(sys,E,t);
% 测试不同的采样密度和长度
E_l=sin(t_l)+sin(20*t_l);
R_l=lsim(sys,E_l,t_l);
% 测试不同的长度
E_l_dt1=sin(t_l_dt1)+sin(20*t_l_dt1);
R_l_dt1=lsim(sys,E_l_dt1,t_l_dt1);
% 测试不同的输入频率
E_feq1=sin(1*t);
R_feq1=lsim(sys,E_feq1,t);
E_feq5=sin(5*t);
R_feq5=lsim(sys,E_feq5,t);
E_feq10=sin(10*t);
R_feq10=lsim(sys,E_feq10,t);
E_feq15=sin(15*t);
R_feq15=lsim(sys,E_feq15,t);
E_feq20=sin(20*t);
R_feq20=lsim(sys,E_feq20,t);
% 测试部分输入的响应
f=@(x) (x<0.05).*sin(20*pi*x)+(x>=0.05).*0;
f2=@(x) (x<0.95).*sin(20*pi*x)+(x>=0.95).*0;
f3=@(x) (x<6.95).*sin(20*pi*x)+(x>=6.95).*0;
t_cut=t0:dt:10;
E_tcut1=f(t_cut);
R_tcut1=lsim(sys,E_tcut1,t_cut);
E_tcut2=sin(20*pi*t_cut);
R_tcut2=lsim(sys,E_tcut2,t_cut);
E_tcut3=f2(t_cut);
R_tcut3=lsim(sys,E_tcut3,t_cut);
E_tcut4=f3(t_cut);
R_tcut4=lsim(sys,E_tcut4,t_cut);
%% 可视化
% fig1
figure('Name','系统响应函数','NumberTitle','off');

subplot(3,2,1);
plot(t,r_step0,'b');xlabel('t');ylabel('g(t)');grid on;
title('经典法：单位阶跃响应g(t)');

subplot(3,2,2);
plot(t,r_h0,'b');xlabel('t');ylabel('h(t)');grid on;
title('经典法：单位冲激响应h(t)');

subplot(3,2,3)
plot(t,r_step1,'r');xlabel('t');ylabel('g(t)');grid on;
title('step()：单位阶跃响应g(t)');

subplot(3,2,4)
plot(t,r_h,'r');xlabel('t');ylabel('h(t)');grid on;
title('impulse()：单位冲激响应h(t)');

subplot(3,2,5)
plot(t,r_step2,'r');xlabel('t');ylabel('g(t)');grid on;
title('lsim()：单位阶跃响应g(t)');

% fig2
figure('Name','系统响应函数','NumberTitle','off');

subplot(2,1,1)
plot(t,E);xlabel('t');ylabel('E(t)');grid on;
title('系统输入信号E(t)');

subplot(2,1,2)
plot(t,R);xlabel('t');ylabel('R(t)');grid on;
title('lsim()：零状态响应R(t)');

%fig3
figure('Name','系统响应函数','NumberTitle','off');

subplot(2,1,1)
plot(t_l,E_l);xlabel('t');ylabel('E(t)');grid on;
title('系统输入信号E(t)');

subplot(2,1,2)
plot(t_l,R_l);xlabel('t');ylabel('R(t)');grid on;
title('lsim()：零状态响应R(t)');

% fig4
figure('Name','系统响应函数','NumberTitle','off');

subplot(2,1,1)
plot(t_l_dt1,E_l_dt1);xlabel('t');ylabel('E(t)');grid on;
title('系统输入信号E(t)');

subplot(2,1,2)
plot(t_l_dt1,R_l_dt1);xlabel('t');ylabel('R(t)');grid on;
title('lsim()：零状态响应R(t)');

% fig5
figure('Name','系统响应函数','NumberTitle','off');

subplot(2,1,1)
plot(t,E_feq1);xlabel('t');ylabel('E(t)');grid on;
title('系统输入信号E(t)=sin(t)');

subplot(2,1,2)
plot(t,R_feq1);xlabel('t');ylabel('R(t)');grid on;
title('lsim()：零状态响应R(t)');

% fig6
figure('Name','系统响应函数','NumberTitle','off');

subplot(2,1,1)
plot(t,E_feq5);xlabel('t');ylabel('E(t)');grid on;
title('系统输入信号E(t)=sin(5t)');

subplot(2,1,2)
plot(t,R_feq5);xlabel('t');ylabel('R(t)');grid on;
title('lsim()：零状态响应R(t)');

% fig7
figure('Name','系统响应函数','NumberTitle','off');

subplot(2,1,1)
plot(t,E_feq10);xlabel('t');ylabel('E(t)');grid on;
title('系统输入信号E(t)=sin(10t)');

subplot(2,1,2)
plot(t,R_feq10);xlabel('t');ylabel('R(t)');grid on;
title('lsim()：零状态响应R(t)');

% fig8
figure('Name','系统响应函数','NumberTitle','off');

subplot(2,1,1)
plot(t,E_feq15);xlabel('t');ylabel('E(t)');grid on;
title('系统输入信号E(t)=sin(15t)');

subplot(2,1,2)
plot(t,R_feq15);xlabel('t');ylabel('R(t)');grid on;
title('lsim()：零状态响应R(t)');

% fig9
figure('Name','系统响应函数','NumberTitle','off');

subplot(2,1,1)
plot(t,E_feq20);xlabel('t');ylabel('E(t)');grid on;
title('系统输入信号E(t)=sin(15t)');

subplot(2,1,2)
plot(t,R_feq20);xlabel('t');ylabel('R(t)');grid on;
title('lsim()：零状态响应R(t)');

% fig10
figure('Name','系统响应函数','NumberTitle','off');

subplot(2,1,1)
plot(t_cut,E_tcut1);xlabel('t');ylabel('E(t)');grid on;
title('系统输入信号E(t)=sin(10pi*t)');

subplot(2,1,2)
plot(t_cut,R_tcut1);xlabel('t');ylabel('R(t)');grid on;
title('lsim()：零状态响应R(t)');

% fig11
figure('Name','系统响应函数','NumberTitle','off');

subplot(2,1,1)
plot(t_cut,E_tcut2);xlabel('t');ylabel('E(t)');grid on;
title('系统输入信号E(t)=sin(10pi*t)');

subplot(2,1,2)
plot(t_cut,R_tcut2);xlabel('t');ylabel('R(t)');grid on;
title('lsim()：零状态响应R(t)');

% fig12
figure('Name','系统响应函数','NumberTitle','off');

subplot(2,1,1)
plot(t_cut,E_tcut3);xlabel('t');ylabel('E(t)');grid on;
title('系统输入信号E(t)=sin(10pi*t)');

subplot(2,1,2)
plot(t_cut,R_tcut3);xlabel('t');ylabel('R(t)');grid on;
title('lsim()：零状态响应R(t)');

% fig13
figure('Name','系统响应函数','NumberTitle','off');

subplot(2,1,1)
plot(t_cut,E_tcut4);xlabel('t');ylabel('E(t)');grid on;
title('系统输入信号E(t)=sin(10pi*t)');

subplot(2,1,2)
plot(t_cut,R_tcut4);xlabel('t');ylabel('R(t)');grid on;
title('lsim()：零状态响应R(t)');