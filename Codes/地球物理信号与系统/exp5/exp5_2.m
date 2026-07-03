clear; clc; close all;

% 参数定义
fs = 44100;
t = 0:1/fs:0.02;
x = sin(2*pi*500*t) + 0.5*randn(size(t)); % 含噪声的正弦信号

M_list = [32, 64, 128];
N_fft = 1024;

for i = 1:length(M_list)
    M = M_list(i);
    k = -M:M;
    
    % --- 1. 滤波器 ---
    b_a = ones(1, 2*M+1) / (2*M+1);
    b_b = sin(2*pi*k/33) ./ (pi*k);
    b_b(k==0) = 2/33;
    
    % --- 2. 频率响应 ---
    
    % 方法1：FFT
    H_fft_a = fft(b_a, N_fft);
    H_fft_b = fft(b_b, N_fft);
    f_axis = (0:N_fft/2-1) / (N_fft/2); 
    H_a_half = H_fft_a(1:N_fft/2);
    H_b_half = H_fft_b(1:N_fft/2);

    % 方法2：freqz
    [H_fz_a, w_a] = freqz(b_a, 1, N_fft/2);
    [H_fz_b, w_b] = freqz(b_b, 1, N_fft/2);

    % --- 3. 绘图---
    figure('Name', ['M = ', num2str(M), ' 频率响应分析'], 'NumberTitle', 'off');
    
    % 滤波器 a
    subplot(2,1,1);
    plot(f_axis, 20*log10(abs(H_a_half)), 'b', 'LineWidth', 1.5); hold on;
    plot(w_a/pi, 20*log10(abs(H_fz_a)), 'r--', 'LineWidth', 1);
    grid on;
    title(['滤波器 a (M=', num2str(M), ') 幅频响应']);
    legend('FFT (卷积定理)', 'freqz 函数');
    ylabel('幅度 (dB)');
    
    % 滤波器 b
    subplot(2,1,2);
    plot(f_axis, 20*log10(abs(H_b_half)), 'b', 'LineWidth', 1.5); hold on;
    plot(w_b/pi, 20*log10(abs(H_fz_b)), 'r--', 'LineWidth', 1);
    grid on;
    title(['滤波器 b (M=', num2str(M), ') 幅频响应']);
    legend('FFT (卷积定理)', 'freqz 函数');
    xlabel('归一化频率 (\times\pi rad/sample)');
    ylabel('幅度 (dB)');


    y_a = conv(x, b_a, 'same');
    y_b = conv(x, b_b, 'same');
    
    figure('Name', ['M = ', num2str(M), ' 时域滤波效果'], 'NumberTitle', 'off');
    subplot(3,1,1); plot(t, x); title('原始含噪信号'); grid on;
    subplot(3,1,2); plot(t, y_a); title(['滤波器 a (M=', num2str(M), ') 输出']); grid on;
    subplot(3,1,3); plot(t, y_b); title(['滤波器 b (M=', num2str(M), ') 输出']); grid on;
end