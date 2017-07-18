import os

file_name = "test_data/Skinny-v5.txt"

file_path = os.path.join(os.getcwd(), file_name)

op_file = open(file_path, 'r')

data_list = []

for line in op_file:
    data_list.append(line)

def convert_data(dat):

    while True:

        try:
            dat = float(dat)

        except ValueError:
            del(dat)

            break

        except TypeError:
            del(dat)

            break



            #continue

        except IndexError:

            break

        else:

            break


def format_list(data):

    for i in range(0, len(data)):
        data[i] = data[i].translate(None, '[')
        data[i] = data[i].translate(None, '\n')
        data[i] = data[i].split(']')

    for m in range(0, len(data)):
         for n in range(0, len(data[m])):
             data[m][n] = data[m][n].split(',')

    for m in range(0, len(data)):
        for n in range(0, len(data[m])):
            #convert_data(data[m][n])
            for o in range(0, len(data[m][n])):
                convert_data(data[m][n][o])


vertices = {'v1':[0,0,0],'v2':[1,8,9], 'v3':[3,2,1], 'v4':[], 'v5':[], 'v6':[], 'v7':[], 'v8':[]}

joins = [['v1', 'v2'], ['v1', 'v3']]

def calc_lines(verts, joins, lines):
    for a in range(0, len(joins)):
        lines.append('L' + str(a+1))
        for n in range(0, 2):
            lines[('L' + str(a+1))] = verts[joins[a][0]][n] - verts[joins[a][1]][n]



def Main():

    format_list(data_list)

    return(data_list)

    print data_list


Main()
