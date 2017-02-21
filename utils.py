from PIL import Image, ImageTk
import os
import re

class BoxEntry:
    coords = (0,0,0,0)
    pic = 0
    box_type = 0
    def __str__(self):
        ret_string = str(self.pic) + ' '
        for c in self.coords:
            ret_string = ret_string + '{0:.3f}'.format(c) + ' '
        ret_string = ret_string + str(self.box_type)
        return ret_string

    def __init__(self, init_string='0 0 0 0 0 0'):
        tokens = init_string.strip().split(' ')
        if len(tokens) != 6:
            print('Invalid init string when creating BoxEntry!')

        self.pic = tokens[0]
        self.coords = (float(tokens[1]),float(tokens[2]),float(tokens[3]),float(tokens[4]))
        self.box_type = tokens[5]


class FileHandler:
    folder = ""
    def __init__(self, folder):
        if not os.path.exists(folder):
            print('Could not find specified data folder:', folder)
        else:
            self.folder = folder


    def write_list(self, bbList, folder):
        f = open(folder+'/list.txt', 'w')
        for list_item in bbList:
            f.write(str(list_item) + '\n')
        f.close()

    def read_list(self, folder):
        bbList = []
        max_index = 0
        f = open(folder+'/list.txt', 'r')
        for line in f:
            bbList.append(BoxEntry(line))
            tokens = line.strip().split(' ')
            fname = tokens[0]
            num = int(fname[3:6])
            if num > max_index:
                max_index = num

        return bbList, max_index

    def read_pic(self, number):
        numString = str(number)
        while len(numString) < 3:
            numString = '0' + numString

        image = Image.open(self.folder + '/img%s.jpg'%numString)
        return ImageTk.PhotoImage(image)

    def count_pics(self,folder):
        num = 0
        file_list = os.listdir(folder)
        for f in file_list:
            if re.match('img[0-9][0-9][0-9]\.jpg',f):
                str_num = int(f[3:6])
                if(str_num > num):
                    num = str_num
        return num
