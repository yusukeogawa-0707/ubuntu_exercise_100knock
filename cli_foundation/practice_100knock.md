# 研究サーバSSH実践100本ノック — 実践編


実践編。VPN/SSH、転送、長時間実験、ログ監視、結果回収。

> 1周目=写経、2周目=説明を見て自力、3周目=目的だけ見て再現。


## 実行環境について

この実践編には `ssh myserver ...` や `rsync ... myserver:...` のように、研究サーバやSSH接続先が必要なKnockが含まれます。Windows PC 1台だけで始める場合は、まず [`docs/setup_windows_single_pc.md`](../docs/setup_windows_single_pc.md) に沿ってWSL Ubuntuとローカル練習データを用意し、`myserver` が必要なKnockは「読む・意味を確認する・ローカル代替で試す」扱いにしてください。

- サーバ不要の確認だけ先に練習する例：`hostname && pwd && free -h`
- rsyncの考え方だけ先に練習する例：`rsync -avP data/ ~/ubuntu100knock/mock_server/ubuntu100_data_rsync/`
- 本物のSSH先ができたら、`~/.ssh/config` に `Host myserver` を登録してから実行します。

## VPN/SSH入口

### Knock 001: ユーザ確認

```bash
whoami
```

**解説**：ユーザ確認。

### Knock 002: ホスト確認

```bash
hostname
```

**解説**：マシン確認。

### Knock 003: IP確認

```bash
ip addr
```

**解説**：IP確認。

### Knock 004: inet抽出

```bash
ip addr | grep "inet "
```

**解説**：IP行抽出。

### Knock 005: 経路

```bash
ip route
```

**解説**：経路確認。

### Knock 006: ping

```bash
ping -c 4 myserver
```

**解説**：疎通確認。

### Knock 007: SSH

```bash
ssh myserver
```

**解説**：接続。

### Knock 008: SSH先hostname

```bash
hostname
```

**解説**：接続先確認。

### Knock 009: SSH先pwd

```bash
pwd
```

**解説**：現在地確認。

### Knock 010: exit

```bash
exit
```

**解説**：ログアウト。

## SSH便利操作

### Knock 011: 遠隔hostname

```bash
ssh myserver "hostname"
```

**解説**：リモート実行。

### Knock 012: 遠隔容量

```bash
ssh myserver "df -h"
```

**解説**：容量確認。

### Knock 013: 遠隔メモリ

```bash
ssh myserver "free -h"
```

**解説**：メモリ確認。

### Knock 014: 遠隔Python

```bash
ssh myserver "pgrep -af python"
```

**解説**：プロセス確認。

### Knock 015: 遠隔GPU

```bash
ssh myserver "nvidia-smi"
```

**解説**：GPU確認。

### Knock 016: ssh config準備

```bash
mkdir -p ~/.ssh && chmod 700 ~/.ssh
```

**解説**：設定準備。

### Knock 017: config作成

```bash
touch ~/.ssh/config && chmod 600 ~/.ssh/config
```

**解説**：設定作成。

### Knock 018: config編集

```bash
code ~/.ssh/config
```

**解説**：編集。

### Knock 019: 短縮名接続

```bash
ssh myserver
```

**解説**：短縮接続。

### Knock 020: 状態一括

```bash
ssh myserver "hostname && pwd && free -h"
```

**解説**：`ssh myserver "..."` は、短縮名 `myserver` に接続してサーバ側でコマンドを実行する書き方です。`&&` は「左のコマンドが成功したら次を実行する」という意味なので、`hostname` で接続先を確認し、`pwd` で実行場所を確認し、`free -h` でメモリ状況を人間が読みやすい単位で確認できます。リモートサーバにログインしっぱなしにせず、状態確認だけをまとめて行いたい場面で役立ちます。

## curl/wget

### Knock 021: curl取得

```bash
curl https://example.com
```

**解説**：取得。

### Knock 022: curl保存

```bash
curl -L https://example.com -o tmp/example.html
```

**解説**：保存。

### Knock 023: wget保存

```bash
wget https://example.com -O tmp/example_wget.html
```

**解説**：保存。

### Knock 024: ヘッダー

```bash
curl -I https://example.com
```

**解説**：ヘッダー。

### Knock 025: API

```bash
curl -s https://api.github.com/repos/python/cpython | head
```

**解説**：API確認。

### Knock 026: URLリスト

```bash
printf 'https://example.com
https://example.com
' > tmp/urls.txt
```

**解説**：URL一覧。

### Knock 027: 一括wget

```bash
wget -i tmp/urls.txt -P tmp/downloads
```

**解説**：一括取得。

### Knock 028: サイズ

```bash
ls -lh tmp/example*
```

**解説**：確認。

### Knock 029: 先頭

```bash
head tmp/example.html
```

