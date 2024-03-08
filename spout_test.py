from spout.streams import Stream
from spout.structs import Function, Predicate, Operation
from PIL import Image
import numpy as np

# 이미지 스트림 정의
class ImageStream(Stream):
    def __init__(self, image_paths):
        super().__init__()
        self.image_paths = image_paths

    def __iter__(self):
        for path in self.image_paths:
            image = Image.open(path)
            yield np.array(image)

# 이미지를 그레이스케일로 변환하는 함수
class ConvertToGrayscale(Function):
    def apply(self, input):
        return Image.fromarray(input).convert('L')

# 이미지를 표시하는 연산
class DisplayImage(Operation):
    def perform(self, input):
        input.show()

# 이미지 파일 경로 목록
image_paths = [r'C:\Users\chsjk\PycharmProjects\kohya_ss\train_dataset\hyerim_sketch_train\model\sample\hyerimsketchxx_015500_00_20240228100112.png']  # 이미지 경로로 교체

# 이미지 스트림 생성
image_stream = ImageStream(image_paths)

# 스트림 처리 파이프라인 구성 및 실행
image_stream.map(ConvertToGrayscale()).for_each(DisplayImage())
