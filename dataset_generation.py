import os
import random
import string
from OpenSSL import crypto
from faker import Faker

os.makedirs('dataset', exist_ok=True)

faker = Faker()

def generate_random_data(size):
    return os.urandom(size)

# XML
def generate_structured_data():
    xml_data = '''
    <?xml version="1.0" encoding="UTF-8"?>
    <user>
        <name>{}</name>
        <email>{}</email>
        <age>{}</age>
    </user>
    '''.format(faker.name(), faker.email(), faker.random_int(min=18, max=80))
    return xml_data.encode('utf-8')

# TEXT
def generate_text_data():
    return faker.text().encode('utf-8')

def generate_dataset():
    # bin file
    for i in range(100):
        size = random.choice([1024, 2048, 4096])  
        data = generate_random_data(size)
        filename = f'dataset/random_data_{i}.bin'
        with open(filename, 'wb') as file:
            file.write(data)

    # xml
    for i in range(100):
        xml_data = generate_structured_data()
        filename = f'dataset/structured_data_{i}.xml'
        with open(filename, 'wb') as file:
            file.write(xml_data)

    # text
    for i in range(100):
        text_data = generate_text_data()
        filename = f'dataset/text_data_{i}.txt'
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(text_data.decode('utf-8'))

generate_dataset()