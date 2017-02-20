import tkinter as tk
from PIL import Image, ImageTk

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
    activeRect = {}
    def __init__(self, canvas):
        self.image_index = 1
        self.canvas = canvas

        self.activeRect = self.canvas.create_rectangle(0,0,0,0,fill='red')
        self.canvas.bind('<Button-1>', self.click_callback)
        self.canvas.bind('<ButtonRelease-1>', self.clickUp_callback)
        self.canvas.bind('<B1-Motion>', self.motion_callback)
        self.canvas.bind('<Key>', self.key_callback)
        self.canvas.focus_set()
        
        self.draw_picture('set1/img%i%i%i.jpg'%(image_index//100,image_index//10))


    def draw_picture(self, filename):
        image = Image.open(filename)
        #image = image.resize((1280,960))
        self.photo = ImageTk.PhotoImage(image)
        w = self.canvas.create_image((0,0), image=self.photo,anchor='nw')


    def click_callback(self, event):
        cx = self.canvas.canvasx(event.x)
        cy = self.canvas.canvasx(event.y)
        print('clicked at ', cx,cy)
        self.activeRect = self.canvas.create_rectangle(cx,cy,cx,cy,fill='red')

    def clickUp_callback(self,event):
        coords = self.canvas.coords(self.activeRect)
        coords[2] = event.x
        coords[3] = event.y

        self.canvas.coords(self.activeRect, coords)

    def motion_callback(self,event):
        coords = self.canvas.coords(self.activeRect)
        coords[2] = event.x
        coords[3] = event.y

        self.canvas.coords(self.activeRect, coords)



    def key_callback(self, event):
        print('pressed', event.char)
        if event.char == " ":
            image = Image.open(filename)
            #image = image.resize((1280,960))
            self.photo = ImageTk.PhotoImage(image)
            self.canvas.itemconfig(self.image, image=photo)

root = tk.Tk()

app = MainWindow(root)
cntrl = PicController(app.canvas)


root.mainloop()
