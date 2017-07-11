import os

from PIL import Image
import numpy as np


def find_duplicates(dir_name, pic_suffices=('.jpg', '.JPG'), hash_size=16, tolerance=0):
    directory = os.path.join(os.path.abspath(os.path.dirname(__name__)), dir_name)
    os.chdir(directory)
    hashes = np.empty((0,), dtype=str)

    for filename in os.listdir(directory):
        if not filename.endswith(pic_suffices):
            continue

        with Image.open(filename) as image:
            img_hash = dhash(image, hash_size)
            print(img_hash)

        if is_duplicate(img_hash, hashes, tolerance=tolerance):
            os.rename(filename, 'DUPLICATE_{0}'.format(filename))
        else:
            hashes = np.append(hashes, img_hash)


def dhash(image, hash_size=16):
    image = image.convert('L').resize(
        (hash_size + 1, hash_size),
        Image.ANTIALIAS,
    )

    difference = np.ndarray((0,), dtype=bool)

    for row in range(hash_size):
        for col in range(hash_size):
            left = image.getpixel((col, row))
            right = image.getpixel((col + 1, row))
            difference = np.append(difference, left > right)

    difference = difference.reshape((-1, 4))

    hex_str: np.ndarray = difference[:, 0] * 2 ** 3 \
        + difference[:, 1] * 2 ** 2 \
        + difference[:, 2] * 2 \
        + difference[:, 3] * 1

    return ''.join('{:01x}'.format(x) for x in hex_str)


def is_duplicate(img_hash, hashes, tolerance=0):
    for h in hashes:
        print(hamming_distance(h, img_hash))
        if hamming_distance(h, img_hash) <= tolerance:
            return True
    return False


def hamming_distance(str_1, str_2):
    if len(str_1) != len(str_2):
        raise ValueError("Strings must be equally long!")

    return sum(e1 != e2 for e1, e2 in zip(str_1, str_2))


if __name__ == '__main__':
    find_duplicates('esimerkki', hash_size=16)
