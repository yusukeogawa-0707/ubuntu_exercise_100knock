# シェルスクリプト100本ノック — 実践編

## 位置づけ

ワンライナーから再利用可能な実験手順へ進む。

- 入門編: まず壊さず、意味を確認しながら手を動かす。
- 実践編: 研究実務で使う形に近づける。

## 使い方

1. まず各Knockのコマンドを読む。
2. 練習用ディレクトリで実行する。
3. 解説と確認ポイントを見て、何が起きたか確認する。

注意: `myserver`, `your_username`, `git@example.com:USER/REPO.git` などは仮の名前です。実環境に合わせて置き換えてください。

## Knock 001: 練習ディレクトリを作る

**目的**: 安全な作業場所を作る。

````bash
mkdir -p ~/shell100knock/{scripts,data,logs,tmp} && cd ~/shell100knock
````
**解説**: シェルスクリプトはファイル削除なども扱うため、練習場所を分けます。

**確認ポイント**: `pwd` で確認。


## Knock 002: 最初のスクリプトを作る

**目的**: スクリプトファイルを作る。

````bash
cat > scripts/hello.sh <<EOF
#!/usr/bin/env bash
echo "hello shell"
EOF
````
**解説**: 先頭のshebangでbash実行を指定します。

**確認ポイント**: `cat scripts/hello.sh` で確認。


## Knock 003: 実行権限を付ける

**目的**: スクリプトを直接実行可能にする。

````bash
chmod +x scripts/hello.sh
````
**解説**: Linuxでは実行権限がないと `./script.sh` で動きません。

**確認ポイント**: `ls -l` でxが見える。


## Knock 004: スクリプトを実行する

**目的**: 作ったスクリプトを実行する。

````bash
./scripts/hello.sh
````
**解説**: コマンド列をファイル化すると再利用できます。

**確認ポイント**: hello shellが出る。


## Knock 005: 実験実行スクリプトを作る

**目的**: 実験実行を再利用可能にする。

````bash
cat > scripts/run_exp.sh <<'EOF
#!/usr/bin/env bash
set -euo pipefail
EXP=${1:?Usage: $0 EXP_NAME}
mkdir -p "experiments/$EXP/logs" "experiments/$EXP/outputs"
{ date; hostname; echo "EXP=$EXP"; } | tee "experiments/$EXP/logs/meta.log"
python3 -c "print("dummy training")" 2>&1 | tee "experiments/$EXP/logs/train.log"
EOF
chmod +x scripts/run_exp.sh
````
**解説**: 手順をスクリプト化すると再現性が上がります。

**確認ポイント**: `./scripts/run_exp.sh test001` が動く。


## Knock 006: 実験スクリプトを実行する

**目的**: 実験の一連処理を起動する。

````bash
./scripts/run_exp.sh exp001
````
**解説**: ディレクトリ作成、メタ情報保存、ログ保存をまとめています。

**確認ポイント**: experiments/exp001ができる。


## Knock 007: 複数実験を回す

**目的**: forで複数条件を回す。

````bash
for lr in 0.1 0.01 0.001; do ./scripts/run_exp.sh "lr_${lr}"; done
````
**解説**: 研究実験では条件違いを一括実行する場面が多いです。

**確認ポイント**: lr_*ディレクトリができる。


## Knock 008: 設定CSVを読む

**目的**: 実験条件表を作る。

````bash
cat > data/params.csv <<EOF
name,lr,seed
a,0.1,1
b,0.01,2
c,0.001,3
EOF
````
**解説**: CSVを元に実験を回す準備です。

**確認ポイント**: `column -s, -t data/params.csv` で確認。


## Knock 009: CSVから実験を回す

**目的**: CSVを1行ずつ処理する。

````bash
tail -n +2 data/params.csv | while IFS=, read -r name lr seed; do echo "name=$name lr=$lr seed=$seed"; done
````
**解説**: 実験条件を手で打たずファイル管理できます。

**確認ポイント**: 各条件が表示される。


## Knock 010: dry-runモードを作る

**目的**: 危険操作前に予行演習する。

````bash
cat > scripts/dryrun.sh <<'EOF
#!/usr/bin/env bash
DRY_RUN=${DRY_RUN:-0}
cmd="mkdir -p tmp/dryrun_test"
if [ "$DRY_RUN" = "1" ]; then echo "DRY: $cmd"; else eval "$cmd"; fi
EOF
chmod +x scripts/dryrun.sh && DRY_RUN=1 ./scripts/dryrun.sh
````
**解説**: 削除や転送スクリプトにはdry-runが重要です。

**確認ポイント**: DRY表示が出る。


## Knock 011: 並列実行の基本

**目的**: バックグラウンド並列とwaitを使う。

````bash
for i in 1 2 3; do (sleep 1; echo done_$i) & done; wait
````
**解説**: 軽い処理を並列化できます。GPU実験では乱用注意です。

