import os
import tensorflow as tf
import spatialdata as sd
import SpatialDE2

gpus = tf.config.experimental.list_physical_devices("GPU")
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
            tf.config.experimental.set_virtual_device_configuration(
                gpu,
                [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=30000)],
            )
    except RuntimeError as e:
        print(e)

out_dir = "outputs/"

sdata = sd.read_zarr("data.zarr")
adata = sdata["square_016um"].copy()

spatialde2_test = SpatialDE2.test(adata, stack_kernels=False, use_cache=False)
spatialde2_test.to_csv(os.path.join(out_dir, "spatialde2_outputs.csv"))
