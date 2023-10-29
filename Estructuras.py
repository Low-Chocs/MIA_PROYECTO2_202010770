import struct
import subprocess
class MBR():
    
    def __init__(self, size, date, signature, fit):
        self.size = size
        self.date = date
        self.signature = signature
        self.fit = fit
        #Status E = Empty, B = Busy and unmounted, D = Deleted, M = Busy and mounted
        self.partition1 = partition('E','I','I',0,0,'0000000000000000')
        self.partition2 = partition('E','I','I',0,0,'0000000000000000')
        self.partition3 = partition('E','I','I',0,0,'0000000000000000')
        self.partition4 = partition('E','I','I',0,0,'0000000000000000')
        self.linked_ebr_list = LinkedList()
    
        self.actual_start = 137
        self.space = 0

    def available_space(self, temp_size):
        available_space = self.size - (self.space + temp_size)
        return available_space
    
    def look_on_start(self):
        if self.partition1.part_status.upper() == 'E':
            print("Empieza por particion 1")
            return
        if self.partition2.part_status.upper() == 'E':
            self.actual_start = (137 + self.partition1.part_size)
            print(f"Empieza por particion 2 {self.actual_start}")
            return
        if self.partition3.part_status.upper() == 'E':
            self.actual_start = (137 + self.partition1.part_size + self.partition2.part_size)
            print(f"Empieza en particion 3 {self.actual_start}")
            return
        if self.partition4.part_status.upper() == 'E':
            self.actual_start = (137 + self.partition1.part_size + self.partition2.part_size + self.partition3.part_size)
            print(f"Empieza en particion4 {self.actual_start}")
            return

    def look_on_operation(self):
        if self.partition1.part_status.upper() == 'E':
            return 0
        if self.partition2.part_status.upper() == 'E':
            return self.partition1.part_size + self.partition1.part_start
        if self.partition3.part_status.upper() == 'E':
            return self.partition2.part_size + self.partition2.part_start
        if self.partition4.part_status.upper() == 'E':
            return self.partition3.part_size + self.partition3.part_start
        else:
            return self.partition4.part_size + self.partition4.part_start

    def look_on_partition(self, name:str):
        print(name, self.partition2.part_name)
        name = name.lower().ljust(16)
        if self.partition1.part_name.lower() == name:
            print("Se encontro el mount en la particion 1")
            return "1"
        if self.partition2.part_name.lower() == name:
            print("Se encontro el mount en la particion 2")
            return "2"
        if self.partition4.part_name.lower() == name:
            print("Se encontro el mount en la particion 3")
            return "3"
        if self.partition4.part_name.lower() == name:
            print("Se encontro el mount en la particion 4")
            return "4"
        return "0"

    def write_mbr_for_partitions(self, path):

        mbr_part_status = self.partition1.part_status.encode('UTF-8')
        mbr_part_type = self.partition1.part_type.encode('UTF-8')
        mbr_part_fit = self.partition1.part_fit.encode('UTF-8')
        mbr_part_start = self.partition1.part_start.to_bytes(4, byteorder = 'big')
        mbr_size = self.partition1.part_size.to_bytes(4, byteorder = 'big')
        mbr_name = self.partition1.part_name.encode('UTF-8')

        mbr_part_status_2 = self.partition2.part_status.encode('UTF-8')
        mbr_part_type_2 = self.partition2.part_type.encode('UTF-8')
        mbr_part_fit_2 = self.partition2.part_fit.encode('UTF-8')
        mbr_part_start_2 = self.partition2.part_start.to_bytes(4, byteorder = 'big')
        mbr_size_2 = self.partition2.part_size.to_bytes(4, byteorder = 'big')
        mbr_name_2 = self.partition2.part_name.encode('UTF-8')

        mbr_part_status_3 = self.partition3.part_status.encode('UTF-8')
        mbr_part_type_3 = self.partition3.part_type.encode('UTF-8')
        mbr_part_fit_3 = self.partition3.part_fit.encode('UTF-8')
        mbr_part_start_3 = self.partition3.part_start.to_bytes(4, byteorder = 'big')
        mbr_size_3 = self.partition3.part_size.to_bytes(4, byteorder = 'big')
        mbr_name_3 = self.partition3.part_name.encode('UTF-8')

        mbr_part_status_4 = self.partition4.part_status.encode('UTF-8')
        mbr_part_type_4 = self.partition4.part_type.encode('UTF-8')
        mbr_part_fit_4 = self.partition4.part_fit.encode('UTF-8')
        mbr_part_start_4 = self.partition4.part_start.to_bytes(4, byteorder = 'big')
        mbr_size_4 = self.partition4.part_size.to_bytes(4, byteorder = 'big')
        mbr_name_4 = self.partition4.part_name.encode('UTF-8')

        array_of_bytes = bytearray()
        array_of_bytes += mbr_part_status
        array_of_bytes += mbr_part_type
        array_of_bytes += mbr_part_fit
        array_of_bytes += mbr_part_start
        array_of_bytes += mbr_size
        array_of_bytes += mbr_name

        array_of_bytes += mbr_part_status_2
        array_of_bytes += mbr_part_type_2
        array_of_bytes += mbr_part_fit_2
        array_of_bytes += mbr_part_start_2
        array_of_bytes += mbr_size_2
        array_of_bytes += mbr_name_2

        array_of_bytes += mbr_part_status_3
        array_of_bytes += mbr_part_type_3
        array_of_bytes += mbr_part_fit_3
        array_of_bytes += mbr_part_start_3
        array_of_bytes += mbr_size_3
        array_of_bytes += mbr_name_3

        array_of_bytes += mbr_part_status_4
        array_of_bytes += mbr_part_type_4
        array_of_bytes += mbr_part_fit_4
        array_of_bytes += mbr_part_start_4
        array_of_bytes += mbr_size_4
        array_of_bytes += mbr_name_4

        with open(path, 'rb+') as file:
            file.seek(28)
            file.write(array_of_bytes)
            file.close()

    def print_mbr(self):
        print("Datos recuperados del disco:")
        print(f"Tamaño: {self.size}")
        print(f"Fecha y hora: {self.date}")
        print(f"Firma (entero): {self.signature}")
        print(f"Ajuste: {self.fit}")

        print(f"Particion 1 Status: {self.partition1.part_status}")
        print(f"Particion 1 Tipo: {self.partition1.part_type}")
        print(f"Particion 1 Fit: {self.partition1.part_fit}")
        print(f"Particion 1 Inicio: {self.partition1.part_start}")
        print(f"Particion 1 Tamaño: {self.partition1.part_size}")
        print(f"Particion 1 Nombre: {self.partition1.part_name}")

        print(f"Particion 2 Status: {self.partition2.part_status}")
        print(f"Particion 2 Tipo: {self.partition2.part_type }")
        print(f"Particion 2 Fit: {self.partition2.part_fit}")
        print(f"Particion 2 Inicio: {self.partition2.part_start}")
        print(f"Particion 2 Tamaño: {self.partition2.part_size}")
        print(f"Particion 2 Nombre: {self.partition2.part_name}")

        print(f"Particion 3 Status: {self.partition3.part_status}")
        print(f"Particion 3 Tipo: {self.partition3.part_type }")
        print(f"Particion 3 Fit: {self.partition3.part_fit}")
        print(f"Particion 3 Inicio: {self.partition3.part_start}")
        print(f"Particion 3 Tamaño: {self.partition3.part_size}")
        print(f"Particion 3 Nombre: {self.partition3.part_name}")
        
        print(f"Particion 4 Status: {self.partition4.part_status}")
        print(f"Particion 4 Tipo: {self.partition4.part_type }")
        print(f"Particion 4 Fit: {self.partition4.part_fit}")
        print(f"Particion 4 Inicio: {self.partition4.part_start}")
        print(f"Particion 4 Tamaño: {self.partition4.part_size}")
        print(f"Particion 4 Nombre: {self.partition4.part_name}")

    def read_mbr(self, path: str):
        with open(path, 'rb') as file:
            size_bytes = file.read(4)
            if len(size_bytes) != 4:
                print("No se pudieron leer los primeros 4 bytes.")
            self.size = int.from_bytes(size_bytes, byteorder='big')
    
            date_bytes = file.read(19)
            if len(date_bytes) != 19:
                print("No se pudieron leer los siguientes 19 bytes.")
            self.date = date_bytes.decode('utf-8')
    
            signature_bytes = file.read(4)
            if len(signature_bytes) != 4:
                print("No se pudieron leer los siguientes 4 bytes.")
            self.signature = int.from_bytes(signature_bytes, byteorder='big')
    
            fit_bytes = file.read(1)
            if len(fit_bytes) != 1:
                print("No se pudo leer el último byte.")
            self.fit = fit_bytes.decode('utf-8')
    
            

            #PARTITION 1
            char1 = file.read(1).decode('utf-8')
            char2 = file.read(1).decode('utf-8')
            char3 = file.read(1).decode('utf-8')
            int1_bytes = file.read(4)
            int2_bytes = file.read(4)
            char16_bytes = file.read(16)

            if len(char16_bytes) != 16:
                print("No se pudieron leer los siguientes 16 bytes.")
        
            self.partition1.part_status = char1
            self.partition1.part_type = char2
            self.partition1.part_fit = char3
            self.partition1.part_start = int.from_bytes(int1_bytes, byteorder='big')
            self.partition1.part_size = int.from_bytes(int2_bytes, byteorder='big')
            self.partition1.part_name = char16_bytes.decode('utf-8')

            #PARTITION 2
            char1_2 = file.read(1).decode('utf-8')
            char2_2 = file.read(1).decode('utf-8')
            char3_2 = file.read(1).decode('utf-8')
            int1_bytes_2 = file.read(4)
            int2_bytes_2 = file.read(4)
            char16_bytes_2 = file.read(16)

            if len(char16_bytes_2) != 16:
                print("No se pudieron leer los siguientes 16 bytes.")

            self.partition2.part_status = char1_2
            self.partition2.part_type = char2_2
            self.partition2.part_fit = char3_2
            self.partition2.part_start = int.from_bytes(int1_bytes_2, byteorder='big')
            self.partition2.part_size = int.from_bytes(int2_bytes_2, byteorder='big')
            self.partition2.part_name = char16_bytes_2.decode('utf-8')

        
            #PARTITION 3
            char1_3 = file.read(1).decode('utf-8')
            char2_3 = file.read(1).decode('utf-8')
            char3_3 = file.read(1).decode('utf-8')
            int1_bytes_3 = file.read(4)
            int2_bytes_3 = file.read(4)
            char16_bytes_3 = file.read(16)

            if len(char16_bytes_3) != 16:
                print("No se pudieron leer los siguientes 16 bytes.")

            self.partition3.part_status = char1_3
            self.partition3.part_type = char2_3
            self.partition3.part_fit = char3_3
            self.partition3.part_start = int.from_bytes(int1_bytes_3, byteorder='big')
            self.partition3.part_size = int.from_bytes(int2_bytes_3, byteorder='big')
            self.partition3.part_name = char16_bytes_3.decode('utf-8')

            #PARTITION 4
            char1_4 = file.read(1).decode('utf-8')
            char2_4 = file.read(1).decode('utf-8')
            char3_4 = file.read(1).decode('utf-8')
            int1_bytes_4 = file.read(4)
            int2_bytes_4 = file.read(4)
            char16_bytes_4 = file.read(16)

            if len(char16_bytes_4) != 16:
                print("No se pudieron leer los siguientes 16 bytes.")

            self.partition4.part_status = char1_4
            self.partition4.part_type = char2_4
            self.partition4.part_fit = char3_4
            self.partition4.part_start = int.from_bytes(int1_bytes_4, byteorder='big')
            self.partition4.part_size = int.from_bytes(int2_bytes_4, byteorder='big')
            self.partition4.part_name = char16_bytes_4.decode('utf-8')
    
    def is_one_extended_partition_on_disk(self):
        if self.partition1.part_type.lower() == 'e':
            return False
        if self.partition2.part_type.lower() == 'e':
            return False
        if self.partition3.part_type.lower() == 'e':
            return False
        if self.partition4.part_type.lower() == 'e':
            return False
        return True
    
    def insert_partition(self, part_status, part_type, part_fit, part_start, part_size, part_name, path):
        if part_type.lower() == 'e':
            if not self.is_one_extended_partition_on_disk():
                print("Ya existe una particion extendida en el disco")
                return
        if self.perfect_fit(part_status, part_type, part_fit, part_size, part_name.ljust(16), path):
            return
        if self.available_space(part_size) < 0:
            print("No se pudo crear por espacio")
            return
        if len(part_name) < 16:
            part_name = part_name.ljust(16)
        #Status E = Empty, B = Busy and unmounted, D = Deleted, M = Busy and mounted
        self.look_on_start()
        self.space += part_size
        part_start = self.actual_start 
        
        if part_type.lower() == 'l':
            #self.create_logic_partition(part_status, part_fit, self.linked_ebr_list.total_size(), part_size, 0, part_name, path)
            if self.get_initial_logic_start() == 0:
                print("NO se puede crear una particion logica si no hay una extendida")
                return
            print("Se procedera  crear una particion logica")
            self.logic_partition("U", part_fit, part_start,  part_size, 0, part_name.ljust(16), path, 1)
            self.read_mbr(path)
            return
            


        if self.partition1.part_status.lower() == 'e':
            self.partition1.part_status = part_status
            self.partition1.part_type = part_type
            self.partition1.part_fit = part_fit
            self.partition1.part_start = part_start
            self.partition1.part_size = part_size
            self.partition1.part_name = part_name
            self.write_mbr_for_partitions(path)
            if part_type.lower() == 'e':
                self.logic_partition("N", "I", part_start,  0, 0,  "0000000000000000", path, 0)
                print("Se ha creado una partición extendida")
            #self.print_mbr()
            return
        if self.partition2.part_status.lower() == 'e':
            self.partition2.part_status = part_status
            self.partition2.part_type = part_type
            self.partition2.part_fit = part_fit
            self.partition2.part_start = part_start
            self.partition2.part_size = part_size
            self.partition2.part_name = part_name
            self.write_mbr_for_partitions(path)
            if part_type.lower() == 'e':
                print("Se creara la extendida")
                self.logic_partition("N", "I", part_start,  0, 0,  "0000000000000000", path, 0)
                print("Se ha creado")
            #self.print_mbr()
            return
        if self.partition3.part_status.lower() == 'e':
            self.partition3.part_status = part_status
            self.partition3.part_type = part_type
            self.partition3.part_fit = part_fit
            self.partition3.part_start = part_start
            self.partition3.part_size = part_size
            self.partition3.part_name = part_name
            self.write_mbr_for_partitions(path)
            if part_type.lower() == 'e':
                print("Se creara la extendida")
                self.logic_partition("N", "I", part_start,  0, 0,  "0000000000000000", path, 0)
                print("Se ha creado")
            #self.print_mbr()
            return
        if self.partition4.part_status.lower() == 'e':
            self.partition4.part_status = part_status
            self.partition4.part_type = part_type
            self.partition4.part_fit = part_fit
            self.partition4.part_start = part_start
            self.partition4.part_size = part_size
            self.partition4.part_name = part_name
            self.write_mbr_for_partitions(path)
            if part_type.lower() == 'e':
                print("Se creara la extendida")
                self.logic_partition('C', 'I', part_start, 0, 0, '0000000000000000', path, 0)
                print("Se ha creado")
            return

        

            
        print("No hay mas particiones disponibles")
    
    #self.partition4 = partition('E','I','I',0,0,'0000000000000000')
    def delete_partition(self, path, name):
        self.read_mbr(path)

        if self.partition1.part_name.lower() == name.lower().ljust(16):
            text_in_zeros = self.bytes_in_zeros(self.partition1.part_size) 
            with open(path, 'rb+') as file:
                file.seek(self.partition1.part_start)
                file.write(text_in_zeros)
                file.close()
            self.partition1.part_name = '0000000000000000'
            self.partition1.part_fit = 'I'
            self.partition1.part_status = 'D'
            self.partition1.part_type = 'I'
            

        if self.partition2.part_name.lower() == name.lower().ljust(16):
            print(self.partition2.part_size)
            text_in_zeros = self.bytes_in_zeros(self.partition2.part_size) 
            with open(path, 'rb+') as file:
                file.seek(self.partition2.part_start)
                file.write(text_in_zeros)
                file.close()
            self.partition2.part_name = '0000000000000000'
            self.partition2.part_fit = 'I'
            self.partition2.part_status = 'D'
            self.partition2.part_type = 'I'

        if self.partition3.part_name.lower() == name.lower().ljust(16):
            print(self.partition3.part_size)
            text_in_zeros = self.bytes_in_zeros(self.partition3.part_size) 
            with open(path, 'rb+') as file:
                file.seek(self.partition3.part_start)
                file.write(text_in_zeros)
                file.close()
            self.partition3.part_name = '0000000000000000'
            self.partition3.part_fit = 'I'
            self.partition3.part_status = 'D'
            self.partition3.part_type = 'I'

        if self.partition4.part_name.lower() == name.lower().ljust(16):
            print(self.partition4.part_size)
            text_in_zeros = self.bytes_in_zeros(self.partition4.part_size) 
            with open(path, 'rb+') as file:
                file.seek(self.partition4.part_start)
                file.write(text_in_zeros)
                file.close()
            self.partition4.part_name = '0000000000000000'
            self.partition4.part_fit = 'I'
            self.partition4.part_status = 'D'
            self.partition4.part_type = 'I'

        if self.get_initial_logic_start() != 0:
            part_to_erase = self.linked_ebr_list.find_ebr_by_name(name.lower().ljust(16))
            self.linked_ebr_list.display()
            if  part_to_erase != None:
                part_to_erase.part_status = "D"
                self.delete_ebr(path, part_to_erase)
                print("Se eliminara la particion logica")
                self.linked_ebr_list.display()
                return
            print("No se encontro la particion logica")
            
            return

        self.write_mbr_for_partitions(path)
        #self.print_mbr()

    
    def bytes_in_zeros(self, size):
        if size < 0:
            raise ValueError("n debe ser un número positivo")
        bytes_value = bytes([0] * size)
        return bytes_value
    
    def verify_deleted_partitions(self):
        counter = []
        if self.partition1.part_status.lower() ==  'd':
            counter.append(1)
        if self.partition2.part_status.lower() ==  'd':
            counter.append(2)
        if self.partition3.part_status.lower() ==  'd':
            counter.append(3)
        if self.partition4.part_status.lower() ==  'd':
            counter.append(4)
        return counter
    
    def more_than_four_partitions(self):
        counter = 4
        if self.partition1.part_status.lower() ==  'e':
            counter -= 1
        if self.partition2.part_status.lower() ==  'e':
            counter -= 1
        if self.partition3.part_status.lower() ==  'e':
            counter -= 1
        if self.partition4.part_status.lower() ==  'e':
            counter -= 1
        return counter
    
    def get_initial_logic_start(self):
        if self.partition1.part_type.lower() ==  'e':
            return self.partition1.part_start
        if self.partition2.part_type.lower() ==  'e':
            return self.partition2.part_start
        if self.partition3.part_type.lower() ==  'e':
            return self.partition3.part_start
        if self.partition4.part_type.lower() ==  'e':
            return self.partition4.part_start
        return 0

    def available_spot_for_partitions(self, partition, space):
        available_space = partition.part_size - space
        return available_space
    
    def first_fit(self, list: list, part_status, part_type, part_fit, part_size, part_name, path):
        first = list[0]
        enough_space = True
        
        if first == 1:
            if self.available_spot_for_partitions(self.partition1, part_size) < 0:
                print("No se ingreso en la particion 1 por espacio")
                enough_space = False
                if len(list) > 1:
                    list.pop(0)
                    first = list[0]
                else:
                    print("No hay espacio suficiente en las particiones")
                    return 
            
            if enough_space:
                self.partition1.part_fit = part_fit
                self.partition1.part_name = part_name
                self.partition1.part_status = part_status
                self.partition1.part_type = part_type
                self.partition1.part_size = part_size
                self.write_mbr_for_partitions(path)
                print(F"{part_name} Se reintegro en la particion 1 (FF)")
                return 
        
        if first == 2:
            enough_space = True
            if self.available_spot_for_partitions(self.partition2, part_size) < 0:
                print("No se ingreso en la particion 2 por espacio")
                enough_space = False
                if len(list) > 1:
                    list.pop(0)
                    first = list[0]
                else:
                    print("No hay espacio suficiente en las particiones")
                    return 
            
            if enough_space:
                self.partition2.part_fit = part_fit
                self.partition2.part_name = part_name
                self.partition2.part_status = part_status
                self.partition2.part_type = part_type
                self.partition2.part_size = part_size
                self.write_mbr_for_partitions(path)
                print("Se reintegro en la particion 2 (FF)")
                return 
        
        if first == 3:
            enough_space = True
            if self.available_spot_for_partitions(self.partition3, part_size) < 0:
                print("No se ingreso en la particion 3 por espacio")
                enough_space = False
                if len(list) > 1:
                    list.pop(0)
                    first = list[0]
                else:
                    print("No hay espacio suficiente en las particiones")
                    return 
            
            if enough_space:
                self.partition3.part_fit = part_fit
                self.partition3.part_name = part_name
                self.partition3.part_status = part_status
                self.partition3.part_type = part_type
                self.partition3.part_size = part_size
                self.write_mbr_for_partitions(path)
                print("Se reintegro en la particion 3 (FF)")
                return 
        
        if first == 4:
            enough_space = True
            if self.available_spot_for_partitions(self.partition4, part_size) < 0:
                print("No se ingreso en la particion 4 por espacio")
                enough_space = False
                if len(list) > 1:
                    list.pop(0)
                    first = list[0]
                else:
                    print("No hay espacio suficiente en las particiones")
                    return 
            
            if enough_space:
                self.partition4.part_fit = part_fit
                self.partition4.part_name = part_name
                self.partition4.part_status = part_status
                self.partition4.part_type = part_type
                self.partition4.part_size = part_size
                self.write_mbr_for_partitions(path)
                print("Se reintegro en la particion 4 (FF)")
                return 
            
    def best_worst_fit(self, part_status, part_type, part_fit, part_size, part_name, path, state):
        first = self.ordered_list_with_value(part_size, state)
        for i in first:
            print("Valor", i.pos, i.value)
        if len(first) <= 1 :
            print("No hay particiones disponibles para hacer fit")
            return
        for i in range(len(first)):
            if first[i].value <= 0:
                print(f"NO hay espacio disponible para la particion {i}")
                continue
            if first[i].pos == 1:
                self.partition1.part_fit = part_fit
                self.partition1.part_name = part_name
                self.partition1.part_status = part_status
                self.partition1.part_type = part_type
                self.partition1.part_size = part_size
                self.write_mbr_for_partitions(path)
                print(F"{part_name} Se reintegro en la particion 1 (BF)")
                return
            if first[i].pos == 2:
                self.partition2.part_fit = part_fit
                self.partition2.part_name = part_name
                self.partition2.part_status = part_status
                self.partition2.part_type = part_type
                self.partition2.part_size = part_size
                self.write_mbr_for_partitions(path)
                print(F"{part_name} Se reintegro en la particion 2 (BF)")
                return
            if first[i].pos == 3:
                self.partition3.part_fit = part_fit
                self.partition3.part_name = part_name
                self.partition3.part_status = part_status
                self.partition3.part_type = part_type
                self.partition3.part_size = part_size
                self.write_mbr_for_partitions(path)
                print(F"{part_name} Se reintegro en la particion 3 (BF)")
                return
            if first[i].pos == 4:
                self.partition4.part_fit = part_fit
                self.partition4.part_name = part_name
                self.partition4.part_status = part_status
                self.partition4.part_type = part_type
                self.partition4.part_size = part_size
                self.write_mbr_for_partitions(path)
                print(F"{part_name} Se reintegro en la particion 4(BF)")
                return

        
        enough_space = True
        print(list)

    def ordered_list_with_value(self, size, state):
        print(f"He entrado aqui {self.partition1.part_status}")
        counter = []
        if self.partition1.part_status.lower() ==  'd':
            counter.append(in_Order(1, self.partition1.part_size - size))
        if self.partition2.part_status.lower() ==  'd':
            counter.append(in_Order(2, self.partition2.part_size - size))
        if self.partition3.part_status.lower() ==  'd':
            counter.append(in_Order(3, self.partition3.part_size - size))
        if self.partition4.part_status.lower() ==  'd':
            counter.append(in_Order(4, self.partition4.part_size - size))
        if state == 'normal':
            ordered_value = sorted(counter, key=lambda x: x.value)
        if state == 'inverted':
            ordered_value = sorted(counter, key=lambda x: x.value, reverse=True)
        return ordered_value



    def perfect_fit(self, part_status, part_type, part_fit, part_size, part_name, path):
       
        if self.more_than_four_partitions() != 4:
            return False
        if len(self.verify_deleted_partitions()) <= 1:
            return False
        
        if self.fit.lower() == 'b':
            print("Se hara en best fit")
            self.best_worst_fit(part_status, part_type, part_fit,  part_size, part_name, path, 'normal')
            print(self.print_mbr())
            return True
        if self.fit.lower() == 'w':
            print("Se hara en worst fit")
            self.best_worst_fit(part_status, part_type, part_fit, part_size, part_name, path, 'inverted')
            print(self.print_mbr())
            return True
        if self.fit.lower() == 'f':
            print("Se hara en first fit")
            self.first_fit(self.verify_deleted_partitions(), part_status, part_type, part_fit, part_size, part_name, path)
            #print(self.print_mbr())
            return True

    def load_ebr(self, path):
        start = self.get_initial_logic_start()
        print(start)
        is_next_one = True
        with open(path, 'rb+') as file:
            #for i in range(self.linked_ebr_list.how_long()):
            while is_next_one:
                file.seek(start)
                part_status = file.read(1).decode('utf-8')  
                part_fit = file.read(1).decode('utf-8')  
                part_start = file.read(4)
                part_size = file.read(4)
                part_next = file.read(4)
                part_name = file.read(16).decode('utf-8')

                real_part_start = int.from_bytes(part_start, byteorder='big')
                real_part_size = int.from_bytes(part_size, byteorder='big')
                real_part_next = int.from_bytes(part_next, byteorder='big')

                print(f"Part_status: {part_status} Fit {part_fit}, Start {real_part_start}, Size {real_part_size}, Next {real_part_next}, Name  {part_name}")
                
                if part_status.lower() == 'n':
                    print("Solo hay una particion")
                    list = []
                    next_start = real_part_start 
                    list.append(next_start)
                    return list
                if real_part_next != 0:
                    ebr_instance = EBR(part_status, part_fit, real_part_start, real_part_size, real_part_next, part_name)
                    self.linked_ebr_list.append(ebr_instance)
                    start = real_part_next
                    continue
                if real_part_next == 0:
                    new_real_part_next = real_part_size + real_part_start
                    new_real_part_next_bytes = new_real_part_next.to_bytes(4, byteorder='big')
                    file.seek(start + 10) 
                    file.write(new_real_part_next_bytes)
                    list = []
                    next_start = real_part_start + real_part_size
                    list.append(next_start)  
                    ebr_instance = EBR(part_status, part_fit, real_part_start, real_part_size, new_real_part_next, part_name)
                    self.linked_ebr_list.append(ebr_instance)
                    file.close()
                    return list   
        file.close()

    def write_ebr(self, path, ebr):
        
        with open(path, 'rb+') as file:
            
            file.seek(ebr.part_start)
            part_status = ebr.part_status.encode('utf-8')
            part_fit = ebr.part_fit.encode('utf-8')
            part_start = ebr.part_start.to_bytes(4, byteorder='big')
            part_size = ebr.part_size.to_bytes(4, byteorder='big')
            part_next = ebr.part_next.to_bytes(4, byteorder='big')
            part_name = ebr.part_name.encode('utf-8')
                
            array_of_bytes = bytearray()
            array_of_bytes += part_status
            array_of_bytes += part_fit
            array_of_bytes += part_start
            array_of_bytes += part_size
            array_of_bytes += part_next
            array_of_bytes += part_name
            file.write(array_of_bytes)   
        file.close()

    def create_logic_partition(self, part_status, part_fit, part_start, part_size, part_next, part_name, path):
        if self.linked_ebr_list.how_long() == -20:
            edit = self.linked_ebr_list.get_ebr_at_index(0)
            edit.part_start = part_start
            edit.part_status = part_status
            edit.part_fit = part_fit
            edit.part_size = part_size
            edit.part_next = 0
            edit.part_name = part_name
            self.write_ebr(path)
            self.linked_ebr_list.display()
            return
        if self.linked_ebr_list.how_long() > 1:
            value = self.linked_ebr_list.how_long() - 1
            value2 = self.linked_ebr_list.get_ebr_at_index(value)
            value2.next = value2.part_start + value2.part_size
        if self.linked_ebr_list.how_long() == 1:
            part_start = self.get_initial_start()
        self.linked_ebr_list.append(EBR(part_status, part_fit, part_start, part_size, 0, part_name))
        self.linked_ebr_list.display()
        self.write_ebr(path)
        self.linked_ebr_list.display()

    def logic_partition(self, part_status, part_fit, part_start, part_size, part_next, part_name, path, value):
        print("Se creara una particion logica")
        print(part_size)
        part_next = 0
        if value != 0:
            list = self.load_ebr(path)
            print(f"Lista {list[0]}")
            if len(list) == 1:
                new_ebr = EBR(part_status, part_fit, list[0], part_size, part_next, part_name)
                self.write_ebr(path, new_ebr)
                self.linked_ebr_list.append(new_ebr)
                return
            else:
                new_ebr = EBR(part_status, part_fit, list[0], part_size, part_next, part_name)
                print(new_ebr)
                self.write_ebr(path, new_ebr)
                self.linked_ebr_list.append(new_ebr)
                self.linked_ebr_list.display()
                return
        part_start = self.get_initial_logic_start()
        new_ebr = EBR(part_status, part_fit, part_start, part_size, part_next, part_name)
        self.write_ebr(path, new_ebr)
    
    def delete_ebr(self, path, ebr):

        with open(path, 'rb+') as file:
            
            file.seek(ebr.part_start)
            part_status = ebr.part_status.encode('utf-8')
            array_of_bytes = bytearray()
            array_of_bytes += part_status

            file.write(array_of_bytes)   
        file.close()

    def mbr_report(self, path, names, path2):
        print("Se procedera a hacer el reporte del mbr")

        text = """digraph G{"""

        text +="""    graph[label="Reporte MBR 202010770"];
            node [shape=plaintext];
            TMBR [
            label=<
                <table border="0" cellborder="1" cellspacing="0">
                    
            <tr>
                <td bgcolor="red">Reporte mbr</td>
                <td bgcolor="red"></td>
            </tr>
            
            <tr>
                <td bgcolor="deepskyblue">mbr_size</td>
                <td bgcolor="deepskyblue">{}</td>
            </tr>
            <tr>
                <td bgcolor="deepskyblue">mbr_fecha</td>
                <td bgcolor="deepskyblue">{}</td>
            </tr>
            
            <tr>
                <td bgcolor="deepskyblue">mbr_fecha</td>
                <td bgcolor="deepskyblue">{}</td>
            </tr>""".format(self.size, self.date, self.signature)
        
        if self.partition1.part_name!= "0000000000000000":
            text +="""
            <tr>
                <td bgcolor="deepskyblue">Particion 1</td>
                <td bgcolor="deepskyblue"></td>
            </tr>  
            <tr>
                <td bgcolor="deepskyblue">part_status</td>
                <td bgcolor="deepskyblue">{}</td>
            </tr>
            <tr>
                <td bgcolor="deepskyblue">part_type</td>
                <td bgcolor="deepskyblue">{}</td>
            </tr>
            <tr>
                <td bgcolor="deepskyblue">part_fit</td>
                <td bgcolor="deepskyblue">{}</td>
            </tr>
            <tr>
                <td bgcolor="deepskyblue">part_start</td>
                <td bgcolor="deepskyblue">{}</td>
            </tr>
            <tr>
                <td bgcolor="deepskyblue">part_size</td>
                <td bgcolor="deepskyblue">{}</td>
            </tr>
            <tr>
                <td bgcolor="deepskyblue">part_name</td>
                <td bgcolor="deepskyblue">{}</td>
            </tr>
            
            """.format(self.partition1.part_status, self.partition1.part_type, self.partition1.part_fit, self.partition1.part_start, self.partition1.part_size, self.partition1.part_name)
            
            if self.partition1.part_type.lower() == 'e':
                self.load_ebr(path2)
                for i in range(self.linked_ebr_list.how_long()):
                    actual = self.linked_ebr_list.get_ebr_at_index(i)
                    if actual == None:
                        continue
                    # self.partition1 = partition('E','I','I',0,0,'0000000000000000')
                    if actual.part_status.lower() == 'd':
                        actual.part_name = '0000000000000000'
                        actual.part_fit = 'I'
                    if actual.part_next == 0:
                        actual.part_next = -1
                    text += """   
            <tr>
                <td bgcolor="deepskyblue">Particion logica</td>
                <td bgcolor="deepskyblue"></td>
            </tr>            
            <tr>
                <td bgcolor="deepskyblue">part_next</td>
                <td bgcolor="deepskyblue">{}</td>
            </tr>
            <tr>
                <td bgcolor="deepskyblue">part_fit</td>
                <td bgcolor="deepskyblue">{}</td>
            </tr>
            <tr>
                <td bgcolor="deepskyblue">part_start</td>
                <td bgcolor="deepskyblue">{}</td>
            </tr>
            <tr>
                <td bgcolor="deepskyblue">part_size</td>
                <td bgcolor="deepskyblue">{}</td>
            </tr>
            <tr>
                <td bgcolor="deepskyblue">part_name</td>
                <td bgcolor="deepskyblue">{}</td>
            </tr>
                    
                    
                    """.format(actual.part_next, actual.part_fit, actual.part_start, actual.part_size, actual.part_name)
        if self.partition2.part_name!= "0000000000000000":
            text +="""
            <tr>
                <td bgcolor="deepskyblue">Particion 2</td>
                <td bgcolor="deepskyblue"></td>
            </tr>  
            <tr>
                <td bgcolor="deepskyblue">part_status</td>
                <td bgcolor="deepskyblue">{}</td>
            </tr>
            <tr>
                <td bgcolor="deepskyblue">part_type</td>
                <td bgcolor="deepskyblue">{}</td>
            </tr>
            <tr>
                <td bgcolor="deepskyblue">part_fit</td>
                <td bgcolor="deepskyblue">{}</td>
            </tr>
            <tr>
                <td bgcolor="deepskyblue">part_start</td>
                <td bgcolor="deepskyblue">{}</td>
            </tr>
            <tr>
                <td bgcolor="deepskyblue">part_size</td>
                <td bgcolor="deepskyblue">{}</td>
            </tr>
            <tr>
                <td bgcolor="deepskyblue">part_name</td>
                <td bgcolor="deepskyblue">{}</td>
            </tr>
            
            """.format(self.partition2.part_status, self.partition2.part_type, self.partition2.part_fit, self.partition2.part_start, self.partition2.part_size, self.partition2.part_name)
            
            if self.partition2.part_type.lower() == 'e':
                self.load_ebr(path2)
                for i in range(self.linked_ebr_list.how_long()):
                    actual = self.linked_ebr_list.get_ebr_at_index(i)
                    if actual == None:
                        continue
                    if actual.part_status.lower() == 'd':
                        actual.part_name = '0000000000000000'
                        actual.part_fit = 'I'
                    if actual.part_next == 0:
                        actual.part_next = -1
                    text += """   
            <tr>
                <td bgcolor="deepskyblue">Particion logica</td>
                <td bgcolor="deepskyblue"></td>
            </tr>            
            <tr>
                <td bgcolor="deepskyblue">part_status</td>
                <td bgcolor="deepskyblue">{}</td>
            </tr>
            <tr>
                <td bgcolor="deepskyblue">part_fit</td>
                <td bgcolor="deepskyblue">{}</td>
            </tr>
            <tr>
                <td bgcolor="deepskyblue">part_start</td>
                <td bgcolor="deepskyblue">{}</td>
            </tr>
            <tr>
                <td bgcolor="deepskyblue">part_size</td>
                <td bgcolor="deepskyblue">{}</td>
            </tr>
            <tr>
                <td bgcolor="deepskyblue">part_name</td>
                <td bgcolor="deepskyblue">{}</td>
            </tr>
            <tr>
                <td bgcolor="deepskyblue">part_next</td>
                <td bgcolor="deepskyblue">{}</td>
            </tr>        
            
                    
                    """.format(actual.part_status, actual.part_fit, actual.part_start, actual.part_size, actual.part_name, actual.part_next)
        if self.partition3.part_name!= "0000000000000000":
            text +="""
            <tr>
                <td bgcolor="deepskyblue">Particion 3</td>
                <td bgcolor="deepskyblue"></td>
            </tr>  
            <tr>
                <td bgcolor="deepskyblue">part_status</td>
                <td bgcolor="deepskyblue">{}</td>
            </tr>
            <tr>
                <td bgcolor="deepskyblue">part_type</td>
                <td bgcolor="deepskyblue">{}</td>
            </tr>
            <tr>
                <td bgcolor="deepskyblue">part_fit</td>
                <td bgcolor="deepskyblue">{}</td>
            </tr>
            <tr>
                <td bgcolor="deepskyblue">part_start</td>
                <td bgcolor="deepskyblue">{}</td>
            </tr>
            <tr>
                <td bgcolor="deepskyblue">part_size</td>
                <td bgcolor="deepskyblue">{}</td>
            </tr>
            <tr>
                <td bgcolor="deepskyblue">part_name</td>
                <td bgcolor="deepskyblue">{}</td>
            </tr>
            
            """.format(self.partition3.part_status, self.partition3.part_type, self.partition3.part_fit, self.partition3.part_start, self.partition3.part_size, self.partition3.part_name)
            if self.partition3.part_type.lower() == 'e':
                self.load_ebr(path2)
                for i in range(self.linked_ebr_list.how_long()):
                    actual = self.linked_ebr_list.get_ebr_at_index(i)
                    if actual == None:
                        continue
                    if actual.part_status.lower() == 'd':
                        actual.part_name = '0000000000000000'
                        actual.part_fit = 'I'
                    if actual.part_next == 0:
                        actual.part_next = -1
                    text += """   
            <tr>
                <td bgcolor="deepskyblue">Particion logica</td>
                <td bgcolor="deepskyblue"></td>
            </tr>            
            <tr>
                <td bgcolor="deepskyblue">part_next</td>
                <td bgcolor="deepskyblue">{}</td>
            </tr>
            <tr>
                <td bgcolor="deepskyblue">part_fit</td>
                <td bgcolor="deepskyblue">{}</td>
            </tr>
            <tr>
                <td bgcolor="deepskyblue">part_start</td>
                <td bgcolor="deepskyblue">{}</td>
            </tr>
            <tr>
                <td bgcolor="deepskyblue">part_size</td>
                <td bgcolor="deepskyblue">{}</td>
            </tr>
            <tr>
                <td bgcolor="deepskyblue">part_name</td>
                <td bgcolor="deepskyblue">{}</td>
            </tr>
            <tr>
                <td bgcolor="deepskyblue">part_name</td>
                <td bgcolor="deepskyblue">{}</td>
            </tr>
                    
                    """.format(actual.part_next, actual.part_fit, actual.part_start, actual.part_size, actual.part_name, actual.part_name, actual.part_type)
        


        if self.partition4.part_name!= "0000000000000000":
            text +="""
            <tr>
                <td bgcolor="deepskyblue">Particion 4</td>
                <td bgcolor="deepskyblue"></td>
            </tr>  
            <tr>
                <td bgcolor="deepskyblue">part_status</td>
                <td bgcolor="deepskyblue">{}</td>
            </tr>
            <tr>
                <td bgcolor="deepskyblue">part_type</td>
                <td bgcolor="deepskyblue">{}</td>
            </tr>
            <tr>
                <td bgcolor="deepskyblue">part_fit</td>
                <td bgcolor="deepskyblue">{}</td>
            </tr>
            <tr>
                <td bgcolor="deepskyblue">part_start</td>
                <td bgcolor="deepskyblue">{}</td>
            </tr>
            <tr>
                <td bgcolor="deepskyblue">part_size</td>
                <td bgcolor="deepskyblue">{}</td>
            </tr>
            <tr>
                <td bgcolor="deepskyblue">part_name</td>
                <td bgcolor="deepskyblue">{}</td>
            </tr>
            
            """.format(self.partition4.part_status, self.partition4.part_type, self.partition4.part_fit, self.partition4.part_start, self.partition4.part_size, self.partition4.part_name)
            if self.partition4.part_type.lower() == 'e':
                self.load_ebr(path2)
                for i in range(self.linked_ebr_list.how_long()):
                    actual = self.linked_ebr_list.get_ebr_at_index(i)
                    if actual == None:
                        continue
                    if actual.part_status.lower() == 'd':
                        actual.part_name = '0000000000000000'
                        actual.part_fit = 'I'
                    if actual.part_next == 0:
                        actual.part_next = -1
                    text += """   
            <tr>
                <td bgcolor="deepskyblue">Particion logica</td>
                <td bgcolor="deepskyblue"></td>
            </tr>            
            <tr>
                <td bgcolor="deepskyblue">part_next</td>
                <td bgcolor="deepskyblue">{}</td>
            </tr>
            <tr>
                <td bgcolor="deepskyblue">part_fit</td>
                <td bgcolor="deepskyblue">{}</td>
            </tr>
            <tr>
                <td bgcolor="deepskyblue">part_start</td>
                <td bgcolor="deepskyblue">{}</td>
            </tr>
            <tr>
                <td bgcolor="deepskyblue">part_size</td>
                <td bgcolor="deepskyblue">{}</td>
            </tr>
            <tr>
                <td bgcolor="deepskyblue">part_name</td>
                <td bgcolor="deepskyblue">{}</td>
            </tr>
                    
            <tr>
                <td bgcolor="deepskyblue">part_type</td>
                <td bgcolor="deepskyblue">{}</td>
            </tr>
                    
                    """.format(actual.part_next, actual.part_fit, actual.part_start, actual.part_size, actual.part_name, actual.part_type)
        
        text += """            
        </table>
            >
            ]

 
            }"""
        
        print("Se imprimio {}".format(names))
        print(text)
        dot = "{}.dot".format(names)
        with open(dot, 'w') as grafo:
            grafo.write(text)
            grafo.close()
        subprocess.run(["dot", "-Tjpg", dot, "-o", path])
        
    def calculate_total_size(self, size_to_compare):
        porcentage = (size_to_compare / self.size ) * 100
        return porcentage
    
    def graph_disk(self, path,names, path2 ):

        text = """
        digraph lista {
   
        rankdir=LR;
        graph[label="Disco 202010770"];


        node [shape=box, style=filled, fillcolor=white]; 

        inicio[label="MBR """+str(self.calculate_total_size(127))+"""%"];
        """
        if self.partition1.part_status.lower() != 'e': 
            if self.partition1.part_status.lower() != 'i':
                text += """
                partition1[label="P1 {} {} {}%"];
                """.format(self.partition1.part_type, self.partition1.part_name, self.calculate_total_size(self.partition1.part_size))
            else:
                text += """
                partition1[label="Libre {}%"];
                """.format(self.calculate_total_size(self.partition1.part_size))

            if self.partition1.part_type.lower() == 'e':
                count = 0
                self.load_ebr(path2)
                print(self.linked_ebr_list.how_long())
                for i in range(self.linked_ebr_list.how_long()):
                    actual = self.linked_ebr_list.get_ebr_at_index(i)
                    if actual == None:
                        continue
                    if actual.part_status.lower() == 'd':
                        actual.part_name = 'Libre'
                    if actual.part_next == 0:
                        actual.part_next = -1
                    text += """   
                    logica{}[label="Logica {} Libre {}%"];  """.format(actual.part_name, actual.part_name, self.calculate_total_size(actual.part_size) )
        
        if self.partition2.part_status.lower() != 'e': 
            if self.partition2.part_status.lower() != 'i':
                text += """
                partition2[label="P2 {} {} {}%"];
                """.format(self.partition2.part_type, self.partition2.part_name, self.calculate_total_size(self.partition2.part_size))
            else:
                text += """
                partition2[label="Libre {}%"];
                """.format(self.calculate_total_size(self.partition2.part_size))

            if self.partition2.part_type.lower() == 'e':
                self.load_ebr(path2)
                count = 0
                for i in range(self.linked_ebr_list.how_long()):
                    actual = self.linked_ebr_list.get_ebr_at_index(i)
                    if actual == None:
                        continue
                    if actual.part_status.lower() == 'd':
                        actual.part_name = 'Libre'
                    if actual.part_next == 0:
                        actual.part_next = -1
                    text += """   
                    logica{}[label="Logica {} Libre {}%"];  """.format(count, actual.part_name, self.calculate_total_size(actual.part_size) )

        if self.partition3.part_status.lower() != 'e': 
            if self.partition3.part_status.lower() != 'i':
                text += """
                partition3[label="P1 {} {} {}%"];
                """.format(self.partition3.part_type, self.partition3.part_name, self.calculate_total_size(self.partition3.part_size))
            else:
                text += """
                partition3[label="Libre {}%"];
                """.format(self.calculate_total_size(self.partition3.part_size))

            if self.partition3.part_type.lower() == 'e':
                self.load_ebr(path2)
                count = 0
                for i in range(self.linked_ebr_list.how_long()):
                    actual = self.linked_ebr_list.get_ebr_at_index(i)
                    if actual == None:
                        continue
                    if actual.part_status.lower() == 'd':
                        actual.part_name = 'Libre'
                    if actual.part_next == 0:
                        actual.part_next = -1
                    text += """   
                    logica{}[label="Logica {} Libre {}%"];  """.format(count, actual.part_name, self.calculate_total_size(actual.part_size) )
        
        if self.partition4.part_status.lower() != 'e': 
            if self.partition4.part_status.lower() != 'i':
                text += """
                partition4[label="P4 {} {} {}%"];
                """.format(self.partition4.part_type, self.partition4.part_name, self.calculate_total_size(self.partition4.part_size))
            else:
                text += """
                partition4[label="Libre {}%"];
                """.format(self.calculate_total_size(self.partition4.part_size))

            if self.partition4.part_type.lower() == 'e':
                self.load_ebr(path2)
                count = 0
                for i in range(self.linked_ebr_list.how_long()):
                    count +=1
                    actual = self.linked_ebr_list.get_ebr_at_index(i)
                    if actual == None:
                        continue
                    if actual.part_status.lower() == 'd':
                        actual.part_name = 'Libre'
                    if actual.part_next == 0:
                        actual.part_next = -1
                    text += """   
                    logica{}[label="Logica {} Libre {}%"];  """.format(count, actual.part_name, self.calculate_total_size(actual.part_size) )
                    
        text += """   
                    libre[label="Libre  Libre {}%"];  """.format(self.calculate_total_size(self.size - self.look_on_operation()) )
        
        text += "}"
        print(text)
        
        dot = "{}.dot".format(names)
        with open(dot, 'w') as grafo:
            grafo.write(text)
            grafo.close()
        subprocess.run(["dot", "-Tjpg", dot, "-o", path])


