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
    
            print("Datos recuperados del disco:")
            print(f"Tamaño: {self.size}")
            print(f"Fecha y hora: {self.date}")
            print(f"Firma (entero): {self.signature}")
            print(f"Ajuste: {self.fit}")

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

            print(f"Particion 1 Status: {self.partition1.part_status}")
            print(f"Particion 1 Tipo: {self.partition1.part_type}")
            print(f"Particion 1 Fit: {self.partition1.part_fit}")
            print(f"Particion 1 Inicio: {self.partition1.part_start}")
            print(f"Particion 1 Tamaño: {self.partition1.part_size}")
            print(f"Particion 1 Nombre: {self.partition1.part_name}")

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

            print(f"Particion 2 Status: {self.partition2.part_status}")
            print(f"Particion 2 Tipo: {self.partition2.part_type }")
            print(f"Particion 2 Fit: {self.partition2.part_fit}")
            print(f"Particion 2 Inicio: {self.partition2.part_start}")
            print(f"Particion 2 Tamaño: {self.partition2.part_size}")
            print(f"Particion 2 Nombre: {self.partition2.part_name}")
            
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

            print(f"Particion 3 Status: {self.partition3.part_status}")
            print(f"Particion 3 Tipo: {self.partition3.part_type }")
            print(f"Particion 3 Fit: {self.partition3.part_fit}")
            print(f"Particion 3 Inicio: {self.partition3.part_start}")
            print(f"Particion 3 Tamaño: {self.partition3.part_size}")
            print(f"Particion 3 Nombre: {self.partition3.part_name}")

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

            print(f"Particion 4 Status: {self.partition4.part_status}")
            print(f"Particion 4 Tipo: {self.partition4.part_type }")
            print(f"Particion 4 Fit: {self.partition4.part_fit}")
            print(f"Particion 4 Inicio: {self.partition4.part_start}")
            print(f"Particion 4 Tamaño: {self.partition4.part_size}")
            print(f"Particion 4 Nombre: {self.partition4.part_name}")
    
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
            
        if len(part_name) < 16:
        # Rellena con espacios en blanco a la derecha hasta alcanzar una longitud de 16
            part_name = part_name.ljust(16)
        #Status E = Empty, B = Busy and unmounted, D = Deleted, M = Busy and mounted
        if self.partition1.part_status.lower() == 'e':
            self.partition1.part_status = part_status
            self.partition1.part_type = part_type
            self.partition1.part_fit = part_fit
            self.partition1.part_start = part_start
            self.partition1.part_size = part_size
            self.partition1.part_name = part_name
            self.write_mbr_for_partitions(path)
            self.read_mbr(path)
            return
        if self.partition2.part_status.lower() == 'e':
            self.partition2.part_status = part_status
            self.partition2.part_type = part_type
            self.partition2.part_fit = part_fit
            self.partition2.part_start = part_start
            self.partition2.part_size = part_size
            self.partition2.part_name = part_name
            self.write_mbr_for_partitions(path)
            self.read_mbr(path)
            return
        if self.partition3.part_status.lower() == 'e':
            self.partition3.part_status = part_status
            self.partition3.part_type = part_type
            self.partition3.part_fit = part_fit
            self.partition3.part_start = part_start
            self.partition3.part_size = part_size
            self.partition3.part_name = part_name
            self.write_mbr_for_partitions(path)
            self.read_mbr(path)
            return
        if self.partition4.part_status.lower() == 'e':
            self.partition4.part_status = part_status
            self.partition4.part_type = part_type
            self.partition4.part_fit = part_fit
            self.partition4.part_start = part_start
            self.partition4.part_size = part_size
            self.partition4.part_name = part_name
            self.write_mbr_for_partitions(path)
            self.read_mbr(path)
            return
        print("No hay mas particiones disponibles")
    
    #self.partition4 = partition('E','I','I',0,0,'0000000000000000')
    def delete_partition(self, path, name):
        self.read_mbr(path)

        if self.partition1.part_name.lower() == 'name':
            print(self.partition1.part_size)
            text_in_zeros = self.bytes_in_zeros(self.partition1.part_size) 
            with open(path, 'rb+') as file:
                file.seek(self.partition1.part_start)
                file.write(text_in_zeros)
                file.close()
            self.partition1.part_name = '0000000000000000'
            self.partition1.part_fit = 'I'
            self.partition1.part_status = 'D'
            self.partition1.part_type = 'I'

        if self.partition2.part_name.lower() == 'name':
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

        if self.partition3.part_name.lower() == 'name':
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

        if self.partition4.part_name.lower() == 'name':
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
        
        self.write_mbr_for_partitions(path)

    
    def bytes_in_zeros(self, size):
        
        if size < 0:
            raise ValueError("n debe ser un número positivo")
        bytes = bytes([0] * size)
        return bytes
            



class partition():
    def __init__(self, part_status, part_type, part_fit, part_start, part_size, part_name):
        self.part_status = part_status
        self.part_type = part_type
        self.part_fit = part_fit
        self.part_start = part_start
        self.part_size = part_size
        self.part_name = part_name


