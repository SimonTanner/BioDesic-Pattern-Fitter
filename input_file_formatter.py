import os

# Functions for formatting data ready for processing by pattern fitter program

class FileFormatter():
    
    def __init__(self, file_name, file_type=None):
        self.error_val = 0.001
        self.data = self.load_data(file_name, file_type)

    def load_data(self, file_name, file_type):
        """
        Load data from file and call format function
        """
        file_path = os.path.join(os.getcwd(), file_name)
        data_list = []
        with open(file_path, 'r') as read_file:
            for line in read_file:
                data_list.append(line)
        
        if file_type == None:
            file_type = file_path.split(".")[-1:][0]

        if file_type == "txt" and len(data_list) != 0:
            data_list = self.format_mesh_txt_data(data_list)
        elif file_type == "obj" and len(data_list) != 0:
            data_list = self.format_mesh_obj_data(data_list)
        return data_list

    def format_mesh_obj_data(self, data):
        """
        Format the data into the correct data structure from *.obj format
        """
        verts, faces = [], []
        for i in range(0, len(data)):
            data[i] = data[i].split(" ")
            if data[i][0] == "v":
                del data[i][0]
                verts.append(map(lambda x: float(x), data[i]))
            elif data[i][0] == "f":
                del data[i][0]
                faces.append(map(lambda x: int(x), data[i]))

        formatted_data = [[[len(verts), len(faces)]]]
        formatted_data.append(verts)
        formatted_data.append(faces)

        return formatted_data

    def format_mesh_txt_data(self, data):
        """
        Format the data into the correct data structure from *.txt format
        """
        for i in range(0, len(data)):
            data[i] = data[i].translate(None, '[')
            data[i] = data[i].translate(None, '\n')
            data[i] = data[i].split(']')

        for m in range(0, len(data)):
            for n in range(0, len(data[m])):
                data[m][n] = data[m][n].split(',')

        for m in range(0, len(data)):
            for n in range(0, len(data[m])):
                self.convert_data_txt(data[m][n])

        for m in range(0, len(data)):
            for n in range(0, len(data[m])):
                if len(data[m][n]) == 0:
                    del(data[m][n])

        return self.check_data(data)

    def convert_data_txt(self, data):
        while True:
            try:
                while True:
                    try:
                        for o in range(0, len(data)):
                            data[o] = float(data[o])
                            if data[o] % 1 == 0:
                                data[o] = int(data[o])
                    except ValueError:
                        del(data[o])
                    except TypeError:
                        del(data[o])
                    except IndexError:
                        break
                    else:
                        break

            except IndexError:
                break
            else:
                break
        

    def check_data(self, data):
        self.error_val = 0.001
        errors = []
        face_delete = []

        for i in range(0, len(data[1])):
            for k in range(i, len(data[1])):
                if i != k:
                    diff = map(lambda a, b: abs(a - b), data[1][i], data[1][k])
                    if diff[0] < self.error_val and diff[1] < self.error_val and diff[2] < self.error_val:
                        errors.append([i+1, k+1])

        for i in range(0, len(errors)):
            for k in range(0, len(data[2])):
                while True:
                    try:
                        n = data[2][k].index(errors[i][1])
                        data[2][k][n] = errors[i][0]
                    except ValueError:
                        break
                    else:
                        break

        for i in range(0, len(errors)):
            index = len(errors) - i -1
            delete = errors[index][1] - 1
            del(data[1][delete])

        for i in range(0, len(data[2])):
            for k in range(i, len(data[2])):
                face_errors = []
                for m in range(0, len(data[2][i])):
                    while i != k and True:
                        try:
                            n = data[2][k].index(data[2][i][m])
                            if len(face_errors) > 0:
                                face_errors.index(n)
                            face_errors.append(n)

                        except ValueError:
                            break

                        else:
                            break

                if len(face_errors) == 3:
                    face_delete.append([i, k, face_errors])

            for l in range(0, len(data[2][i])-1):
                for p in range(1, len(data[2][i])):
                    if l != p:
                        if data[2][i][l] == data[2][i][p]:
                            face_delete.append([i])

        for i in range(0, len(face_delete)):
            index = len(face_delete) - 1 - i
            delete = face_delete[index][-1]
            del(data[2][delete])

        data[0][0][0] = len(data[1])
        data[0][0][1] = len(data[2])
    
        return data
