import tensorflow as tf

from .aeh import SpatialPatternParameters, SpatialPatterns, spatial_patterns
from .de_test import test
from .dp_hmrf import (
    TissueSegmentation,
    TissueSegmentationParameters,
    TissueSegmentationStatus,
    tissue_segmentation,
)
from .gaussian_process import GP, SGPIPM, GPControl, fit, fit_detailed, fit_fast
from .io import read_spaceranger
from .svca import fit_spatial_interactions, test_spatial_interactions
from .version import version as __version__

gpus = tf.config.experimental.list_physical_devices("GPU")
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
            tf.config.experimental.set_virtual_device_configuration(
                gpu,
                [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=30000)],
            )
        logical_gpus = tf.config.experimental.list_logical_devices("GPU")
    except RuntimeError as e:
        print(e)

del tf
del gpus
