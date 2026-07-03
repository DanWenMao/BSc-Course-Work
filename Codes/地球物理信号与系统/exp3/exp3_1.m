clear; close all; clc;

t0=-5;t1=5;dt=1e-5;
t=t0:dt:t1;

t_x10=10*t0:10*dt:10*t1;
t_x100=100*t0:100*dt:100*t1;

% 周期性矩形脉冲
% CFT幅度谱和相位谱
CFS_SQA_05_1 = my_square(t,0.5,1,1);

%% 改变占空比，周期=1
CFS_SQA_01_1 = my_square(t,0.1,1,1);
% 趋向于Delta函数
CFS_SQA_001_1 = my_square(t,0.01,1,1);

CFS_SQA_09_1 = my_square(t,0.9,1,1);
% 趋向于直流信号
CFS_SQA_099_1 = my_square(t,0.99,1,1);

%% 改变周期，宽度=0.5
CFS_SQA_05_10 = my_square(t_x10,0.5,10,1);
% 趋向于Delta函数
CFS_SQA_05_100 = my_square(t_x100,0.5,100,1);

%% 单脉冲
CFT_SQA_s_05_1 = my_square_single(t,0.5,1);
CFT_SQA_s_05_1 = my_square_single(t_x10,0.5,1);

%% 信号抽样
F=100;f=-F:F;
my_sample(f,10,CFS_SQA_05_1);
my_sample(f,20,CFS_SQA_05_1);
my_sample(f,50,CFS_SQA_05_1);

%% 通用函数
function[CFS_SQA]=my_square(t,tau,T,E)
% SQA:周期性矩形脉冲信号
% t:时间轴;tau:脉冲宽度;T:周期;E:能量

    % 信号生成
    SQA=E*(abs(mod(t+T/2,T)-T/2)<=tau/2);
    
    % 频域区间
    N=100;n=-N:N;
    
    % 傅里叶级数
    CFS_SQA=E*(tau/T).*sinc(n*pi*tau/T);
    Amp=abs(CFS_SQA);
    Phase=angle(CFS_SQA);
    for k = 1:N
        Phase(k)=-Phase(k);
    end

    figure;
    subplot(3,1,1);
    plot(t,SQA);xlabel('t');ylabel('f(t)');grid on;
    title(sprintf('原始信号 \\tau=%g T=%d E=%d',tau,T,E));
    subplot(3,1,2);
    stem(n,Amp,'MarkerSize',2);xlabel('f*T');ylabel('|F(f)|');grid on;
    title('幅度频谱');
    subplot(3,1,3);
    stem(n,Phase/pi,'MarkerSize',2);xlabel('f*T');ylabel('Angle/\pi');grid on;
    title('相位频谱');
end

function[CFT_SQA]=my_square_single(t,tau,E)
% SQA:矩形单脉冲信号
% t:时间轴;tau:脉冲宽度;E:能量
    SQA=E*(abs(t)<=tau/2);

    F=100;df=1e-5;f=-F:df:F;N=length(f);
    CFT_SQA=E*tau.*sinc(f*tau);
    Amp=abs(CFT_SQA);
    Phase=angle(CFT_SQA);
    for k = 1:round(N/2)
        Phase(k)=-Phase(k);
    end

    figure;
    subplot(3,1,1);
    plot(t,SQA);xlabel('t');ylabel('f(t)');grid on;
    title(sprintf('原始信号 \\tau=%g E=%d',tau,E));
    subplot(3,1,2);
    plot(f,Amp,'MarkerSize',2);xlabel('f*T');ylabel('|F(f)|');grid on;
    title('幅度频谱');
    subplot(3,1,3);
    plot(f,Phase/pi,'MarkerSize',2);xlabel('f*T');ylabel('Angle/\pi');grid on;
    title('相位频谱');
end

function[CFS_Sampled]=my_sample(f,fs,CFS)
% f:频率轴;fs:采样频率;CFS:信号的频率谱
    % 可视化delta函数序列
    delta_comb=zeros(size(f));
    
    N=length(f);
    df=f(2)-f(1); % 频率分辨率
    k=round(f/fs);
    idx=abs(f-k*fs)<df/2; % 查找到fs的整数倍
    delta_comb(idx)=2*pi*fs;

    % 时域卷积，频域叠加
    n=round(fs/df); % 叠加间隔
    K=ceil(N/n); % 叠加次数
    CFS_Sampled=zeros(size(f));
    for k = -K:K
        f_shifted=f-k*fs;
        CFS_shifted=interp1(f_shifted,CFS,f,"linear",0);
        CFS_Sampled=CFS_shifted+CFS_Sampled;
    end
    CFS_Sampled=CFS_Sampled*2*pi*fs;

    figure
    subplot(3,1,1);
    stem(f,abs(CFS),'MarkerSize',2);xlabel('f*T');ylabel('|F(f)|');
    title('原始频谱');
    subplot(3,1,2);
    stem(f,delta_comb,'MarkerSize',2);xlabel('f*T');ylabel('Amp');
    title(sprintf('\\delta函数序列 抽样频率=%d Hz',fs));
    subplot(3,1,3);
    stem(f,abs(CFS_Sampled),'MarkerSize',2);xlabel('f*T');ylabel('|F(f)|');
    title(sprintf('抽样频谱 抽样频率=%d Hz',fs));
end