**解説**：中身確認。

### Knock 030: サーバ直接wget

```bash
ssh myserver "mkdir -p ~/downloads && cd ~/downloads && wget https://example.com -O example.html"
```

**解説**：サーバ直接取得。

## 転送

### Knock 031: scp送信

```bash
scp notes/research.md myserver:~/research.md
```

**解説**：送信。

### Knock 032: scp回収

```bash
scp myserver:~/research.md tmp/research_from_server.md
```

**解説**：回収。

### Knock 033: scpディレクトリ送信

```bash
scp -r data myserver:~/ubuntu100_data
```

**解説**：送信。

### Knock 034: scpディレクトリ回収

```bash
scp -r myserver:~/ubuntu100_data backup/ubuntu100_data_from_server
```

**解説**：回収。

### Knock 035: rsync dry-run

```bash
rsync -avP --dry-run data/ myserver:~/ubuntu100_data_rsync/
```

**解説**：予行演習。

### Knock 036: rsync送信

```bash
rsync -avP data/ myserver:~/ubuntu100_data_rsync/
```

**解説**：`rsync` で `data/` の中身をリモートの `~/ubuntu100_data_rsync/` へ実際に同期します。`-a` は属性を保って再帰コピーする archive、`-v` は詳細表示、`-P` は進捗表示と途中再開をまとめた指定です。研究データ・実験結果・大量ファイルを転送するときは、差分だけを送り直せる `rsync` が `scp` より便利な場面が多く、転送が中断しても再実行しやすいのが強みです。

### Knock 037: rsync回収

```bash
rsync -avP myserver:~/ubuntu100_data_rsync/ backup/ubuntu100_data_rsync/
```

**解説**：差分回収。

### Knock 038: CSVだけ

```bash
rsync -avP --include="*.csv" --exclude="*" data/ myserver:~/csv_only/
```

**解説**：対象限定。

### Knock 039: log除外

```bash
rsync -avP --exclude="*.log" ./ myserver:~/project_without_logs/
```

**解説**：除外。

### Knock 040: 容量確認

```bash
du -sh data
```

**解説**：送る前に確認。

## 長時間実験

### Knock 041: 普通実行

```bash
python3 src/train.py
```

**解説**：普通に実行。

### Knock 042: ログ保存

```bash
python3 src/train.py > logs/train.log 2>&1
```

**解説**：保存。

### Knock 043: tee

```bash
python3 src/train.py 2>&1 | tee logs/train_tee.log
```

**解説**：画面と保存。

### Knock 044: バックグラウンド

```bash
python3 src/train.py > logs/bg_train.log 2>&1 &
```

**解説**：裏で実行。

### Knock 045: jobs

```bash
jobs
```

**解説**：ジョブ確認。

### Knock 046: pgrep

```bash
pgrep -af python
```

**解説**：プロセス確認。

### Knock 047: nohup

```bash
nohup python3 src/train.py > logs/nohup_train.log 2>&1 &
```

**解説**：切断対策。

### Knock 048: tailログ

```bash
tail -f logs/nohup_train.log
```

**解説**：監視。

### Knock 049: 遠隔nohup

```bash
ssh myserver "cd ~/ubuntu100knock && nohup python3 src/train.py > logs/remote_train.log 2>&1 &"
```

**解説**：遠隔起動。

### Knock 050: 遠隔tail

```bash
ssh myserver "tail -n 50 ~/ubuntu100knock/logs/remote_train.log"
```

**解説**：遠隔確認。

## tmux

### Knock 051: tmux

```bash
tmux
```

**解説**：起動。

### Knock 052: 名前つき

```bash
tmux new -s exp001
```

**解説**：作成。

### Knock 053: detach

```bash
Ctrl+b then d
```

**解説**：離脱。

### Knock 054: 一覧

```bash
tmux ls
```

**解説**：一覧。

### Knock 055: 戻る

```bash
tmux attach -t exp001
```

**解説**：再接続。

### Knock 056: tmux内実験

```bash
python3 src/train.py 2>&1 | tee logs/tmux_train.log
```

**解説**：実験。

### Knock 057: 新窓

```bash
Ctrl+b then c
```

**解説**：新ウィンドウ。

### Knock 058: 次

```bash
Ctrl+b then n
```

**解説**：移動。

### Knock 059: 前

```bash
Ctrl+b then p
```

**解説**：移動。

### Knock 060: 終了

```bash
tmux kill-session -t exp001
```

**解説**：終了。

## 監視

### Knock 061: tail -f

```bash
tail -f logs/app.log
```

**解説**：監視。

### Knock 062: ERROR監視

```bash
tail -f logs/app.log | grep "ERROR"
```

**解説**：エラー監視。

### Knock 063: WARN/ERROR

