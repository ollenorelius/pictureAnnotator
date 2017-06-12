from PIL import Image
import re
import os
import math
import random

'''
Quick dirty script to split data into test and training data sets.
Specify folders in the code below, the data will be split into two folders:
./test and ./training, with respective data list files.

ratio_training decides the split.
0.8 gives 80% training data and 20% test data and so forth

Code's ugly but it works. Dont judge me :x

'''


folders = ['set1', 'set2', 'set3', 'set4', 'set5', 'set6', 'set7', 'set8', 'set9']
ratio_training = 0.8
class ListItem():
    filename = ''
    coords = (0,0,0,0)
    cl = -1

    def __init__(self, filename, coords, cl):
        self.filename = filename
        self.coords = coords
        self.cl = cl


tr_folder = 'training'
if not os.path.exists(tr_folder):
    os.makedirs(tr_folder)

test_folder = 'test'
if not os.path.exists(test_folder):
    os.makedirs(test_folder)

train_list = open(tr_folder + '/' + 'list.txt', 'w')
test_list = open(test_folder + '/' + 'list.txt', 'w')
pic_number = 0
for folder in folders:
    filenames = []
    list_file = open(folder+'/list.txt', 'r')
    list_list = []
    for line in list_file:
        tokens = line.strip().split(' ')
        list_list.append(ListItem(tokens[0],
                                (tokens[1],tokens[2],tokens[3],tokens[4]),
                                tokens[5]))


    filenames_unfiltered = os.listdir(folder)
    for unf in filenames_unfiltered:
        if re.search('\.jpg\Z', unf) != None:
            filenames.append(folder + '/' + unf)


    for f in filenames:
        im = Image.open(f)
        r = random.random()
        if r < ratio_training:
            im.save(tr_folder + '/' + 'im%i.jpg'%pic_number)
        else:
            im.save(test_folder + '/' + 'im%i.jpg'%pic_number)
        for item in list_list:
            if folder + '/' + item.filename == f:
                if r < ratio_training:
                    train_list.write('%s %s %s %s %s %s\n'%('im%i.jpg'%pic_number,
                                                            item.coords[0],
                                                            item.coords[1],
                                                            item.coords[2],
                                                            item.coords[3],
                                                            item.cl))
                else:
                    test_list.write('%s %s %s %s %s %s\n'%('im%i.jpg'%pic_number,
                                                            item.coords[0],
                                                            item.coords[1],
                                                            item.coords[2],
                                                            item.coords[3],
                                                            item.cl))

        pic_number = pic_number + 1
        im.close()
