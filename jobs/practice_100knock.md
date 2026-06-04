# ジョブ管理・長時間実験100本ノック — 実践編

## 位置づけ

tmux/nohup/watch/Slurm雛形でサーバ実験を運用する。

- 入門編: まず壊さず、意味を確認しながら手を動かす。
- 実践編: 研究実務で使う形に近づける。

## 使い方

1. まず各Knockのコマンドを読む。
2. 練習用ディレクトリで実行する。
3. 解説と確認ポイントを見て、何が起きたか確認する。

注意: `myserver`, `your_username`, `git@example.com:USER/REPO.git` などは仮の名前です。実環境に合わせて置き換えてください。

## Knock 001: tmuxがあるか確認する

**目的**: 長時間作業ツールの有無を確認する。

````bash
command -v tmux || echo "tmux not installed"
````
**解説**: SSHが切れても作業を残すにはtmuxが便利です。

**確認ポイント**: パスまたは未導入表示。


## Knock 002: nvidia-smi確認

**目的**: GPU状況を確認する。

````bash
command -v nvidia-smi && nvidia-smi || echo "no nvidia-smi"
````
**解説**: GPUサーバかどうかも分かります。

**確認ポイント**: GPU表または未導入表示。


## Knock 003: Pythonプロセス確認

**目的**: 実験プロセスを探す。

````bash
pgrep -af python || true
````
**解説**: サーバで実験が動いているか確認します。

**確認ポイント**: 該当があれば表示。


## Knock 004: CPU/メモリ確認

**目的**: メモリとCPU数を見る。

````bash
free -h && nproc
````
**解説**: ジョブの重さを考える基本情報です。

**確認ポイント**: メモリとコア数が出る。


## Knock 005: ディスク確認

**目的**: 出力先の空き容量を見る。

````bash
df -h .
````
**解説**: 実験前に容量を確認します。

**確認ポイント**: 空き容量が出る。


## Knock 006: 実験監視スクリプトを作る

**目的**: ログ監視をスクリプト化する。

````bash
cat > monitor_job.sh <<'EOF
#!/usr/bin/env bash
set -euo pipefail
LOG=${1:?Usage: $0 LOG}
tail -n 20 "$LOG"
grep -E "ERROR|WARN|loss|acc" "$LOG" || true
EOF
chmod +x monitor_job.sh
````
**解説**: 毎回grep/tailを打たずに済みます。

**確認ポイント**: `./monitor_job.sh logfile` で使う。


## Knock 007: ジョブ一覧サマリを作る

**目的**: Pythonジョブ一覧を保存する。

````bash
pgrep -af python > python_jobs.txt || true
````
**解説**: あとで誰が何を動かしていたか確認できます。

**確認ポイント**: python_jobs.txtができる。


## Knock 008: メタ情報保存スクリプト

**目的**: ジョブ開始時の環境情報を保存する。

````bash
cat > save_meta.sh <<'EOF
#!/usr/bin/env bash
set -euo pipefail
OUT=${1:-meta.txt}
{ date; hostname; whoami; pwd; free -h; df -h .; command -v nvidia-smi && nvidia-smi || true; } > "$OUT"
EOF
chmod +x save_meta.sh
````
**解説**: 再現性とトラブル調査に効きます。

**確認ポイント**: `./save_meta.sh meta.txt` で確認。


## Knock 009: GPU空き確認ワンライナー

**目的**: GPU状況をCSV風に見る。

````bash
nvidia-smi --query-gpu=index,name,memory.used,memory.total,utilization.gpu --format=csv 2>/dev/null || nvidia-smi
````
**解説**: 表の必要列だけ見ると判断が速くなります。

**確認ポイント**: GPU情報が表示される。


## Knock 010: 自分のGPUプロセス候補

**目的**: 自分の実験プロセスを探す。

````bash
ps -u $(whoami) -o pid,ppid,stat,etime,cmd | grep -E "python|train" || true
````
**解説**: 共有サーバで他人と混同しないためです。

**確認ポイント**: 該当行が出る。


## Knock 011: 優先度を下げて実行する型

**目的**: CPU優先度を下げる。

````bash
nice -n 10 python3 -c "print("low priority job")"
````
**解説**: 共有サーバで軽い補助処理を回す時に使うことがあります。

