# 圧縮・バックアップ・cron 100本ノック — v2 応用・実践編

## 位置づけ

tar/zip/バックアップ検証/定期実行の型を扱う。

- v1入門編: まず壊さず、意味を確認しながら手を動かす。
- v2応用・実践編: 研究実務で使う形に近づける。

## 使い方

1. まず各Knockのコマンドを読む。
2. 練習用ディレクトリで実行する。
3. 解説と確認ポイントを見て、何が起きたか確認する。

注意: `myserver`, `your_username`, `git@example.com:USER/REPO.git` などは仮の名前です。実環境に合わせて置き換えてください。

## Knock 001: tarがあるか確認

**目的**: 圧縮・展開ツールを確認する。

````bash
tar --version | head -n 1
````
**解説**: Linuxではtar.gzが頻出です。

**確認ポイント**: tarのバージョンが出る。


## Knock 002: 練習ディレクトリを作る

**目的**: 安全な練習場所を作る。

````bash
mkdir -p ~/archive100knock/{data,outputs,logs,backup,tmp} && cd ~/archive100knock
````
**解説**: 圧縮や削除を扱うので隔離します。

**確認ポイント**: pwdで確認。


## Knock 003: サンプルファイルを作る

**目的**: 圧縮対象を用意する。

````bash
for i in 1 2 3; do echo "sample $i" > data/file_$i.txt; done
````
**解説**: 小さいファイルで練習します。

**確認ポイント**: dataにファイルができる。


## Knock 004: 容量を見る

**目的**: 圧縮前の容量を見る。

````bash
du -sh data
````
**解説**: 圧縮やバックアップ前には容量確認します。

**確認ポイント**: 容量が出る。


## Knock 005: ファイル一覧を見る

**目的**: 対象ファイルを確認する。

````bash
find data -type f -exec ls -lh {} \;
````
**解説**: 圧縮や削除前の確認です。

**確認ポイント**: ファイル一覧が出る。


## Knock 006: バックアップスクリプトを作る

**目的**: 再利用可能なバックアップ手順を作る。

````bash
cat > backup_project.sh <<'EOF
#!/usr/bin/env bash
set -euo pipefail
SRC=${1:-data}
DEST=${2:-backup}
mkdir -p "$DEST"
OUT="$DEST/$(basename "$SRC")_$(date +%Y%m%d_%H%M%S).tar.gz"
tar -czf "$OUT" "$SRC"
sha256sum "$OUT" > "$OUT.sha256"
echo "$OUT"
EOF
chmod +x backup_project.sh
````
**解説**: 対象と保存先を引数にして汎用化します。

**確認ポイント**: `./backup_project.sh data backup` で動く。


## Knock 007: バックアップを実行する

**目的**: スクリプトでバックアップを作る。

````bash
./backup_project.sh data backup
````
**解説**: 手打ちtarよりミスが減ります。

**確認ポイント**: tar.gzとsha256ができる。


## Knock 008: バックアップ検証スクリプトを作る

**目的**: バックアップの破損確認を自動化する。

````bash
cat > verify_backup.sh <<'EOF
#!/usr/bin/env bash
set -euo pipefail
FILE=${1:?Usage: $0 FILE.tar.gz}
sha256sum -c "$FILE.sha256"
tar -tzf "$FILE" > /dev/null
echo "OK: $FILE"
EOF
chmod +x verify_backup.sh
````
**解説**: 作っただけでなく検証まで行います。

**確認ポイント**: 検証OKが出る。


## Knock 009: 最新バックアップを検証する

**目的**: 最新バックアップを検証する。

