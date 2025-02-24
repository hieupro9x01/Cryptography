





import numpy as np
import matplotlib.pyplot as plt
import librosa
import soundfile as sf
from sklearn.metrics import mean_squared_error
import subprocess  # Thư viện cho lệnh subprocess

# Hàm chuyển đổi MP3 sang WAV sử dụng librosa
def convert_mp3_to_wav(mp3_file_path, wav_file_path):
    signal, sample_rate = librosa.load(mp3_file_path, sr=None)
    sf.write(wav_file_path, signal, sample_rate)
    print(f"Đã chuyển đổi MP3 sang WAV: {wav_file_path}")

# Hàm chuyển WAV sang MP3 sử dụng LAME
def convert_wav_to_mp3(wav_file, mp3_file):
    y, sr = librosa.load(wav_file, sr=None)
    sf.write(mp3_file, y, sr, format='MP3')
    print(f"Đã chuyển đổi WAV sang MP3: {mp3_file}")

# Hàm nén tín hiệu theo luật A
def a_law_compress(signal, A=87.6, eps=1e-12):
    abs_signal = np.abs(signal)
    compressed_signal = np.where(abs_signal < 1/A,
                                 A * abs_signal / (1 + np.log(A)),
                                 (1 + np.log(A * (abs_signal + eps))) / (1 + np.log(A)))
    return np.sign(signal) * compressed_signal

# Hàm giải nén tín hiệu theo luật A
def a_law_expand(compressed_signal, A=87.6, eps=1e-12):
    abs_signal = np.abs(compressed_signal)
    expanded_signal = np.where(abs_signal < 1 / (1 + np.log(A)),
                               abs_signal * (1 + np.log(A)) / A,
                               np.exp(abs_signal * (1 + np.log(A)) - 1) / A)
    return np.sign(compressed_signal) * expanded_signal

# Hàm tính SNR (Signal-to-Noise Ratio)
def calculate_snr(original_signal, processed_signal):
    noise = original_signal - processed_signal
    signal_power = np.mean(original_signal ** 2) # tính giá trị trung bình bình phương giá trị của từng mẫu tín hiệu gốc
    noise_power = np.mean(noise ** 2) # tính giá trị trung bình bình phương giá trị của từng mẫu tín hiệu nhiễu
    snr = 10 * np.log10(signal_power / noise_power)
    return snr

# Đọc file âm thanh
def load_audio(file_path):
    signal, sample_rate = librosa.load(file_path, sr=None)
    return signal, sample_rate

# Lưu tín hiệu nén thành file âm thanh mới
def save_compressed_audio(file_path, compressed_signal, sample_rate):
    sf.write(file_path, compressed_signal, sample_rate, format='WAV', subtype='PCM_16')

# Lưu tín hiệu đã giải nén thành file âm thanh mới
def save_expanded_audio(file_path, expanded_signal, sample_rate):
    sf.write(file_path, expanded_signal, sample_rate, format='WAV', subtype='PCM_16')

