clear all
N=100; k=0:N;
a=[1 -1 0.9];b=[1];

% 单位脉冲响应
r_h=impz(b,a,k);

% 单位阶跃响应
u = ones(size(k)); % 单位阶跃函数
R_filter=filter(b,a,u); 
conv_same=conv(r_h,u,"same"); 
conv_full=conv(r_h,u,"full"); 

% 输入信号
func=cos(2*pi*k);
func_big=4.*func;
func_lazy=cos(2*pi*(k-10));

conv_1=conv(r_h,func,'full');
conv_big=conv(r_h,func_big,'full');
conv_lazy=conv(r_h,func_lazy,'full');

%% 可视化
% fig1
figure('Name','LTI性质','NumberTitle','off');

subplot(4,1,1);
stem(k,r_h,'filled','MarkerSize',3);
title('单位脉冲响应h[n]：impz(b,a,n)');
xlabel('n');  ylabel('h[n]'); 
subplot(4,1,2);
stem(k,R_filter,'filled','MarkerSize',3);
title('单位阶跃响应g[n]：R[n]=filter(b,a,u(t))' );
xlabel('n');  ylabel('g[n]');
subplot(4,1,3);
stem(k,conv_same(1:N+1),'filled','MarkerSize',3);
title('单位阶跃响应g[n]=conv(h[n],u[n])' );
xlabel('n');  ylabel('g[n]');
subplot(4,1,4);
stem(k,conv_full(1:N+1),'filled','MarkerSize',3);
title('单位阶跃响应g[n]=conv(h[n],u[n])' );
xlabel('n');  ylabel('g[n]');

% fig2
figure('Name','LTI性质','NumberTitle','off');

subplot(3,1,1);
stem(k,conv_1(1:N+1),'filled','MarkerSize',3);
title('R[n]=conv(h[n],cos(2*pi*k))' );
xlabel('n');  ylabel('R[n]');
subplot(3,1,2);
stem(k,conv_big(1:N+1),'filled','MarkerSize',3);
title('R[n]=conv(h[n],4cos(2*pi*k))' );
xlabel('n');  ylabel('R[n]');
subplot(3,1,3);
stem(k,conv_lazy(1:N+1),'filled','MarkerSize',3);
title('R[n]=conv(h[n],cos(2*pi*(k-10)))' );
xlabel('n');  ylabel('R[n]');