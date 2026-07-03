clear; close all; clc;

t0=0;t1=2;dt=1/64;t=t0:dt:t1;

square=(t<1);

makeDFT=@(N)exp(-1i*2*pi/N*((0:N-1).'*(0:N-1))); % 矩阵外积，返回N*N的矩阵

F128=makeDFT(128);
F256=makeDFT(256);
F1024=makeDFT(1024);

X128=my_DFT(square,F128,128);
fprintf('FFT128');
tic;
X128_fft=fft(square,128);
toc;

X256=my_DFT(square,F256,256);
fprintf('FFT256');
tic;
X256_fft=fft(square,256);
toc;

X1024=my_DFT(square,F1024,1024);
fprintf('FFT1024');
tic;
X1024_fft=fft(square,1024);
toc;

function[X]=my_DFT(signal,matrix,N)
    fprintf('DFT%g',N);
    tic;
    if length(signal)<N
        signal_pad=[signal, zeros(1,N-length(signal))]; % 补0
    elseif length(signal)>N
        signal_pad=signal(1:N);
    else
        signal_pad=signal;
    end
    X=matrix*signal_pad(:);
    toc;
end