clear; close all; clc;

t0=0;t1=2;
dt_16=1/16;t_16=t0:dt_16:t1;
dt_64=1/64;t_64=t0:dt_64:t1;
dt_256=1/256;t_256=t0:dt_256:t1;

square_16=(t_16<1);
square_64=(t_64<1);
square_256=(t_256<1);

% 构建DFT矩阵 (F_N)k,n=e^{-i2pi (k-1)(n-1)/N}
makeDFT=@(N)exp(-1i*2*pi/N*((0:N-1).'*(0:N-1))); % 矩阵外积，返回N*N的矩阵

F64=makeDFT(64);
F128=makeDFT(128);
F256=makeDFT(256);

% fs=16Hz
X_16_N64=my_DFT(square_16,F64,64);
X_16_N128=my_DFT(square_16,F128,128);
X_16_N256=my_DFT(square_16,F256,256);
my_plot_DFT(square_16,t_16,X_16_N64,X_16_N128,X_16_N256,16);

X_16_N64_fft=fft(square_16,64);
X_16_N128_fft=fft(square_16,128);
X_16_N256_fft=fft(square_16,256);
my_plot_FFT(square_16,t_16,X_16_N64_fft,X_16_N128_fft,X_16_N256_fft,16);

% fs=64Hz
X_64_N64=my_DFT(square_64,F64,64);
X_64_N128=my_DFT(square_64,F128,128);
X_64_N256=my_DFT(square_64,F256,256);
my_plot_DFT(square_64,t_64,X_64_N64,X_64_N128,X_64_N256,64);

X_64_N64_fft=fft(square_64,64);
X_64_N128_fft=fft(square_64,128);
X_64_N256_fft=fft(square_64,256);
my_plot_FFT(square_64,t_64,X_64_N64_fft,X_64_N128_fft,X_64_N256_fft,64);

% fs=256Hz
X_256_N64=my_DFT(square_256,F64,64);
X_256_N128=my_DFT(square_256,F128,128);
X_256_N256=my_DFT(square_256,F256,256);
my_plot_DFT(square_256,t_256,X_256_N64,X_256_N128,X_256_N256,256);

X_256_N64_fft=fft(square_256,64);
X_256_N128_fft=fft(square_256,128);
X_256_N256_fft=fft(square_256,256);
my_plot_FFT(square_256,t_256,X_256_N64_fft,X_256_N128_fft,X_256_N256_fft,256);

function[X]=my_DFT(signal,matrix,N)
    if length(signal)<N
        signal_pad=[signal, zeros(1,N-length(signal))]; % 补0
    elseif length(signal)>N
        signal_pad=signal(1:N); % 截断（试试看效果）
    else
        signal_pad=signal;
    end
    X=matrix*signal_pad(:);
end

function[]=my_plot_DFT(square,t,X64,X128,X256,fs)
    figure;
    k64=0:63;k128=0:127;k256=0:255;

    subplot(4,1,1);
    stem(t,square,'MarkerSize',2);xlabel('t');ylabel('x[t]');
    title(sprintf('矩形脉冲信号 fs=%g',fs));

    subplot(4,1,2);
    stem(k64,abs(X64),'MarkerSize',2);xlabel('k');ylabel('|X_64[k]|');
    title(sprintf('DFT64 数字频谱范围[0,2pi]  物理频谱范围[0,%g] Hz  物理频谱间隔%f Hz',fs,fs/64));

    subplot(4,1,3);
    stem(k128,abs(X128),'MarkerSize',2);xlabel('k');ylabel('|X_128[k]|');
    title(sprintf('DFT128 数字频谱范围[0,2pi]  物理频谱范围[0,%g] Hz  物理频谱间隔%f Hz',fs,fs/128));

    subplot(4,1,4);
    stem(k256,abs(X256),'MarkerSize',2);xlabel('k');ylabel('|X_256[k]|');
    title(sprintf('DFT256 数字频谱范围[0,2pi]  物理频谱范围[0,%g] Hz  物理频谱间隔%f Hz',fs,fs/256));
end

function[]=my_plot_FFT(square,t,X64,X128,X256,fs)
    figure;
    k64=0:63;k128=0:127;k256=0:255;

    subplot(4,1,1);
    stem(t,square,'MarkerSize',2);xlabel('t');ylabel('x[t]');
    title(sprintf('矩形脉冲信号 fs=%g',fs));

    subplot(4,1,2);
    stem(k64,abs(X64),'MarkerSize',2);xlabel('k');ylabel('|X_64[k]|');
    title('FFT64');

    subplot(4,1,3);
    stem(k128,abs(X128),'MarkerSize',2);xlabel('k');ylabel('|X_128[k]|');
    title('FFT128');

    subplot(4,1,4);
    stem(k256,abs(X256),'MarkerSize',2);xlabel('k');ylabel('|X_256[k]|');
    title('FFT256');
end