class partition():
    def __init__(self, part_status, part_type, part_fit, part_start, part_size, part_name):
        self.part_status = part_status
        self.part_type = part_type
        self.part_fit = part_fit
        self.part_start = part_start
        self.part_size = part_size
        self.part_name = part_name
    
class EBR():
    def __init__(self, part_status, part_fit, part_start, part_size, part_next, part_name):
        self.part_status = part_status #CHar
        self.part_fit = part_fit #char
        self.part_start = part_start #int 4
        self.part_size = part_size # int 4
        self.part_next = part_next #int 4
        self.part_name = part_name # char 16
        #total 30 bytes
    
class Node():
    def __init__(self, ebr):
        self.ebr = ebr
        self.next = None

class LinkedList():
    def __init__(self):
        self.head = None

    def append(self, ebr):
        new_node = Node(ebr)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        self.display()

    def display(self):
        current = self.head
        while current != None:
            ebr = current.ebr
            print(f"Part Status {ebr.part_status} Part Name: {ebr.part_name}, Part Size: {ebr.part_size},  Part Start: {ebr.part_start}, part next {ebr.part_next}")
            current = current.next
        
    def get_ebr_at_index(self, index):
        if index < 0:
            return None  # Índice negativo, no válido

        current = self.head
        count = 0

        while current:
            if count == index:
                return current.ebr  # Se encontró el EBR en el índice especificado
            current = current.next
            count += 1

        return None

    def how_long(self):
        current = self.head
        count = 0

        while current:
            count += 1
            current = current.next

        return count

    def total_size(self):
        total = 0
        current = self.head

        while current:
            ebr = current.ebr
            total += ebr.part_start + ebr.part_size
            current = current.next

        return total

    def find_ebr_by_name(self, name):
        current = self.head
        while current:
            if current.ebr.part_name.lower() == name:
                return current.ebr
            current = current.next
        return None 

class in_Order():
    def __init__(self, pos, value):
        self.pos = pos
        self.value = value

class Mounty_python():
    def __init__(self, name, id, path):
        self.name = name
        self.id = id
        self.path = path

class Graphviz():
    def __init__(self):
        pass

    def generate(self, text, path):
        dot = "graphviz.dot"
        with open(dot, 'w') as grafo:
            grafo.write(text)
            grafo.close()
        subprocess.run(["dot", "-Tjpg", dot, "-o", path])