#!/bin/sh
#SBATCH --partition=GPUQ
#SBATCH --account=share-ie-idi
#SBATCH --time=12:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --gres=gpu:V10032:4
#SBATCH --cpus-per-task=32
#SBATCH --mem=64G
#SBATCH --job-name="miniproject"
#SBATCH --output=yolo-mixed.out
#SBATCH --mail-user=jorgbor@ntnu.no


cd ${SLURM_SUBMIT_DIR}/yolov7

module purge
module load Python/3.8.6-GCCcore-10.2.0

pip install -r requirements.txt --user -q
pip install wandb --user -q

wandb login "ef4c5c0b5b612d591e12bfd25fb32fad417d60e5"

python3 -m torch.distributed.launch --nproc_per_node=4 train.py --batch 64 --epochs 300 --data road-data/data.yaml --weights 'yolov7_training.pt' --device 0,1 --workers 24 --image 1280
