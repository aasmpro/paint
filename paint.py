from tkinter import *
from tkinter.colorchooser import askcolor
from PIL import Image, ImageDraw
import datetime


class Paint(Frame):
    def __init__(self):
        self.root = Tk()
        super().__init__()
        self.master.title("Paint")

        self.old_x = None
        self.old_y = None
        self.shape_x = None
        self.shape_y = None
        self.line_width = 1
        self.color1 = 'black'
        self.color2 = 'white'

        tools_frame = Frame(self)
        tools_frame.pack(fill='both')

        # color buttons
        self.color1_button = Button(tools_frame, command=self.choose_color1, highlightbackground=self.color1,
                                    background=self.color1, activebackground=self.color1)
        self.color1_button.pack(side="left", padx=0, pady=5)

        self.color2_button = Button(tools_frame, command=self.choose_color2, highlightbackground=self.color2,
                                    background=self.color2, activebackground=self.color2)
        self.color2_button.pack(side="left", padx=0, pady=5)

        self.color1_button.bind("<Enter>", self.set_color1_button)
        self.color2_button.bind("<Enter>", self.set_color2_button)

        # tool buttons
        self.brush_button = Button(tools_frame, text='\u23FA', command=self.use_brush, height=1, width=1)
        self.brush_button.pack(side="left", padx=(100, 0), pady=5)

        self.line_button = Button(tools_frame, text='\\', command=self.use_line, height=1, width=1)
        self.line_button.pack(side="left", padx=0, pady=5)

        self.circle_button = Button(tools_frame, text='\u20DD', command=self.use_circle, height=1, width=1)
        self.circle_button.pack(side="left", padx=0, pady=5)

        self.rectangle_button = Button(tools_frame, text='\u20DE', command=self.use_rectangle, height=1, width=1)
        self.rectangle_button.pack(side="left", padx=0, pady=5)

        self.eraser_button = Button(tools_frame, text='\u232B', command=self.use_eraser, height=1, width=1)
        self.eraser_button.pack(side="left", padx=0, pady=5)

        self.choose_size_button = Scale(tools_frame, from_=1, to=50, orient=HORIZONTAL, command=self.size)
        self.choose_size_button.pack(side="left", padx=5, pady=5)

        # save button
        self.save_button = Button(tools_frame, text='save', command=self.save)
        self.save_button.pack(side="right", padx=0, pady=5)

        # canvas
        canvas_frame = Frame(self)
        canvas_frame.pack(fill='both')

        self.canvas = Canvas(canvas_frame, bg='white', width=600, height=600)
        self.canvas.pack(side="left", padx=0, pady=0)

        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)
        self.canvas.bind('<Motion>', self.set_position)

        # cursor position
        footer_frame = Frame(self)
        footer_frame.pack(fill='both')

        self.position_label = Label(footer_frame, text='x = 0  y = 0')
        self.position_label.pack(side='right')

        # PIL image variable
        self.image = Image.new('RGB', (600, 600), 'white')
        self.draw = ImageDraw.Draw(self.image)

        self.active_button = self.brush_button
        self.brush_button.config(relief=SUNKEN)

        self.pack()
        self.root.mainloop()

    def set_color1_button(self, event):
        self.color1_button['background'] = self.color1
        self.color1_button['highlightbackground'] = self.color1
        self.color1_button['activebackground'] = self.color1

    def set_color2_button(self, event):
        self.color2_button['background'] = self.color2
        self.color2_button['highlightbackground'] = self.color2
        self.color2_button['activebackground'] = self.color2

    def choose_color1(self):
        self.eraser_on = False
        self.color1 = askcolor(color=self.color1)[1]
        self.set_color1_button(None)

    def choose_color2(self):
        self.eraser_on = False
        self.color2 = askcolor(color=self.color2)[1]
        self.set_color2_button(None)

    def use_brush(self):
        self.activate_button(self.brush_button)

    def use_line(self):
        self.activate_button(self.line_button)

    def use_circle(self):
        self.activate_button(self.circle_button)

    def use_rectangle(self):
        self.activate_button(self.rectangle_button)

    def use_eraser(self):
        self.activate_button(self.eraser_button)

    def activate_button(self, some_button):
        self.active_button.config(relief=RAISED)
        some_button.config(relief=SUNKEN)
        self.active_button = some_button

    def paint(self, event):
        paint_color = self.color2 if self.active_button == self.eraser_button else self.color1
        if self.old_x and self.old_y:
            self.canvas.create_line(self.old_x, self.old_y, event.x, event.y,
                                    width=self.line_width, fill=paint_color,
                                    capstyle=ROUND, smooth=TRUE, splinesteps=1)

            self.draw.line([self.old_x, self.old_y, event.x, event.y], width=self.line_width, fill=paint_color)

        self.old_x = event.x
        self.old_y = event.y

    def set_position(self, event):
        self.position_label['text'] = 'x = {}  y = {}'.format(event.x, event.y)

    def create_rectangle(self, event):
        if self.shape_x and self.shape_y:
            pass

    def size(self, size):
        self.line_width = int(size)

    def reset(self, event):
        self.old_x, self.old_y = None, None

    def save(self):
        self.image.save("image{}.png".format(datetime.datetime.now().strftime("%Y%m%d%H%M%S")))


if __name__ == '__main__':
    Paint()
