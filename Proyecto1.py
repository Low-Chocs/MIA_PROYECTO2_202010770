import os
from Estructuras import *
import random
import time
import struct

def start():
    is_on_run = True
    while is_on_run:
        command = input("Ingresar texto (1 para salir): ")
        if command == '1':
            is_on_run = False
            continue
        command_splitted = command.split()
        if command_splitted[0].lower() == 'execute':
            path = command_splitted[1].split('=')
            path[1] = return_path_with_correct_user(path[1])
            open_file(path[1])
        else:
            print('No se reconoció el comando')
    

def open_file(path: str):
    try:
        with open(path, 'r') as search_file:
            line_commands = search_file.readlines()
            for instruction in line_commands:
                instructions_splitted = instruction.split()
                check_next_instruction(instructions_splitted)

    except FileNotFoundError:
        print("El archivo no se encontró en la ruta especificada.")
    except Exception as e:
        print("Ocurrió un error:", e)

def return_path_with_correct_user(path: str):
    if path.find('user') == -1:
        return path
    return path.replace('user', os.getlogin())

def check_file_extension(path):
    path_to_check = path.split('/')
    last_index = len(path_to_check) - 1

    if path_to_check[last_index].find('.adsj') == -1:
        print('El archivo debe de ser con la extensión .adsj')
    else:
        print('Todo correcto')
   

def check_next_instruction(next_instruction):
    if next_instruction[0].lower() == 'mkdisk':
        mkdisk(next_instruction)

def mkdisk(instruction):
    #Removes the first element "mkdisk"
    instruction.pop(0)
    size = 0
    path = ""
    fit = 'ff'
    unit = 'm'
    for i in range(len(instruction)):
        instruction[i] = instruction[i].replace('-', '')
        instruction_set = instruction[i].split('=')
        if instruction_set[0].lower() == 'size':
            size = instruction_set[1]
        if instruction_set[0].lower() == 'path':
            path = return_path_with_correct_user(instruction_set[1])
        if instruction_set[0].lower() == 'fit':
            fit = instruction_set[1].lower()
        if instruction_set[0].lower() == 'unit':
            unit = instruction_set[1].lower()
    new_disk(size, path, fit, unit)

def new_disk(size: int, path: str, fit: str, unit: str):
    size = int(size)
    if unit.lower() == 'k':
        no_bytes = size * 1024 
        print(no_bytes) 
    elif unit.lower() == 'm':
        no_bytes = size * 1024 * 1024
        print(no_bytes)  
    else:
        raise ValueError("El tipo debe ser 'k' o 'm'")
    
    mbr_date = time.strftime('%Y-%m-%d %H:%M:%S')
    mbr_dsk_signature = random.randint(0, 2**32 - 1) 
    mbr = MBR(no_bytes, mbr_date, mbr_dsk_signature, fit)

    size_in_bytes = bytes([mbr.size])
    size_in_hex = size_in_bytes.hex()
    date_in_bytes = bytes([mbr.date])
    date_in_hex = date_in_bytes.hex()
    signature_in_bytes = bytes([mbr.signature])
    signature_in_hex = signature_in_bytes.hex()
    fit_in_bytes = bytes([mbr.fit])
    fit_in_hex = fit_in_bytes.hex()
    print(size_in_hex, date_in_hex, signature_in_hex, fit_in_hex)

    
    with open(os.path.join(path, 'mi_disco.dsk'), 'wb') as archivo:
        archivo.write(b'\x00' * no_bytes)  
        archivo.seek(0)
        #archivo.write(mbr_data)
        #archivo.write(mbr_data2)
    
    


path = 'execute -path=/home/chocs/Desktop/Calificacion.adsj'

start()