**確認ポイント**: done_1〜3が出る。


## Knock 012: 失敗を検知する

**目的**: 失敗時処理を書く。

````bash
(false) || echo "command failed"
````
**解説**: `||` は前のコマンドが失敗したら実行です。

**確認ポイント**: command failedが出る。


## Knock 013: ログ関数を共通化する

**目的**: 共通関数ファイルを作る。

````bash
cat > scripts/lib.sh <<'EOF
log(){ echo "[$(date +%F_%T)] $*"; }
EOF
````
**解説**: 複数スクリプトで同じ関数を使えます。

**確認ポイント**: lib.shができる。


## Knock 014: sourceで共通関数を読む

**目的**: 別ファイルの関数を読み込む。

````bash
cat > scripts/use_lib.sh <<'EOF
#!/usr/bin/env bash
set -euo pipefail
source scripts/lib.sh
log "loaded"
EOF
chmod +x scripts/use_lib.sh && ./scripts/use_lib.sh
````
**解説**: スクリプトが大きくなったら分割します。

**確認ポイント**: loadedが出る。


## Knock 015: 一括実験条件 01 を生成する

**目的**: 実験条件を追記生成する。

````bash
printf "exp_%02d,%.4f,%d
" 1 "0.001" 1 >> data/generated_params.csv
````
**解説**: シェルだけでも簡単な条件表を作れます。

**確認ポイント**: `tail data/generated_params.csv` で確認。


## Knock 016: 一括実験条件 02 を生成する

**目的**: 実験条件を追記生成する。

````bash
printf "exp_%02d,%.4f,%d
" 2 "0.002" 2 >> data/generated_params.csv
````
**解説**: シェルだけでも簡単な条件表を作れます。

**確認ポイント**: `tail data/generated_params.csv` で確認。


## Knock 017: 一括実験条件 03 を生成する

**目的**: 実験条件を追記生成する。

````bash
printf "exp_%02d,%.4f,%d
" 3 "0.003" 3 >> data/generated_params.csv
````
**解説**: シェルだけでも簡単な条件表を作れます。

**確認ポイント**: `tail data/generated_params.csv` で確認。


## Knock 018: 一括実験条件 04 を生成する

**目的**: 実験条件を追記生成する。

````bash
printf "exp_%02d,%.4f,%d
" 4 "0.004" 4 >> data/generated_params.csv
````
**解説**: シェルだけでも簡単な条件表を作れます。

**確認ポイント**: `tail data/generated_params.csv` で確認。


## Knock 019: 一括実験条件 05 を生成する

**目的**: 実験条件を追記生成する。

````bash
printf "exp_%02d,%.4f,%d
" 5 "0.005" 5 >> data/generated_params.csv
````
**解説**: シェルだけでも簡単な条件表を作れます。

**確認ポイント**: `tail data/generated_params.csv` で確認。


## Knock 020: 一括実験条件 06 を生成する

**目的**: 実験条件を追記生成する。

````bash
printf "exp_%02d,%.4f,%d
" 6 "0.006" 6 >> data/generated_params.csv
````
**解説**: シェルだけでも簡単な条件表を作れます。

**確認ポイント**: `tail data/generated_params.csv` で確認。


## Knock 021: 一括実験条件 07 を生成する

**目的**: 実験条件を追記生成する。

````bash
printf "exp_%02d,%.4f,%d
" 7 "0.007" 7 >> data/generated_params.csv
````
**解説**: シェルだけでも簡単な条件表を作れます。

**確認ポイント**: `tail data/generated_params.csv` で確認。


## Knock 022: 一括実験条件 08 を生成する

**目的**: 実験条件を追記生成する。

````bash
printf "exp_%02d,%.4f,%d
" 8 "0.008" 8 >> data/generated_params.csv
````
**解説**: シェルだけでも簡単な条件表を作れます。

**確認ポイント**: `tail data/generated_params.csv` で確認。


## Knock 023: 一括実験条件 09 を生成する

**目的**: 実験条件を追記生成する。

````bash
printf "exp_%02d,%.4f,%d
" 9 "0.009" 9 >> data/generated_params.csv
````
**解説**: シェルだけでも簡単な条件表を作れます。

**確認ポイント**: `tail data/generated_params.csv` で確認。


## Knock 024: 一括実験条件 10 を生成する

**目的**: 実験条件を追記生成する。

````bash
printf "exp_%02d,%.4f,%d
" 10 "0.010" 10 >> data/generated_params.csv
````
**解説**: シェルだけでも簡単な条件表を作れます。

**確認ポイント**: `tail data/generated_params.csv` で確認。


## Knock 025: 一括実験条件 11 を生成する

**目的**: 実験条件を追記生成する。

````bash
printf "exp_%02d,%.4f,%d
" 11 "0.011" 11 >> data/generated_params.csv
````
**解説**: シェルだけでも簡単な条件表を作れます。

