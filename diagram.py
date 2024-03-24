import pandas as pd
import matplotlib.pyplot as plt

# Đọc dữ liệu từ file kết quả
data = pd.read_csv('results.txt', sep='\t')

# Vẽ biểu đồ thời gian mã hóa và giải mã theo kích thước thông điệp cho từng biến thể RSA
plt.figure(figsize=(12, 6))

for variant in data['RSA Variant'].unique():
    variant_data = data[data['RSA Variant'] == variant]
    
    plt.subplot(1, 2, 1)
    plt.plot(variant_data['Key Size'], variant_data['Avg. Encryption Time'], marker='o', label=variant)
    plt.xlabel('Key Size')
    plt.ylabel('Avg. Encryption Time')
    plt.title('Encryption Time vs Key Size')
    plt.legend()
    
    plt.subplot(1, 2, 2)
    plt.plot(variant_data['Key Size'], variant_data['Avg. Decryption Time'], marker='o', label=variant)
    plt.xlabel('Key Size')
    plt.ylabel('Avg. Decryption Time')
    plt.title('Decryption Time vs Key Size')
    plt.legend()

plt.tight_layout()
plt.savefig('rsa_variants_time.png')
plt.show()

# Vẽ biểu đồ so sánh hiệu suất giữa các biến thể RSA về thời gian và sử dụng CPU
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
for variant in data['RSA Variant'].unique():
    variant_data = data[data['RSA Variant'] == variant]
    plt.plot(variant_data['Key Size'], variant_data['Avg. Encryption Time'] + variant_data['Avg. Decryption Time'], marker='o', label=variant)
plt.xlabel('Key Size')
plt.ylabel('Total Time (Encryption + Decryption)')
plt.title('Total Time vs Key Size')
plt.legend()

plt.subplot(1, 2, 2)
for variant in data['RSA Variant'].unique():
    variant_data = data[data['RSA Variant'] == variant]
    plt.plot(variant_data['Key Size'], variant_data['Avg. CPU Usage'], marker='o', label=variant)
plt.xlabel('Key Size')
plt.ylabel('Avg. CPU Usage')
plt.title('CPU Usage vs Key Size')
plt.legend()

plt.tight_layout()
plt.savefig('rsa_variants_performance.png')
plt.show()