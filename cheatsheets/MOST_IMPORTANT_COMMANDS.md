# 最重要チートシート

## Python環境
```bash
which python
python --version
python -m pip list
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
CUDA_VISIBLE_DEVICES=0 python train.py 2>&1 | tee train.log
```

## Git
```bash
git status -sb
git diff
git add FILE
git commit -m "message"
git log --oneline --graph --all -n 20
git switch -c feature/name
```

## Shell
```bash
#!/usr/bin/env bash
set -euo pipefail
EXP=${1:?Usage: $0 EXP}
mkdir -p experiments/$EXP/logs
python train.py 2>&1 | tee experiments/$EXP/logs/train.log
```

## Server / Jobs
```bash
ssh myserver "hostname && df -h && free -h"
tmux new -s exp001
nohup python train.py > train.log 2>&1 &
tail -f train.log
watch -n 2 nvidia-smi
rsync -avP myserver:~/project/outputs/ ./outputs/
```

## Trouble shooting
```bash
pwd
whoami
groups
ls -lah
ls -ld .
stat FILE
namei -l FILE
df -h .
du -h --max-depth=1 . | sort -hr
pgrep -af python
```

## Docker safety
```bash
docker ps
docker ps -a
docker images
docker system df
docker run --rm hello-world
docker run --rm -v "$PWD:/work" ubuntu:22.04 ls /work
```
