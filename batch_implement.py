import os
import time
import psutil
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
import matplotlib.pyplot as plt

def load_private_key(filename):
    with open(filename, 'rb') as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None
        )
    return private_key

def load_public_key(filename):
    with open(filename, 'rb') as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read()
        )
    return public_key

def encrypt_batch(public_key, messages):
    encrypted_messages = []
    for message in messages:
        try:
            encrypted = public_key.encrypt(
                message,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            encrypted_messages.append(encrypted)
        except ValueError as e:
            print(f"Encryption failed for message: {message}. Error: {str(e)}")
    return encrypted_messages

def decrypt_batch(private_key, encrypted_messages):
    decrypted_messages = []
    for encrypted in encrypted_messages:
        try:
            decrypted = private_key.decrypt(
                encrypted,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            decrypted_messages.append(decrypted)
        except ValueError as e:
            print(f"Decryption failed for encrypted message: {encrypted}. Error: {str(e)}")
    return decrypted_messages

def measure_resource_usage(func, *args, **kwargs):
    start_time = time.perf_counter()
    start_memory = psutil.Process().memory_info().rss
    start_cpu = psutil.cpu_percent()

    result = func(*args, **kwargs)

    end_time = time.perf_counter()
    end_memory = psutil.Process().memory_info().rss
    end_cpu = psutil.cpu_percent()

    execution_time = end_time - start_time
    memory_usage = end_memory - start_memory
    cpu_usage = end_cpu - start_cpu

    return result, execution_time, memory_usage, cpu_usage

def run_batch_rsa_experiment(key_size, dataset_type, num_iterations):
    private_key_file = f'key/rsa-batch/rsa_private_key_{key_size}.pem'
    public_key_file = f'key/rsa-batch/rsa_public_key_{key_size}.pem'

    private_key = load_private_key(private_key_file)
    public_key = load_public_key(public_key_file)

    dataset_files = [f for f in os.listdir('dataset') if f.startswith(dataset_type)]

    encryption_times = []
    decryption_times = []
    memory_usages = []
    cpu_usages = []

    for _ in range(num_iterations):
        messages = [open(f'dataset/{file}', 'rb').read() for file in dataset_files]

        encrypted_messages, enc_time, enc_memory, enc_cpu = measure_resource_usage(encrypt_batch, public_key, messages)
        decrypted_messages, dec_time, dec_memory, dec_cpu = measure_resource_usage(decrypt_batch, private_key, encrypted_messages)

        encryption_times.append(enc_time)
        decryption_times.append(dec_time)
        memory_usages.append(enc_memory + dec_memory)
        cpu_usages.append(enc_cpu + dec_cpu)

    avg_encryption_time = sum(encryption_times) / num_iterations
    avg_decryption_time = sum(decryption_times) / num_iterations
    avg_memory_usage = sum(memory_usages) / num_iterations
    avg_cpu_usage = sum(cpu_usages) / num_iterations

    return avg_encryption_time, avg_decryption_time, avg_memory_usage, avg_cpu_usage

def run_multi_prime_rsa_experiment(key_size, num_primes, dataset_type, num_iterations):
    private_key_file = f'key/rsa-multi-prime/multi_prime_rsa_private_key_{key_size}_{num_primes}primes.pem'
    public_key_file = f'key/rsa-multi-prime/multi_prime_rsa_public_key_{key_size}_{num_primes}primes.pem'

    private_key = load_private_key(private_key_file)
    public_key = load_public_key(public_key_file)

    dataset_files = [f for f in os.listdir('dataset') if f.startswith(dataset_type)]

    encryption_times = []
    decryption_times = []
    memory_usages = []
    cpu_usages = []

    for _ in range(num_iterations):
        messages = [open(f'dataset/{file}', 'rb').read() for file in dataset_files]

        encrypted_messages, enc_time, enc_memory, enc_cpu = measure_resource_usage(encrypt_batch, public_key, messages)
        decrypted_messages, dec_time, dec_memory, dec_cpu = measure_resource_usage(decrypt_batch, private_key, encrypted_messages)

        encryption_times.append(enc_time)
        decryption_times.append(dec_time)
        memory_usages.append(enc_memory + dec_memory)
        cpu_usages.append(enc_cpu + dec_cpu)

    avg_encryption_time = sum(encryption_times) / num_iterations
    avg_decryption_time = sum(decryption_times) / num_iterations
    avg_memory_usage = sum(memory_usages) / num_iterations
    avg_cpu_usage = sum(cpu_usages) / num_iterations

    return avg_encryption_time, avg_decryption_time, avg_memory_usage, avg_cpu_usage

def run_rsa_aep_experiment(key_size, dataset_type, num_iterations):
    private_key_file = f'key/rsa-aep/rsa_aep_private_key_{key_size}.pem'
    public_key_file = f'key/rsa-aep/rsa_aep_public_key_{key_size}.pem'

    private_key = load_private_key(private_key_file)
    public_key = load_public_key(public_key_file)

    dataset_files = [f for f in os.listdir('dataset') if f.startswith(dataset_type)]

    encryption_times = []
    decryption_times = []
    memory_usages = []
    cpu_usages = []

    for _ in range(num_iterations):
        messages = [open(f'dataset/{file}', 'rb').read() for file in dataset_files]

        encrypted_messages = []
        total_enc_time = 0
        total_enc_memory = 0
        total_enc_cpu = 0

        for message in messages:
            try:
                encrypted, enc_time, enc_memory, enc_cpu = measure_resource_usage(public_key.encrypt,
                                                                                  message,
                                                                                  padding.OAEP(
                                                                                      mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                                                                      algorithm=hashes.SHA256(),
                                                                                      label=None
                                                                                  ))
                encrypted_messages.append(encrypted)
                total_enc_time += enc_time
                total_enc_memory += enc_memory
                total_enc_cpu += enc_cpu
            except ValueError as e:
                print(f"Encryption failed for message: {message}. Error: {str(e)}. Skipping this message.")
                continue

        decrypted_messages = []
        total_dec_time = 0
        total_dec_memory = 0
        total_dec_cpu = 0

        for encrypted in encrypted_messages:
            decrypted, dec_time, dec_memory, dec_cpu = measure_resource_usage(
                private_key.decrypt,
                encrypted,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            decrypted_messages.append(decrypted)
            total_dec_time += dec_time
            total_dec_memory += dec_memory
            total_dec_cpu += dec_cpu

        encryption_times.append(total_enc_time)
        decryption_times.append(total_dec_time)
        memory_usages.append(total_enc_memory + total_dec_memory)
        cpu_usages.append(total_enc_cpu + total_dec_cpu)

    avg_encryption_time = sum(encryption_times) / num_iterations
    avg_decryption_time = sum(decryption_times) / num_iterations
    avg_memory_usage = sum(memory_usages) / num_iterations
    avg_cpu_usage = sum(cpu_usages) / num_iterations

    return avg_encryption_time, avg_decryption_time, avg_memory_usage, avg_cpu_usage
def plot_results(results):
    rsa_variants = ['Batch RSA', 'Multi-prime RSA', 'RSA-AEP']
    key_sizes = [2048, 3072, 4096]
    dataset_types = ['random_data', 'structured_data', 'text_data']

    for dataset_type in dataset_types:
        fig, axs = plt.subplots(2, 2, figsize=(12, 8))
        fig.suptitle(f'Performance Metrics for Dataset Type: {dataset_type}', fontsize=16)

        for i, metric in enumerate(['Avg. Encryption Time', 'Avg. Decryption Time', 'Avg. CPU Usage']):
            row = i // 2
            col = i % 2

            for rsa_variant in rsa_variants:
                x = []
                y = []
                for result in results:
                    if result[0] == rsa_variant and result[2] == dataset_type:
                        if metric == 'Avg. CPU Usage' and result[6] > 0:
                            x.append(result[1])
                            y.append(result[i+3])
                        elif metric != 'Avg. CPU Usage':
                            x.append(result[1])
                            y.append(result[i+3])

                if len(x) > 0 and len(y) > 0:
                    axs[row, col].plot(x, y, marker='o', label=rsa_variant)
                    axs[row, col].set_xlabel('Key Size')
                    axs[row, col].set_ylabel(metric)
                    axs[row, col].legend()

        plt.tight_layout()
        plt.savefig(f'performance_metrics_{dataset_type}.png')
        plt.close()
def main():
    key_sizes = [2048, 3072, 4096]
    num_primes_list = [3, 4, 5]
    dataset_types = ['random_data', 'structured_data', 'text_data']
    num_iterations = 10

    results = []

    print("Running Batch RSA experiments...")
    for key_size in key_sizes:
        for dataset_type in dataset_types:
            print(f'Running Batch RSA experiment for key size {key_size} and dataset type {dataset_type}...')
            avg_encryption_time, avg_decryption_time, avg_memory_usage, avg_cpu_usage = run_batch_rsa_experiment(key_size, dataset_type, num_iterations)
            results.append(('Batch RSA', key_size, dataset_type, avg_encryption_time, avg_decryption_time, avg_memory_usage, avg_cpu_usage))

    print("Running Multi-prime RSA experiments...")
    for index, key_size in enumerate(key_sizes):
        for dataset_type in dataset_types:
            avg_encryption_time, avg_decryption_time, avg_memory_usage, avg_cpu_usage = run_multi_prime_rsa_experiment(key_size, num_primes_list[index], dataset_type, num_iterations)
            results.append(('Multi-prime RSA', key_size, dataset_type, avg_encryption_time, avg_decryption_time, avg_memory_usage, avg_cpu_usage))

    print("Running RSA-AEP experiments...")
    for key_size in key_sizes:
        for dataset_type in dataset_types:
            print(f'Running RSA-AEP experiment for key size {key_size} and dataset type {dataset_type}...')
            avg_encryption_time, avg_decryption_time, avg_memory_usage, avg_cpu_usage = run_rsa_aep_experiment(key_size, dataset_type, num_iterations)
            results.append(('RSA-AEP', key_size, dataset_type, avg_encryption_time, avg_decryption_time, avg_memory_usage, avg_cpu_usage))

    with open('results.txt', 'w') as file:
        file.write('RSA Variant\tKey Size\tDataset Type\tAvg. Encryption Time\tAvg. Decryption Time\tAvg. Memory Usage\tAvg. CPU Usage\n')
        for result in results:
            file.write(f'{result[0]}\t{result[1]}\t{result[2]}\t{result[3]:.6f}\t{result[4]:.6f}\t{result[5]}\t{result[6]:.2f}\n')

    plot_results(results)

if __name__ == '__main__':
    main()