# Hàm chính để xử lý tín hiệu từ file âm thanh
def process_audio_file(file_path, compressed_output_file, final_wav_file, final_mp3_file, compressed_audio_file_mp3):
    # Đọc file âm thanh
    input_signal, sample_rate = load_audio(file_path)
    # Hiển thị giá trị của tín hiệu gốc
    print("Bản giá trị tín hiệu thoại tương tự bản gốc: \n", input_signal[5000:5050])
    print("Tần số mẫu:", sample_rate)
    # Nén tín hiệu theo luật A
    compressed_signal = a_law_compress(input_signal)
    # Hiển thị giá trị của tín hiệu nén
    print("Bản giá trị tín hiệu thoại tương tự bản nén: \n", compressed_signal[5000:5050])
    # print("Tần số mẫu:", sample_rate1)
    # Giải nén tín hiệu
    expanded_signal = a_law_expand(compressed_signal)
    # Hiển thị giá trị của tín hiệu
    print("Bản giá trị tín hiệu thoại tương tự giải nén: \n", expanded_signal[5000:5050])
    # print("Tần số mẫu:", sample_rate2)
    # Tính toán MSE và SNR
    mse_compressed = mean_squared_error(input_signal, compressed_signal)
    mse_expanded = mean_squared_error(input_signal, expanded_signal)
    snr_expanded = calculate_snr(input_signal, expanded_signal)
    
    # In kết quả MSE và SNR
    print(f"MSE giữa tín hiệu gốc và nén: {mse_compressed}")
    print(f"MSE giữa tín hiệu gốc và giải nén: {mse_expanded}")
    print(f"SNR giữa tín hiệu gốc và giải nén: {snr_expanded:.2f} dB")
    
    # Điều chỉnh khoảng thời gian để hiển thị tín hiệu chi tiết
    t = np.linspace(0, len(input_signal) / sample_rate, len(input_signal))
    t_zoomed = t[:15000]  # Chỉ hiển thị 15000 mẫu đầu tiên
    input_signal_zoomed = input_signal[:15000]
    compressed_signal_zoomed = compressed_signal[:15000]
    expanded_signal_zoomed = expanded_signal[:15000]
    difference_signal_zoomed = input_signal_zoomed - expanded_signal_zoomed  # Tín hiệu khác biệt
    print("Khác biệt giữa tín hiệu gốc và đã giải nén:\n", difference_signal_zoomed[5000:5050])
    # Hiển thị các biểu đồ
    plt.figure(figsize=(12, 12))

    # Biểu đồ tín hiệu gốc
    plt.subplot(4, 1, 1)
    plt.plot(t_zoomed, input_signal_zoomed, color='blue', linewidth=2)
    plt.title("Tín hiệu gốc (Zoom)", fontsize=14, pad=20)
    plt.xlabel("Thời gian (s)", fontsize=12)
    plt.ylabel("Biên độ", fontsize=12)
    plt.grid(True)

    # Biểu đồ tín hiệu sau khi nén
    plt.subplot(4, 1, 2)
    plt.plot(t_zoomed, compressed_signal_zoomed, color='green', linewidth=2)
    plt.title(f"Tín hiệu sau khi nén theo luật A (Zoom)\nMSE: {mse_compressed:.6f}", fontsize=14, pad=20)
    plt.xlabel("Thời gian (s)", fontsize=12)
    plt.ylabel("Biên độ", fontsize=12)
    plt.grid(True)

    # Biểu đồ tín hiệu sau khi giải nén
    plt.subplot(4, 1, 3)
    plt.plot(t_zoomed, expanded_signal_zoomed, color='red', linewidth=2)
    plt.title(f"Tín hiệu sau khi giải nén theo luật A (Zoom)\nMSE: {mse_expanded:.6f}, SNR: {snr_expanded:.2f} dB", fontsize=14, pad=20)
    plt.xlabel("Thời gian (s)", fontsize=12)
    plt.ylabel("Biên độ", fontsize=12)
    plt.grid(True)

    # Biểu đồ sự khác biệt giữa tín hiệu gốc và giải nén
    plt.subplot(4, 1, 4)
    plt.plot(t_zoomed, difference_signal_zoomed, color='purple', linewidth=2)
    plt.title("Sự khác biệt giữa tín hiệu gốc và tín hiệu giải nén", fontsize=14, pad=20)
    plt.xlabel("Thời gian (s)", fontsize=12)
    plt.ylabel("Biên độ khác biệt", fontsize=12)
    plt.grid(True)

    plt.tight_layout(pad=3.0)
    plt.show()
    
    # Lưu tín hiệu đã nén thành file âm thanh mới
    save_compressed_audio(compressed_output_file, compressed_signal, sample_rate)
    print(f"File âm thanh đã nén được lưu tại: {compressed_output_file}")

    # Chuyển file nén WAV thành file nén MP3 bằng LAME
    convert_wav_to_mp3(compressed_audio_file, compressed_audio_file_mp3)

    # Lưu tín hiệu đã giải nén thành file âm thanh mới
    save_expanded_audio(final_wav_file, expanded_signal, sample_rate)
    print(f"File âm thanh đã giải nén được lưu tại: {final_wav_file}")

    # Chuyển file WAV cuối cùng thành MP3 bằng LAME
    convert_wav_to_mp3(final_wav_file, final_mp3_file)



# File âm thanh đầu vào ('.mp3' -> '.wav')
mp3_file_path = input("Nhập file âm thanh cần nén:")  # Đường dẫn file MP3 gốc
wav_file_path = "Em Của Ngày Hôm Qua WAV.wav"  # File WAV sẽ được lưu

# File WAV mới sau khi chuyển đổi từ MP3
convert_mp3_to_wav(mp3_file_path, wav_file_path)

# Tên các file sau khi nén và giải nén
compressed_audio_file = "file_nén_dạng_WAV.wav"
compressed_audio_file_mp3 = "file_nén_dạng_MP3.mp3"

final_wav_file = "file_đã_giải_nén_dạng_WAV.wav"
final_mp3_file = "file_đã_giải_nén_dạng_MP3.mp3"

# Xử lý file WAV đã chuyển đổi từ MP3 và tiến hành nén/giải nén
process_audio_file(wav_file_path, compressed_audio_file, final_wav_file, final_mp3_file, compressed_audio_file_mp3)
