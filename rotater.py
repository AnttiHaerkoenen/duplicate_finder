import sys
import os


def rotate_pics(files):
    for file in files:
        new_name = '_'.join((file, 'ROT'))
        os.system(f'convert {file} -rotate 180 {file}_ROT')
        os.rename(new_name, file)
        print(f'{file} rotated')


if __name__ == '__main__':
    rotate_pics(sys.argv[1:])
