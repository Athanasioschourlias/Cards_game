import tkinter as tk
import tkinter.colorchooser as col
import tkinter.simpledialog as sd
import time


class MyApp():
    
    def __init__(self, root):
        self.root = root
        root.title("Drwing V1.0.0")
        root.geometry("{}x{}+{}+{}".format("800","700","300","300"))
        root.resizable(True, True)
        self.mb = tk.Menubutton(self.root, text="Options")
        self.mb.pack()
        self.root.config(menu = self.mb)
        self.m = tk.Menu(self.mb)
        self.mb.config(menu = self.m)
        self.m.add_command(label = "line  color", command = self.color_select)
        self.m.add_command(label = "line thiknes", command = self.line_select)
        self.m.add_command(label = "clear", command = self.clear)
        self.m.add_separator()
        self.m.add_command(label = "Exit", command = self.Exit)
        self.create_canvas()
        self.line_color = "black" #default line drawing color
        self.line_width = 2 #default line drawing size

    def create_canvas(self):
        self.canvas = tk.Canvas(self.root, bg = '#e0e0ff')
        self.canvas.pack(fill = 'both', expand = 1)
        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw_line)
    
    def color_select(self):
        color = col.askcolor(initialcolor = self.line_color, parent = self.root, title = "color selection")
        print(color)
        if color[1]:
            self.line_color = color[1]
    
    def line_select(self):
        line = sd.askstring("line thickness", "please give a number from [1-10] for how thick the line you want to be")

        try:
            line = int(line)
            if 0 < line < 11: self.line_width = line
        except:
            pass
    
    def clear(self):
        self.canvas.delete("all")

    def start_draw(self, event):
        self.lastx, self.lasty = event.x, event.y
    
    def draw_line(self, event):
        self.canvas.create_line((self.lastx, self.lasty, event.x, event.y), fill = 'black' , width = 2)
        self.lastx, self.lasty = event.x, event.y



def main():
        root = tk.Tk()
        MyApp(root)
        root.mainloop()
    
if __name__ == "__main__":
    main()

     


