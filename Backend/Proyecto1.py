import os
from Estructuras import *
import random
import time
import struct
import traceback

mounted_list = []

def start():
    is_on_run = True
    while is_on_run:
        command = input("Ingresar texto (1 para salir): ")
        if command == '':
            continue
        if command == '1':
            is_on_run = False
            continue
        print(command)
        command_splitted = command.split()
        if command_splitted[0].lower() == 'execute':
            path = command_splitted[1].split('=')
            path[1] = return_path_with_correct_user(path[1])
            open_file(path[1])
        if command_splitted[0].lower() == 'mount':
            print_mount()
        else:
            print(f'No se reconoció el comando {command_splitted[0]}')
            
    

def open_file(path: str):
    try:
        with open(path, 'r') as search_file:
            line_number = 0  # Inicializamos un contador de línea
            for instruction in search_file:
                line_number += 1  # Incrementamos el contador de línea
                if instruction == "":
                    print(f"Línea en blanco (Línea {line_number})")
                index = instruction.find("#")
                if index != -1:
                    text_after_hash = instruction[index + 1:].strip()
                    print(f"Comentario: {text_after_hash} (Línea {line_number})")
                instructions_splitted = instruction.split()
                #print(instructions_splitted)
                check_next_instruction(instructions_splitted)

    except FileNotFoundError:
        print("El archivo no se encontró en la ruta especificada.")
    except Exception as e:
        print(f"Ocurrió un error en la línea {line_number}: {e}")
        traceback.print_exc() 

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

def check_file_name(path):
    path_to_check = path.split('/')
    last_index = len(path_to_check) - 1
    return path_to_check[last_index].split('.')[0]


def verify_existance(path):
    directory = os.path.dirname(path)  # Obtiene el directorio del camino
    if not os.path.exists(directory):  # Verifica si el directorio no existe
        try:
            os.makedirs(directory)  # Crea el directorio y todos los directorios intermedios si no existen
            print(f"Directorio '{directory}' creado con éxito.")
        except OSError as e:
            print(f"Error al crear el directorio '{directory}': {str(e)}")

    if not os.path.exists(path):  # Verifica si el camino no existe
        try:
            with open(path, 'w'):
                pass  # Crea un archivo vacío si el camino no existe
            print(f"Archivo '{path}' creado con éxito.")
        except OSError as e:
            print(f"Error al crear el archivo '{path}': {str(e)}")
    else:
        print()


def verify_existance2(path):
    path = os.path.dirname(path)
    if not os.path.exists(path):  # Verifica si el camino no existe
        try:
            with open(path, 'w'):
                pass  # Crea un archivo vacío si el camino no existe
            #os.makedirs(path)
            print(f"Archivo '{path}' creado con éxito.")
        except OSError as e:
            print(f"Error al crear el archivo '{path}': {str(e)}")
    else:
        print(f"El archivo o directorio '{path}' ya existe.")
   
def get_file_name(path):
    path_to_check = path.split('/')
    last_index = len(path_to_check) - 1
    return path_to_check[last_index]

def quit_name(path):
    path_to_check = path.split('/')
    last_index = len(path_to_check) - 1
    return path_to_check[last_index]

def check_next_instruction(next_instruction):
    if next_instruction[0].lower() == 'mkdisk':
        print("Instrucción: Mkdisk")
        mkdisk(next_instruction)
    if next_instruction[0].lower() == 'rmdisk':
        print("Instrucción: Rmdisk")
        rmdisk(next_instruction)
    if next_instruction[0].lower() == 'fdisk':
        print("Instrucción: Fdisk")
        fdisk(next_instruction)
    if next_instruction[0].lower() == 'mount':
        print("Instrucción: Mount")
        Mount(next_instruction)
    if next_instruction[0].lower() == 'unmount':
        print("Instrucción: Unmount")
        unmount(next_instruction)
    if next_instruction[0].lower() == 'rep':
        print("Instrucción: Rep")
        rep(next_instruction)
    if next_instruction[0].lower() == 'pause':
        input("Estamos en pausa")




