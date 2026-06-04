# Ubuntu CLI基礎100本ノック — 入門編


入門編。ファイル操作、検索、パイプライン、CSV/ログ確認。

> 1周目=写経、2周目=説明を見て自力、3周目=目的だけ見て再現。

## 現在地・一覧

### Knock 001: pwd を使う

```bash
pwd
```

**解説**：現在地確認。

### Knock 002: cd ~ を使う

```bash
cd ~
```

**解説**：ホームに戻る。

### Knock 003: mkdir -p ~/ubuntu100knock/{data,logs,src,notes,tmp,backup} を使う

```bash
mkdir -p ~/ubuntu100knock/{data,logs,src,notes,tmp,backup}
```

**解説**：練習環境作成。

### Knock 004: cd ~/ubuntu100knock を使う

```bash
cd ~/ubuntu100knock
```

**解説**：練習環境へ移動。

### Knock 005: ls を使う

```bash
ls
```

**解説**：一覧。

### Knock 006: ls -l を使う

```bash
ls -l
```

**解説**：詳細一覧。

### Knock 007: ls -la を使う

```bash
ls -la
```

**解説**：隠しファイル込み。

### Knock 008: ls -lh を使う

```bash
ls -lh
```

**解説**：読みやすいサイズ。

### Knock 009: ls -lah を使う

```bash
ls -lah
```

**解説**：最頻出一覧。

### Knock 010: find . -maxdepth 2 を使う

```bash
find . -maxdepth 2
```

**解説**：構造確認。

## 教材データ

### Knock 011: CSVを作る

```bash
cat > data/members.csv <<'EOF'
id,name,team,score,city
1,Aki,radio,78,Urawa
2,Bob,ai,92,Hachioji
3,Chika,radio,85,Osaka
4,Daichi,core,66,Tokyo
5,Ema,ai,73,Urawa
6,Fumi,core,88,Kyoto
7,Gaku,radio,91,Saitama
8,Hana,ai,58,Tokyo
EOF
```

**解説**：CSV処理の練習データ。

### Knock 012: ログを作る

```bash
cat > logs/app.log <<'EOF'
2026-06-01 09:00:01 INFO scheduler started
2026-06-01 09:05:33 WARN gpu memory high
2026-06-01 09:06:10 ERROR failed to load config
2026-06-01 09:15:20 ERROR cuda out of memory
2026-06-02 10:03:21 WARN network unstable
2026-06-02 10:08:55 ERROR failed to save checkpoint
2026-06-02 10:12:30 INFO training finished acc=0.84
EOF
```

**解説**：ログ検索練習データ。

### Knock 013: JSONLを作る

```bash
cat > data/metrics.jsonl <<'EOF'
{"exp":"exp001","model":"rqn","acc":0.81,"loss":0.52}
{"exp":"exp002","model":"rqn","acc":0.84,"loss":0.47}
{"exp":"exp003","model":"transformer","acc":0.88,"loss":0.39}
EOF
```

**解説**：実験結果風のJSONL。

### Knock 014: Pythonを作る

```bash
cat > src/train.py <<'EOF'
print('training started')
print('epoch=1 loss=0.52 acc=0.81')
print('epoch=2 loss=0.47 acc=0.84')
print('training finished')
EOF
```

**解説**：ログ保存練習。

## ファイル操作

### Knock 015: 空ファイル作成

```bash
touch tmp/memo.txt
```

**解説**：touchで空ファイル作成。

### Knock 016: 上書き保存

```bash
echo "hello ubuntu" > tmp/hello.txt
```

**解説**：> は上書き。

### Knock 017: 追記保存

```bash
echo "second line" >> tmp/hello.txt
```

**解説**：>> は追記。

### Knock 018: 中身表示

```bash
cat tmp/hello.txt
```

**解説**：短いファイル表示。

### Knock 019: コピー

```bash
cp tmp/hello.txt tmp/hello_copy.txt
```

**解説**：cpでコピー。

### Knock 020: リネーム

```bash
mv tmp/hello_copy.txt tmp/hello_renamed.txt
```

**解説**：mvでリネーム。

### Knock 021: 移動

```bash
mv tmp/hello_renamed.txt backup/
```

**解説**：mvで移動。

### Knock 022: 確認削除

```bash
rm -i tmp/memo.txt
```

**解説**：rm -iで安全削除。

### Knock 023: ディレクトリコピー

```bash
cp -r data backup/data_backup
```

**解説**：ディレクトリは-r。

### Knock 024: 結果確認

```bash
ls -lah backup
```

**解説**：操作結果確認。

## 中身・件数・サイズ

### Knock 025: CSV表示

```bash
cat data/members.csv
```

**解説**：小さいCSVを見る。

### Knock 026: 先頭5行

```bash
head -n 5 data/members.csv
```

**解説**：形式確認。

### Knock 027: 末尾5行

```bash
tail -n 5 data/members.csv
```

