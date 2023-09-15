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

def quit_quote(path: str):
    path.replace("\"", "")
    return path

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
    if next_instruction[0].lower() == 'fdisk':
        fdisk(next_instruction)

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

    date_in_bytes = mbr.date.encode('UTF-8')
    print(path)
    signature_in_bytes = mbr.signature.to_bytes(4, byteorder = 'big')
    fit_in_bytes = mbr.fit.encode('UTF-8')
    
    print(size_in_bytes, date_in_bytes, signature_in_bytes, fit_in_bytes)

    mbr_part_status = mbr.partition1.part_status.encode('UTF-8')
    mbr_part_type = mbr.partition1.part_type.encode('UTF-8')
    mbr_part_fit = mbr.partition1.part_fit.encode('UTF-8')
    mbr_part_start = mbr.partition1.part_start.to_bytes(4, byteorder = 'big')
    mbr_size = mbr.partition1.part_size.to_bytes(4, byteorder = 'big')
    mbr_name = mbr.partition1.part_name.encode('UTF-8')
    array_of_bytes = bytearray()
    array_of_bytes += mbr_part_status
    array_of_bytes += mbr_part_type
    array_of_bytes += mbr_part_fit
    array_of_bytes += mbr_part_start
    array_of_bytes += mbr_size
    array_of_bytes += mbr_name

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
        #Continuar desde 28
        file.seek(28)
        file.write(array_of_bytes)
        file.seek(55)
        file.write(array_of_bytes)
        file.seek(82)
        file.write(array_of_bytes)
        file.seek(109)
        file.write(array_of_bytes)
        
        #136 final del mbr 27 por cada mbr

        
        file.close()
    
    mbr.read_mbr(path)
    




def delete_disk(path: str):
    try:
        os.remove(path)
        print(f"El archivo {path} ha sido eliminado correctamente.")
    except FileNotFoundError:
        print(f"El archivo {path} no se encontró.")
    except Exception as e:
        print(f"Se produjo un error al eliminar el archivo: {str(e)}")

def fdisk(instruction):
    print("LOgramos entrar")
    print(instruction)
    size = 0
    path = ""
    fit = 'w'
    unit = 'k'
    delete = 0
    type = 'P'
    add = 0
    instruction.pop(0)
    for i in range(len(instruction)):
        instruction[i] = instruction[i].replace('-', '')
        instruction_set = instruction[i].split('=')
        if instruction_set[0].lower() == 'path':
            path = return_path_with_correct_user(instruction_set[1])
        if instruction_set[0].lower() == 'size':
            size = instruction_set[1]
        if instruction_set[0].lower() == 'name':
            name = instruction_set[1]
        if instruction_set[0].lower() == 'unit':
            unit = instruction_set[1]
        if instruction_set[0].lower() == 'type':
            type = instruction_set[1]
        if instruction_set[0].lower() == 'fit':
            fit = instruction_set[1]
        if instruction_set[0].lower() == 'delete':
            delete = instruction_set[1]
        if instruction_set[0].lower() == 'add':
            new_add = instruction_set[1]
    new_partition(size, path, name, unit, type, fit, delete, add)
    
def new_partition(size: str, path: str, name: str, unit: str, type: str, fit: str, delete: str, new_add: int):
    size = int(size)
    if unit.lower() == 'k':
        no_bytes = size * 1024 
        print(no_bytes) 
    elif unit.lower() == 'm':
        no_bytes = size * 1024 * 1024
        print(no_bytes) 
    elif unit.lower() == 'b':
        no_bytes = size
        print(no_bytes)
    else:
        raise ValueError("El tipo debe ser 'k' o 'm'")
    if delete != 0:
        print("Se procedera eliminar {path}, la particion {name}")
        return
    if new_add != 0:
        print("Se procedera a agregar {new_add} en la ruta: {path} con el nombre: {name}")
        return
    
    mbr = MBR(0,0,0,0)
    mbr.read_mbr(path)
    mbr.insert_partition('B', type, fit, 50, size, name, path)
    
path = 'execute -path=/home/chocs/Desktop/Calificacion.adsj'

print(quit_quote("/home/mis discos/Disco4.dsk"))
print(get_file_name('home/chocs/Desktop/Calificacion.adsj'))

start()


