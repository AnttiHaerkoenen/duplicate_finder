import os
import argparse

from PIL import Image
import numpy as np


def find_duplicates(
        files,
        hash_size,
        tolerance,
        duplicate_mark,
):
    hashes = np.empty((0,), dtype=str)
    duplicates = []

    print("Analysing...")
    for file in files:
        with Image.open(file) as image:
            img_hash = dhash(image, hash_size)

        if is_duplicate(img_hash, hashes, tolerance=tolerance):
            basename, suffix = file.split('.')
            os.rename(file, f'{basename}{duplicate_mark}.{suffix}')
            duplicates.append(file)
        else:
            hashes = np.append(hashes, img_hash)
    print(f"{len(duplicates)} duplicates found.")


def dhash(image, hash_size):
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

    difference = difference.reshape((-1, hash_size))

    hex_str = difference[:, 0] * 2 ** 3 \
        + difference[:, 1] * 2 ** 2 \
        + difference[:, 2] * 2 \
        + difference[:, 3] * 1

    return ''.join('{:01x}'.format(x) for x in hex_str)


def is_duplicate(img_hash, hashes, tolerance=0):
    for h in hashes:
        if hamming_distance(h, img_hash) <= tolerance:
            return True
    return False


def hamming_distance(str_1, str_2):
    if len(str_1) != len(str_2):
        raise ValueError("Strings must be equally long!")

    return sum(e1 != e2 for e1, e2 in zip(str_1, str_2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Find similar pictures using perceptual hashing")
    parser.add_argument(
        'files',
        nargs='+',
        help="File names",
    )
    parser.add_argument(
        '--hash-size',
        dest='hash_size',
        type=int,
        default=9,
        help="Size of hash (one side), default 9",
    )
    parser.add_argument(
        '--tolerance',
        dest='tolerance',
        type=int,
        default=0,
        help="Tolerance level for differences, default 0",
    )
    parser.add_argument(
        '--duplicate-mark',
        dest='duplicate',
        default='_DUPLICATE',
        help="Duplicate mark",
    )

    args = parser.parse_args()
    find_duplicates(
        args.files,
        hash_size=args.hash_size,
        tolerance=args.tolerance,
        duplicate_mark=args.duplicate,
    )