**確認ポイント**: 出力が出る。


## Knock 012: ioniceでI/O優先度を下げる型

**目的**: I/O負荷に配慮する。

````bash
ionice -c2 -n7 bash -lc "echo io friendly" 2>/dev/null || echo "ionice unavailable"
````
**解説**: 大きなコピーや圧縮で使うことがあります。

**確認ポイント**: 出力を見る。


## Knock 013: timeoutを使う

**目的**: 長引く処理を制限する。

````bash
timeout 5s bash -lc "sleep 10" || echo "timed out"
````
**解説**: ハング対策に便利です。

**確認ポイント**: timed outが出る。


## Knock 014: リトライの型

**目的**: 失敗時リトライを覚える。

````bash
for i in 1 2 3; do echo "try $i"; false && break || sleep 1; done
````
**解説**: ネットワーク取得や一時エラーに使います。

**確認ポイント**: tryが複数表示される。


## Knock 015: ロックファイルの型

**目的**: 二重起動防止の考え方を知る。

````bash
mkdir -p locks && if mkdir locks/job.lock 2>/dev/null; then echo running; rmdir locks/job.lock; else echo locked; fi
````
**解説**: 同じ実験を二重に走らせる事故を防げます。

**確認ポイント**: runningが出る。


## Knock 016: 実験01のメタ保存

**目的**: 実験ごとに環境情報を保存する。

````bash
mkdir -p batch/exp_01 && ./save_meta.sh batch/exp_01/meta.txt
````
**解説**: 後から比較できるようになります。

**確認ポイント**: meta.txtができる。


## Knock 017: 実験01のログ監視

**目的**: 監視スクリプトを使う。

````bash
echo "epoch=1 loss=0.01 acc=0.71" > batch/exp_01/train.log && ./monitor_job.sh batch/exp_01/train.log
````
**解説**: ログ形式が揃うほど自動監視しやすくなります。

**確認ポイント**: loss/accが出る。


## Knock 018: 実験02のメタ保存

**目的**: 実験ごとに環境情報を保存する。

````bash
mkdir -p batch/exp_02 && ./save_meta.sh batch/exp_02/meta.txt
````
**解説**: 後から比較できるようになります。

**確認ポイント**: meta.txtができる。


## Knock 019: 実験02のログ監視

**目的**: 監視スクリプトを使う。

````bash
echo "epoch=1 loss=0.02 acc=0.72" > batch/exp_02/train.log && ./monitor_job.sh batch/exp_02/train.log
````
**解説**: ログ形式が揃うほど自動監視しやすくなります。

**確認ポイント**: loss/accが出る。


## Knock 020: 実験03のメタ保存

**目的**: 実験ごとに環境情報を保存する。

````bash
mkdir -p batch/exp_03 && ./save_meta.sh batch/exp_03/meta.txt
````
**解説**: 後から比較できるようになります。

**確認ポイント**: meta.txtができる。


## Knock 021: 実験03のログ監視

**目的**: 監視スクリプトを使う。

````bash
echo "epoch=1 loss=0.03 acc=0.73" > batch/exp_03/train.log && ./monitor_job.sh batch/exp_03/train.log
````
**解説**: ログ形式が揃うほど自動監視しやすくなります。

**確認ポイント**: loss/accが出る。


## Knock 022: 実験04のメタ保存

**目的**: 実験ごとに環境情報を保存する。

````bash
mkdir -p batch/exp_04 && ./save_meta.sh batch/exp_04/meta.txt
````
**解説**: 後から比較できるようになります。

**確認ポイント**: meta.txtができる。


## Knock 023: 実験04のログ監視

**目的**: 監視スクリプトを使う。

````bash
echo "epoch=1 loss=0.04 acc=0.74" > batch/exp_04/train.log && ./monitor_job.sh batch/exp_04/train.log
````
**解説**: ログ形式が揃うほど自動監視しやすくなります。

**確認ポイント**: loss/accが出る。


## Knock 024: 実験05のメタ保存

**目的**: 実験ごとに環境情報を保存する。

````bash
mkdir -p batch/exp_05 && ./save_meta.sh batch/exp_05/meta.txt
````
**解説**: 後から比較できるようになります。

**確認ポイント**: meta.txtができる。


## Knock 025: 実験05のログ監視

