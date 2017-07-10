import os

from PIL import Image
import numpy as np


def find_duplicates(dir_name, pic_suffices=('.jpg',)):
    directory = os.fsencode(dir_name)
    hashes = np.array()

    for file in os.listdir(directory):
        filename = os.fsdecode(file)

        if not filename.endswith(pic_suffices):
            continue

        with Image.open(filename) as image:
            img_hash = dhash(image)

        if is_duplicate(img_hash, hashes):
            os.rename(filename, 'DUPLICATE_{0}'.format(filename))
        else:
            hashes = np.append(hashes, img_hash)


def dhash(image, hash_size=25):
    image = image.convert('L').resize(
        (hash_size + 1, hash_size),
        Image.ANTIALIAS,
    )

    pixels = np.array(image.getdata()).flatten()


def is_duplicate(img_hash, hashes, tolerance=0):
    pass


def hamming_distance(str_1, str_2):
    if len(str_1) != len(str_2):
        raise ValueError("Strings must be equally long!")

    return sum(e1 != e2 for e1, e2 in zip(str_1, str_1))


if __name__ == '__main__':
    pass