**確認ポイント**: `tail data/generated_params.csv` で確認。


## Knock 026: 一括実験条件 12 を生成する

**目的**: 実験条件を追記生成する。

````bash
printf "exp_%02d,%.4f,%d
" 12 "0.012" 12 >> data/generated_params.csv
````
**解説**: シェルだけでも簡単な条件表を作れます。

**確認ポイント**: `tail data/generated_params.csv` で確認。


## Knock 027: 一括実験条件 13 を生成する

**目的**: 実験条件を追記生成する。

````bash
printf "exp_%02d,%.4f,%d
" 13 "0.013" 13 >> data/generated_params.csv
````
**解説**: シェルだけでも簡単な条件表を作れます。

**確認ポイント**: `tail data/generated_params.csv` で確認。


## Knock 028: 一括実験条件 14 を生成する

**目的**: 実験条件を追記生成する。

````bash
printf "exp_%02d,%.4f,%d
" 14 "0.014" 14 >> data/generated_params.csv
````
**解説**: シェルだけでも簡単な条件表を作れます。

**確認ポイント**: `tail data/generated_params.csv` で確認。


## Knock 029: 一括実験条件 15 を生成する

**目的**: 実験条件を追記生成する。

````bash
printf "exp_%02d,%.4f,%d
" 15 "0.015" 15 >> data/generated_params.csv
````
**解説**: シェルだけでも簡単な条件表を作れます。

**確認ポイント**: `tail data/generated_params.csv` で確認。


## Knock 030: 一括実験条件 16 を生成する

**目的**: 実験条件を追記生成する。

````bash
printf "exp_%02d,%.4f,%d
" 16 "0.016" 16 >> data/generated_params.csv
````
**解説**: シェルだけでも簡単な条件表を作れます。

**確認ポイント**: `tail data/generated_params.csv` で確認。


## Knock 031: 一括実験条件 17 を生成する

**目的**: 実験条件を追記生成する。

````bash
printf "exp_%02d,%.4f,%d
" 17 "0.017" 17 >> data/generated_params.csv
````
**解説**: シェルだけでも簡単な条件表を作れます。

**確認ポイント**: `tail data/generated_params.csv` で確認。


## Knock 032: 一括実験条件 18 を生成する

**目的**: 実験条件を追記生成する。

````bash
printf "exp_%02d,%.4f,%d
" 18 "0.018" 18 >> data/generated_params.csv
````
**解説**: シェルだけでも簡単な条件表を作れます。

**確認ポイント**: `tail data/generated_params.csv` で確認。


## Knock 033: 一括実験条件 19 を生成する

**目的**: 実験条件を追記生成する。

````bash
printf "exp_%02d,%.4f,%d
" 19 "0.019" 19 >> data/generated_params.csv
````
**解説**: シェルだけでも簡単な条件表を作れます。

**確認ポイント**: `tail data/generated_params.csv` で確認。


## Knock 034: 一括実験条件 20 を生成する

**目的**: 実験条件を追記生成する。

````bash
printf "exp_%02d,%.4f,%d
" 20 "0.020" 20 >> data/generated_params.csv
````
**解説**: シェルだけでも簡単な条件表を作れます。

**確認ポイント**: `tail data/generated_params.csv` で確認。


## Knock 035: 一括実験条件 21 を生成する

**目的**: 実験条件を追記生成する。

````bash
printf "exp_%02d,%.4f,%d
" 21 "0.021" 21 >> data/generated_params.csv
````
**解説**: シェルだけでも簡単な条件表を作れます。

**確認ポイント**: `tail data/generated_params.csv` で確認。


## Knock 036: 一括実験条件 22 を生成する

**目的**: 実験条件を追記生成する。

````bash
printf "exp_%02d,%.4f,%d
" 22 "0.022" 22 >> data/generated_params.csv
````
**解説**: シェルだけでも簡単な条件表を作れます。

**確認ポイント**: `tail data/generated_params.csv` で確認。


## Knock 037: 一括実験条件 23 を生成する

**目的**: 実験条件を追記生成する。

````bash
printf "exp_%02d,%.4f,%d
" 23 "0.023" 23 >> data/generated_params.csv
````
**解説**: シェルだけでも簡単な条件表を作れます。

**確認ポイント**: `tail data/generated_params.csv` で確認。


## Knock 038: 一括実験条件 24 を生成する

**目的**: 実験条件を追記生成する。

````bash
printf "exp_%02d,%.4f,%d
" 24 "0.024" 24 >> data/generated_params.csv
````
**解説**: シェルだけでも簡単な条件表を作れます。

**確認ポイント**: `tail data/generated_params.csv` で確認。


## Knock 039: 一括実験条件 25 を生成する

**目的**: 実験条件を追記生成する。

