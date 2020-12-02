from __future__ import print_function

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from os import listdir, makedirs
from os.path import join, isfile, exists
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import shutil
from tqdm import tqdm
from time import time
# import keras
from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout, Reshape, GlobalMaxPooling1D
from keras.layers import Conv1D, MaxPooling1D
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.callbacks import TensorBoard