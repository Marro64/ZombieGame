from numpy import asarray
from PIL import Image


class heightMap:
    def __init__(self, ref="AI/map.bmp"):
        image = Image.open(ref).convert("L")
        # noinspection PyTypeChecker
        image_array = asarray(image)
        self.heightmap_array = []
        for row in image_array:
            normalized_row = []
            for pixel in row:
                normalized_row.append(pixel / 255)
            self.heightmap_array.append(normalized_row)

    def get_height_at(self, x, y):
        if x < 0:
            x = 0
        elif x > len(self.heightmap_array) - 1:
            x = len(self.heightmap_array) - 1
        if y < 0:
            y = 0
        elif y > len(self.heightmap_array[0]) - 1:
            y = len(self.heightmap_array) - 1

        return self.heightmap_array[x][y]
