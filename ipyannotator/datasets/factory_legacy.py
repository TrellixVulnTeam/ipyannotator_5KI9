# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/14_datasets_factory_legacy.ipynb (unless otherwise specified).

__all__ = ['get_settings']

# Internal Cell
import json
import os

import pandas as pd

from enum import Enum, auto
from pathlib import Path


from ..base import Settings
from .download import (get_cifar10,
                                            get_cub_200_2011,
                                            get_oxford_102_flowers)
from .generators_legacy import create_color_classification

from .generators import create_object_detection, xyxy_to_xywh

# Internal Cell
class DS(Enum):
    ARTIFICIAL_CLASSIFICATION = auto()
    ARTIFICIAL_DETECTION = auto()
    CIFAR10 = auto()
    CUB200 = auto()
    OXFORD102 = auto()

# Cell
def get_settings(dataset: DS):
    """
    Handle the necessary to dowload and save the datasets
    """
    if dataset == DS.ARTIFICIAL_CLASSIFICATION:
        project_path = Path('data/artificial_classification/')
        project_file = project_path / 'annotations.json'
        image_dir = 'images'
        create_color_classification(path=project_path, n_samples=50, size=(500, 500))
        annotations = pd.read_json(project_file).T['labels'].to_dict()
        anno = {str(project_path / image_dir / k): [f'{v}.jpg'] for k, v in annotations.items()}

        with open(project_file, 'w') as f:
            json.dump(anno, f)

        return Settings(project_path=project_path,
                        project_file=project_file,
                        image_dir=image_dir,
                        label_dir='class_images',
                        # used on create step - should be empty!
                        result_dir='create_results',
                        im_width=50, im_height=50,
                        label_width=30, label_height=30,
                        n_cols=3)

    elif dataset == DS.ARTIFICIAL_DETECTION:
        project_path = Path('data/artificial_detection/')
        project_file = project_path / 'annotations.json'
        image_dir = 'images'
        label_dir = None
        im_width = 50
        im_height = im_width

        create_object_detection(path=project_path, n_samples=50, n_objects=1, size=(500, 500))
        annotations = pd.read_json(project_file).T

        """Convert artifical dataset annotations to old bbox ipyannotator format
        {'imagename.jpg': {
            'bbox': [{'x':0, 'y': 0, 'width': 100, 'heigth': 100}],
            'labels': [[]]
        }}"""
        anno = annotations.T.to_dict('records')[0]
        annotation_on_explore = {}
        bbox_keys = ['x', 'y', 'width', 'height']

        for k, v in anno.items():
            key = os.path.join(project_path, image_dir, k)
            value = dict(
                zip(bbox_keys, xyxy_to_xywh(v))
            )
            annotation_on_explore[key] = {'bbox': [value], 'labels': [[]]}

        with open(project_file, 'w') as f:
            json.dump(annotation_on_explore, f)

        return Settings(project_path=project_path,
                        project_file=project_file,
                        image_dir=image_dir,
                        label_dir=label_dir,
                        result_dir='create_results',
                        im_width=im_width, im_height=im_height)

    elif dataset == DS.CIFAR10:
        cifar_train_p, cifar_test_p = get_cifar10(Path('data'))

        return Settings(project_path=Path('data/cifar10/'),
                        project_file=cifar_test_p,
                        image_dir='test',
                        label_dir=None,
                        # used on create step - should be empty!
                        result_dir='create_results',
                        im_width=50, im_height=50,
                        label_width=140, label_height=30,
                        n_cols=2)

    elif dataset == DS.OXFORD102:
        flowers102_train_p, flowers102_test_p = get_oxford_102_flowers(Path('data'))

        return Settings(project_path=Path('data/oxford-102-flowers'),
                        project_file=flowers102_test_p,
                        image_dir='jpg',
                        label_dir=None,
                        # used on create step - should be empty!
                        result_dir='create_results',
                        im_width=50, im_height=50,
                        label_width=40, label_height=30,
                        n_cols=7)

    elif dataset == DS.CUB200:
        cub200_train_p, cub200_test_p = get_cub_200_2011(Path('data'))

        return Settings(project_path=Path('data/CUB_200_2011'),
                        project_file=cub200_test_p,
                        image_dir='images',
                        label_dir=None,
                        # used on create step - should be empty!
                        result_dir='create_results',
                        im_width=50, im_height=50,
                        label_width=50, label_height=50,
                        n_cols=7)
    else:
        raise UserWarning(f"Dataset {dataset} is not supported!")

# Internal Cell
def _combine_train_test(project_path: Path):
    # combine train/test in one json file.
    # Used to generate all possible class labels
    all_annotations = project_path / "annotations.json"

    with open(project_path / "annotations_train.json", "rb") as train:
        tr = json.load(train)

    with open(project_path / "annotations_test.json", "rb") as test:
        te = json.load(test)

    with open(all_annotations, "w") as outfile:
        json.dump({**tr, **te}, outfile)
    return all_annotations