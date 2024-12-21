import os

import numpy as np
import scanpy as sc
import spatialdata as sd
import tensorflow as tf

import SpatialDE2

out_dir = "outputs/"

sdata = sd.read_zarr("data.zarr")
bb_xmin = 3214.7043187579725
bb_ymin = 1724.7046301254618
bb_xmax = 4423.303665508516
bb_ymax = 2670.3031223505536

sdata_subset = sdata.query.bounding_box(
    axes=["x", "y"],
    min_coordinate=[bb_xmin, bb_ymin],
    max_coordinate=[bb_xmax, bb_ymax],
    target_coordinate_system="downscaled_hires",
)
adata = sdata_subset["square_016um"].copy()
adata.var_names_make_unique()

adata.var["mt"] = adata.var_names.str.startswith("^mt-")
sc.pp.calculate_qc_metrics(adata, qc_vars=["mt"], inplace=True)

sc.pp.filter_cells(adata, min_counts=800)
sc.pp.filter_genes(adata, min_cells=100)

svg_full, _ = SpatialDE2.test(adata, stack_kernels=False, use_cache=False, omnibus=True)
svg_full["total_counts"] = np.asarray(adata.X.sum(axis=0)).squeeze()
svg_full.to_pickle("svg_full.pkl")
