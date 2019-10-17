import os


class OutputFormatter():
    """
    Must be initialised with a file path to where the file should be saved and the
    desired ouput format e.g .txt
    """
    def __init__(self, file_path, output_format="txt"):
        self.file_path = file_path
        self.output_format = output_format

    def freecad_format(self, data_list):
        converted = []
        for poly in data_list[2]:
            polygon = []
            for vert in poly:
                polygon.append(data_list[1][vert - 1])
            converted += polygon

        return converted

    def obj_format(self, data_list):
        data = ""
        try:
            for vert in data_list[1]:
                data += "v {}\n".format(" ".join(map(lambda x: str(x), vert)))
            for face in data_list[2]:
                data += "f {}\n".format(" ".join(map(lambda x: str(x), face)))
        except Exception as error:
            print self.__class__.__module__+ ".py" + ", " + self.__class__.__name__ + ":"
            print error

        return data

    def check_file_exists(self, file_path, file_number):
        try:
            file_name = file_path.format(file_number, self.output_format)
            print file_name
            if os.path.exists(file_name):
                file_number += 1
                file_name = self.check_file_exists(file_path, file_number)
        except Exception as error:
            print self.__class__.__module__+ ".py" + ", " + self.__class__.__name__ + ":"
            print error

        return file_name

    def save_new_file_name(self, data):
        file_path_new = str(self.file_path.split(".")[0]) + "_blah_{}.{}"
        start_num = 1
        file_path_new = self.check_file_exists(file_path_new, start_num)
        op_file_new = open(file_path_new, "w")
        if self.output_format == "txt":
            data = self.freecad_format(data)
        elif self.output_format == "obj":
            data = self.obj_format(data)
        op_file_new.write(str(data))
        op_file_new.close()