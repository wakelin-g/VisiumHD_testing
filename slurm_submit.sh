#!/bin/bash
#SBATCH --mem=125G
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
#SBATCH --time=0-1:00
#SBATCH --gres=gpu:1
#SBATCH --output=%N-%j.out

set -e
set -o pipefail

log() {
    echo "$(date +"%Y-%m-%d %H:%M:%S") - $1"
}

cd $SLURM_TMPDIR
log "Cloning repository..."
git clone https://github.com/wakelin-g/VisiumHD_testing.git
cd ./VisiumHD_testing

if [ ! -f $project/spatialde2/visiumhd-mouse-embryo-zarr.tar ]; then
    if [ ! -d $project/spatialde2/data.zarr ]; then
        if [ ! -d $project/spatialde2/data ]; then
            log "Downloading test data..."
            python3 setup_scripts/download_test_data.py
        fi
        log "Converting test data to Zarr format..."
        python3 setup_scripts/make_zarr.py
    fi
    log "Creating tarball of Zarr data..."
    cd $project/spatialde2
    tar -cf visiumhd-mouse-embryo-zarr.tar data.zarr
    cd $SLURM_TMPDIR/VisiumHD_testing
fi

log "Extracting tarball..."
tar -xf $project/spatialde2/visiumhd-mouse-embryo-zarr.tar

log "Creating outputs directory..."
mkdir -p outputs/

log "Loading modules..."
module purge
module load StdEnv/2023 gcc python/3.12.4 arrow
source $project/spatialde2/tensorflow/bin/activate

python3 run_spatialde2.py

log "Moving output file to project directory..."
mv outputs/svg_full.pkl $project/spatialde2/svg_full.pkl

log "Job completed successfully."