**解説**：末尾確認。

### Knock 028: ログ末尾

```bash
tail logs/app.log
```

**解説**：`tail` はファイルの末尾を表示するコマンドです。ログファイルは新しい情報が末尾に追加されることが多いため、直近のエラー・警告・実験終了メッセージをすばやく確認したいときに使います。まず `tail logs/app.log` で最後の数行を見て、必要なら `tail -n 50` や `tail -f` に進む、という流れが現場でよく使われます。

### Knock 029: 行数

```bash
wc -l data/members.csv
```

**解説**：行数確認。

### Knock 030: ヘッダー除外件数

```bash
tail -n +2 data/members.csv | wc -l
```

**解説**：実データ件数。

### Knock 031: ファイル種別

```bash
file data/members.csv
```

**解説**：種別確認。

### Knock 032: ファイル容量

```bash
du -h data/members.csv
```

**解説**：容量確認。

### Knock 033: 全体容量

```bash
du -sh .
```

**解説**：プロジェクト容量。

### Knock 034: 容量ランキング

```bash
du -ah . | sort -rh | head -n 20
```

**解説**：重いファイル探し。

## grep検索

### Knock 035: ERROR検索

```bash
grep "ERROR" logs/app.log
```

**解説**：エラー抽出。

### Knock 036: 行番号つき

```bash
grep -n "ERROR" logs/app.log
```

**解説**：場所確認。

### Knock 037: 大小無視

```bash
grep -i "error" logs/app.log
```

**解説**：表記ゆれ対応。

### Knock 038: WARN/ERROR

```bash
grep -E "WARN|ERROR" logs/app.log
```

**解説**：OR検索。

### Knock 039: INFO除外

```bash
grep -v "INFO" logs/app.log
```

**解説**：除外。

### Knock 040: 再帰検索

```bash
grep -r "print" src
```

**解説**：配下検索。

### Knock 041: 件数

```bash
grep -c "ERROR" logs/app.log
```

**解説**：`grep -c` の `-c` は count（件数）の意味で、マッチした行を表示せず「何行ヒットしたか」だけを出します。エラーログの件数をざっくり把握したいとき、修正前後でエラー数が減ったか確認したいとき、監視スクリプトで閾値判定したいときに便利です。詳細を見る前に件数だけ確認すると、ログ全体を読む時間を減らせます。

### Knock 042: 保存

```bash
grep "ERROR" logs/app.log > tmp/errors.log
```

**解説**：検索結果保存。

### Knock 043: 前後

```bash
grep -n -C 1 "ERROR" logs/app.log
```

**解説**：文脈確認。

### Knock 044: TODO

```bash
grep -r "TODO" notes || true
```

**解説**：TODO検索。

## パイプライン・CSV集計

### Knock 045: ERROR件数

```bash
grep "ERROR" logs/app.log | wc -l
```

**解説**：検索して数える。

### Knock 046: 末尾からERROR

```bash
tail -n 5 logs/app.log | grep "ERROR"
```

**解説**：範囲を絞る。

### Knock 047: 名前列

```bash
cut -d, -f2 data/members.csv
```

**解説**：列抽出。

### Knock 048: ヘッダーなし名前

```bash
tail -n +2 data/members.csv | cut -d, -f2
```

**解説**：ヘッダー除外。

### Knock 049: city件数

```bash
tail -n +2 data/members.csv | cut -d, -f5 | sort | uniq -c
```

**解説**：出現回数。

### Knock 050: city件数降順

```bash
tail -n +2 data/members.csv | cut -d, -f5 | sort | uniq -c | sort -nr
```

**解説**：ランキング。

### Knock 051: score昇順

```bash
tail -n +2 data/members.csv | cut -d, -f4 | sort -n
```

**解説**：数値ソート。

### Knock 052: score降順

```bash
tail -n +2 data/members.csv | cut -d, -f4 | sort -nr
```

**解説**：降順。

### Knock 053: team件数

```bash
tail -n +2 data/members.csv | cut -d, -f3 | sort | uniq -c | sort -nr
```

**解説**：チーム分布。

### Knock 054: 抽出型

```bash
cat data/members.csv | grep "ai" | cut -d, -f2,4
```

**解説**：絞って列抽出。

## awk/sed/tr/column

### Knock 055: 80点以上

```bash
awk -F, 'NR==1 || $4 >= 80' data/members.csv
```

**解説**：条件抽出。

### Knock 056: 80点以上名前

```bash
awk -F, 'NR>1 && $4 >= 80 {print $2}' data/members.csv
```

**解説**：条件＋列抽出。

### Knock 057: 平均点

```bash
awk -F, 'NR>1 {sum+=$4; n++} END {print sum/n}' data/members.csv
```

**解説**：平均。

### Knock 058: team平均

```bash
awk -F, 'NR>1 {sum[$3]+=$4; n[$3]++} END {for(t in sum) print t, sum[t]/n[t]}' data/members.csv
```