````bash
printf "exp_%02d,%.4f,%d
" 25 "0.025" 25 >> data/generated_params.csv
````
**解説**: シェルだけでも簡単な条件表を作れます。

**確認ポイント**: `tail data/generated_params.csv` で確認。


## Knock 040: 一括実験条件 26 を生成する

**目的**: 実験条件を追記生成する。

````bash
printf "exp_%02d,%.4f,%d
" 26 "0.026" 26 >> data/generated_params.csv
````
**解説**: シェルだけでも簡単な条件表を作れます。

**確認ポイント**: `tail data/generated_params.csv` で確認。


## Knock 041: 一括実験条件 27 を生成する

**目的**: 実験条件を追記生成する。

````bash
printf "exp_%02d,%.4f,%d
" 27 "0.027" 27 >> data/generated_params.csv
````
**解説**: シェルだけでも簡単な条件表を作れます。

**確認ポイント**: `tail data/generated_params.csv` で確認。


## Knock 042: 一括実験条件 28 を生成する

**目的**: 実験条件を追記生成する。

````bash
printf "exp_%02d,%.4f,%d
" 28 "0.028" 28 >> data/generated_params.csv
````
**解説**: シェルだけでも簡単な条件表を作れます。

**確認ポイント**: `tail data/generated_params.csv` で確認。


## Knock 043: 一括実験条件 29 を生成する

**目的**: 実験条件を追記生成する。

````bash
printf "exp_%02d,%.4f,%d
" 29 "0.029" 29 >> data/generated_params.csv
````
**解説**: シェルだけでも簡単な条件表を作れます。

**確認ポイント**: `tail data/generated_params.csv` で確認。


## Knock 044: 一括実験条件 30 を生成する

**目的**: 実験条件を追記生成する。

````bash
printf "exp_%02d,%.4f,%d
" 30 "0.030" 30 >> data/generated_params.csv
````
**解説**: シェルだけでも簡単な条件表を作れます。

**確認ポイント**: `tail data/generated_params.csv` で確認。


## Knock 045: 一括実験条件 31 を生成する

**目的**: 実験条件を追記生成する。

````bash
printf "exp_%02d,%.4f,%d
" 31 "0.031" 31 >> data/generated_params.csv
````
**解説**: シェルだけでも簡単な条件表を作れます。

**確認ポイント**: `tail data/generated_params.csv` で確認。


## Knock 046: 一括実験条件 32 を生成する

**目的**: 実験条件を追記生成する。

````bash
printf "exp_%02d,%.4f,%d
" 32 "0.032" 32 >> data/generated_params.csv
````
**解説**: シェルだけでも簡単な条件表を作れます。

**確認ポイント**: `tail data/generated_params.csv` で確認。


## Knock 047: 一括実験条件 33 を生成する

**目的**: 実験条件を追記生成する。

````bash
printf "exp_%02d,%.4f,%d
" 33 "0.033" 33 >> data/generated_params.csv
````
**解説**: シェルだけでも簡単な条件表を作れます。

**確認ポイント**: `tail data/generated_params.csv` で確認。


## Knock 048: 一括実験条件 34 を生成する

**目的**: 実験条件を追記生成する。

````bash
printf "exp_%02d,%.4f,%d
" 34 "0.034" 34 >> data/generated_params.csv
````
**解説**: シェルだけでも簡単な条件表を作れます。

**確認ポイント**: `tail data/generated_params.csv` で確認。


## Knock 049: 一括実験条件 35 を生成する

**目的**: 実験条件を追記生成する。

````bash
printf "exp_%02d,%.4f,%d
" 35 "0.035" 35 >> data/generated_params.csv
````
**解説**: シェルだけでも簡単な条件表を作れます。

**確認ポイント**: `tail data/generated_params.csv` で確認。


## Knock 050: 一括実験条件 36 を生成する

**目的**: 実験条件を追記生成する。

````bash
printf "exp_%02d,%.4f,%d
" 36 "0.036" 36 >> data/generated_params.csv
````
**解説**: シェルだけでも簡単な条件表を作れます。

**確認ポイント**: `tail data/generated_params.csv` で確認。


## Knock 051: 一括実験条件 37 を生成する

**目的**: 実験条件を追記生成する。

````bash
printf "exp_%02d,%.4f,%d
" 37 "0.037" 37 >> data/generated_params.csv
````
**解説**: シェルだけでも簡単な条件表を作れます。

**確認ポイント**: `tail data/generated_params.csv` で確認。


## Knock 052: 一括実験条件 38 を生成する

**目的**: 実験条件を追記生成する。

````bash
printf "exp_%02d,%.4f,%d
" 38 "0.038" 38 >> data/generated_params.csv
````
**解説**: シェルだけでも簡単な条件表を作れます。

**確認ポイント**: `tail data/generated_params.csv` で確認。


## Knock 053: 一括実験条件 39 を生成する

**目的**: 実験条件を追記生成する。