**目的**: 監視スクリプトを使う。

````bash
echo "epoch=1 loss=0.05 acc=0.75" > batch/exp_05/train.log && ./monitor_job.sh batch/exp_05/train.log
````
**解説**: ログ形式が揃うほど自動監視しやすくなります。

**確認ポイント**: loss/accが出る。


## Knock 026: 実験06のメタ保存

**目的**: 実験ごとに環境情報を保存する。

````bash
mkdir -p batch/exp_06 && ./save_meta.sh batch/exp_06/meta.txt
````
**解説**: 後から比較できるようになります。

**確認ポイント**: meta.txtができる。


## Knock 027: 実験06のログ監視

**目的**: 監視スクリプトを使う。

````bash
echo "epoch=1 loss=0.06 acc=0.76" > batch/exp_06/train.log && ./monitor_job.sh batch/exp_06/train.log
````
**解説**: ログ形式が揃うほど自動監視しやすくなります。

**確認ポイント**: loss/accが出る。


## Knock 028: 実験07のメタ保存

**目的**: 実験ごとに環境情報を保存する。

````bash
mkdir -p batch/exp_07 && ./save_meta.sh batch/exp_07/meta.txt
````
**解説**: 後から比較できるようになります。

**確認ポイント**: meta.txtができる。


## Knock 029: 実験07のログ監視

**目的**: 監視スクリプトを使う。

````bash
echo "epoch=1 loss=0.07 acc=0.77" > batch/exp_07/train.log && ./monitor_job.sh batch/exp_07/train.log
````
**解説**: ログ形式が揃うほど自動監視しやすくなります。

**確認ポイント**: loss/accが出る。


## Knock 030: 実験08のメタ保存

**目的**: 実験ごとに環境情報を保存する。

````bash
mkdir -p batch/exp_08 && ./save_meta.sh batch/exp_08/meta.txt
````
**解説**: 後から比較できるようになります。

**確認ポイント**: meta.txtができる。


## Knock 031: 実験08のログ監視

**目的**: 監視スクリプトを使う。

````bash
echo "epoch=1 loss=0.08 acc=0.78" > batch/exp_08/train.log && ./monitor_job.sh batch/exp_08/train.log
````
**解説**: ログ形式が揃うほど自動監視しやすくなります。

**確認ポイント**: loss/accが出る。


## Knock 032: 実験09のメタ保存

**目的**: 実験ごとに環境情報を保存する。

````bash
mkdir -p batch/exp_09 && ./save_meta.sh batch/exp_09/meta.txt
````
**解説**: 後から比較できるようになります。

**確認ポイント**: meta.txtができる。


## Knock 033: 実験09のログ監視

**目的**: 監視スクリプトを使う。

````bash
echo "epoch=1 loss=0.09 acc=0.79" > batch/exp_09/train.log && ./monitor_job.sh batch/exp_09/train.log
````
**解説**: ログ形式が揃うほど自動監視しやすくなります。

**確認ポイント**: loss/accが出る。


## Knock 034: 実験10のメタ保存

**目的**: 実験ごとに環境情報を保存する。

````bash
mkdir -p batch/exp_10 && ./save_meta.sh batch/exp_10/meta.txt
````
**解説**: 後から比較できるようになります。

**確認ポイント**: meta.txtができる。


## Knock 035: 実験10のログ監視

**目的**: 監視スクリプトを使う。

````bash
echo "epoch=1 loss=0.10 acc=0.80" > batch/exp_10/train.log && ./monitor_job.sh batch/exp_10/train.log
````
**解説**: ログ形式が揃うほど自動監視しやすくなります。

**確認ポイント**: loss/accが出る。


## Knock 036: 実験11のメタ保存

**目的**: 実験ごとに環境情報を保存する。

````bash
mkdir -p batch/exp_11 && ./save_meta.sh batch/exp_11/meta.txt
````
**解説**: 後から比較できるようになります。

**確認ポイント**: meta.txtができる。


## Knock 037: 実験11のログ監視

**目的**: 監視スクリプトを使う。

````bash
echo "epoch=1 loss=0.11 acc=0.81" > batch/exp_11/train.log && ./monitor_job.sh batch/exp_11/train.log
````
**解説**: ログ形式が揃うほど自動監視しやすくなります。

