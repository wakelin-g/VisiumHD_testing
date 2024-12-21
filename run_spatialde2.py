import os

import spatialdata as sd
import SpatialDE2

out_dir = "outputs/"

sdata = sd.read_zarr("data.zarr")
adata = sdata["square_016um"].copy()

spatialde2_test = SpatialDE.test(adata, stack_kernels=False, use_cache=False)
spatialde2_test.to_csv(os.path.join(out_dir, "spatialde2_outputs.csv"))
