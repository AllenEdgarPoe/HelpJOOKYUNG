import glob
import os
import logging 
import msvcrt
from PIL import Image
import tkinter as tk
from PIL import Image, ImageTk

def open_image(image_path):
    root = tk.Tk()
    img = Image.open(image_path)
    tk_img = ImageTk.PhotoImage(img)

    def on_esc(event):
        root.destroy()

    def on_delete(event):
        os.remove(image_path)
        print(f'Deleted image for {image_path}')
        root.destroy()

    label = tk.Label(root, image=tk_img)
    label.pack()
    root.bind('<End>', on_esc)
    root.bind('<Delete>', on_delete)
    root.after(500, lambda:root.focus_force())
    root.mainloop()
def main(root_dir):
    for dir_path, dirs, files in os.walk(root_dir):
        file_list = glob.glob(os.path.join(dir_path, '*.png'))
        if len(file_list)>0:
            for file in file_list:
                open_image(file)


if __name__=='__main__':
    main(r'C:\Users\chsjk\PycharmProjects\ProjectBlueHouse\result6')