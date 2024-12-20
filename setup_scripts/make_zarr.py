import os
import shutil
from pathlib import Path

import spatialdata as sd
from spatialdata_io import visium_hd

project_path = os.environ["project"]
path = Path(project_path).resolve()
path_read = path / "data"
path_write = path / "data.zarr"

sdata = visium_hd(
    path_read,
    load_all_images=True,
    fullres_image_file="data/Visium_HD_Mouse_Embryo_tissue_image.btf",
)

if path_write.exists():
    shutil.rmtree(path_write)
sdata.write(path_write)
