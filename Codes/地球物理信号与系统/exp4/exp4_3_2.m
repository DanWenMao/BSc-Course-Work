clear; clc; close all

%% signal
N1 = 80;                 
N2 = 40;                 

x = zeros(1, N1);
x(20:50) = 1;          

h = zeros(1, N2);
h(10:25) = 1;            

%% conv
y_linear = conv(x, h);

%% fft
Nfft1 = length(x) + length(h) - 1;
Nfft2 = length(x);
Nfft3 = length(h);
Nfft4 = 2 * Nfft1;
Y_circ1 = ifft( fft(x, Nfft1) .* fft(h, Nfft1) );
Y_circ2 = ifft( fft(x, Nfft2) .* fft(h, Nfft2) );
Y_circ3 = ifft( fft(x, Nfft3) .* fft(h, Nfft3) );
Y_circ4 = ifft( fft(x, Nfft4) .* fft(h, Nfft4) );

my_plot(x,h,y_linear,Y_circ1,N1,N2,Nfft1);
my_plot(x,h,y_linear,Y_circ2,N1,N2,Nfft2);
my_plot(x,h,y_linear,Y_circ3,N1,N2,Nfft3);
my_plot(x,h,y_linear,Y_circ4,N1,N2,Nfft4);

%% plot
function[]=my_plot(x,h,y_linear,Y_circ,N1,N2,Nfft)

figure
subplot(4,1,1)
stem(x, 'k', 'MarkerSize',2)
title(sprintf('矩形信号 x(n)，信号长度 %g',N1))
ylim([-0.2 1.2])

subplot(4,1,2)
stem(h, 'k', 'MarkerSize', 2)
title(sprintf('矩形信号 h(n)，信号长度 %g',N2))
ylim([-0.2 1.2])

subplot(4,1,3)
stem(y_linear, 'r', 'MarkerSize', 2)
title('线性卷积 y\_linear = conv(x,h)')

subplot(4,1,4)
stem(real(Y_circ), 'b', 'MarkerSize', 2)
title(sprintf('圆周卷积 y\\_circ = ifft(fft(x).*fft(h))，信号长度 %g',Nfft))

end

