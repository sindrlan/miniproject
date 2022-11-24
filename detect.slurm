#!/bin/sh
#SBATCH --partition=GPUQ
#SBATCH --account=share-ie-idi
#SBATCH --time=24:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --gres=gpu:P100:2
#SBATCH --job-name="miniproject"
#SBATCH --output=detect-yolo_2.out
#SBATCH --mail-user=jorgbor@ntnu.no


cd ${SLURM_SUBMIT_DIR}/yolov7

module purge
module load Python/3.8.6-GCCcore-10.2.0

pip install -r requirements.txt --user -q

#python detect.py --weights runs/train/exp78/weights/best.pt --img-size 2044 --source /cluster/projects/vc/courses/TDT17/2022/open/RDD2022/Norway/test/images

python detect.py --weights runs/train/exp78/weights/best.pt --img-size 1280 --source ../test2