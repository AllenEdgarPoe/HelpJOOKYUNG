import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import logging
import os
import tkinter as tk
from PIL import Image, ImageTk
import pyautogui

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
observer = Observer()

class CustomEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        new_file = event.src_path
        if new_file.lower().endswith(('.png', '.jpg', '.jpeg')):
            time.sleep(4)
            open_image(new_file)

def open_image(image_path):
    root = tk.Tk()
    img = Image.open(image_path)
    tk_img = ImageTk.PhotoImage(img)
    tk.Label(root, image=tk_img).pack()

    window_width = root.winfo_reqwidth()
    window_height = root.winfo_reqheight()
    position_right = int(root.winfo_screenwidth() / 2 - window_width / 2)
    position_down = int(root.winfo_screenheight() / 2 - window_height / 2)

    root.geometry("+{}+{}".format(position_right, position_down))

    # pyautogui.moveTo(root.winfo_screenwidth() / 2, root.winfo_screenheight() / 2)
    root.focus_set()
    def on_esc(event):
        root.destroy()

    def on_delete(event):
        os.remove(image_path)
        print(f'Deleted image for {image_path}')
        root.destroy()

    root.bind('<End>', on_esc)
    root.bind('<Delete>', on_delete)
    root.mainloop()



def watch_dir(dir_path):
    logging.info(f'start watching the directory {dir_path}')
    event_handler = CustomEventHandler()
    observer.schedule(event_handler, dir_path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        observer.stop()
        observer.join()

if __name__ == '__main__':
    watch_dir(r'C:\Users\chsjk\PycharmProjects\ProjectBlueHouse\result5')