**確認ポイント**: loss/accが出る。


## Knock 038: 実験12のメタ保存

**目的**: 実験ごとに環境情報を保存する。

````bash
mkdir -p batch/exp_12 && ./save_meta.sh batch/exp_12/meta.txt
````
**解説**: 後から比較できるようになります。

**確認ポイント**: meta.txtができる。


## Knock 039: 実験12のログ監視

**目的**: 監視スクリプトを使う。

````bash
echo "epoch=1 loss=0.12 acc=0.82" > batch/exp_12/train.log && ./monitor_job.sh batch/exp_12/train.log
````
**解説**: ログ形式が揃うほど自動監視しやすくなります。

**確認ポイント**: loss/accが出る。


## Knock 040: 実験13のメタ保存

**目的**: 実験ごとに環境情報を保存する。

````bash
mkdir -p batch/exp_13 && ./save_meta.sh batch/exp_13/meta.txt
````
**解説**: 後から比較できるようになります。

**確認ポイント**: meta.txtができる。


## Knock 041: 実験13のログ監視

**目的**: 監視スクリプトを使う。

````bash
echo "epoch=1 loss=0.13 acc=0.83" > batch/exp_13/train.log && ./monitor_job.sh batch/exp_13/train.log
````
**解説**: ログ形式が揃うほど自動監視しやすくなります。

**確認ポイント**: loss/accが出る。


## Knock 042: 実験14のメタ保存

**目的**: 実験ごとに環境情報を保存する。

````bash
mkdir -p batch/exp_14 && ./save_meta.sh batch/exp_14/meta.txt
````
**解説**: 後から比較できるようになります。

**確認ポイント**: meta.txtができる。


## Knock 043: 実験14のログ監視

**目的**: 監視スクリプトを使う。

````bash
echo "epoch=1 loss=0.14 acc=0.84" > batch/exp_14/train.log && ./monitor_job.sh batch/exp_14/train.log
````
**解説**: ログ形式が揃うほど自動監視しやすくなります。

**確認ポイント**: loss/accが出る。


## Knock 044: 実験15のメタ保存

**目的**: 実験ごとに環境情報を保存する。

````bash
mkdir -p batch/exp_15 && ./save_meta.sh batch/exp_15/meta.txt
````
**解説**: 後から比較できるようになります。

**確認ポイント**: meta.txtができる。


## Knock 045: 実験15のログ監視

**目的**: 監視スクリプトを使う。

````bash
echo "epoch=1 loss=0.15 acc=0.85" > batch/exp_15/train.log && ./monitor_job.sh batch/exp_15/train.log
````
**解説**: ログ形式が揃うほど自動監視しやすくなります。

**確認ポイント**: loss/accが出る。


## Knock 046: 実験16のメタ保存

**目的**: 実験ごとに環境情報を保存する。

````bash
mkdir -p batch/exp_16 && ./save_meta.sh batch/exp_16/meta.txt
````
**解説**: 後から比較できるようになります。

**確認ポイント**: meta.txtができる。


## Knock 047: 実験16のログ監視

**目的**: 監視スクリプトを使う。

````bash
echo "epoch=1 loss=0.16 acc=0.86" > batch/exp_16/train.log && ./monitor_job.sh batch/exp_16/train.log
````
**解説**: ログ形式が揃うほど自動監視しやすくなります。

**確認ポイント**: loss/accが出る。


## Knock 048: 実験17のメタ保存

**目的**: 実験ごとに環境情報を保存する。

````bash
mkdir -p batch/exp_17 && ./save_meta.sh batch/exp_17/meta.txt
````
**解説**: 後から比較できるようになります。

**確認ポイント**: meta.txtができる。


## Knock 049: 実験17のログ監視

**目的**: 監視スクリプトを使う。

````bash
echo "epoch=1 loss=0.17 acc=0.87" > batch/exp_17/train.log && ./monitor_job.sh batch/exp_17/train.log
````
**解説**: ログ形式が揃うほど自動監視しやすくなります。

**確認ポイント**: loss/accが出る。


## Knock 050: 実験18のメタ保存

**目的**: 実験ごとに環境情報を保存する。

````bash
mkdir -p batch/exp_18 && ./save_meta.sh batch/exp_18/meta.txt
````
**解説**: 後から比較できるようになります。

