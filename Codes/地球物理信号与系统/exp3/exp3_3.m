clear; close all; clc;
figure
omega=logspace(-5,5,100); % 1e-5~1e5，对数坐标均匀采样

% h=1,改变omega0
[Amp1_01,Phase1_01]=Func(1,0.1,omega);
[Amp1_1,Phase1_1]=Func(1,1,omega);
[Amp1_10,Phase1_10]=Func(1,10,omega);

% omega0=1,改变h
[Amp01_1,Phase01_1]=Func(0.1,1,omega);
[Amp05_1,Phase05_1]=Func(0.5,1,omega);
[Amp5_1,Phase5_1]=Func(5,1,omega);
[Amp10_1,Phase10_1]=Func(10,1,omega);

%% 可视化
% fig1_1, h=1
figure('Name','h=1');
semilogx(omega,Amp1_01,'LineWidth',1.5);hold on; % 对数坐标绘图
semilogx(omega,Amp1_1,'LineWidth',1.5);hold on;
semilogx(omega,Amp1_10,'LineWidth',1.5);
xlabel('\omega');ylabel('Amp');grid on;
legend('\omega_0=0.1', '\omega_0=1', '\omega_0=10', 'Location', 'best');
title('h=1')

figure('Name','h=1');
semilogx(omega,Phase1_01,'LineWidth',1.5);hold on;
semilogx(omega,Phase1_1,'LineWidth',1.5);hold on;
semilogx(omega,Phase1_10,'LineWidth',1.5);
xlabel('\omega');ylabel('Phase');grid on;
legend('\omega_0=0.1', '\omega_0=1', '\omega_0=10', 'Location', 'best');
title('h=1')

% fig2_1
figure('Name','\omega_0=1');
semilogx(omega,Amp01_1,'LineWidth',1.5);hold on; % 对数坐标绘图
semilogx(omega,Amp05_1,'LineWidth',1.5);hold on;
semilogx(omega,Amp1_1,'LineWidth',1.5);hold on;
semilogx(omega,Amp5_1,'LineWidth',1.5);hold on;
semilogx(omega,Amp10_1,'LineWidth',1.5);
xlabel('\omega');ylabel('Amp');grid on;
legend('h=0.1', 'h=0.5', 'h=1', 'h=5','h=10', 'Location', 'best');
title('\omega_0=1')

figure('Name','\omega_0=1');
semilogx(omega,Phase01_1,'LineWidth',1.5);hold on;
semilogx(omega,Phase05_1,'LineWidth',1.5);hold on;
semilogx(omega,Phase1_1,'LineWidth',1.5);hold on;
semilogx(omega,Phase5_1,'LineWidth',1.5);hold on;
semilogx(omega,Phase10_1,'LineWidth',1.5);
xlabel('\omega');ylabel('Phase');grid on;
legend('h=0.1', 'h=0.5', 'h=1', 'h=5','h=10', 'Location', 'best');
title('\omega_0=1')



function[Amp,Phase]=Func(h,omega0,omega)
    H_omega=-omega.^2./(-omega.^2+2*1i*h*omega0*omega+omega0^2);
    Amp=abs(H_omega);
    Phase=angle(H_omega);
end