````bash
printf "exp_%02d,%.4f,%d
" 39 "0.039" 39 >> data/generated_params.csv
````
**解説**: シェルだけでも簡単な条件表を作れます。

**確認ポイント**: `tail data/generated_params.csv` で確認。


## Knock 054: 一括実験条件 40 を生成する

**目的**: 実験条件を追記生成する。

````bash
printf "exp_%02d,%.4f,%d
" 40 "0.040" 40 >> data/generated_params.csv
````
**解説**: シェルだけでも簡単な条件表を作れます。

**確認ポイント**: `tail data/generated_params.csv` で確認。


## Knock 055: 一括実験条件 41 を生成する

**目的**: 実験条件を追記生成する。

````bash
printf "exp_%02d,%.4f,%d
" 41 "0.041" 41 >> data/generated_params.csv
````
**解説**: シェルだけでも簡単な条件表を作れます。

**確認ポイント**: `tail data/generated_params.csv` で確認。


## Knock 056: 一括実験条件 42 を生成する

**目的**: 実験条件を追記生成する。

````bash
printf "exp_%02d,%.4f,%d
" 42 "0.042" 42 >> data/generated_params.csv
````
**解説**: シェルだけでも簡単な条件表を作れます。

**確認ポイント**: `tail data/generated_params.csv` で確認。


## Knock 057: 一括実験条件 43 を生成する

**目的**: 実験条件を追記生成する。

````bash
printf "exp_%02d,%.4f,%d
" 43 "0.043" 43 >> data/generated_params.csv
````
**解説**: シェルだけでも簡単な条件表を作れます。

**確認ポイント**: `tail data/generated_params.csv` で確認。


## Knock 058: 一括実験条件 44 を生成する

**目的**: 実験条件を追記生成する。

````bash
printf "exp_%02d,%.4f,%d
" 44 "0.044" 44 >> data/generated_params.csv
````
**解説**: シェルだけでも簡単な条件表を作れます。

**確認ポイント**: `tail data/generated_params.csv` で確認。


## Knock 059: 一括実験条件 45 を生成する

**目的**: 実験条件を追記生成する。

````bash
printf "exp_%02d,%.4f,%d
" 45 "0.045" 45 >> data/generated_params.csv
````
**解説**: シェルだけでも簡単な条件表を作れます。

**確認ポイント**: `tail data/generated_params.csv` で確認。


## Knock 060: 条件 01 を安全に実行表示する

**目的**: 実行コマンドを組み立てる。

````bash
awk -F, "NR==1{print \$0}" data/generated_params.csv | while IFS=, read -r exp lr seed; do echo "python train.py --exp $exp --lr $lr --seed $seed"; done
````
**解説**: いきなり実行せず、まずechoで確認するのが安全です。

**確認ポイント**: コマンド文字列が表示される。


## Knock 061: 条件 02 を安全に実行表示する

**目的**: 実行コマンドを組み立てる。

````bash
awk -F, "NR==2{print \$0}" data/generated_params.csv | while IFS=, read -r exp lr seed; do echo "python train.py --exp $exp --lr $lr --seed $seed"; done
````
**解説**: いきなり実行せず、まずechoで確認するのが安全です。

**確認ポイント**: コマンド文字列が表示される。


## Knock 062: 条件 03 を安全に実行表示する

**目的**: 実行コマンドを組み立てる。

````bash
awk -F, "NR==3{print \$0}" data/generated_params.csv | while IFS=, read -r exp lr seed; do echo "python train.py --exp $exp --lr $lr --seed $seed"; done
````
**解説**: いきなり実行せず、まずechoで確認するのが安全です。

**確認ポイント**: コマンド文字列が表示される。


## Knock 063: 条件 04 を安全に実行表示する

**目的**: 実行コマンドを組み立てる。

````bash
awk -F, "NR==4{print \$0}" data/generated_params.csv | while IFS=, read -r exp lr seed; do echo "python train.py --exp $exp --lr $lr --seed $seed"; done
````
**解説**: いきなり実行せず、まずechoで確認するのが安全です。

**確認ポイント**: コマンド文字列が表示される。


## Knock 064: 条件 05 を安全に実行表示する

**目的**: 実行コマンドを組み立てる。

````bash
awk -F, "NR==5{print \$0}" data/generated_params.csv | while IFS=, read -r exp lr seed; do echo "python train.py --exp $exp --lr $lr --seed $seed"; done
````
**解説**: いきなり実行せず、まずechoで確認するのが安全です。

**確認ポイント**: コマンド文字列が表示される。


## Knock 065: 条件 06 を安全に実行表示する

**目的**: 実行コマンドを組み立てる。

````bash
awk -F, "NR==6{print \$0}" data/generated_params.csv | while IFS=, read -r exp lr seed; do echo "python train.py --exp $exp --lr $lr --seed $seed"; done
````
**解説**: いきなり実行せず、まずechoで確認するのが安全です。

