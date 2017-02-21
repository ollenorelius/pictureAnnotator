import tkinter as tk
from PIL import Image, ImageTk
from utils import BoxEntry, FileHandler
import math

class MainWindow:
    def __init__(self, master):
        frame = tk.Frame(master)
        frame.pack()

        self.canvas = tk.Canvas(frame,width=640, height=480)
        #master.geometry('640x530+0+0')
        self.canvas.pack()

        self.button = tk.Button(frame, text='Quit', fg='red', command=frame.quit)
        self.button.pack(side=tk.LEFT)

        self.hi_there = tk.Button(frame, text='Hello!', command=self.say_hi)
        self.hi_there.pack(side=tk.LEFT)

    def say_hi(self):
        print('Heya!')

    def click_callback(self, event):
        print('clicked at ', event.x, event.y)

    def key_callback(self, event):
        print('pressed', event.char)

class PicController:
    rectList = []
    activeRect = 0
    bbList = []
    active_type = 1
    active_color = 'red'
    folder = 'set1'
    fileCont = FileHandler(folder)
    picture_count = fileCont.count_pics(folder)
    x_size = 640
    y_size = 480
    image_index = 1

    def __init__(self, canvas):
        self.image_index = 1
        self.canvas = canvas

        self.activeRect = self.canvas.create_rectangle(0,0,0,0,fill='red')
        self.canvas.bind('<Button-1>', self.click_callback)
        self.canvas.bind('<ButtonRelease-1>', self.clickUp_callback)
        self.canvas.bind('<B1-Motion>', self.motion_callback)
        self.canvas.bind('<Key>', self.key_callback)
        self.canvas.focus_set()

        self.pic = self.draw_picture()


    def draw_picture(self):

        self.photo = self.fileCont.read_pic(self.image_index)
        w = self.canvas.create_image((0,0), image=self.photo,anchor='nw')
        return w

    def click_callback(self, event):
        cx = self.canvas.canvasx(event.x)
        cy = self.canvas.canvasx(event.y)
        print('clicked at ', cx,cy)
        self.activeRect = self.canvas.create_rectangle(cx,cy,cx,cy,
                                            fill=self.active_color,
                                            stipple='gray25')
        self.rectList.append(self.activeRect)


    def clickUp_callback(self,event):
        coords = self.canvas.coords(self.activeRect)
        coords[2] = event.x
        coords[3] = event.y
        if self.check_box(coords):
            a = BoxEntry()
            a.coords = self.normalize_coords(coords)
            a.pic = self.get_current_filename()
            a.box_type = self.active_type
            self.bbList.append(a)
        self.canvas.coords(self.activeRect, coords)

    def check_box(self, coords):
        dx = coords[2] - coords[0]
        dy = coords[1] - coords[3]

        area = abs(dx*dy)
        if area > 10:
            return True
        else:
            return False

    def get_current_filename(self):
        numString = str(self.image_index)
        while len(numString) < 3:
            numString = '0' + numString
        return 'img' + numString + '.jpg'


    def normalize_coords(self, coords):
        r_coords = [0,0,0,0]
        r_coords[0] = coords[0] / self.x_size
        r_coords[1] = coords[1] / self.y_size
        r_coords[2] = coords[2] / self.x_size
        r_coords[3] = coords[3] / self.y_size
        return r_coords

    def motion_callback(self,event):
        coords = self.canvas.coords(self.activeRect)
        coords[2] = event.x
        coords[3] = event.y

        self.canvas.coords(self.activeRect, coords)

    def key_callback(self, event):
        print('pressed', event.char)
        if event.char == " ":
            if self.image_index != self.picture_count:
                self.image_index = self.image_index + 1
            else:
                print('Done! No more pictures to annotate.')
                self.fileCont.write_list(self.bbList, self.folder)

            for ibox in self.rectList:
                self.canvas.delete(ibox)

            self.rectList = []
            self.photo = self.fileCont.read_pic(self.image_index)
            self.canvas.itemconfig(self.pic, image=self.photo)

        elif event.char == 'q':
            print(self.rectList)
            for i in self.bbList:
                print(i)

        elif event.char == 'w':
            self.fileCont.write_list(self.bbList, self.folder)

        elif event.char == 'r':
            self.rectList = []
            self.bbList, self.image_index = self.fileCont.read_list(self.folder)
            print('loaded list up to picture %i'%self.image_index)
            self.image_index = self.image_index + 1

            self.photo = self.fileCont.read_pic(self.image_index)
            self.canvas.itemconfig(self.pic, image=self.photo)


        elif event.char == '1':
            self.active_type = 1
            self.active_color = 'red'

        elif event.char == '2':
            self.active_type = 2
            self.active_color = 'blue'

        elif event.char == '3':
            self.active_type = 3
            self.active_color = 'green'

        elif event.char == '4':
            self.active_type = 4
            self.active_color = 'yellow'

        elif event.char == '5':
            self.active_type = 5
            self.active_color = 'pink'

root = tk.Tk()

app = MainWindow(root)
cntrl = PicController(app.canvas)


root.mainloop()
