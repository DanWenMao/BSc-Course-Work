clear; clc; close all;

%% Step 1 & 2: 指标定义与参数计算
wp = 0.2*pi;       % 通带截止频率
ws = 0.3*pi;       % 阻带截止频率
Rs = 50;           % 阻带衰减需求
wc = (wp + ws) / 2; % 理想低通的截止频率（取过渡带中心）

% N=67 (基于汉明窗主瓣宽度 6.6*pi/N 满足过渡带 0.1*pi)
N = 67; 
alpha = (N-1)/2;   % 序列偏移量
n = 0:N-1;         % 离散时间序列

%% Step 3: 计算单位脉冲响应
% 理想低通滤波器的单位脉冲响应 (Sinc函数)

hd = sin(wc * (n - alpha)) ./ (pi * (n - alpha));
hd(n == alpha) = wc / pi; 

% 生成汉明窗
w = hamming(N)';

% 实际滤波序列 h(n) = hd(n) * w(n)
h = hd .* w;

%% Step 4: 性能验证与绘图
% 计算频率响应
[H, f] = freqz(h, 1, 1024);
mag = 20*log10(abs(H));

% 绘制幅频响应曲线
figure;
plot(f/pi, mag, 'LineWidth', 1.5);
hold on;
grid on;

% 标注技术指标线
line([0 1], [-0.25 -0.25], 'Color', 'r', 'LineStyle', '--'); % 通带纹波线
line([0.3 0.3], [-100 0], 'Color', 'g', 'LineStyle', '--');  % 阻带起始线
line([0 1], [-50 -50], 'Color', 'm', 'LineStyle', '--');    % 阻带衰减线

title(['使用汉明窗设计的FIR低通滤波器 (N=', num2str(N), ')']);
xlabel('归一化频率 (\times\pi rad/sample)');
ylabel('幅度 (dB)');
axis([0 1 -100 10]);
legend('幅频响应', '通带纹波限制', '阻带起始频率', '阻带衰减要求');

%% 验证具体指标
% 计算通带波动（0 到 0.2pi 范围内的最大/最小值）
pass_indices = f <= 0.2*pi;
Rp_actual = -min(mag(pass_indices));
% 计算阻带衰减（0.3pi 到 pi 范围内的最大值）
stop_indices = f >= 0.3*pi;
Rs_actual = -max(mag(stop_indices));

fprintf('--- 设计结果验证 ---\n');
fprintf('通带纹波 Rp = %.4f dB (指标 < 0.25dB)\n', Rp_actual);
fprintf('阻带衰减 Rs = %.4f dB (指标 > 50dB)\n', Rs_actual);