**確認ポイント**: コマンド文字列が表示される。


## Knock 066: 条件 07 を安全に実行表示する

**目的**: 実行コマンドを組み立てる。

````bash
awk -F, "NR==7{print \$0}" data/generated_params.csv | while IFS=, read -r exp lr seed; do echo "python train.py --exp $exp --lr $lr --seed $seed"; done
````
**解説**: いきなり実行せず、まずechoで確認するのが安全です。

**確認ポイント**: コマンド文字列が表示される。


## Knock 067: 条件 08 を安全に実行表示する

**目的**: 実行コマンドを組み立てる。

````bash
awk -F, "NR==8{print \$0}" data/generated_params.csv | while IFS=, read -r exp lr seed; do echo "python train.py --exp $exp --lr $lr --seed $seed"; done
````
**解説**: いきなり実行せず、まずechoで確認するのが安全です。

**確認ポイント**: コマンド文字列が表示される。


## Knock 068: 条件 09 を安全に実行表示する

**目的**: 実行コマンドを組み立てる。

````bash
awk -F, "NR==9{print \$0}" data/generated_params.csv | while IFS=, read -r exp lr seed; do echo "python train.py --exp $exp --lr $lr --seed $seed"; done
````
**解説**: いきなり実行せず、まずechoで確認するのが安全です。

**確認ポイント**: コマンド文字列が表示される。


## Knock 069: 条件 10 を安全に実行表示する

**目的**: 実行コマンドを組み立てる。

````bash
awk -F, "NR==10{print \$0}" data/generated_params.csv | while IFS=, read -r exp lr seed; do echo "python train.py --exp $exp --lr $lr --seed $seed"; done
````
**解説**: いきなり実行せず、まずechoで確認するのが安全です。

**確認ポイント**: コマンド文字列が表示される。


## Knock 070: 条件 11 を安全に実行表示する

**目的**: 実行コマンドを組み立てる。

````bash
awk -F, "NR==11{print \$0}" data/generated_params.csv | while IFS=, read -r exp lr seed; do echo "python train.py --exp $exp --lr $lr --seed $seed"; done
````
**解説**: いきなり実行せず、まずechoで確認するのが安全です。

**確認ポイント**: コマンド文字列が表示される。


## Knock 071: 条件 12 を安全に実行表示する

**目的**: 実行コマンドを組み立てる。

````bash
awk -F, "NR==12{print \$0}" data/generated_params.csv | while IFS=, read -r exp lr seed; do echo "python train.py --exp $exp --lr $lr --seed $seed"; done
````
**解説**: いきなり実行せず、まずechoで確認するのが安全です。

**確認ポイント**: コマンド文字列が表示される。


## Knock 072: 条件 13 を安全に実行表示する

**目的**: 実行コマンドを組み立てる。

````bash
awk -F, "NR==13{print \$0}" data/generated_params.csv | while IFS=, read -r exp lr seed; do echo "python train.py --exp $exp --lr $lr --seed $seed"; done
````
**解説**: いきなり実行せず、まずechoで確認するのが安全です。

**確認ポイント**: コマンド文字列が表示される。


## Knock 073: 条件 14 を安全に実行表示する

**目的**: 実行コマンドを組み立てる。

````bash
awk -F, "NR==14{print \$0}" data/generated_params.csv | while IFS=, read -r exp lr seed; do echo "python train.py --exp $exp --lr $lr --seed $seed"; done
````
**解説**: いきなり実行せず、まずechoで確認するのが安全です。

**確認ポイント**: コマンド文字列が表示される。


## Knock 074: 条件 15 を安全に実行表示する

**目的**: 実行コマンドを組み立てる。

````bash
awk -F, "NR==15{print \$0}" data/generated_params.csv | while IFS=, read -r exp lr seed; do echo "python train.py --exp $exp --lr $lr --seed $seed"; done
````
**解説**: いきなり実行せず、まずechoで確認するのが安全です。

**確認ポイント**: コマンド文字列が表示される。


## Knock 075: 条件 16 を安全に実行表示する

**目的**: 実行コマンドを組み立てる。

````bash
awk -F, "NR==16{print \$0}" data/generated_params.csv | while IFS=, read -r exp lr seed; do echo "python train.py --exp $exp --lr $lr --seed $seed"; done
````
**解説**: いきなり実行せず、まずechoで確認するのが安全です。

**確認ポイント**: コマンド文字列が表示される。


## Knock 076: 条件 17 を安全に実行表示する

**目的**: 実行コマンドを組み立てる。

````bash
awk -F, "NR==17{print \$0}" data/generated_params.csv | while IFS=, read -r exp lr seed; do echo "python train.py --exp $exp --lr $lr --seed $seed"; done
````
**解説**: いきなり実行せず、まずechoで確認するのが安全です。

**確認ポイント**: コマンド文字列が表示される。


