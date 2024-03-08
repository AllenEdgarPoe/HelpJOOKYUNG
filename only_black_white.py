from PIL import Image
import numpy as np
def only_black_or_white(image, threshold=200):
    """
    :param image: PIL Image object
    :param threshold: float
    :return: PIL Image object
    """
    if image.mode != 'RGB':
        image = image.convert('RGB')

    data = np.array(image)
    is_nearly_black = (data < threshold).all(axis=-1)
    data[is_nearly_black] = [0,0,0]
    data[~is_nearly_black] = [255,255,255]

    return Image.fromarray(data, 'RGB')


if __name__ == "__main__":
    img = Image.open(r'C:\Users\chsjk\PycharmProjects\kohya_ss\train_dataset\hyerim_sketch_train2\img\100_hyerimsketchxx_lineart\ComfyUI_0109.png')
    new_img = only_black_or_white(img)
    new_img.save(r'C:\Users\chsjk\PycharmProjects\kohya_ss\train_dataset\hyerim_sketch_train2\img\100_hyerimsketchxx_lineart\test.png')