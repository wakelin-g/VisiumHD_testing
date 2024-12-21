#!/bin/bash
#SBATCH --mem=125G
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
#SBATCH --time=0-1:00
#SBATCH --gres=gpu:1
#SBATCH --output=%N-%j.out

cd $SLURM_TMPDIR
git clone https://github.com/wakelin-g/VisiumHD_testing.git
cd ./VisiumHD_testing

if [ ! -f $project/spatialde2/visiumhd-mouse-embryo-zarr.tar ]; then
    if [ ! -d $project/spatialde2/data.zarr ]; then
        if [ ! -d $project/spatialde2/data ]; then
            python3 setup_scripts/download_test_data.py
        fi
        python3 setup_scripts/make_zarr.py
    fi
    tar -cf $project/spatialde2/visiumhd-mouse-embryo-zarr.tar $project/spatialde2/data.zarr
fi

mkdir -p data.zarr/
mkdir -p outputs/
tar -xf $project/spatialde2/visiumhd-mouse-embryo-zarr.tar -C data.zarr/

module purge
module load StdEnv/2023 gcc python/3.12.4 arrow
source $project/spatialde2/tensorflow/bin/activate

python3 run_spatialde2.py

tar -cf $project/spatialde2/outputs/results-archive.tar outputs/