## Knock 077: 条件 18 を安全に実行表示する

**目的**: 実行コマンドを組み立てる。

````bash
awk -F, "NR==18{print \$0}" data/generated_params.csv | while IFS=, read -r exp lr seed; do echo "python train.py --exp $exp --lr $lr --seed $seed"; done
````
**解説**: いきなり実行せず、まずechoで確認するのが安全です。

**確認ポイント**: コマンド文字列が表示される。


## Knock 078: 条件 19 を安全に実行表示する

**目的**: 実行コマンドを組み立てる。

````bash
awk -F, "NR==19{print \$0}" data/generated_params.csv | while IFS=, read -r exp lr seed; do echo "python train.py --exp $exp --lr $lr --seed $seed"; done
````
**解説**: いきなり実行せず、まずechoで確認するのが安全です。

**確認ポイント**: コマンド文字列が表示される。


## Knock 079: 条件 20 を安全に実行表示する

**目的**: 実行コマンドを組み立てる。

````bash
awk -F, "NR==20{print \$0}" data/generated_params.csv | while IFS=, read -r exp lr seed; do echo "python train.py --exp $exp --lr $lr --seed $seed"; done
````
**解説**: いきなり実行せず、まずechoで確認するのが安全です。

**確認ポイント**: コマンド文字列が表示される。


## Knock 080: 条件 21 を安全に実行表示する

**目的**: 実行コマンドを組み立てる。

````bash
awk -F, "NR==21{print \$0}" data/generated_params.csv | while IFS=, read -r exp lr seed; do echo "python train.py --exp $exp --lr $lr --seed $seed"; done
````
**解説**: いきなり実行せず、まずechoで確認するのが安全です。

**確認ポイント**: コマンド文字列が表示される。


## Knock 081: 条件 22 を安全に実行表示する

**目的**: 実行コマンドを組み立てる。

````bash
awk -F, "NR==22{print \$0}" data/generated_params.csv | while IFS=, read -r exp lr seed; do echo "python train.py --exp $exp --lr $lr --seed $seed"; done
````
**解説**: いきなり実行せず、まずechoで確認するのが安全です。

**確認ポイント**: コマンド文字列が表示される。


## Knock 082: 条件 23 を安全に実行表示する

**目的**: 実行コマンドを組み立てる。

````bash
awk -F, "NR==23{print \$0}" data/generated_params.csv | while IFS=, read -r exp lr seed; do echo "python train.py --exp $exp --lr $lr --seed $seed"; done
````
**解説**: いきなり実行せず、まずechoで確認するのが安全です。

**確認ポイント**: コマンド文字列が表示される。


## Knock 083: 条件 24 を安全に実行表示する

**目的**: 実行コマンドを組み立てる。

````bash
awk -F, "NR==24{print \$0}" data/generated_params.csv | while IFS=, read -r exp lr seed; do echo "python train.py --exp $exp --lr $lr --seed $seed"; done
````
**解説**: いきなり実行せず、まずechoで確認するのが安全です。

**確認ポイント**: コマンド文字列が表示される。


## Knock 084: 条件 25 を安全に実行表示する

**目的**: 実行コマンドを組み立てる。

````bash
awk -F, "NR==25{print \$0}" data/generated_params.csv | while IFS=, read -r exp lr seed; do echo "python train.py --exp $exp --lr $lr --seed $seed"; done
````
**解説**: いきなり実行せず、まずechoで確認するのが安全です。

**確認ポイント**: コマンド文字列が表示される。


## Knock 085: 実行ログをまとめる

**目的**: 複数実験ログを横断検索する。

````bash
find experiments -name train.log -print0 | xargs -0 grep -H "dummy" || true
````
**解説**: 実験が増えるほどfind+xargsが効きます。

**確認ポイント**: 該当ログが表示される。


## Knock 086: 失敗ログだけ集める

**目的**: 失敗情報をサマリ保存する。

````bash
find experiments -name "*.log" -print0 | xargs -0 grep -H "ERROR" > tmp/error_summary.txt || true
````
**解説**: ログ監視の自動化に近い処理です。

**確認ポイント**: summaryファイルができる。


## Knock 087: 総復習チェック 087

**目的**: その領域の練習前後で現在地・時刻・ファイル状態を確認する。

````bash
pwd && date && ls -lah | head
````
**解説**: 初心者ほど、現在地と対象ファイルを確認する癖が重要です。迷ったらまずこの確認セットに戻ります。

**確認ポイント**: 現在地、日時、ファイル一覧の先頭が表示される。


## Knock 088: 総復習チェック 088

**目的**: その領域の練習前後で現在地・時刻・ファイル状態を確認する。

````bash
pwd && date && ls -lah | head
````
**解説**: 初心者ほど、現在地と対象ファイルを確認する癖が重要です。迷ったらまずこの確認セットに戻ります。