def rep(instruction):
    #Removes the first element "mkdisk"
    instruction.pop(0)
    path = ""
    id = 'f'
    route = 'm'
    name = ""
    for i in range(len(instruction)):
        instruction[i] = instruction[i].replace('-', '')
        instruction_set = instruction[i].split('=')
        if instruction_set[0].lower() == 'name':
            name = instruction_set[1]
        elif instruction_set[0].lower() == 'path':
            path = return_path_with_correct_user(instruction_set[1])
        elif instruction_set[0].lower() == 'id':
            id = instruction_set[1].lower()
        elif instruction_set[0].lower() == 'ruta':
            route = instruction_set[1].lower()
        else:
            print(f"Error no se reconocio el comando {instruction_set[0]}")
            return
    reports(name, path, id, route)


def reports(name, path, id, route):
    if name.lower() == 'mbr':
        mbr_report(name, path, id, route)
        return
    if name.lower() == 'disk':
        disk_report(name, path, id, route)
        return
    


def mbr_report(name, path, id, route):
    print("Estamos aca")
    mounty = check_mounted(id)
    if mounty == None:
        return
    mbr = MBR(0,0,0,0)
    mbr.read_mbr(mounty.path)
    file_name = os.path.basename(path)
    mbr.mbr_report(path, file_name, mounty.path)

def disk_report(name, path, id, route):
    mounty = check_mounted(id)
    if mounty == None:
        return
    mbr = MBR(0,0,0,0)
    mbr.read_mbr(mounty.path)
    file_name = os.path.basename(path)
    mbr.graph_disk(path, file_name, mounty.path)


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
        elif instruction_set[0].lower() == 'path':
            path = return_path_with_correct_user(instruction_set[1])
        elif instruction_set[0].lower() == 'fit':
            fit = instruction_set[1].lower()
        elif instruction_set[0].lower() == 'unit':
            unit = instruction_set[1].lower()
        else:
            print(f"Error no se reconocio el comando {instruction_set[0]}")
            return
    new_disk(size, path, fit, unit)

def rmdisk(instruction):
    instruction.pop(0)
    instruction[0] = instruction[0].replace('-', '')
    instruction_set = instruction[0].split('=')
    if instruction_set[0].lower() == 'path':
            path = return_path_with_correct_user(instruction_set[1])
            delete_disk(path)
    else:
        print(f"Error no se reconocio el comando {instruction_set[0]}")
        return

def unmount(instruction):
    instruction.pop(0)
    instruction[0] = instruction[0].replace('-', '')
    instruction_set = instruction[0].split('=')
    print(instruction_set[0].lower())
    if instruction_set[0].lower() == 'id':
            name = return_path_with_correct_user(instruction_set[1])
            unmounted(name)
    else:
        print(f"Error no se reconocio el comando {instruction_set[0]}")
        return
    
def Mount(instruction):
    #Removes the first element "mkdisk"
    instruction.pop(0)
    name = ""
    path = ""
    for i in range(len(instruction)):
        instruction[i] = instruction[i].replace('-', '')
        instruction_set = instruction[i].split('=')
        if instruction_set[0].lower() == 'path':
            path = return_path_with_correct_user(instruction_set[1])
        elif instruction_set[0].lower() == 'name':
            name = instruction_set[1].lower()
        else:
            print(f"Error no se reconocio el comando {instruction_set[0]}")
            return
    mount(path, name)

