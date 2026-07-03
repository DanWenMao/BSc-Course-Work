clear; close all; clc;

N=32; %窗函数长度
f=-0.5:0.001:0.5; %频域区间

W=@(f) (exp(-1i*2*pi*f*(N-1)/2)).*sin(N*pi*f)./sin(pi*f);

% 矩形窗
rect=W(f); rect(f==0)=N;

% 三角窗
tri=rect.^2;

% Hann窗
delta=1/(N-1);
hann=0.5*rect-0.25*(W(f-delta)+W(f+delta));

% Hamming窗
hamming=0.54*rect-0.23*(W(f-delta)+W(f+delta));

% Blackman窗
blackman=0.42*rect-0.25*(W(f-delta)+W(f+delta))+0.04*(W(f-2*delta)+W(f+2*delta));

my_plot_windows(rect,f,'Rectangular');
my_plot_windows(tri,f,'Triangular');
my_plot_windows(hann,f,'Hann');
my_plot_windows(hamming,f,'Hamming');
my_plot_windows(blackman,f,'Blackman');

function[]=my_plot_windows(window,f,wname)
    figure;
    semilogy(f,abs(window));xlabel('f');ylabel('|W[f]|');
    title(sprintf('%s Window Amplitude',wname));grid on;
end