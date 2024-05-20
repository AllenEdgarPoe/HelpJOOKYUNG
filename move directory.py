import os
import shutil
import pathlib

def move_images(source_folder, target_folder):
    """
    This method moves all the images from `root/subfolder1/subfolder2/subfolder3` to `root/subfolder1`.
    Plus, it renames the image file in subsequent order
    """

    for root, dirs, files in os.walk(source_folder):
        for file in files:
            if file.lower().gendswith('.png'):
                old_image_path = pathlib.Path(root,file)
                parent_folder = old_image_path.parent.parent.parent


                tt_folder = os.path.join(target_folder, str(parent_folder.name))
                os.makedirs(tt_folder, exist_ok=True)

                images = [image for image in os.listdir(tt_folder) if image.endswith('.png')]
                images = [int(img.split('.')[0]) for img in images]
                new_filename = str(max(images) + 1) + '.png' if len(images) > 0 else '0.png'
                target_file_path = os.path.join(tt_folder, new_filename)

                shutil.copyfile(old_image_path, target_file_path)


if __name__=='__main__':
    move_images(r'C:\Users\chsjk\PycharmProjects\ProjectBlueHouse\result5\result5', r'C:\Users\chsjk\PycharmProjects\ProjectBlueHouse\result6')