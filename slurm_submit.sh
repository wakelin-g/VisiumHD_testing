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
    # -- TODO: this actually won't work... recursively tarballs the expanded
    #          $project var and screws up all downstream path resolving
    tar -cf $project/spatialde2/visiumhd-mouse-embryo-zarr.tar $project/spatialde2/data.zarr
fi

mkdir -p outputs/
tar -xf $project/spatialde2/visiumhd-mouse-embryo-zarr.tar

module purge
module load StdEnv/2023 gcc python/3.12.4 arrow
source $project/spatialde2/tensorflow/bin/activate

python3 run_spatialde2.py

mv outputs/spatialde2_outputs.csv $project/spatialde2/spatialde2_outputs.csv
