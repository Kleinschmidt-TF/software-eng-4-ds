from PIL import Image, ImageDraw, ImageFont, ImageTk
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt
import tkinter as tk
import numpy as np
import time

class RenderGUI:
    def __init__(self):
        self.frame = tk.Tk()

        self.img = None
        self.panel = tk.Label(self.frame)
        self.panel.pack(side=tk.TOP,fill="both",expand="yes")

        self.s = tk.Label(self.frame, text="")
        self.s.pack()
        self.v = tk.IntVar()
        self.v.set(0)  # initializing the choice, i.e. Python

        shapes = [
            ("CIRCLE",1),
            ("SQUARE",2),
            ("RECT",3),
            ("TRIANGLE",4)
        ]

    def draw_square(self):
        im = Image.new("RGB",(600,300),(256,256,256))
        draw = ImageDraw.Draw(im)
        draw.rectangle((250, 100, 350, 200), outline="black")
        outfile = "/Users/saxen/Desktop/cube.png"
        im.save(outfile,"JPEG")
        #time.sleep(3)
        self.img = ImageTk.PhotoImage(Image.open(outfile))
        self.panel.configure(image=self.img)
        #frame.update_idletasks()

    def draw_circle(self):
        #global img
        im = Image.new("RGB",(600,300),(256,256,256))
        draw = ImageDraw.Draw(im)
        draw.ellipse((100,100,200,200),outline="black")
        outfile = "/Users/saxen/Desktop/circle.png"
        im.save(outfile,"JPEG")
        # time.sleep(3)
        self.img = ImageTk.PhotoImage(Image.open(outfile))
        self.panel.configure(image=self.img)
        #frame.update_idletasks()

    def draw_3D(self):
        #global frame
        self.panel.configure(image=None)

        fig = plt.figure()
        ax = Axes3D(fig)
        X = np.array([[0,0,1,1],[0,0,1,1],[0,0,1,1],[0,0,1,1],[0,0,1,1]])
        Y = np.array([[0,0,0,0],[1,1,1,1],[1,1,1,1],[0,0,0,0],[0,0,0,0]])
        Z = np.array([[1,0,0,1],[1,0,0,1],[1,1,1,1],[1,1,1,1],[0,0,0,0]])
        ax.plot_surface(X,Y,Z,rstride=1,cstride=1,alpha=0.5)

        canvas = FigureCanvasTkAgg(fig,master=self.frame)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP,fill=tk.BOTH,expand=1)

        toolbar = NavigationToolbar2Tk(canvas,self.frame)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tk.TOP,fill=tk.BOTH,expand=1)

    def draw_shape(self):
        #global img

        im = Image.new("RGB",(600,300),(256,256,256))
        draw = ImageDraw.Draw(im)
        blk = "black"
        if (self.v.get() == 0):
            draw.ellipse((100,100,200,200),outline=blk)
        else:
            draw.rectangle((250,100,350,200),outline=blk)

        outfile = "/Users/saxen/Desktop/circle.png"
        im.save(outfile,"JPEG")
        # time.sleep(3)
        self.img = ImageTk.PhotoImage(Image.open(outfile))
        self.panel.configure(image=self.img)

    def guiElements(self,call:bool):
        if call is False:
            pass
        else:
            for val,language in enumerate(self.shapes):
                tk.Radiobutton(self.frame,
                               text=language,
                               padx=20,
                               variable=self.v,
                               value=val).pack(anchor=tk.W)

            btn_greet = tk.Button(self.frame,
                                  text="SAY HELLO",
                                  command=self.say_hello)

            btn_greet.pack(side=tk.BOTTOM)

            btn_draw_sqr = tk.Button(self.frame,
                                     text="DRAW SQUARE",
                                     command=self.draw_square)

            btn_draw_sqr.pack(side=tk.BOTTOM)

            btn_draw_cir = tk.Button(self.frame,
                                     text="DRAW CIRCLE",
                                     command=self.draw_circle)

            btn_draw_cir.pack(side=tk.BOTTOM)

            btn_draw_shape = tk.Button(self.frame,
                                       text="DRAW SHAPE",
                                       command=self.draw_shape)

            btn_draw_shape.pack(side=tk.BOTTOM)

            btn_draw_3D = tk.Button(self.frame,
                                    text="DRAW 3D",
                                    command=self.draw_3D)

            btn_draw_3D.pack(side=tk.BOTTOM)

    def prepare_frame(self):
        window_height = 500
        window_width = 500

        screen_width = self.frame.winfo_screenwidth()
        screen_height = self.frame.winfo_screenheight()

        x_coordinate = int((screen_width / 2) - (window_width / 2))
        y_coordinate = int((screen_height / 2) - (window_height / 2))

        self.frame.geometry("{}x{}+{}+{}".format(window_width,window_height,x_coordinate,y_coordinate))
        import os
        os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')

    def run(self):
        self.guiElements(False)
        self.prepare_frame()
        # draw_circle()
        self.draw_square()
        self.frame.mainloop()

if __name__ == '__main__':
    RenderGUI().run()