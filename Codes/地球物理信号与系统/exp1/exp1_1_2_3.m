%% Continous
% parameter
t = 0:1/1000:1;
f = 5; % frequency
A = 2; % amplitude
alpha = -2; % attenuation parameter

% signals
x1 = A * sin(2*pi*f*t);
x2 = square(2*pi*f*t);
x3 = sawtooth(2*pi*f*t);
x4 = tripuls(t-0.5,0.2);
x5 = exp(alpha*t);               
x6 = randn(size(t));              
x7 = rectpuls(t-0.5,0.2);

% plot
figure('Name','Continous Signals','NumberTitle','off');

subplot(4,2,1);
plot(t, x1); grid on;
title('A sin()'); xlabel('t'); ylabel('x(t)');

subplot(4,2,2);
plot(t, x2); grid on;
title('square()'); xlabel('t'); ylabel('x(t)');

subplot(4,2,3);
plot(t, x3); grid on;
title('sawtooth()'); xlabel('t'); ylabel('x(t)');

subplot(4,2,4);
plot(t, x4); grid on;
title('tripuls()'); xlabel('t'); ylabel('x(t)');

subplot(4,2,5);
plot(t, x5); grid on;
title('exp()'); xlabel('t'); ylabel('x(t)');

subplot(4,2,6);
plot(t, x6); grid on;
title('randn()'); xlabel('t'); ylabel('x(t)');

subplot(4,2,7);
plot(t, x7); grid on;
title('rectpuls()'); xlabel('t'); ylabel('x(t)');

%% Discrete
n = 0:0.05:1;
x1 = A * sin(2*pi*f*n);
x2 = square(2*pi*f*n);
x3 = sawtooth(2*pi*f*n);
x4 = tripuls(n-0.5,0.2);
x5 = exp(alpha*n);               
x6 = randn(size(n));              
x7 = rectpuls(n-0.5,0.2);

figure('Name','Discrete Signals','NumberTitle','off');

subplot(4,2,1); stem(n,x1,'filled','MarkerSize',3); grid on;
title('sin[n]'); xlabel('n'); ylabel('x[n]');

subplot(4,2,2); stem(n,x2,'filled','MarkerSize',3); grid on;
title('square[n]'); xlabel('n'); ylabel('x[n]');

subplot(4,2,3); stem(n,x3,'filled','MarkerSize',3); grid on;
title('sawtooth[n]'); xlabel('n'); ylabel('x[n]');

subplot(4,2,4); stem(n,x4,'filled','MarkerSize',3); grid on;
title('tripuls[n]'); xlabel('n'); ylabel('x[n]');

subplot(4,2,5); stem(n,x5,"filled",'MarkerSize',3); grid on;
title('exp[n]'); xlabel('n'); ylabel('x[n]');

subplot(4,2,6); stem(n,x6,"filled",'MarkerSize',3); grid on;
title('randn[n]'); xlabel('n'); ylabel('x[n]');

subplot(4,2,7); stem(n,x7,"filled",'MarkerSize',3); grid on;
title('rectpuls[n]'); xlabel('n'); ylabel('x[n]');

%% x[n] = cos(n*Omega)
Omega = 0:pi/8:2*pi;
n = linspace(0,31,32);

figure('Name','x[n]=sin(n*Omega)','NumberTitle','off');

for k = 1:length(Omega)
    x = sin(n*Omega(k));
    subplot(9,2,k); stem(n,x,'filled','MarkerSize',3); grid on;
    title(['\Omega = ', num2str(Omega(k))]);
    xlabel('n'); ylabel('x[n]');
    axis([0 2*pi -1.2 1.2]);
end

%% x[n]=(1+1/2 sin(Omega*t))*sin(8*Omega*t)
Omega = 2*pi;

x1 = sin(t*Omega);
x2 = 1/2*x1;
x3 = 1+x2;
x4 = x3 .* sin(8*Omega*t);

figure('Name','Basic Calc','NumberTitle','off');

subplot(4,1,1); plot(t,x1); grid on;
title('sin(t*Omega)'); xlabel('n'); ylabel('x[n]');

subplot(4,1,2); plot(t,x2); grid on;
title('1/2sin(t*Omega)'); xlabel('n'); ylabel('x[n]');

subplot(4,1,3); plot(t,x3); grid on;
title('1+1/2sin(t*Omega)'); xlabel('n'); ylabel('x[n]');

subplot(4,1,4); plot(t,x4); grid on;
title('[1+1/2sin(t*Omega)]*sin(8*t*Omega)'); xlabel('n'); ylabel('x[n]');

