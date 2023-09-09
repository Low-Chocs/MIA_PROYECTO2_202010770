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
                print(instructions_splitted)
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
   
def get_file_name(path):
    path_to_check = path.split('/')
    last_index = len(path_to_check) - 1
    return path_to_check[last_index]

def check_next_instruction(next_instruction):
    if next_instruction[0].lower() == 'mkdisk':
        mkdisk(next_instruction)
    if next_instruction[0].lower() == 'rmdisk':
        rmdisk(next_instruction)

def mkdisk(instruction):
    #Removes the first element "mkdisk"
    instruction.pop(0)
    size = 0
    path = ""
    fit = 'f'
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

def rmdisk(instruction):
    instruction.pop(0)
    instruction[0] = instruction[0].replace('-', '')
    instruction_set = instruction[0].split('=')
    if instruction_set[0].lower() == 'path':
            path = return_path_with_correct_user(instruction_set[1])
            delete_disk(path)

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
    
    mbr_date = str(time.strftime('%Y-%m-%d %H:%M:%S'))
    mbr_dsk_signature = random.randint(0, 2**32 - 1)
    print(mbr_dsk_signature) 
    mbr = MBR(no_bytes, mbr_date, mbr_dsk_signature, fit)

    size_in_bytes = mbr.size.to_bytes(4, byteorder = 'big')
    print(size_in_bytes)
    #original_value = int.from_bytes(size_in_bytes, byteorder='big')

    #Imprimir el valor original
    date_in_bytes = mbr.date.encode('UTF-8')
    print(path)
    signature_in_bytes = mbr.signature.to_bytes(4, byteorder = 'big')
    fit_in_bytes = mbr.fit.encode('UTF-8')
    
    print(size_in_bytes, date_in_bytes, signature_in_bytes, fit_in_bytes)

    if os.path.exists(path):
        print("Ya existe un disco con el mismo nombre")
    else:
        print("Se creo el disco")
        with open(path, 'wb') as file:
            file.write(b'\x00' * no_bytes)  
            file.close()
    with open(path, 'rb+') as file:
        
        file.write(size_in_bytes)
        file.seek(4)
        file.write(date_in_bytes)
        file.seek(23)
        file.write(signature_in_bytes)
        file.seek(27)
        file.write(fit_in_bytes)
        file.close()
    
    with open(path, 'rb') as file:
        size_bytes = file.read(4)
        if len(size_bytes) != 4:
            print("No se pudieron leer los primeros 4 bytes.")
        size = int.from_bytes(size_bytes, byteorder='big')
        
        date_bytes = file.read(19)
        if len(date_bytes) != 19:
            print("No se pudieron leer los siguientes 19 bytes.")
        date = date_bytes.decode('utf-8')
        
        signature_bytes = file.read(4)
        if len(signature_bytes) != 4:
            print("No se pudieron leer los siguientes 4 bytes.")
        signature = int.from_bytes(signature_bytes, byteorder='big')
        
        fit_bytes = file.read(1)
        if len(fit_bytes) != 1:
            print("No se pudo leer el último byte.")
        fit = fit_bytes.decode('utf-8')
        
        print("Datos recuperados del disco:")
        print(f"Tamaño: {size}")
        print(f"Fecha y hora: {date}")
        print(f"Firma (entero): {signature}")
        print(f"Ajuste: {fit}")
    




def delete_disk(path: str):
    try:
        os.remove(path)
        print(f"El archivo {path} ha sido eliminado correctamente.")
    except FileNotFoundError:
        print(f"El archivo {path} no se encontró.")
    except Exception as e:
        print(f"Se produjo un error al eliminar el archivo: {str(e)}")

path = 'execute -path=/home/chocs/Desktop/Calificacion.adsj'

print(get_file_name('home/chocs/Desktop/Calificacion.adsj'))

start()


