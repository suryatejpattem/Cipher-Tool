import os
import string
import random

#----Reversing Algorithm----#

#Reversing Encryption Text
def reverse_encrypt(text):
    reversed_text=text[::-1]
    return reversed_text

#Reversing Decryption Text
def reverse_decrypt(text):
    reversed_text=text[::-1]
    return reversed_text


#----Substitution Cipher Algorithm----#

#global variables
char = string.whitespace + string.punctuation + string.ascii_letters + string.digits
substitution_key = list(char)
random.shuffle(substitution_key)
key_map = dict(zip(char, substitution_key))
reverse_key_map = dict(zip(substitution_key, char))

#Substitution Cipher Encryption
def substitution_encrypt(text):
    return ''.join(key_map[char] for char in text)

#Substitution Cipher Decryption
def substitution_decrypt(text):
    return ''.join(reverse_key_map[char] for char in text)

#----Caesar Cipher Algorithm----#

#Caesar Cipher Encryption
def caesar_encrypt(text, shift):
    encrypted_text = ""
    for char in text:
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            new_char = chr((ord(char) - start + shift) % 26 + start)
            encrypted_text += new_char
        else:
            encrypted_text += char
    return encrypted_text

#Caesar Cipher Decryption
def caesar_decrypt(text, shift):
    decrypted_text = ""
    for char in text:
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            new_char = chr((ord(char) - start - shift) % 26 + start)
            decrypted_text += new_char
        else:
            decrypted_text += char
    return decrypted_text


#----Vigenere cipher Algorithm----#

#Vigenere Cipher Encryption
def vigenere_encrypt(text,key):
    key_index=0
    encrypted_text=""
    for char in text:
        start=ord('A') if char.isupper() else ord('a')
        shift=ord(key[key_index].upper())- ord('A')
        new_char=chr((ord(char)-start+shift)%26+start)
        encrypted_text+=new_char
        key_index+=1
    return encrypted_text

#Vigenere Cipher Encryption
def vigenere_decrypt(text,key):
    key_index=0
    encrypted_text=""
    for char in text:
        if char.isalpha():
            start=ord('A') if char.isupper() else ord('a')
            shift=ord(key[key_index].upper())- ord('A')
            new_char=chr((ord(char)-start-shift)%26+start)
            encrypted_text+=new_char
            key_index+=1
        else:
            print("In vigenere cipher it must contain only alphabets")
    return encrypted_text


# File processing
def processfile(input_file, output_file,cipher_function):
    try:
        with open(input_file, 'r') as inputfile:
            text = inputfile.read()
            result=cipher_function(text)
        with open(output_file, 'w') as outputfile:
            outputfile.write(result)
            print("Process completed\n")
            print(f"{len(text)} characters are processed, Output saved in {output_file}")
    except PermissionError:
        print(f"Premission to file {input_file} is denied")


#select cipher
def select_cipher():
    while True:
        print("----Cipher Algorithms----")
        print("1. Reversing Text")
        print("2. Substitution Cipher")
        print("3. Caesar Cipher")
        print("4. Vigenere Cipher")

        cipher=input("Select the cipher(1/2/3/4):")
        if cipher not in ["1","2","3","4"]:
            print("Invalid option, select valid option")
            continue
        return cipher
 


#main
def main():

        while True:
            print("--------CIPH3R T00L--------")    
            cipher_choice=select_cipher()

            choice = input("Enter the mode (E/D): ").upper()
            if choice not in ["E", "D"]:
                print("Invalid mode. Please enter E or D.")
                continue

            input_format = input("Process text or file? (T/F): ").upper()
            if input_format not in ["T","F"]:
                print("Invalid input format")
                continue
            if input_format == "T":
                text = input("Enter the text to process: ")
                if cipher_choice=="1":
                    result=reverse_encrypt(text) if choice=="E" else reverse_decrypt(text)
                elif cipher_choice=="2":
                    result=substitution_encrypt(text) if choice=="E" else substitution_decrypt(text)
                elif cipher_choice=="3":
                    while True:  # Loop to keep asking for a valid shift
                        try:
                            shift = int(input("Enter the shift: "))
                            if shift <= 0:
                                print("Shift cannot be zero or negative.")
                                continue  # Keep asking for a valid shift
                            shift=shift%26
                            result=caesar_encrypt(text,shift) if choice=="E" else caesar_decrypt(text,shift)
                            break  # Exit the loop if valid shift is entered
                        except ValueError:
                            print("Invalid input, shift must be a number")
                            continue
                elif cipher_choice=="4":
                    key=input("Enter the key:")
                    if not key.isalpha():
                        print("Key must contain only alphabets")    
                        continue
                    if len(key)!=len(text):
                        new_key=(key*(len(text)//len(key)))+key[:len(text)%len(key)]
                    result=vigenere_encrypt(text,new_key) if choice=="E" else vigenere_decrypt(text,new_key)
                
                print(f"Message: {result}")

            elif input_format =="F":
                input_file=input("Enter the input file name:")
                if not os.path.exists(input_file):
                    print(f"Error {input_file} not found")
                    continue
                output_file=input("Enter the output name:")
                if cipher_choice=="1":
                    processfile(input_file,output_file,reverse_encrypt if choice=="E" else reverse_decrypt)
                elif cipher_choice=="2":
                    key_map, reversed_key_map = substitution_key()
                    processfile(input_file,output_file,lambda text: substitution_encrypt(text,key_map) if choice=="E" else substitution_decrypt(text, reversed_key_map))
                elif cipher_choice=="3":
                    while True:
                        try:
                            shift = int(input("Enter the shift value: "))
                            if shift <= 0:
                                print("Shift must be a positive integer.")
                                continue
                            shift=shift%26
                            break
                        except ValueError:
                            print("Invalid input. Shift must be a number.")
                    processfile(input_file, output_file, lambda text: caesar_encrypt(text, shift) if choice == "E" else caesar_decrypt(text, shift))
                elif cipher_choice == "4":
                    key = input("Enter the key (letters only): ")
                    if not key.isalpha():
                        print("Key must contain only alphabets.")
                        continue
                    processfile(input_file, output_file, lambda text: vigenere_encrypt(text, key) if choice == "E" else vigenere_decrypt(text, key))


            #Ask user to continue or not
            repeat = input("Do you want to process another text or file? (Y/N): ").upper()
            if repeat == "N":
                # Exit the loop and end the program
                print("Exiting the program.")
                break 

if __name__ == "__main__":
    main()
