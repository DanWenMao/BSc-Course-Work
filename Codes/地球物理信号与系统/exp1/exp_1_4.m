fs = 2000; % sampling frequency
frequencies = [262, 294, 330, 349, 392, 440, 494, 524];
t = 0:1/fs:1;

figure('Name','Different Frequency');
for i = 1:length(frequencies)
    f = frequencies(i);
    x = sin(2 * pi * f * t);
    subplot(4, 2, i);
    plot(t, x);
    title(['Frequency ' num2str(f) ' Hz']);
    xlabel('Time(s)');
    ylabel('Amplitude');
    sound(x,fs);
    %pause(5)
    grid on;
end

[audio_data_1,fs] = audioread('c.wav');
audio_data_1 = audio_data_1(fs:2*fs);
t_dis = (0:(length(audio_data_1)-1))/fs; % time points
N_dis = length(audio_data_1); % number of point

% stretch: t_large~audio_data_2
N_dense = round(N_dis*2); % new number of points
t_dense = linspace(0,max(t_dis),N_dense); % dense time points
audio_data_2 = interp1(t_dis,audio_data_1,t_dense,'linear',0);
t_large = linspace(0,max(t_dis)*2,N_dense);

% compress: t_small~audio_data_3
N_sparse = round(N_dis/2);
t_sparse = linspace(0,max(t_dis),N_sparse);
audio_data_3 = interp1(t_dis,audio_data_1,t_sparse,'linear',0);
t_small = linspace(0,max(t_dis)/2,N_sparse);

% translation
t_trans = linspace(2,max(t_dis)+2,N_dis);

figure('Name','c.wav');
subplot(2,2,1);
plot(t_dis, audio_data_1);
title('Original Sound');
xlabel('Time(s)');
ylabel('Amplitude');
sound(audio_data_1, fs);
grid on;
pause(5);

subplot(2,2,2);
plot(t_large, audio_data_2);
title('Stretched Sound');
xlabel('Time(s)');
ylabel('Amplitude');
sound(audio_data_2, fs*2);
grid on;
pause(5);

subplot(2,2,3);
plot(t_small, audio_data_3);
title('Compressed Sound');
xlabel('Time(s)');
ylabel('Amplitude');
sound(audio_data_3, fs*0.5);
grid on;
pause(5);

subplot(2,2,4);
plot(t_trans, audio_data_1);
title('Translated Sound');
xlabel('Time(s)');
ylabel('Amplitude');
sound(audio_data_1, fs);
grid on;