**確認ポイント**: meta.txtができる。


## Knock 051: 実験18のログ監視

**目的**: 監視スクリプトを使う。

````bash
echo "epoch=1 loss=0.18 acc=0.88" > batch/exp_18/train.log && ./monitor_job.sh batch/exp_18/train.log
````
**解説**: ログ形式が揃うほど自動監視しやすくなります。

**確認ポイント**: loss/accが出る。


## Knock 052: 実験19のメタ保存

**目的**: 実験ごとに環境情報を保存する。

````bash
mkdir -p batch/exp_19 && ./save_meta.sh batch/exp_19/meta.txt
````
**解説**: 後から比較できるようになります。

**確認ポイント**: meta.txtができる。


## Knock 053: 実験19のログ監視

**目的**: 監視スクリプトを使う。

````bash
echo "epoch=1 loss=0.19 acc=0.89" > batch/exp_19/train.log && ./monitor_job.sh batch/exp_19/train.log
````
**解説**: ログ形式が揃うほど自動監視しやすくなります。

**確認ポイント**: loss/accが出る。


## Knock 054: 実験20のメタ保存

**目的**: 実験ごとに環境情報を保存する。

````bash
mkdir -p batch/exp_20 && ./save_meta.sh batch/exp_20/meta.txt
````
**解説**: 後から比較できるようになります。

**確認ポイント**: meta.txtができる。


## Knock 055: 実験20のログ監視

**目的**: 監視スクリプトを使う。

````bash
echo "epoch=1 loss=0.20 acc=0.90" > batch/exp_20/train.log && ./monitor_job.sh batch/exp_20/train.log
````
**解説**: ログ形式が揃うほど自動監視しやすくなります。

**確認ポイント**: loss/accが出る。


## Knock 056: 実験21のメタ保存

**目的**: 実験ごとに環境情報を保存する。

````bash
mkdir -p batch/exp_21 && ./save_meta.sh batch/exp_21/meta.txt
````
**解説**: 後から比較できるようになります。

**確認ポイント**: meta.txtができる。


## Knock 057: 実験21のログ監視

**目的**: 監視スクリプトを使う。

````bash
echo "epoch=1 loss=0.21 acc=0.91" > batch/exp_21/train.log && ./monitor_job.sh batch/exp_21/train.log
````
**解説**: ログ形式が揃うほど自動監視しやすくなります。

**確認ポイント**: loss/accが出る。


## Knock 058: 実験22のメタ保存

**目的**: 実験ごとに環境情報を保存する。

````bash
mkdir -p batch/exp_22 && ./save_meta.sh batch/exp_22/meta.txt
````
**解説**: 後から比較できるようになります。

**確認ポイント**: meta.txtができる。


## Knock 059: 実験22のログ監視

**目的**: 監視スクリプトを使う。

````bash
echo "epoch=1 loss=0.22 acc=0.92" > batch/exp_22/train.log && ./monitor_job.sh batch/exp_22/train.log
````
**解説**: ログ形式が揃うほど自動監視しやすくなります。

**確認ポイント**: loss/accが出る。


## Knock 060: 実験23のメタ保存

**目的**: 実験ごとに環境情報を保存する。

````bash
mkdir -p batch/exp_23 && ./save_meta.sh batch/exp_23/meta.txt
````
**解説**: 後から比較できるようになります。

**確認ポイント**: meta.txtができる。


## Knock 061: 実験23のログ監視

**目的**: 監視スクリプトを使う。

````bash
echo "epoch=1 loss=0.23 acc=0.93" > batch/exp_23/train.log && ./monitor_job.sh batch/exp_23/train.log
````
**解説**: ログ形式が揃うほど自動監視しやすくなります。

**確認ポイント**: loss/accが出る。


## Knock 062: 実験24のメタ保存

**目的**: 実験ごとに環境情報を保存する。

````bash
mkdir -p batch/exp_24 && ./save_meta.sh batch/exp_24/meta.txt
````
**解説**: 後から比較できるようになります。

**確認ポイント**: meta.txtができる。


## Knock 063: 実験24のログ監視

**目的**: 監視スクリプトを使う。

````bash
echo "epoch=1 loss=0.24 acc=0.94" > batch/exp_24/train.log && ./monitor_job.sh batch/exp_24/train.log
````
**解説**: ログ形式が揃うほど自動監視しやすくなります。