**解説**：グループ平均。

### Knock 059: score降順表

```bash
{ head -n 1 data/members.csv; tail -n +2 data/members.csv | sort -t, -k4,4nr; }
```

**解説**：ヘッダー維持。

### Knock 060: 置換表示

```bash
sed 's/Ubuntu/Linux/g' notes/research.md
```

**解説**：置換。

### Knock 061: 空行削除

```bash
sed '/^$/d' notes/research.md
```

**解説**：空行削除。

### Knock 062: 小文字化

```bash
cat notes/research.md | tr 'A-Z' 'a-z'
```

**解説**：文字変換。

### Knock 063: CSV表表示

```bash
column -s, -t data/members.csv
```

**解説**：表表示。

### Knock 064: ログレベル

```bash
awk '{print $3}' logs/app.log
```

**解説**：ログレベル抽出。

## find/xargs

### Knock 065: CSV探索

```bash
find . -name "*.csv"
```

**解説**：CSV探し。

### Knock 066: log探索

```bash
find . -name "*.log"
```

**解説**：ログ探し。

### Knock 067: py探索

```bash
find . -name "*.py"
```

**解説**：Python探し。

### Knock 068: ファイルだけ

```bash
find . -type f
```

**解説**：通常ファイル。

### Knock 069: 空ファイル

```bash
find . -type f -empty
```

**解説**：空ファイル。

### Knock 070: 最近更新

```bash
find . -type f -mtime -1
```

**解説**：最近の変更。

### Knock 071: 名前検索

```bash
find . -iname "*research*"
```

**解説**：名前検索。

### Knock 072: 全行数

```bash
find . -type f -print0 | xargs -0 wc -l
```

**解説**：行数集計。

### Knock 073: Markdown TODO

```bash
find . -name "*.md" -print0 | xargs -0 grep -n "TODO" || true
```

**解説**：対象検索。

### Knock 074: 大ファイル

```bash
find . -type f -exec du -h {} + | sort -hr | head
```

**解説**：容量確認。

## ログ保存・システム・総合

### Knock 075: ls保存

```bash
ls -lah > tmp/list.txt
```

**解説**：標準出力保存。

### Knock 076: date追記

```bash
date >> tmp/list.txt
```

**解説**：追記。

### Knock 077: tee保存

```bash
ls -lah | tee tmp/list_tee.txt
```

**解説**：画面と保存。

### Knock 078: stderr分離

```bash
ls existing not_existing > tmp/stdout.log 2> tmp/stderr.log
```

**解説**：標準エラー分離。

### Knock 079: 出力まとめ

```bash
ls existing not_existing > tmp/all.log 2>&1
```

**解説**：標準出力とエラーをまとめる。

### Knock 080: Pythonログ

```bash
python3 src/train.py > logs/train.log 2>&1
```

**解説**：実験ログ。

### Knock 081: Python tee

```bash
python3 src/train.py 2>&1 | tee logs/train_tee.log
```

**解説**：画面とログ。

### Knock 082: OS情報

```bash
cat /etc/os-release
```

**解説**：OS確認。

### Knock 083: メモリ

```bash
free -h
```

**解説**：メモリ確認。

### Knock 084: ディスク

```bash
df -h
```

**解説**：ディスク確認。

### Knock 085: Pythonプロセス

```bash
pgrep -af python
```

**解説**：プロセス確認。

### Knock 086: ログレベル件数

```bash
awk '{print $3}' logs/app.log | sort | uniq -c | sort -nr
```

**解説**：ログ集計。

### Knock 087: ERROR本文

```bash
grep "ERROR" logs/app.log | cut -d" " -f4-
```

**解説**：本文抽出。

### Knock 088: 重要ログ保存

```bash
grep -E "ERROR|WARN" logs/app.log | tee tmp/warn_error_summary.txt
```

**解説**：抽出保存。

### Knock 089: jq整形

```bash
cat data/metrics.jsonl | jq .
```

**解説**：JSONL整形。

### Knock 090: acc抽出

```bash
cat data/metrics.jsonl | jq -r .acc
```

**解説**：指標抽出。

### Knock 091: 高acc

```bash
cat data/metrics.jsonl | jq "select(.acc >= 0.8)"
```

**解説**：条件抽出。

### Knock 092: CSV化

```bash
cat data/metrics.jsonl | jq -r "[.exp, .acc] | @csv"
```

**解説**：CSV化。

### Knock 093: 総合型

```bash
grep -E "ERROR|WARN" logs/app.log | awk '{print $1, $3, substr($0,index($0,$4))}' | tee tmp/summary.txt
```

**解説**：抽出・整形・保存。

### Knock 094: 復唱型

```bash
cat file | grep "keyword" | cut -d, -f2 | sort | uniq -c | sort -nr
```

**解説**：CLIデータ処理の基本型。
