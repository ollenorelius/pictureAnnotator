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
    file_list = []
    file_count = 0
    current_pic = ""
    listnum = None
    def __init__(self, folder, listnum=None):
        if not os.path.exists(folder):
            print('Could not find specified data folder:', folder)
        else:
            self.listnum = listnum
            self.folder = folder
            files = os.listdir(folder)
            for f in files:
                if re.search('\.jpg\Z', f) != None:
                    self.file_list.append(f)
            self.file_count = len(self.file_list)
            self.file_list.sort()



    def write_list(self, bbList, folder):
        f = open(folder+'/list%s.txt'%self.listnum, 'w')
        for list_item in bbList:
            f.write(str(list_item) + '\n')
        f.close()

    def read_list(self, folder):
        bbList = []
        max_index = 0
        name_list = []
        list_file = open(folder+'/list.txt', 'r')

        files = os.listdir(folder)
        self.file_list = []
        for f in files:
            if re.search('\.jpg\Z', f) != None:
                self.file_list.append(f)
        self.file_count = len(self.file_list)

        for line in list_file:
            bbList.append(BoxEntry(line))
            tokens = line.strip().split(' ')
            name_list.append(tokens[0])

        self.file_list = [x for x in self.file_list if x not in name_list]
        self.file_list.sort()

        return bbList

    def read_pic(self):
        self.current_pic = self.file_list.pop()
        image = Image.open(self.folder + '/' + self.current_pic)
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