````bash
LATEST=$(ls -t backup/*.tar.gz | head -n 1); ./verify_backup.sh "$LATEST"
````
**解説**: 復元できないバックアップは意味がありません。

**確認ポイント**: OKが出る。


## Knock 010: 復元スクリプトを作る

**目的**: 復元手順をスクリプト化する。

````bash
cat > restore_backup.sh <<'EOF
#!/usr/bin/env bash
set -euo pipefail
FILE=${1:?Usage: $0 FILE.tar.gz DEST}
DEST=${2:?Usage: $0 FILE.tar.gz DEST}
mkdir -p "$DEST"
tar -xzf "$FILE" -C "$DEST"
EOF
chmod +x restore_backup.sh
````
**解説**: バックアップは復元まで練習して価値があります。

**確認ポイント**: スクリプトができる。


## Knock 011: 最新バックアップを復元する

**目的**: 復元を実際に試す。

````bash
LATEST=$(ls -t backup/*.tar.gz | head -n 1); ./restore_backup.sh "$LATEST" tmp/restore_test
````
**解説**: 本番障害前に復元確認するのが大事です。

**確認ポイント**: tmp/restore_testを見る。


## Knock 012: 古いバックアップ削除dry-run

**目的**: 削除候補だけ表示する。

````bash
find backup -type f -name "*.tar.gz" -mtime +30 -print
````
**解説**: 削除前は必ずdry-run相当の表示をします。

**確認ポイント**: 候補が表示される。


## Knock 013: 削除を確認付きにする

**目的**: 確認しながら削除する。

````bash
find backup -type f -name "*.tar.gz" -mtime +30 -ok rm {} \;
````
**解説**: 初心者は `-delete` より `-ok rm` が安全です。

**確認ポイント**: 1件ずつ確認される。


## Knock 014: cron投入用ファイルを作る

**目的**: cron設定例を作る。

````bash
cat > mycron.example <<EOF
# Example only. Review before installing.
0 3 * * * cd $PWD && ./backup_project.sh data backup >> logs/cron_backup.log 2>&1
EOF
````
**解説**: まずexampleファイルとして作り、すぐ投入しません。

**確認ポイント**: 内容を確認。


## Knock 015: cron投入コマンドを表示

**目的**: cron登録の型を確認する。

````bash
echo "crontab mycron.example"
````
**解説**: 実行すると本当に定期実行されるので、まず表示だけにします。

**確認ポイント**: コマンド例が出る。


## Knock 016: data用バックアップ実行

**目的**: 対象別にバックアップを作る。

````bash
mkdir -p data; ./backup_project.sh data backup
````
**解説**: 研究プロジェクトの主要ディレクトリを個別に固めます。

**確認ポイント**: dataのtar.gzができる。


## Knock 017: data用バックアップ検証

**目的**: 対象別バックアップを検証する。

````bash
LATEST=$(ls -t backup/data_*.tar.gz | head -n 1); ./verify_backup.sh "$LATEST"
````
**解説**: 壊れていないことを確認します。

**確認ポイント**: OKが出る。


## Knock 018: outputs用バックアップ実行

**目的**: 対象別にバックアップを作る。

````bash
mkdir -p outputs; ./backup_project.sh outputs backup
````
**解説**: 研究プロジェクトの主要ディレクトリを個別に固めます。

**確認ポイント**: outputsのtar.gzができる。


## Knock 019: outputs用バックアップ検証

**目的**: 対象別バックアップを検証する。

````bash
LATEST=$(ls -t backup/outputs_*.tar.gz | head -n 1); ./verify_backup.sh "$LATEST"
````
**解説**: 壊れていないことを確認します。

**確認ポイント**: OKが出る。


## Knock 020: logs用バックアップ実行

**目的**: 対象別にバックアップを作る。

````bash
mkdir -p logs; ./backup_project.sh logs backup
````
**解説**: 研究プロジェクトの主要ディレクトリを個別に固めます。

**確認ポイント**: logsのtar.gzができる。


## Knock 021: logs用バックアップ検証

**目的**: 対象別バックアップを検証する。

````bash
LATEST=$(ls -t backup/logs_*.tar.gz | head -n 1); ./verify_backup.sh "$LATEST"
````
**解説**: 壊れていないことを確認します。

**確認ポイント**: OKが出る。


## Knock 022: configs用バックアップ実行

**目的**: 対象別にバックアップを作る。

````bash
mkdir -p configs; ./backup_project.sh configs backup
````
**解説**: 研究プロジェクトの主要ディレクトリを個別に固めます。

**確認ポイント**: configsのtar.gzができる。


## Knock 023: configs用バックアップ検証

**目的**: 対象別バックアップを検証する。

````bash
LATEST=$(ls -t backup/configs_*.tar.gz | head -n 1); ./verify_backup.sh "$LATEST"
````
**解説**: 壊れていないことを確認します。

**確認ポイント**: OKが出る。


## Knock 024: src用バックアップ実行

**目的**: 対象別にバックアップを作る。

````bash
mkdir -p src; ./backup_project.sh src backup
````
**解説**: 研究プロジェクトの主要ディレクトリを個別に固めます。

**確認ポイント**: srcのtar.gzができる。


## Knock 025: src用バックアップ検証

**目的**: 対象別バックアップを検証する。

````bash
LATEST=$(ls -t backup/src_*.tar.gz | head -n 1); ./verify_backup.sh "$LATEST"
````
**解説**: 壊れていないことを確認します。

**確認ポイント**: OKが出る。


## Knock 026: notes用バックアップ実行

**目的**: 対象別にバックアップを作る。

````bash
mkdir -p notes; ./backup_project.sh notes backup
````
**解説**: 研究プロジェクトの主要ディレクトリを個別に固めます。

**確認ポイント**: notesのtar.gzができる。


## Knock 027: notes用バックアップ検証

**目的**: 対象別バックアップを検証する。

````bash
LATEST=$(ls -t backup/notes_*.tar.gz | head -n 1); ./verify_backup.sh "$LATEST"
````
**解説**: 壊れていないことを確認します。

**確認ポイント**: OKが出る。


## Knock 028: experiments用バックアップ実行

**目的**: 対象別にバックアップを作る。

````bash
mkdir -p experiments; ./backup_project.sh experiments backup
````
**解説**: 研究プロジェクトの主要ディレクトリを個別に固めます。

**確認ポイント**: experimentsのtar.gzができる。


## Knock 029: experiments用バックアップ検証

**目的**: 対象別バックアップを検証する。

````bash
LATEST=$(ls -t backup/experiments_*.tar.gz | head -n 1); ./verify_backup.sh "$LATEST"
````
**解説**: 壊れていないことを確認します。

**確認ポイント**: OKが出る。


## Knock 030: results用バックアップ実行

**目的**: 対象別にバックアップを作る。

````bash
mkdir -p results; ./backup_project.sh results backup
````
**解説**: 研究プロジェクトの主要ディレクトリを個別に固めます。

**確認ポイント**: resultsのtar.gzができる。


## Knock 031: results用バックアップ検証

**目的**: 対象別バックアップを検証する。

````bash
LATEST=$(ls -t backup/results_*.tar.gz | head -n 1); ./verify_backup.sh "$LATEST"
````
**解説**: 壊れていないことを確認します。

**確認ポイント**: OKが出る。


## Knock 032: checkpoints用バックアップ実行

**目的**: 対象別にバックアップを作る。

````bash
mkdir -p checkpoints; ./backup_project.sh checkpoints backup
````
**解説**: 研究プロジェクトの主要ディレクトリを個別に固めます。

**確認ポイント**: checkpointsのtar.gzができる。


## Knock 033: checkpoints用バックアップ検証

**目的**: 対象別バックアップを検証する。

````bash
LATEST=$(ls -t backup/checkpoints_*.tar.gz | head -n 1); ./verify_backup.sh "$LATEST"
````
**解説**: 壊れていないことを確認します。

**確認ポイント**: OKが出る。


## Knock 034: reports用バックアップ実行

**目的**: 対象別にバックアップを作る。

````bash
mkdir -p reports; ./backup_project.sh reports backup
````
**解説**: 研究プロジェクトの主要ディレクトリを個別に固めます。

**確認ポイント**: reportsのtar.gzができる。


## Knock 035: reports用バックアップ検証

**目的**: 対象別バックアップを検証する。

````bash
LATEST=$(ls -t backup/reports_*.tar.gz | head -n 1); ./verify_backup.sh "$LATEST"
````
**解説**: 壊れていないことを確認します。

**確認ポイント**: OKが出る。


## Knock 036: cron例: 5分ごと

**目的**: cron時刻指定を覚える。

````bash
echo "*/5 * * * * echo cron_5 >> $PWD/logs/cron_example.log" >> cron_examples.txt
````
**解説**: 実行登録ではなく例としてファイルに貯めます。

**確認ポイント**: cron_examples.txtを確認。


## Knock 037: cron例: 毎時

**目的**: cron時刻指定を覚える。

````bash
echo "0 * * * * echo cron_ >> $PWD/logs/cron_example.log" >> cron_examples.txt
````
**解説**: 実行登録ではなく例としてファイルに貯めます。

**確認ポイント**: cron_examples.txtを確認。


## Knock 038: cron例: 毎日深夜

**目的**: cron時刻指定を覚える。

````bash
echo "0 3 * * * echo cron_ >> $PWD/logs/cron_example.log" >> cron_examples.txt
````
**解説**: 実行登録ではなく例としてファイルに貯めます。

**確認ポイント**: cron_examples.txtを確認。


## Knock 039: cron例: 平日朝

**目的**: cron時刻指定を覚える。

````bash
echo "0 8 * * 1-5 echo cron_ >> $PWD/logs/cron_example.log" >> cron_examples.txt
````
**解説**: 実行登録ではなく例としてファイルに貯めます。

**確認ポイント**: cron_examples.txtを確認。


## Knock 040: cron例: 毎週日曜

**目的**: cron時刻指定を覚える。

````bash
echo "0 4 * * 0 echo cron_ >> $PWD/logs/cron_example.log" >> cron_examples.txt
````
**解説**: 実行登録ではなく例としてファイルに貯めます。

**確認ポイント**: cron_examples.txtを確認。


## Knock 041: cron例: 毎月1日

**目的**: cron時刻指定を覚える。

````bash
echo "0 5 1 * * echo cron_1 >> $PWD/logs/cron_example.log" >> cron_examples.txt
````
**解説**: 実行登録ではなく例としてファイルに貯めます。

**確認ポイント**: cron_examples.txtを確認。


## Knock 042: cron例: 月金

**目的**: cron時刻指定を覚える。

````bash
echo "30 7 * * 1,5 echo cron_ >> $PWD/logs/cron_example.log" >> cron_examples.txt
````
**解説**: 実行登録ではなく例としてファイルに貯めます。

**確認ポイント**: cron_examples.txtを確認。


## Knock 043: cron例: 年1回

**目的**: cron時刻指定を覚える。

````bash
echo "0 0 1 1 * echo cron_1 >> $PWD/logs/cron_example.log" >> cron_examples.txt
````
**解説**: 実行登録ではなく例としてファイルに貯めます。

**確認ポイント**: cron_examples.txtを確認。


## Knock 044: cron例: 起動時

**目的**: cron時刻指定を覚える。

````bash
echo "@reboot echo cron_ >> $PWD/logs/cron_example.log" >> cron_examples.txt
````
**解説**: 実行登録ではなく例としてファイルに貯めます。

**確認ポイント**: cron_examples.txtを確認。


## Knock 045: cron例: 毎日2回

**目的**: cron時刻指定を覚える。

````bash
echo "0 8,20 * * * echo cron_2 >> $PWD/logs/cron_example.log" >> cron_examples.txt
````
**解説**: 実行登録ではなく例としてファイルに貯めます。

**確認ポイント**: cron_examples.txtを確認。


## Knock 046: systemdユーザサービス例を作る

**目的**: systemdサービス定義の例を作る。

````bash
mkdir -p systemd_examples && cat > systemd_examples/ubuntu100.service <<EOF
[Unit]
Description=Ubuntu100 sample service

[Service]
Type=oneshot
WorkingDirectory=$PWD
ExecStart=$PWD/backup_project.sh data backup
EOF
````
**解説**: 実登録はしません。構造理解用です。

**確認ポイント**: serviceファイルを確認。


## Knock 047: systemd timer例を作る

**目的**: systemd timer例を作る。

````bash
cat > systemd_examples/ubuntu100.timer <<EOF
[Unit]
Description=Run Ubuntu100 backup daily

[Timer]
OnCalendar=*-*-* 03:00:00
Persistent=true

[Install]
WantedBy=timers.target
EOF
````
**解説**: cronの代替として使われることがあります。

**確認ポイント**: timerファイルを確認。


## Knock 048: ユーザtimer一覧を見る

**目的**: systemd timer確認の型を覚える。

````bash
systemctl --user list-timers 2>/dev/null || echo "systemd user unavailable"
````
**解説**: 環境により使えない場合があります。

**確認ポイント**: 一覧または不可表示。


## Knock 049: journalctlの型を見る

**目的**: ログ確認コマンドの型を覚える。

````bash
echo "journalctl --user -u ubuntu100.service -n 50"
````
**解説**: systemd管理のログはjournalctlで見ます。

**確認ポイント**: 型を確認。


## Knock 050: バックアップ世代01を作る

**目的**: 世代管理を体験する。

````bash
echo "generation 1" > data/gen_01.txt && ./backup_project.sh data backup
````
**解説**: バックアップは1個だけでなく世代を残します。

**確認ポイント**: backupにファイルが増える。


## Knock 051: バックアップ世代02を作る

**目的**: 世代管理を体験する。

````bash
echo "generation 2" > data/gen_02.txt && ./backup_project.sh data backup
````
**解説**: バックアップは1個だけでなく世代を残します。

**確認ポイント**: backupにファイルが増える。


## Knock 052: バックアップ世代03を作る

**目的**: 世代管理を体験する。

````bash
echo "generation 3" > data/gen_03.txt && ./backup_project.sh data backup
````
**解説**: バックアップは1個だけでなく世代を残します。

**確認ポイント**: backupにファイルが増える。


## Knock 053: バックアップ世代04を作る

**目的**: 世代管理を体験する。

````bash
echo "generation 4" > data/gen_04.txt && ./backup_project.sh data backup
````
**解説**: バックアップは1個だけでなく世代を残します。

**確認ポイント**: backupにファイルが増える。


## Knock 054: バックアップ世代05を作る

**目的**: 世代管理を体験する。

````bash
echo "generation 5" > data/gen_05.txt && ./backup_project.sh data backup
````
**解説**: バックアップは1個だけでなく世代を残します。

**確認ポイント**: backupにファイルが増える。


## Knock 055: バックアップ世代06を作る

**目的**: 世代管理を体験する。

````bash
echo "generation 6" > data/gen_06.txt && ./backup_project.sh data backup
````
**解説**: バックアップは1個だけでなく世代を残します。

**確認ポイント**: backupにファイルが増える。


## Knock 056: バックアップ世代07を作る

**目的**: 世代管理を体験する。

````bash
echo "generation 7" > data/gen_07.txt && ./backup_project.sh data backup
````
**解説**: バックアップは1個だけでなく世代を残します。

**確認ポイント**: backupにファイルが増える。


## Knock 057: バックアップ世代08を作る

**目的**: 世代管理を体験する。

````bash
echo "generation 8" > data/gen_08.txt && ./backup_project.sh data backup
````
**解説**: バックアップは1個だけでなく世代を残します。

**確認ポイント**: backupにファイルが増える。


## Knock 058: バックアップ世代09を作る

**目的**: 世代管理を体験する。

````bash
echo "generation 9" > data/gen_09.txt && ./backup_project.sh data backup
````
**解説**: バックアップは1個だけでなく世代を残します。

**確認ポイント**: backupにファイルが増える。


## Knock 059: バックアップ世代10を作る

**目的**: 世代管理を体験する。

````bash
echo "generation 10" > data/gen_10.txt && ./backup_project.sh data backup
````
**解説**: バックアップは1個だけでなく世代を残します。

**確認ポイント**: backupにファイルが増える。


## Knock 060: バックアップ世代11を作る

**目的**: 世代管理を体験する。

````bash
echo "generation 11" > data/gen_11.txt && ./backup_project.sh data backup
````
**解説**: バックアップは1個だけでなく世代を残します。

**確認ポイント**: backupにファイルが増える。


## Knock 061: バックアップ世代12を作る

**目的**: 世代管理を体験する。

````bash
echo "generation 12" > data/gen_12.txt && ./backup_project.sh data backup
````
**解説**: バックアップは1個だけでなく世代を残します。

**確認ポイント**: backupにファイルが増える。


## Knock 062: バックアップ世代13を作る

**目的**: 世代管理を体験する。

````bash
echo "generation 13" > data/gen_13.txt && ./backup_project.sh data backup
````
**解説**: バックアップは1個だけでなく世代を残します。

**確認ポイント**: backupにファイルが増える。


## Knock 063: バックアップ世代14を作る

**目的**: 世代管理を体験する。

````bash
echo "generation 14" > data/gen_14.txt && ./backup_project.sh data backup
````
**解説**: バックアップは1個だけでなく世代を残します。

**確認ポイント**: backupにファイルが増える。


## Knock 064: バックアップ世代15を作る

**目的**: 世代管理を体験する。

````bash
echo "generation 15" > data/gen_15.txt && ./backup_project.sh data backup
````
**解説**: バックアップは1個だけでなく世代を残します。

**確認ポイント**: backupにファイルが増える。


## Knock 065: バックアップ世代16を作る

**目的**: 世代管理を体験する。

````bash
echo "generation 16" > data/gen_16.txt && ./backup_project.sh data backup
````
**解説**: バックアップは1個だけでなく世代を残します。

**確認ポイント**: backupにファイルが増える。


## Knock 066: 総復習チェック 066

**目的**: その領域の練習前後で現在地・時刻・ファイル状態を確認する。

````bash
pwd && date && ls -lah | head
````
**解説**: 初心者ほど、現在地と対象ファイルを確認する癖が重要です。迷ったらまずこの確認セットに戻ります。

**確認ポイント**: 現在地、日時、ファイル一覧の先頭が表示される。


## Knock 067: 総復習チェック 067

**目的**: その領域の練習前後で現在地・時刻・ファイル状態を確認する。

````bash
pwd && date && ls -lah | head
````
**解説**: 初心者ほど、現在地と対象ファイルを確認する癖が重要です。迷ったらまずこの確認セットに戻ります。

**確認ポイント**: 現在地、日時、ファイル一覧の先頭が表示される。


## Knock 068: 総復習チェック 068

**目的**: その領域の練習前後で現在地・時刻・ファイル状態を確認する。

````bash
pwd && date && ls -lah | head
````
**解説**: 初心者ほど、現在地と対象ファイルを確認する癖が重要です。迷ったらまずこの確認セットに戻ります。

**確認ポイント**: 現在地、日時、ファイル一覧の先頭が表示される。


## Knock 069: 総復習チェック 069

**目的**: その領域の練習前後で現在地・時刻・ファイル状態を確認する。

````bash
pwd && date && ls -lah | head
````
**解説**: 初心者ほど、現在地と対象ファイルを確認する癖が重要です。迷ったらまずこの確認セットに戻ります。

**確認ポイント**: 現在地、日時、ファイル一覧の先頭が表示される。


## Knock 070: 総復習チェック 070

**目的**: その領域の練習前後で現在地・時刻・ファイル状態を確認する。

````bash
pwd && date && ls -lah | head
````
**解説**: 初心者ほど、現在地と対象ファイルを確認する癖が重要です。迷ったらまずこの確認セットに戻ります。

**確認ポイント**: 現在地、日時、ファイル一覧の先頭が表示される。


## Knock 071: 総復習チェック 071

**目的**: その領域の練習前後で現在地・時刻・ファイル状態を確認する。

````bash
pwd && date && ls -lah | head
````
**解説**: 初心者ほど、現在地と対象ファイルを確認する癖が重要です。迷ったらまずこの確認セットに戻ります。

**確認ポイント**: 現在地、日時、ファイル一覧の先頭が表示される。


## Knock 072: 総復習チェック 072

**目的**: その領域の練習前後で現在地・時刻・ファイル状態を確認する。

````bash
pwd && date && ls -lah | head
````
**解説**: 初心者ほど、現在地と対象ファイルを確認する癖が重要です。迷ったらまずこの確認セットに戻ります。

**確認ポイント**: 現在地、日時、ファイル一覧の先頭が表示される。


## Knock 073: 総復習チェック 073

**目的**: その領域の練習前後で現在地・時刻・ファイル状態を確認する。

````bash
pwd && date && ls -lah | head
````
**解説**: 初心者ほど、現在地と対象ファイルを確認する癖が重要です。迷ったらまずこの確認セットに戻ります。

**確認ポイント**: 現在地、日時、ファイル一覧の先頭が表示される。


## Knock 074: 総復習チェック 074

**目的**: その領域の練習前後で現在地・時刻・ファイル状態を確認する。

````bash
pwd && date && ls -lah | head
````
**解説**: 初心者ほど、現在地と対象ファイルを確認する癖が重要です。迷ったらまずこの確認セットに戻ります。

**確認ポイント**: 現在地、日時、ファイル一覧の先頭が表示される。


## Knock 075: 総復習チェック 075

**目的**: その領域の練習前後で現在地・時刻・ファイル状態を確認する。

````bash
pwd && date && ls -lah | head
````
**解説**: 初心者ほど、現在地と対象ファイルを確認する癖が重要です。迷ったらまずこの確認セットに戻ります。

**確認ポイント**: 現在地、日時、ファイル一覧の先頭が表示される。


## Knock 076: 総復習チェック 076

**目的**: その領域の練習前後で現在地・時刻・ファイル状態を確認する。

````bash
pwd && date && ls -lah | head
````
**解説**: 初心者ほど、現在地と対象ファイルを確認する癖が重要です。迷ったらまずこの確認セットに戻ります。

**確認ポイント**: 現在地、日時、ファイル一覧の先頭が表示される。


## Knock 077: 総復習チェック 077

**目的**: その領域の練習前後で現在地・時刻・ファイル状態を確認する。

````bash
pwd && date && ls -lah | head
````
**解説**: 初心者ほど、現在地と対象ファイルを確認する癖が重要です。迷ったらまずこの確認セットに戻ります。

**確認ポイント**: 現在地、日時、ファイル一覧の先頭が表示される。


## Knock 078: 総復習チェック 078

**目的**: その領域の練習前後で現在地・時刻・ファイル状態を確認する。

````bash
pwd && date && ls -lah | head
````
**解説**: 初心者ほど、現在地と対象ファイルを確認する癖が重要です。迷ったらまずこの確認セットに戻ります。

**確認ポイント**: 現在地、日時、ファイル一覧の先頭が表示される。


## Knock 079: 総復習チェック 079

**目的**: その領域の練習前後で現在地・時刻・ファイル状態を確認する。

````bash
pwd && date && ls -lah | head
````
**解説**: 初心者ほど、現在地と対象ファイルを確認する癖が重要です。迷ったらまずこの確認セットに戻ります。

**確認ポイント**: 現在地、日時、ファイル一覧の先頭が表示される。


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

