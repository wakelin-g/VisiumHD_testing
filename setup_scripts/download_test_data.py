import os
import shutil
import subprocess
from pathlib import Path

from utils import download

project_path = os.environ["project"]
data_dir = os.path.join(project_path, "data")

# Visium_HD_Mouse_Embryo
urls = [
    "https://cf.10xgenomics.com/samples/spatial-exp/3.0.0/Visium_HD_Mouse_Embryo/Visium_HD_Mouse_Embryo_tissue_image.btf",
    "https://cf.10xgenomics.com/samples/spatial-exp/3.0.0/Visium_HD_Mouse_Embryo/Visium_HD_Mouse_Embryo_cloupe_008um.cloupe",
    "https://cf.10xgenomics.com/samples/spatial-exp/3.0.0/Visium_HD_Mouse_Embryo/Visium_HD_Mouse_Embryo_feature_slice.h5",
    "https://cf.10xgenomics.com/samples/spatial-exp/3.0.0/Visium_HD_Mouse_Embryo/Visium_HD_Mouse_Embryo_spatial.tar.gz",
    "https://cf.10xgenomics.com/samples/spatial-exp/3.0.0/Visium_HD_Mouse_Embryo/Visium_HD_Mouse_Embryo_binned_outputs.tar.gz",
]

os.makedirs(data_dir, exist_ok=True)

for url in urls:
    print(url)
    name = Path(url).name
    download(url, os.path.join(data_dir, name), name)

files = [
    "Visium_HD_Mouse_Embryo_spatial.tar.gz",
    "Visium_HD_Mouse_Embryo_binned_outputs.tar.gz",
]

for file in files:
    command = f"tar -xzf {data_dir}/{file} -C {data_dir}"
    subprocess.run(command, shell=True, check=True)

for dir in list(Path(f"{data_dir}/binned_outputs").glob("*")):
    if not (Path(data_dir) / dir.name).exists():
        shutil.move(dir, data_dir)
subprocess.run(f"rm -r {data_dir}/binned_outputs", shell=True, check=True)
