import os
import time
import psutil
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization

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

def run_experiment(key_size, dataset_type, num_iterations):
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

def main():
    key_sizes = [2048, 3072, 4096]
    dataset_types = ['random_data', 'structured_data', 'text_data']
    num_iterations = 10

    results = []

    for key_size in key_sizes:
        for dataset_type in dataset_types:
            print(f'Running experiment for key size {key_size} and dataset type {dataset_type}...')
            avg_encryption_time, avg_decryption_time, avg_memory_usage, avg_cpu_usage = run_experiment(key_size, dataset_type, num_iterations)
            results.append((key_size, dataset_type, avg_encryption_time, avg_decryption_time, avg_memory_usage, avg_cpu_usage))

    with open('results.txt', 'w') as file:
        file.write('Key Size\tDataset Type\tAvg. Encryption Time\tAvg. Decryption Time\tAvg. Memory Usage\tAvg. CPU Usage\n')
        for result in results:
            file.write(f'{result[0]}\t{result[1]}\t{result[2]:.6f}\t{result[3]:.6f}\t{result[4]}\t{result[5]:.2f}\n')

if __name__ == '__main__':
    main()