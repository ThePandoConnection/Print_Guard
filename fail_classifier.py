import matplotlib.pyplot as plt
import numpy as np
import PIL
import tensorflow as tf

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential

import pathlib
dataset_url = "file://Images.zip"
data_dir = tf.keras.utils.get_file('print_photos', origin=dataset_url, untar=True)
data_dir = pathlib.Path(data_dir)