clear; clc; close all;

%% 1. & 2. 系统频率响应函数

b = [2];
a = [1, 3, 2];
w = 0 : 1 : 300;

% --- 1 卷积定理---
jw = 1j * w;
H_formula = 2 ./ (jw.^2 + 3*jw + 2);

% --- 2：freqs  ---
H_freqs = freqs(b, a, w);

% plot
figure('Name', '系统频率响应');
subplot(2, 1, 1);
plot(w, abs(H_freqs), 'LineWidth', 1.5);
title('幅频响应 |H(j\omega)|'); xlabel('\omega (rad/s)'); ylabel('幅值'); grid on;

subplot(2, 1, 2);
plot(w, angle(H_freqs), 'LineWidth', 1.5);
title('相频响应 \angleH(j\omega)'); xlabel('\omega (rad/s)'); ylabel('相位 (rad)'); grid on;

%% 输入 e(t) = sin(t) + sin(20t) ，求输出

omega = [1, 20];
H = freqs(b, a, omega);

amp1 = abs(H(1));   pha1 = angle(H(1));
amp2 = abs(H(2));   pha2 = angle(H(2));

t = 0 : 0.01 : 20;

% input
e_t = sin(t) + sin(20*t);

% output
r_t = amp1 .* sin(t + pha1) + amp2 .* sin(20*t + pha2);

% plot
figure('Name', '时域输入输出对比');
subplot(2, 1, 1);
plot(t, e_t); title('输入信号 e(t) = sin(t) + sin(20t)'); grid on;
subplot(2, 1, 2);
plot(t, r_t); title('系统输出响应 r(t)'); grid on;
xlabel('时间 t (s)');