def new_disk(size: int, path: str, fit: str, unit: str):
    size = int(size)
    if unit.lower() == 'k':
        no_bytes = size * 1024 
        #print(no_bytes) 
    elif unit.lower() == 'm':
        no_bytes = size * 1024 * 1024
        #print(no_bytes)  
    else:
        raise ValueError("El tipo debe ser 'k' o 'm'")
    
    mbr_date = str(time.strftime('%Y-%m-%d %H:%M:%S'))
    mbr_dsk_signature = random.randint(0, 2**32 - 1)
    #print(mbr_dsk_signature) 
    mbr = MBR(no_bytes, mbr_date, mbr_dsk_signature, fit)

    size_in_bytes = mbr.size.to_bytes(4, byteorder = 'big')
    #print(size_in_bytes)

    date_in_bytes = mbr.date.encode('UTF-8')
    #print(path)
    signature_in_bytes = mbr.signature.to_bytes(4, byteorder = 'big')
    fit_in_bytes = mbr.fit.encode('UTF-8')
    
    #print(size_in_bytes, date_in_bytes, signature_in_bytes, fit_in_bytes)

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
    #print("LOgramos entrar")
    #print(instruction)
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
            verify_existance(path)
            print(path)
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
        #print(no_bytes) 
    elif unit.lower() == 'm':
        no_bytes = size * 1024 * 1024
        #print(no_bytes) 
    elif unit.lower() == 'b':
        no_bytes = size
        #print(no_bytes)
    else:
        raise ValueError("El tipo debe ser 'k' o 'm'")
    if delete != 0:
        print(f"Se procedera eliminar {path}, la particion {name}")
        mbr = MBR(0,0,0,0)
        mbr.delete_partition(path, name)
        return
    if new_add != 0:
        print(f"Se procedera a agregar {new_add} en la ruta: {path} con el nombre: {name}")
        return
    
    mbr = MBR(0,0,0,0)
    mbr.read_mbr(path)
    #if mbr.get_initial_logic_start() != 0:
     #  print("Si")
    # mbr.load_ebr(path)
    mbr.insert_partition('B', type, fit, 50, no_bytes, name, path)
    #mbr.look_on_start()



def mount(path: str, name:str):
    mbr = MBR(0,0,0,0)
    mbr.read_mbr(path)
    partition_number = mbr.look_on_partition(name)
    if partition_number == 2:
        partition_number = 1
    print(partition_number)
    if partition_number == "0":
        print("No se encontro la particion deseada")
        return
    disk_name = check_file_name(path)
    id = "70"+partition_number+disk_name
    print("Se montara la particion: "+id)
    mount = Mounty_python(disk_name, id ,path)
    mounted_list.append(mount)
    
def print_mount():
    count = 0
    for i in mounted_list:
        count += 1
        print(f"Nombre del disco {i.name} Id del disco {i.id} Path {i.path}")
    if count == 0:
        print("No hay particiones montadas")


def check_mounted(name: str):
    for i in mounted_list:
        if name.lower() == i.id.lower():
            print(f"Nombre del disco {i.name} Id del disco {i.id} Path {i.path}")
            return i
    print(f"ERROR: No se encontro ese mount con el id: {name}")

def unmounted(name: str):
    for i in range(len(mounted_list)):
        if name.lower() == mounted_list[i].id.lower():
            print(f"Se desmontara el disco {mounted_list[i].name} Id del disco {mounted_list[i].id} Path {mounted_list[i].path}")
            mounted_list.pop(i)
            return
    print(f"ERROR: No se encontro ese mount con el id: {name}")


path = 'execute -path=/home/chocs/Downloads/ArchivosdeEntrada2S2023/Parte1/1_crear_discos.adsj'
path2= 'execute -path=/home/chocs/Downloads/ArchivosdeEntrada2S2023/Parte1/2_crear_particiones.adsj'
path3 = 'execute -path=/home/chocs/Downloads/ArchivosdeEntrada2S2023/Parte1/3_montar_particiones.adsj'
path5 = 'execute -path=/home/chocs/Downloads/ArchivosdeEntrada2S2023/Parte1/5_eliminar_particiones_discos.adsj'
path4 = 'execute -path=/home/chocs/Downloads/ArchivosdeEntrada2S2023/Parte1/6_reportes_parte_1.adsj'
#print(quit_quote("/home/mis discos/Disco4.dsk"))
#print(get_file_name('home/chocs/Desktop/Calificacion.adsj'))

start()