**確認ポイント**: 現在地、日時、ファイル一覧の先頭が表示される。


## Knock 089: 総復習チェック 089

**目的**: その領域の練習前後で現在地・時刻・ファイル状態を確認する。

````bash
pwd && date && ls -lah | head
````
**解説**: 初心者ほど、現在地と対象ファイルを確認する癖が重要です。迷ったらまずこの確認セットに戻ります。

**確認ポイント**: 現在地、日時、ファイル一覧の先頭が表示される。


## Knock 090: 総復習チェック 090

**目的**: その領域の練習前後で現在地・時刻・ファイル状態を確認する。

````bash
pwd && date && ls -lah | head
````
**解説**: 初心者ほど、現在地と対象ファイルを確認する癖が重要です。迷ったらまずこの確認セットに戻ります。

**確認ポイント**: 現在地、日時、ファイル一覧の先頭が表示される。


## Knock 091: 総復習チェック 091

**目的**: その領域の練習前後で現在地・時刻・ファイル状態を確認する。

````bash
pwd && date && ls -lah | head
````
**解説**: 初心者ほど、現在地と対象ファイルを確認する癖が重要です。迷ったらまずこの確認セットに戻ります。

**確認ポイント**: 現在地、日時、ファイル一覧の先頭が表示される。


## Knock 092: 総復習チェック 092

**目的**: その領域の練習前後で現在地・時刻・ファイル状態を確認する。

````bash
pwd && date && ls -lah | head
````
**解説**: 初心者ほど、現在地と対象ファイルを確認する癖が重要です。迷ったらまずこの確認セットに戻ります。

**確認ポイント**: 現在地、日時、ファイル一覧の先頭が表示される。


## Knock 093: 総復習チェック 093

**目的**: その領域の練習前後で現在地・時刻・ファイル状態を確認する。

````bash
pwd && date && ls -lah | head
````
**解説**: 初心者ほど、現在地と対象ファイルを確認する癖が重要です。迷ったらまずこの確認セットに戻ります。

**確認ポイント**: 現在地、日時、ファイル一覧の先頭が表示される。


## Knock 094: 総復習チェック 094

**目的**: その領域の練習前後で現在地・時刻・ファイル状態を確認する。

````bash
pwd && date && ls -lah | head
````
**解説**: 初心者ほど、現在地と対象ファイルを確認する癖が重要です。迷ったらまずこの確認セットに戻ります。

**確認ポイント**: 現在地、日時、ファイル一覧の先頭が表示される。


## Knock 095: 総復習チェック 095

**目的**: その領域の練習前後で現在地・時刻・ファイル状態を確認する。

````bash
pwd && date && ls -lah | head
````
**解説**: 初心者ほど、現在地と対象ファイルを確認する癖が重要です。迷ったらまずこの確認セットに戻ります。

**確認ポイント**: 現在地、日時、ファイル一覧の先頭が表示される。


## Knock 096: 総復習チェック 096

**目的**: その領域の練習前後で現在地・時刻・ファイル状態を確認する。

````bash
pwd && date && ls -lah | head
````
**解説**: 初心者ほど、現在地と対象ファイルを確認する癖が重要です。迷ったらまずこの確認セットに戻ります。

**確認ポイント**: 現在地、日時、ファイル一覧の先頭が表示される。


## Knock 097: 総復習チェック 097

**目的**: その領域の練習前後で現在地・時刻・ファイル状態を確認する。

````bash
pwd && date && ls -lah | head
````
**解説**: 初心者ほど、現在地と対象ファイルを確認する癖が重要です。迷ったらまずこの確認セットに戻ります。

**確認ポイント**: 現在地、日時、ファイル一覧の先頭が表示される。


## Knock 098: 総復習チェック 098

**目的**: その領域の練習前後で現在地・時刻・ファイル状態を確認する。

````bash
pwd && date && ls -lah | head
````
**解説**: 初心者ほど、現在地と対象ファイルを確認する癖が重要です。迷ったらまずこの確認セットに戻ります。

**確認ポイント**: 現在地、日時、ファイル一覧の先頭が表示される。


## Knock 099: 総復習チェック 099

**目的**: その領域の練習前後で現在地・時刻・ファイル状態を確認する。

````bash
pwd && date && ls -lah | head
````
**解説**: 初心者ほど、現在地と対象ファイルを確認する癖が重要です。迷ったらまずこの確認セットに戻ります。

**確認ポイント**: 現在地、日時、ファイル一覧の先頭が表示される。


## Knock 100: 総復習チェック 100

**目的**: その領域の練習前後で現在地・時刻・ファイル状態を確認する。

````bash
pwd && date && ls -lah | head
````
**解説**: 初心者ほど、現在地と対象ファイルを確認する癖が重要です。迷ったらまずこの確認セットに戻ります。

**確認ポイント**: 現在地、日時、ファイル一覧の先頭が表示される。

