import os
import shutil
import subprocess
from pathlib import Path

from utils import download

# Visium_HD_Mouse_Embryo
urls = [
    "https://cf.10xgenomics.com/samples/spatial-exp/3.0.0/Visium_HD_Mouse_Embryo/Visium_HD_Mouse_Embryo_tissue_image.btf",
    "https://cf.10xgenomics.com/samples/spatial-exp/3.0.0/Visium_HD_Mouse_Embryo/Visium_HD_Mouse_Embryo_cloupe_008um.cloupe",
    "https://cf.10xgenomics.com/samples/spatial-exp/3.0.0/Visium_HD_Mouse_Embryo/Visium_HD_Mouse_Embryo_feature_slice.h5",
    "https://cf.10xgenomics.com/samples/spatial-exp/3.0.0/Visium_HD_Mouse_Embryo/Visium_HD_Mouse_Embryo_spatial.tar.gz",
    "https://cf.10xgenomics.com/samples/spatial-exp/3.0.0/Visium_HD_Mouse_Embryo/Visium_HD_Mouse_Embryo_binned_outputs.tar.gz",
]

os.makedirs("data", exist_ok=True)

for url in urls:
    print(url)
    name = Path(url).name
    download(url, os.path.join("data", name), name)

files = [
    "Visium_HD_Mouse_Embryo_spatial.tar.gz",
    "Visium_HD_Mouse_Embryo_binned_outputs.tar.gz",
]

for file in files:
    command = f"tar -xzf data/{file} -C data"
    subprocess.run(command, shell=True, check=True)

for dir in list(Path("data/binned_outputs").glob("*")):
    if not (Path("data") / dir.name).exists():
        shutil.move(dir, "data")
subprocess.run("rm -r data/binned_outputs", shell=True, check=True)
