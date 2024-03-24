from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def generate_rsa_key(key_size):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size
    )
    public_key = private_key.public_key()
    return private_key, public_key

def generate_multi_prime_rsa_key(key_size, num_primes):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
        backend=rsa.RSAPrivateKeyWithSerialization
    )
    public_key = private_key.public_key()
    return private_key, public_key

def generate_rsa_aep_key(key_size):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size
    )
    public_key = private_key.public_key()
    return private_key, public_key

def save_key_to_file(key, filename):
    pem = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    with open(filename, 'wb') as file:
        file.write(pem)

def save_public_key_to_file(key, filename):
    pem = key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    with open(filename, 'wb') as file:
        file.write(pem)

# RSA
key_sizes = [2048, 3072, 4096]

for key_size in key_sizes:
    private_key, public_key = generate_rsa_key(key_size)
    save_key_to_file(private_key, f'key/rsa-batch/rsa_private_key_{key_size}.pem')
    save_public_key_to_file(public_key, f'key/rsa-batch/rsa_public_key_{key_size}.pem')

# Multi-prime RSA
num_primes_list = [3, 4, 5]

for key_size, num_primes in zip(key_sizes, num_primes_list):
    private_key, public_key = generate_multi_prime_rsa_key(key_size, num_primes)
    save_key_to_file(private_key, f'key/rsa-multi-prime/multi_prime_rsa_private_key_{key_size}_{num_primes}primes.pem')
    save_public_key_to_file(public_key, f'key/rsa-multi-prime/multi_prime_rsa_public_key_{key_size}_{num_primes}primes.pem')

# RSA-AEP
for key_size in key_sizes:
    private_key, public_key = generate_rsa_aep_key(key_size)
    save_key_to_file(private_key, f'key/rsa-aep/rsa_aep_private_key_{key_size}.pem')
    save_public_key_to_file(public_key, f'key/rsa-aep/rsa_aep_public_key_{key_size}.pem')