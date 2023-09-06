import os

def start():
    is_on_run = True
    while is_on_run:
        command = input("Ingresar texto (1 para salir): ")
        if command == '1':
            is_on_run = False
            continue
        command_splitted = command.split()
        if command_splitted[0] == 'execute':
            path = command_splitted[1].split('=')
            print(path[0])
            open_file(path[1])
        else:
            print('No se reconoció el comando')
    

def open_file(path: str):
    try:
        with open(path, 'r') as search_file:
            line_commands = search_file.readlines()
            for instruction in line_commands:
                check_next_instruction(instruction)
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

def check_next_instruction(next_instruction: str):
    #next_instruction_splitted = next_instruction.split()
    print(next_instruction)    
    

path = '-path=/home/Desktop/calificacion.adsj'
path = check_file_extension(path)
start()


