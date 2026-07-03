clear; close all; clc;

tt0=0;tt1=1;dt=1e-5;
t0=tt0:dt:tt1-dt;

x=sin(20*pi*t0)+2*sin(40*pi*t0)+3*sin(80*pi*t0);

%% 傅里叶变换
X=fft(x);

N=length(X);
fs=1/dt;
df=fs/(N-1); % 频率分辨率
f=-N/2:N/2-1; % 频率区间

X_shift=fftshift(X);
Amp=abs(X_shift)/N; % MATLAB的fft()结果恢复
Phase=angle(X_shift);

% 可视化
% fig1: x(t), X_mag, X_ang
figure('Name','波形图和频谱图');

subplot(3,1,1);
plot(t0,x);xlabel('t');ylabel('x');grid on;
title('x=sin(20*pi*t)+2*sin(40*pi*t)+3*sin(80*pi*t)');

subplot(3,1,2);
stem(f,Amp,'MarkerSize',2);xlabel('f');ylabel('|X|');grid on;
title('|X|=|fft(x)|');
xlim([-50 50]);

subplot(3,1,3);
stem(f,Phase,'MarkerSize',2);xlabel('f');ylabel('phi');grid on;
title('phi=angle(fft(x))');
xlim([-50 50]);

%% 抽样，恢复
f1=10;f2=40;f3=100;f4=200;
[t1,x1,h1,x_f1]=my_sample_signal(tt0,tt1,t0,x,f1,40);
[t2,x2,h2,x_f2]=my_sample_signal(tt0,tt1,t0,x,f2,40);
[t3,x3,h3,x_f3]=my_sample_signal(tt0,tt1,t0,x,f3,40);
[t4,x4,h4,x_f4]=my_sample_signal(tt0,tt1,t0,x,f4,40);

function[t,x_s,h_s,x_filter]=my_sample_signal(tt0,tt1,t0,x0,fs,fc)
% fs:采样频率; fc:截止频率
% t:时间轴; x_s:采样信号; h_s:低通滤波器（时域）; x_filter:重建信号
    dt=1/fs;
    t_offset=dt/19;
    t=tt0-t_offset:dt:tt1-dt;
    x_s=sin(20*pi*t)+2*sin(40*pi*t)+3*sin(80*pi*t); % 抽样信号
    X_s=fft(x_s); % 抽样信号频谱
    N=length(X_s);

    % 抽样信号幅度频谱
    f_sym =-N/2:N/2-1; % 关于x=0对称的频率轴
    X_s_shift=fftshift(X_s); % 平移至关于x=0对称
    Amp_X_s=abs(X_s_shift)/N;

    % 频域低通滤波器
    f=(0:N-1)*(fs/N);
    f(f >= fs/2) = f(f >= fs/2) - fs;
    H=double(abs(f)<=fc);
    % 时域低通滤波器
    h_s=2*fc*sinc(2*fc*(t0-(tt0+tt1)/2)); % sinc(x)=sin(pi*x)/(pi*x)

    X_s_filter=X_s.*H; % 重建信号
    x_filter=ifft(X_s_filter);

    figure;
    subplot(5,1,1);
    plot(t0,x0);xlabel('t');ylabel('x(t)');grid on;
    title('x=sin(20*pi*t)+2*sin(40*pi*t)+3*sin(80*pi*t)');

    subplot(5,1,2);
    stem(t,x_s,'Markersize',1);xlabel('t');ylabel('x[t]');grid on;
    title(sprintf('抽样信号 采样频率%d Hz',fs));

    subplot(5,1,3);
    stem(f_sym,Amp_X_s,'Markersize',2);xlabel('f');ylabel('|X|');grid on;
    title(sprintf('抽样信号 频域，偏移%d s',t_offset))

    subplot(5,1,4);
    plot(t0,h_s);xlabel('t');ylabel('h(t)');grid on;
    title(sprintf('低通滤波器 截止频率%d Hz',fc))

    subplot(5,1,5);
    plot(t,x_filter);xlabel('t');ylabel('x');grid on;
    title('重建信号')
end