**確認ポイント**: loss/accが出る。


## Knock 064: 実験25のメタ保存

**目的**: 実験ごとに環境情報を保存する。

````bash
mkdir -p batch/exp_25 && ./save_meta.sh batch/exp_25/meta.txt
````
**解説**: 後から比較できるようになります。

**確認ポイント**: meta.txtができる。


## Knock 065: 実験25のログ監視

**目的**: 監視スクリプトを使う。

````bash
echo "epoch=1 loss=0.25 acc=0.95" > batch/exp_25/train.log && ./monitor_job.sh batch/exp_25/train.log
````
**解説**: ログ形式が揃うほど自動監視しやすくなります。

**確認ポイント**: loss/accが出る。


## Knock 066: 実験26のメタ保存

**目的**: 実験ごとに環境情報を保存する。

````bash
mkdir -p batch/exp_26 && ./save_meta.sh batch/exp_26/meta.txt
````
**解説**: 後から比較できるようになります。

**確認ポイント**: meta.txtができる。


## Knock 067: 実験26のログ監視

**目的**: 監視スクリプトを使う。

````bash
echo "epoch=1 loss=0.26 acc=0.96" > batch/exp_26/train.log && ./monitor_job.sh batch/exp_26/train.log
````
**解説**: ログ形式が揃うほど自動監視しやすくなります。

**確認ポイント**: loss/accが出る。


## Knock 068: 実験27のメタ保存

**目的**: 実験ごとに環境情報を保存する。

````bash
mkdir -p batch/exp_27 && ./save_meta.sh batch/exp_27/meta.txt
````
**解説**: 後から比較できるようになります。

**確認ポイント**: meta.txtができる。


## Knock 069: 実験27のログ監視

**目的**: 監視スクリプトを使う。

````bash
echo "epoch=1 loss=0.27 acc=0.97" > batch/exp_27/train.log && ./monitor_job.sh batch/exp_27/train.log
````
**解説**: ログ形式が揃うほど自動監視しやすくなります。

**確認ポイント**: loss/accが出る。


## Knock 070: 実験28のメタ保存

**目的**: 実験ごとに環境情報を保存する。

````bash
mkdir -p batch/exp_28 && ./save_meta.sh batch/exp_28/meta.txt
````
**解説**: 後から比較できるようになります。

**確認ポイント**: meta.txtができる。


## Knock 071: 実験28のログ監視

**目的**: 監視スクリプトを使う。

````bash
echo "epoch=1 loss=0.28 acc=0.98" > batch/exp_28/train.log && ./monitor_job.sh batch/exp_28/train.log
````
**解説**: ログ形式が揃うほど自動監視しやすくなります。

**確認ポイント**: loss/accが出る。


## Knock 072: 実験29のメタ保存

**目的**: 実験ごとに環境情報を保存する。

````bash
mkdir -p batch/exp_29 && ./save_meta.sh batch/exp_29/meta.txt
````
**解説**: 後から比較できるようになります。

**確認ポイント**: meta.txtができる。


## Knock 073: 実験29のログ監視

**目的**: 監視スクリプトを使う。

````bash
echo "epoch=1 loss=0.29 acc=0.99" > batch/exp_29/train.log && ./monitor_job.sh batch/exp_29/train.log
````
**解説**: ログ形式が揃うほど自動監視しやすくなります。

**確認ポイント**: loss/accが出る。


## Knock 074: 実験30のメタ保存

**目的**: 実験ごとに環境情報を保存する。

````bash
mkdir -p batch/exp_30 && ./save_meta.sh batch/exp_30/meta.txt
````
**解説**: 後から比較できるようになります。

**確認ポイント**: meta.txtができる。


## Knock 075: 実験30のログ監視

**目的**: 監視スクリプトを使う。

````bash
echo "epoch=1 loss=0.30 acc=0.100" > batch/exp_30/train.log && ./monitor_job.sh batch/exp_30/train.log
````
**解説**: ログ形式が揃うほど自動監視しやすくなります。

**確認ポイント**: loss/accが出る。


## Knock 076: Slurm GPUジョブ雛形

**目的**: GPUジョブのSBATCH例を作る。

