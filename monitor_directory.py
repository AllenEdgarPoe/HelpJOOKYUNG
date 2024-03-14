import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import logging
from PIL import Image
import cv2

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
observer = Observer()
new_event = True

class CustomEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        global new_event
        new_file = event.src_path
        if new_file.lower().endswith(('.png', '.jpg', '.jpeg')):
            time.sleep(3)
            open_image(new_file)

def open_image(image_path):
    global new_event
    logging.info(f'Opening image: {image_path}')
    img = cv2.imread(image_path)
    cv2.imshow(image_path, img)
    while True:
        key = cv2.waitKey(1)
        if new_event:
            cv2.destroyWindow(image_path)



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
    watch_dir(r'C:\Users\chsjk\PycharmProjects\ProjectBlueHouse\result2')
