# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/01a_datasets_download.ipynb (unless otherwise specified).

__all__ = ['get_cifar10', 'get_oxford_102_flowers', 'get_cub_200_2011']

# Internal Cell

import glob
import json
from pathlib import Path
import os
import subprocess
import tarfile
import urllib
import zlib

# Internal Cell

def _download_url(url, root, filename=None):
    """Download a file from a url and place it in root.
    Args:
        url (str): URL to download file from
        root (str): Directory to place downloaded file in
        filename (str, optional): Name to save the file under. If None, use the basename of the URL
    """
    root = os.path.expanduser(root)
    if not filename:
        filename = os.path.basename(url)
    fpath = os.path.join(root, filename)
    os.makedirs(root, exist_ok=True)

    if not os.path.isfile(fpath):
        try:
            print('Downloading ' + url + ' to ' + fpath)
            urllib.request.urlretrieve(url, fpath)
        except (urllib.error.URLError, IOError) as e:
            if url[:5] == 'https':
                url = url.replace('https:', 'http:')
                print('Failed download. Trying https -> http instead.'
                        ' Downloading ' + url + ' to ' + fpath)
                urllib.request.urlretrieve(url, fpath)
    else:
        print(f'File {filename} already exists, skip download.')


# Internal Cell
def _extract_tar(tar_path, output_dir):
    try:
        print('Extracting...')
        with tarfile.open(tar_path) as tar:
            tar.extractall(output_dir)
    except (tarfile.TarError, IOError, zlib.error) as e:
        print('Failed to extract!', e)

# Cell
def get_cifar10(output_dir):
    """
    Download the cifar10 dataset.
    """

    output_dir = Path(output_dir)
    dataset_dir = output_dir / 'cifar10'

    _download_url(url='https://s3.amazonaws.com/fast-ai-imageclas/cifar10.tgz', root=output_dir)

    if not dataset_dir.is_dir():
        _extract_tar(output_dir / 'cifar10.tgz', output_dir)
    else:
        print(f'Directory {dataset_dir} already exists, skip extraction.')

    print('Generating train/test data..')
    imdir_train = dataset_dir / 'train'
    imdir_test = dataset_dir / 'test'

    # split train/test
    train = [Path(p) for p in glob.glob(f'{imdir_train}/*/*')]
    test = [Path(p) for p in glob.glob(f'{imdir_test}/*/*')]

    # generate data for annotations.json
    # {'image-file.jpg': ['label1.jpg']}
    annotations_train = dict((str(p), [f'{p.parts[-2]}.jpg']) for p in train)
    annotations_test = dict((str(p), [f'{p.parts[-2]}.jpg']) for p in test)

    train_path = dataset_dir / 'annotations_train.json'
    test_path = dataset_dir / 'annotations_test.json'

    with open(train_path, 'w') as f:
        json.dump(annotations_train, f)

    with open(test_path, 'w') as f:
        json.dump(annotations_test, f)
    print("Done")
    return train_path, test_path

# Cell
def get_oxford_102_flowers(output_dir):
    """
    Download the oxford flowers dataset.
    """
    output_dir = Path(output_dir)
    dataset_dir = output_dir / 'oxford-102-flowers'

    _download_url(url='https://s3.amazonaws.com/fast-ai-imageclas/oxford-102-flowers.tgz', root=output_dir)

    if not dataset_dir.is_dir():
        _extract_tar(output_dir / 'oxford-102-flowers.tgz', output_dir)
    else:
        print(f'Directory {dataset_dir} already exists, skip extraction.')

    print('Generating train/test data..')
    with open(dataset_dir / 'train.txt', 'r') as f:
        annotations_train = dict(tuple(line.split()) for line in f)

    annotations_train = {str(dataset_dir / k): [v+'.jpg'] for k, v in annotations_train.items()}

    with open(dataset_dir / 'test.txt', 'r') as f:
        annotations_test = dict(tuple(line.split()) for line in f)

    annotations_test = {str(dataset_dir / k): [v+'.jpg'] for k, v in annotations_test.items()}

    train_path = dataset_dir / 'annotations_train.json'
    test_path = dataset_dir / 'annotations_test.json'

    with open(train_path, 'w') as f:
        json.dump(annotations_train, f)

    with open(test_path, 'w') as f:
        json.dump(annotations_test, f)
    print("Done")
    return train_path, test_path

# Cell
def get_cub_200_2011(output_dir):
    """
    Download the CUB 200 2001 dataset.
    """
    output_dir = Path(output_dir)
    dataset_dir = output_dir / 'CUB_200_2011'

    _download_url(url='https://s3.amazonaws.com/fast-ai-imageclas/CUB_200_2011.tgz', root=output_dir)

    if not dataset_dir.is_dir():
        _extract_tar(output_dir / 'CUB_200_2011.tgz', output_dir)
    else:
        print(f'Directory {dataset_dir} already exists, skip extraction.')

    print('Generating train/test data..')
    with open(dataset_dir / 'images.txt','r') as f:
        image_id_map = dict(tuple(line.split()) for line in f)

    with open(dataset_dir / 'classes.txt','r') as f:
        class_id_map = dict(tuple(line.split()) for line in f)

    with open(dataset_dir / 'train_test_split.txt','r') as f:
        splitter = dict(tuple(line.split()) for line in f)

    # image ids for test/train
    train_k = [k for k, v in splitter.items() if v == '0']
    test_k = [k for k, v in splitter.items() if v == '1']

    with open(dataset_dir / 'image_class_labels.txt','r') as f:
        anno_ = dict(tuple(line.split()) for line in f)

    annotations_train = {str(dataset_dir / 'images' / image_id_map[k]): [class_id_map[v]+'.jpg'] for k, v in anno_.items() if k in train_k}
    annotations_test = {str(dataset_dir / 'images' / image_id_map[k]): [class_id_map[v]+'.jpg'] for k, v in anno_.items() if k in test_k}

    train_path = dataset_dir  / 'annotations_train.json'
    test_path = dataset_dir  / 'annotations_test.json'

    with open(train_path, 'w') as f:
        json.dump(annotations_train, f)

    with open(test_path, 'w') as f:
        json.dump(annotations_test, f)
    print("Done")
    return train_path, test_path