````bash
cat > slurm_gpu.sh <<EOF
#!/usr/bin/env bash
#SBATCH --job-name=gpu_test
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=01:00:00
#SBATCH --output=logs/%x-%j.out

set -euo pipefail
mkdir -p logs
hostname
nvidia-smi
python3 train.py
EOF
````
**解説**: 実際のオプション名はクラスタルールに合わせます。

**確認ポイント**: ファイルを確認。


## Knock 077: Slurm配列ジョブ雛形

**目的**: 配列ジョブの型を覚える。

````bash
cat > slurm_array.sh <<EOF
#!/usr/bin/env bash
#SBATCH --job-name=array_test
#SBATCH --array=1-10
#SBATCH --output=logs/%x-%A_%a.out

echo "task=$SLURM_ARRAY_TASK_ID"
EOF
````
**解説**: 複数条件実験をクラスタに投げる時に便利です。

**確認ポイント**: ファイルを確認。


## Knock 078: Slurmキャンセル型

**目的**: ジョブ停止コマンドの型を覚える。

````bash
echo "scancel JOB_ID"
````
**解説**: 実IDを確認してから使います。

**確認ポイント**: 型を確認。


## Knock 079: Slurmログ名の意味をメモ

**目的**: ログファイル名のプレースホルダを覚える。

````bash
echo "%x=job name, %j=job id, %A=array job id, %a=array task id" > slurm_log_placeholders.txt
````
**解説**: ログ整理で重要です。

**確認ポイント**: メモを確認。


## Knock 080: 総復習チェック 080

**目的**: その領域の練習前後で現在地・時刻・ファイル状態を確認する。

````bash
pwd && date && ls -lah | head
````
**解説**: 初心者ほど、現在地と対象ファイルを確認する癖が重要です。迷ったらまずこの確認セットに戻ります。

**確認ポイント**: 現在地、日時、ファイル一覧の先頭が表示される。


## Knock 081: 総復習チェック 081

**目的**: その領域の練習前後で現在地・時刻・ファイル状態を確認する。

````bash
pwd && date && ls -lah | head
````
**解説**: 初心者ほど、現在地と対象ファイルを確認する癖が重要です。迷ったらまずこの確認セットに戻ります。

**確認ポイント**: 現在地、日時、ファイル一覧の先頭が表示される。


## Knock 082: 総復習チェック 082

**目的**: その領域の練習前後で現在地・時刻・ファイル状態を確認する。

````bash
pwd && date && ls -lah | head
````
**解説**: 初心者ほど、現在地と対象ファイルを確認する癖が重要です。迷ったらまずこの確認セットに戻ります。

**確認ポイント**: 現在地、日時、ファイル一覧の先頭が表示される。


## Knock 083: 総復習チェック 083

**目的**: その領域の練習前後で現在地・時刻・ファイル状態を確認する。

````bash
pwd && date && ls -lah | head
````
**解説**: 初心者ほど、現在地と対象ファイルを確認する癖が重要です。迷ったらまずこの確認セットに戻ります。

**確認ポイント**: 現在地、日時、ファイル一覧の先頭が表示される。


## Knock 084: 総復習チェック 084

**目的**: その領域の練習前後で現在地・時刻・ファイル状態を確認する。

````bash
pwd && date && ls -lah | head
````
**解説**: 初心者ほど、現在地と対象ファイルを確認する癖が重要です。迷ったらまずこの確認セットに戻ります。

**確認ポイント**: 現在地、日時、ファイル一覧の先頭が表示される。


## Knock 085: 総復習チェック 085

**目的**: その領域の練習前後で現在地・時刻・ファイル状態を確認する。

````bash
pwd && date && ls -lah | head
````
**解説**: 初心者ほど、現在地と対象ファイルを確認する癖が重要です。迷ったらまずこの確認セットに戻ります。

**確認ポイント**: 現在地、日時、ファイル一覧の先頭が表示される。


## Knock 086: 総復習チェック 086

**目的**: その領域の練習前後で現在地・時刻・ファイル状態を確認する。

````bash
pwd && date && ls -lah | head
````
**解説**: 初心者ほど、現在地と対象ファイルを確認する癖が重要です。迷ったらまずこの確認セットに戻ります。

**確認ポイント**: 現在地、日時、ファイル一覧の先頭が表示される。


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

