from tkinter import *
from PIL import ImageTk,Image
from tkinter import filedialog
from tkinter.colorchooser import askcolor
import threading
import os
import cv2

c_width = 1024*0.8
c_height = 768*0.8
background = '#FFFFFF'

class Application(Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.x = 0
        self.y = 0
        self.default_color = 'black'
        self.lastdraw = 0
        self.master = master
        self.start_flag = False
        self.pack()
        self.createDrawBoard()

    def createDrawBoard(self):
        #Canvas
        self.drawboard = Canvas(self, width = c_width, height = c_height, bg = background)
        self.drawboard.pack()
        #Buttons
        self.btn_pen = Button(self, name = 'pen', text = "pen")
        self.btn_pen.pack(side='left',padx = 10)
        self.btn_oval = Button(self, name='oval', text="oval")
        self.btn_oval.pack(side='left', padx=10)
        self.btn_oval_hollow = Button(self, name='oval_hollow', text="oval_hollow")
        self.btn_oval_hollow.pack(side='left', padx=10)
        self.btn_rect = Button(self, name='rect', text="rect")
        self.btn_rect.pack(side='left', padx=10)
        self.btn_line = Button(self, name='line', text="line")
        self.btn_line.pack(side='left', padx=10)
        self.btn_vect = Button(self, name='vect', text="vect")
        self.btn_vect.pack(side='left', padx=10)
        self.btn_arc = Button(self, name='arc', text="arc")
        self.btn_arc.pack(side='left', padx=10)
        self.btn_bmp = Button(self, name='bmp', text="open")
        self.btn_bmp.pack(side='left', padx=10)
        self.btn_eraser = Button(self, name='eraser', text="eraser")
        self.btn_eraser.pack(side='left', padx=10)
        self.btn_clear = Button(self, name='clear', text="clear")
        self.btn_clear.pack(side='left', padx=10)
        self.btn_color = Button(self, name='color', text="color")
        self.btn_color.pack(side='left', padx=10)


        #bind_events
        self.btn_pen.bind('<Button-1>',self.eventManager)  #Click event
        self.btn_oval.bind('<Button-1>', self.eventManager)  # Click event
        self.btn_oval_hollow.bind('<Button-1>', self.eventManager)  # Click event
        self.btn_rect.bind('<Button-1>', self.eventManager)  # Click event
        self.btn_line.bind('<Button-1>', self.eventManager)  # Click event
        self.btn_vect.bind('<Button-1>', self.eventManager)  # Click event
        self.btn_arc.bind('<Button-1>', self.eventManager)  # Click event
        self.btn_bmp.bind('<Button-1>', self.eventManager)  # Click event
        self.btn_eraser.bind('<Button-1>', self.eventManager)  # Click event
        self.btn_clear.bind('<Button-1>', self.eventManager)  # Click event
        self.btn_color.bind('<Button-1>', self.eventManager)  # Click event
        self.drawboard.bind('<ButtonRelease-1>',self.stopDraw)  #松开鼠标 event

    def eventManager(self, event):
        name = event.widget.winfo_name()
        print(name)
        self.start_flag = True
        if name == "pen":
            self.drawboard.bind('<B1-Motion>', self.use_pen)
        elif name == "oval":
            self.drawboard.bind('<B1-Motion>', self.draw_oval)
        elif name == "oval_hollow":
            self.drawboard.bind('<B1-Motion>', self.draw_oval_hollow)
        elif name == "rect":
            self.drawboard.bind('<B1-Motion>', self.draw_rect)
        elif name == "line":
            self.drawboard.bind('<B1-Motion>', self.draw_line)
        elif name == "vect":
            self.drawboard.bind('<B1-Motion>', self.draw_vect)
        elif name == "arc":
            self.drawboard.bind('<B1-Motion>', self.draw_arc)
        elif name == "bmp":
            global filename
            filename = filedialog.askopenfilename()
            self.drawboard.bind('<B1-Motion>', self.draw_bmp)
        elif name == "eraser":
            self.drawboard.bind('<B1-Motion>', self.draw_eraser)
        elif name == "clear":
            self.drawboard.delete('all')
        elif name == "color":
            c = askcolor(color=self.default_color, title='请选择颜色')
            print(c)  # c的值 ((128.5, 255.99609375, 0.0), '#80ff00')
            self.default_color = c[1]

    # def pen(self,event):
    #     self.start_flag = True
    #     self.drawboard.bind('<B1-Motion>',self.use_pen)

    def use_pen(self,event):
        self.startDraw(event)
        print('self.x=', self.x, ',self.y=', self.y)
        self.drawboard.create_line(self.x, self.y, event.x, event.y, fill=self.default_color)
        self.x = event.x  #改变画线起点
        self.y = event.y

    def draw_oval(self,event):
        self.startDraw(event)
        print('self.x=', self.x, ',self.y=', self.y)
        self.lastdraw = self.drawboard.create_oval(self.x, self.y, event.x, event.y, outline = self.default_color, fill=self.default_color)#用这个lastdraw是为了让不出现方的情况
        # self.x = event.x  #改变画线起点
        # self.y = event.y
    def draw_oval_hollow(self,event):
        self.startDraw(event)
        print('self.x=', self.x, ',self.y=', self.y)
        self.lastdraw = self.drawboard.create_oval(self.x, self.y, event.x, event.y, outline = self.default_color)#用这个lastdraw是为了让不出现方的情况
        # self.x = event.x  #改变画线起点
        # self.y = event.y

    def draw_rect(self,event):
        self.startDraw(event)
        print('self.x=', self.x, ',self.y=', self.y)
        self.lastdraw = self.drawboard.create_rectangle(self.x, self.y, event.x, event.y, outline=self.default_color)
        # self.x = event.x  #改变画线起点
        # self.y = event.y

    def draw_line(self,event):
        self.startDraw(event)
        print('self.x=', self.x, ',self.y=', self.y)
        self.lastdraw = self.drawboard.create_line(self.x, self.y, event.x, event.y, fill=self.default_color)
        # self.x = event.x  #改变画线起点
        # self.y = event.y

    def draw_vect(self,event):
        self.startDraw(event)
        print('self.x=', self.x, ',self.y=', self.y)
        self.lastdraw = self.drawboard.create_line(self.x, self.y, event.x, event.y, arrow=LAST, fill=self.default_color)
        # self.x = event.x  #改变画线起点
        # self.y = event.y
    def draw_arc(self,event):
        self.startDraw(event)
        print('self.x=', self.x, ',self.y=', self.y)
        self.lastdraw = self.drawboard.create_arc(self.x, self.y, event.x, event.y, outline = self.default_color, fill=self.default_color)
        # self.x = event.x  #改变画线起点
        # self.y = event.y
    def draw_bmp(self,event):
        self.startDraw(event)
        print('self.x=', self.x, ',self.y=', self.y)
        global filename
        global load
        global render
        load = Image.open(filename)
        render = ImageTk.PhotoImage(load)
        self.lastdraw = self.drawboard.create_image((render.width()/2, render.height()/2),image=render)
        # self.x = event.x  #改变画线起点
        # self.y = event.y
    def draw_eraser(self,event):
        self.startDraw(event)
        print('self.x=', self.x, ',self.y=', self.y)
        self.drawboard.create_rectangle(event.x - 3, event.y - 3, event.x + 3, event.y + 3, outline = background, fill=background)
        self.x = event.x  #改变画线起点
        self.y = event.y
    def startDraw(self,event):
        self.drawboard.delete(self.lastdraw)
        if self.start_flag:
            self.start_flag = False
            self.x = event.x
            self.y = event.y

    def stopDraw(self,event):
        self.start_flag = True
        self.lastdraw = 0

def color2gray():
    global filename
    img = cv2.imread(filename)
    template = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return template







if __name__ == '__main__':
    root = Tk()
    # filename = 'pic.jpg'
    # load = Image.open(filename)
    # render = ImageTk.PhotoImage(load)

    # img_cv = cv2.imread(filename)
    # c_img = Image.fromarray(img_cv)  # 将图像转换为Image对象
    # render = ImageTk.PhotoImage(image=c_img)

    root.title("画图板-小雨制作")
    root.geometry('1024x768+200+20')
    app = Application(master = root)
    root.mainloop()


