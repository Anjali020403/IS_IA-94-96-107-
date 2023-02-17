import os
import wave
import struct
import random

def generate_key(length):
    """
    Generate a random encryption key of the given length.
    """
    return os.urandom(length)

def save_key(key, filename):
    """
    Save the encryption key to a file.
    """
    with open(filename, 'wb') as key_file:
        key_file.write(key)

def load_key(filename):
    """
    Load the encryption key from a file.
    """
    with open(filename, 'rb') as key_file:
        key = key_file.read()
    return key

def encrypt_audio_file(input_filename, output_filename, key):
    """
    Encrypt an audio file using a key and save the result to a new file.
    """
    with wave.open(input_filename, 'rb') as input_file, wave.open(output_filename, 'wb') as output_file:
        # Copy the audio file headers.
        output_file.setparams(input_file.getparams())

        # Generate a random seed based on the key.
        random.seed(key)

        # Encrypt each audio sample.
        for i in range(input_file.getnframes()):
            sample = input_file.readframes(1)
            encrypted_sample = struct.pack('h', struct.unpack('h', sample)[0] ^ random.randint(-32767, 32767))
            output_file.writeframes(encrypted_sample)

def decrypt_audio_file(input_filename, output_filename, key):
    """
    Decrypt an audio file using a key and save the result to a new file.
    """
    encrypt_audio_file(input_filename, output_filename, key)

# Example usage
input_filename = 'input.wav'
encrypted_filename = 'encrypted.wav'
decrypted_filename = 'decrypted.wav'
key_filename = 'key.bin'

# Generate a random key and save it to a file
key = generate_key(16)
save_key(key, key_filename)

# Encrypt the input file using the key and save the result to a new file
encrypt_audio_file(input_filename, encrypted_filename, key)

# Load the key from the file and decrypt the encrypted file to a new file
key = load_key(key_filename)
decrypt_audio_file(encrypted_filename, decrypted_filename, key)