```bash
tail -f logs/app.log | grep -E "ERROR|WARN"
```

**解説**：重要ログ。

### Knock 064: 前後

```bash
grep -n -C 2 "ERROR" logs/app.log
```

**解説**：文脈。

### Knock 065: 前

```bash
grep -n -B 3 "ERROR" logs/app.log
```

**解説**：`grep -n` は行番号を付け、`-B 3` は before（マッチした行の直前3行も表示）を意味します。エラー行だけでは原因が分からず、その直前の `WARN` や設定読み込みメッセージに手がかりがあることがよくあります。ログ調査では、まず `grep "ERROR"` で場所を見つけ、次に `-B` や `-A` で前後の文脈を読むと、原因特定が速くなります。

### Knock 066: 後

```bash
grep -n -A 3 "ERROR" logs/app.log
```

**解説**：直後。

### Knock 067: レベル集計

```bash
awk '{print $3}' logs/app.log | sort | uniq -c | sort -nr
```

**解説**：集計。

### Knock 068: 日別ERROR

```bash
grep "ERROR" logs/app.log | awk '{print $1}' | sort | uniq -c
```

**解説**：日別。

### Knock 069: GPU watch

```bash
watch -n 2 nvidia-smi
```

**解説**：GPU監視。

### Knock 070: 遠隔GPU watch

```bash
ssh myserver "watch -n 2 nvidia-smi"
```

**解説**：遠隔監視。

## 容量掃除

### Knock 071: df

```bash
df -h
```

**解説**：容量。

### Knock 072: du

```bash
du -sh .
```

**解説**：現在地容量。

### Knock 073: 直下

```bash
du -h --max-depth=1 . | sort -hr
```

**解説**：直下容量。

### Knock 074: 大ファイル

```bash
find . -type f -exec du -h {} + | sort -hr | head -n 20
```

**解説**：重いファイル。

### Knock 075: 100MB

```bash
find . -type f -size +100M -print
```

**解説**：100MB超。

### Knock 076: 1GB

```bash
find . -type f -size +1G -print
```

**解説**：1GB超。

### Knock 077: 古いログ

```bash
find . -name "*.log" -mtime +7 -print
```

**解説**：候補。

### Knock 078: 確認削除

```bash
find . -name "*.log" -mtime +7 -ok rm {} \;
```

**解説**：安全削除。

### Knock 079: 遠隔容量

```bash
ssh myserver "du -h --max-depth=1 ~/ubuntu100knock | sort -hr"
```

**解説**：遠隔容量。

### Knock 080: 遠隔大ファイル

```bash
ssh myserver "find ~/ubuntu100knock -type f -size +1G -print"
```

**解説**：遠隔大ファイル。

## 総合

### Knock 081: 状態一括

```bash
ssh myserver "hostname && nvidia-smi && df -h"
```

**解説**：便利型。

### Knock 082: 送信起動

```bash
rsync -avP ./ myserver:~/ubuntu100knock/ && ssh myserver "cd ~/ubuntu100knock && nohup python3 src/train.py > logs/run.log 2>&1 &"
```

**解説**：送信から起動。

### Knock 083: ログ確認

```bash
ssh myserver "tail -n 30 ~/ubuntu100knock/logs/run.log"
```

**解説**：確認。

### Knock 084: 回収

```bash
rsync -avP myserver:~/ubuntu100knock/logs/ backup/logs_from_server/
```

**解説**：回収。

### Knock 085: 対話実行

```bash
ssh myserver "cd ~/ubuntu100knock && python3 src/train.py 2>&1 | tee logs/interactive.log"
```

**解説**：見ながら実行。

### Knock 086: 実験dir

```bash
ssh myserver "cd ~/ubuntu100knock && mkdir -p experiments/$(date +%Y%m%d)_exp001"
```

**解説**：実験dir。

### Knock 087: 設定保存

```bash
ssh myserver "cd ~/ubuntu100knock && date > experiments/latest_config.txt"
```

**解説**：メモ。

### Knock 088: 警告抽出

```bash
ssh myserver "grep -E 'ERROR|WARN' ~/ubuntu100knock/logs/app.log"
```

**解説**：ログ抽出。

### Knock 089: 重いモデル除外回収

```bash
rsync -avP --exclude="*.pt" myserver:~/ubuntu100knock/experiments/ backup/experiments/
```

**解説**：除外回収。

### Knock 090: 最終型

```bash
ssh myserver "cd ~/ubuntu100knock && nohup python3 src/train.py > experiments/remote_exp001.log 2>&1 &" && ssh myserver "tail -n 20 ~/ubuntu100knock/experiments/remote_exp001.log" && rsync -avP myserver:~/ubuntu100knock/experiments/ backup/remote_experiments/
```

**解説**：開始→確認→回収。
