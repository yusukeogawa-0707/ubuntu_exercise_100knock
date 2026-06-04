# シェルスクリプト100本ノック — 入門編

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


## Knock 005: 変数を使う

**目的**: 変数の基本を覚える。

````bash
cat > scripts/var.sh <<EOF
#!/usr/bin/env bash
NAME="Ubuntu"
echo "Hello $NAME"
EOF
chmod +x scripts/var.sh && ./scripts/var.sh
````
**解説**: bashでは `NAME=value` で変数を定義し、`$NAME` で参照します。

**確認ポイント**: Hello Ubuntuが出る。


## Knock 006: 引数を使う

**目的**: コマンドライン引数を読む。

````bash
cat > scripts/arg.sh <<EOF
#!/usr/bin/env bash
echo "first arg: $1"
EOF
chmod +x scripts/arg.sh && ./scripts/arg.sh test
````
**解説**: `$1` は1番目の引数です。

**確認ポイント**: first arg: test が出る。


## Knock 007: 引数個数を見る

**目的**: 引数の個数を確認する。

````bash
cat > scripts/argc.sh <<EOF
#!/usr/bin/env bash
echo "argc: $#"
EOF
chmod +x scripts/argc.sh && ./scripts/argc.sh a b c
````
**解説**: `$#` は引数の数です。

**確認ポイント**: argc: 3が出る。


## Knock 008: 全引数を安全に扱う

**目的**: 全引数をループする。

````bash
cat > scripts/args.sh <<'EOF
#!/usr/bin/env bash
for x in "$@"; do
  echo "arg=$x"
done
EOF
chmod +x scripts/args.sh && ./scripts/args.sh "a b" c
````
**解説**: `"$@"` は空白を含む引数を壊しにくい基本形です。

**確認ポイント**: a bが1つの引数として出る。


## Knock 009: ifを書く

**目的**: 条件分岐を書く。

````bash
cat > scripts/if_file.sh <<EOF
#!/usr/bin/env bash
if [ -f README.md ]; then
  echo "README exists"
else
  echo "README missing"
fi
EOF
chmod +x scripts/if_file.sh && ./scripts/if_file.sh
````
**解説**: `[ -f file ]` は通常ファイルがあるか確認します。

**確認ポイント**: 存在に応じた表示が出る。


## Knock 010: forループを書く

**目的**: 繰り返し処理を覚える。

````bash
cat > scripts/for.sh <<EOF
#!/usr/bin/env bash
for i in 1 2 3; do
  echo "i=$i"
done
EOF
chmod +x scripts/for.sh && ./scripts/for.sh
````
**解説**: 複数実験や複数ファイル処理の基礎です。

**確認ポイント**: i=1〜3が出る。


## Knock 011: whileでファイルを読む

**目的**: 1行ずつ処理する。

````bash
printf "a\nb\nc\n" > data/list.txt
cat > scripts/read_lines.sh <<'EOF
#!/usr/bin/env bash
while IFS= read -r line; do
  echo "line=$line"
done < data/list.txt
EOF
chmod +x scripts/read_lines.sh && ./scripts/read_lines.sh
````
**解説**: ファイル一覧やURL一覧を処理する基本形です。

**確認ポイント**: 各行が表示される。


## Knock 012: 終了ステータスを見る

**目的**: コマンドの成否を数値で見る。

````bash
true; echo $?; false; echo $?
````
**解説**: 0は成功、0以外は失敗です。

**確認ポイント**: 0と1が出る。


## Knock 013: set -eを使う

**目的**: 失敗時に停止する。

````bash
cat > scripts/sete.sh <<EOF
#!/usr/bin/env bash
set -e
echo before
false
echo after
EOF
chmod +x scripts/sete.sh; ./scripts/sete.sh || echo stopped
````
**解説**: `set -e` は途中失敗を見逃さないための基本です。

**確認ポイント**: afterは表示されない。


## Knock 014: set -uを使う

**目的**: 未定義変数をエラーにする。

````bash
cat > scripts/setu.sh <<EOF
#!/usr/bin/env bash
set -u
echo "$UNDEFINED_VAR"
EOF
chmod +x scripts/setu.sh; ./scripts/setu.sh || echo undefined
````
**解説**: typoで空文字扱いになる事故を防げます。

**確認ポイント**: undefinedが出る。


## Knock 015: 番号付き実験ディレクトリを作る 01

**目的**: 変数を使ってディレクトリを作る。

````bash
EXP=exp_01; mkdir -p experiments/$EXP/logs experiments/$EXP/outputs; echo $EXP
````
**解説**: 手打ちミスを避け、規則的な実験管理をします。

**確認ポイント**: `find experiments/exp_01` で確認。


## Knock 016: 番号付きログを作る 01

**目的**: ログファイルを作る。

````bash
echo "exp_01 started at $(date)" | tee experiments/exp_01/logs/run.log
````
**解説**: スクリプトからログ保存する感覚を身につけます。

**確認ポイント**: ログに日時が入る。


## Knock 017: 番号付き実験ディレクトリを作る 02

**目的**: 変数を使ってディレクトリを作る。

````bash
EXP=exp_02; mkdir -p experiments/$EXP/logs experiments/$EXP/outputs; echo $EXP
````
**解説**: 手打ちミスを避け、規則的な実験管理をします。

**確認ポイント**: `find experiments/exp_02` で確認。


## Knock 018: 番号付きログを作る 02

**目的**: ログファイルを作る。

````bash
echo "exp_02 started at $(date)" | tee experiments/exp_02/logs/run.log
````
**解説**: スクリプトからログ保存する感覚を身につけます。

**確認ポイント**: ログに日時が入る。


## Knock 019: 番号付き実験ディレクトリを作る 03

**目的**: 変数を使ってディレクトリを作る。

````bash
EXP=exp_03; mkdir -p experiments/$EXP/logs experiments/$EXP/outputs; echo $EXP
````
**解説**: 手打ちミスを避け、規則的な実験管理をします。

**確認ポイント**: `find experiments/exp_03` で確認。


## Knock 020: 番号付きログを作る 03

**目的**: ログファイルを作る。

````bash
echo "exp_03 started at $(date)" | tee experiments/exp_03/logs/run.log
````
**解説**: スクリプトからログ保存する感覚を身につけます。

**確認ポイント**: ログに日時が入る。


## Knock 021: 番号付き実験ディレクトリを作る 04

**目的**: 変数を使ってディレクトリを作る。

````bash
EXP=exp_04; mkdir -p experiments/$EXP/logs experiments/$EXP/outputs; echo $EXP
````
**解説**: 手打ちミスを避け、規則的な実験管理をします。

**確認ポイント**: `find experiments/exp_04` で確認。


## Knock 022: 番号付きログを作る 04

**目的**: ログファイルを作る。

````bash
echo "exp_04 started at $(date)" | tee experiments/exp_04/logs/run.log
````
**解説**: スクリプトからログ保存する感覚を身につけます。

**確認ポイント**: ログに日時が入る。


## Knock 023: 番号付き実験ディレクトリを作る 05

**目的**: 変数を使ってディレクトリを作る。

````bash
EXP=exp_05; mkdir -p experiments/$EXP/logs experiments/$EXP/outputs; echo $EXP
````
**解説**: 手打ちミスを避け、規則的な実験管理をします。

**確認ポイント**: `find experiments/exp_05` で確認。


## Knock 024: 番号付きログを作る 05

**目的**: ログファイルを作る。

````bash
echo "exp_05 started at $(date)" | tee experiments/exp_05/logs/run.log
````
**解説**: スクリプトからログ保存する感覚を身につけます。

**確認ポイント**: ログに日時が入る。


## Knock 025: 番号付き実験ディレクトリを作る 06

**目的**: 変数を使ってディレクトリを作る。

````bash
EXP=exp_06; mkdir -p experiments/$EXP/logs experiments/$EXP/outputs; echo $EXP
````
**解説**: 手打ちミスを避け、規則的な実験管理をします。

**確認ポイント**: `find experiments/exp_06` で確認。


## Knock 026: 番号付きログを作る 06

**目的**: ログファイルを作る。

````bash
echo "exp_06 started at $(date)" | tee experiments/exp_06/logs/run.log
````
**解説**: スクリプトからログ保存する感覚を身につけます。

**確認ポイント**: ログに日時が入る。


## Knock 027: 番号付き実験ディレクトリを作る 07

**目的**: 変数を使ってディレクトリを作る。

````bash
EXP=exp_07; mkdir -p experiments/$EXP/logs experiments/$EXP/outputs; echo $EXP
````
**解説**: 手打ちミスを避け、規則的な実験管理をします。

**確認ポイント**: `find experiments/exp_07` で確認。


## Knock 028: 番号付きログを作る 07

**目的**: ログファイルを作る。

````bash
echo "exp_07 started at $(date)" | tee experiments/exp_07/logs/run.log
````
**解説**: スクリプトからログ保存する感覚を身につけます。

**確認ポイント**: ログに日時が入る。


## Knock 029: 番号付き実験ディレクトリを作る 08

**目的**: 変数を使ってディレクトリを作る。

````bash
EXP=exp_08; mkdir -p experiments/$EXP/logs experiments/$EXP/outputs; echo $EXP
````
**解説**: 手打ちミスを避け、規則的な実験管理をします。

**確認ポイント**: `find experiments/exp_08` で確認。


## Knock 030: 番号付きログを作る 08

**目的**: ログファイルを作る。

````bash
echo "exp_08 started at $(date)" | tee experiments/exp_08/logs/run.log
````
**解説**: スクリプトからログ保存する感覚を身につけます。

**確認ポイント**: ログに日時が入る。


## Knock 031: 番号付き実験ディレクトリを作る 09

**目的**: 変数を使ってディレクトリを作る。

````bash
EXP=exp_09; mkdir -p experiments/$EXP/logs experiments/$EXP/outputs; echo $EXP
````
**解説**: 手打ちミスを避け、規則的な実験管理をします。

**確認ポイント**: `find experiments/exp_09` で確認。


## Knock 032: 番号付きログを作る 09

**目的**: ログファイルを作る。

````bash
echo "exp_09 started at $(date)" | tee experiments/exp_09/logs/run.log
````
**解説**: スクリプトからログ保存する感覚を身につけます。

**確認ポイント**: ログに日時が入る。


## Knock 033: 番号付き実験ディレクトリを作る 10

**目的**: 変数を使ってディレクトリを作る。

````bash
EXP=exp_10; mkdir -p experiments/$EXP/logs experiments/$EXP/outputs; echo $EXP
````
**解説**: 手打ちミスを避け、規則的な実験管理をします。

**確認ポイント**: `find experiments/exp_10` で確認。


## Knock 034: 番号付きログを作る 10

**目的**: ログファイルを作る。

````bash
echo "exp_10 started at $(date)" | tee experiments/exp_10/logs/run.log
````
**解説**: スクリプトからログ保存する感覚を身につけます。

**確認ポイント**: ログに日時が入る。


## Knock 035: 番号付き実験ディレクトリを作る 11

**目的**: 変数を使ってディレクトリを作る。

````bash
EXP=exp_11; mkdir -p experiments/$EXP/logs experiments/$EXP/outputs; echo $EXP
````
**解説**: 手打ちミスを避け、規則的な実験管理をします。

**確認ポイント**: `find experiments/exp_11` で確認。


## Knock 036: 番号付きログを作る 11

**目的**: ログファイルを作る。

````bash
echo "exp_11 started at $(date)" | tee experiments/exp_11/logs/run.log
````
**解説**: スクリプトからログ保存する感覚を身につけます。

**確認ポイント**: ログに日時が入る。


## Knock 037: 番号付き実験ディレクトリを作る 12

**目的**: 変数を使ってディレクトリを作る。

````bash
EXP=exp_12; mkdir -p experiments/$EXP/logs experiments/$EXP/outputs; echo $EXP
````
**解説**: 手打ちミスを避け、規則的な実験管理をします。

**確認ポイント**: `find experiments/exp_12` で確認。


## Knock 038: 番号付きログを作る 12

**目的**: ログファイルを作る。

````bash
echo "exp_12 started at $(date)" | tee experiments/exp_12/logs/run.log
````
**解説**: スクリプトからログ保存する感覚を身につけます。

**確認ポイント**: ログに日時が入る。


## Knock 039: 番号付き実験ディレクトリを作る 13

**目的**: 変数を使ってディレクトリを作る。

````bash
EXP=exp_13; mkdir -p experiments/$EXP/logs experiments/$EXP/outputs; echo $EXP
````
**解説**: 手打ちミスを避け、規則的な実験管理をします。

**確認ポイント**: `find experiments/exp_13` で確認。


## Knock 040: 番号付きログを作る 13

**目的**: ログファイルを作る。

````bash
echo "exp_13 started at $(date)" | tee experiments/exp_13/logs/run.log
````
**解説**: スクリプトからログ保存する感覚を身につけます。

**確認ポイント**: ログに日時が入る。


## Knock 041: 番号付き実験ディレクトリを作る 14

**目的**: 変数を使ってディレクトリを作る。

````bash
EXP=exp_14; mkdir -p experiments/$EXP/logs experiments/$EXP/outputs; echo $EXP
````
**解説**: 手打ちミスを避け、規則的な実験管理をします。

**確認ポイント**: `find experiments/exp_14` で確認。


## Knock 042: 番号付きログを作る 14

**目的**: ログファイルを作る。

````bash
echo "exp_14 started at $(date)" | tee experiments/exp_14/logs/run.log
````
**解説**: スクリプトからログ保存する感覚を身につけます。

**確認ポイント**: ログに日時が入る。


## Knock 043: 番号付き実験ディレクトリを作る 15

**目的**: 変数を使ってディレクトリを作る。

````bash
EXP=exp_15; mkdir -p experiments/$EXP/logs experiments/$EXP/outputs; echo $EXP
````
**解説**: 手打ちミスを避け、規則的な実験管理をします。

**確認ポイント**: `find experiments/exp_15` で確認。


## Knock 044: 番号付きログを作る 15

**目的**: ログファイルを作る。

````bash
echo "exp_15 started at $(date)" | tee experiments/exp_15/logs/run.log
````
**解説**: スクリプトからログ保存する感覚を身につけます。

**確認ポイント**: ログに日時が入る。


## Knock 045: 番号付き実験ディレクトリを作る 16

**目的**: 変数を使ってディレクトリを作る。

````bash
EXP=exp_16; mkdir -p experiments/$EXP/logs experiments/$EXP/outputs; echo $EXP
````
**解説**: 手打ちミスを避け、規則的な実験管理をします。

**確認ポイント**: `find experiments/exp_16` で確認。


## Knock 046: 番号付きログを作る 16

**目的**: ログファイルを作る。

````bash
echo "exp_16 started at $(date)" | tee experiments/exp_16/logs/run.log
````
**解説**: スクリプトからログ保存する感覚を身につけます。

**確認ポイント**: ログに日時が入る。


## Knock 047: 番号付き実験ディレクトリを作る 17

**目的**: 変数を使ってディレクトリを作る。

````bash
EXP=exp_17; mkdir -p experiments/$EXP/logs experiments/$EXP/outputs; echo $EXP
````
**解説**: 手打ちミスを避け、規則的な実験管理をします。

**確認ポイント**: `find experiments/exp_17` で確認。


## Knock 048: 番号付きログを作る 17

**目的**: ログファイルを作る。

````bash
echo "exp_17 started at $(date)" | tee experiments/exp_17/logs/run.log
````
**解説**: スクリプトからログ保存する感覚を身につけます。

**確認ポイント**: ログに日時が入る。


## Knock 049: 番号付き実験ディレクトリを作る 18

**目的**: 変数を使ってディレクトリを作る。

````bash
EXP=exp_18; mkdir -p experiments/$EXP/logs experiments/$EXP/outputs; echo $EXP
````
**解説**: 手打ちミスを避け、規則的な実験管理をします。

**確認ポイント**: `find experiments/exp_18` で確認。


## Knock 050: 番号付きログを作る 18

**目的**: ログファイルを作る。

````bash
echo "exp_18 started at $(date)" | tee experiments/exp_18/logs/run.log
````
**解説**: スクリプトからログ保存する感覚を身につけます。

**確認ポイント**: ログに日時が入る。


## Knock 051: 番号付き実験ディレクトリを作る 19

**目的**: 変数を使ってディレクトリを作る。

````bash
EXP=exp_19; mkdir -p experiments/$EXP/logs experiments/$EXP/outputs; echo $EXP
````
**解説**: 手打ちミスを避け、規則的な実験管理をします。

**確認ポイント**: `find experiments/exp_19` で確認。


## Knock 052: 番号付きログを作る 19

**目的**: ログファイルを作る。

````bash
echo "exp_19 started at $(date)" | tee experiments/exp_19/logs/run.log
````
**解説**: スクリプトからログ保存する感覚を身につけます。

**確認ポイント**: ログに日時が入る。


## Knock 053: 番号付き実験ディレクトリを作る 20

**目的**: 変数を使ってディレクトリを作る。

````bash
EXP=exp_20; mkdir -p experiments/$EXP/logs experiments/$EXP/outputs; echo $EXP
````
**解説**: 手打ちミスを避け、規則的な実験管理をします。

**確認ポイント**: `find experiments/exp_20` で確認。


## Knock 054: 番号付きログを作る 20

**目的**: ログファイルを作る。

````bash
echo "exp_20 started at $(date)" | tee experiments/exp_20/logs/run.log
````
**解説**: スクリプトからログ保存する感覚を身につけます。

**確認ポイント**: ログに日時が入る。


## Knock 055: 番号付き実験ディレクトリを作る 21

**目的**: 変数を使ってディレクトリを作る。

````bash
EXP=exp_21; mkdir -p experiments/$EXP/logs experiments/$EXP/outputs; echo $EXP
````
**解説**: 手打ちミスを避け、規則的な実験管理をします。

**確認ポイント**: `find experiments/exp_21` で確認。


## Knock 056: 番号付きログを作る 21

**目的**: ログファイルを作る。

````bash
echo "exp_21 started at $(date)" | tee experiments/exp_21/logs/run.log
````
**解説**: スクリプトからログ保存する感覚を身につけます。

**確認ポイント**: ログに日時が入る。


## Knock 057: 番号付き実験ディレクトリを作る 22

**目的**: 変数を使ってディレクトリを作る。

````bash
EXP=exp_22; mkdir -p experiments/$EXP/logs experiments/$EXP/outputs; echo $EXP
````
**解説**: 手打ちミスを避け、規則的な実験管理をします。

**確認ポイント**: `find experiments/exp_22` で確認。


## Knock 058: 番号付きログを作る 22

**目的**: ログファイルを作る。

````bash
echo "exp_22 started at $(date)" | tee experiments/exp_22/logs/run.log
````
**解説**: スクリプトからログ保存する感覚を身につけます。

**確認ポイント**: ログに日時が入る。


## Knock 059: 番号付き実験ディレクトリを作る 23

**目的**: 変数を使ってディレクトリを作る。

````bash
EXP=exp_23; mkdir -p experiments/$EXP/logs experiments/$EXP/outputs; echo $EXP
````
**解説**: 手打ちミスを避け、規則的な実験管理をします。

**確認ポイント**: `find experiments/exp_23` で確認。


## Knock 060: 番号付きログを作る 23

**目的**: ログファイルを作る。

````bash
echo "exp_23 started at $(date)" | tee experiments/exp_23/logs/run.log
````
**解説**: スクリプトからログ保存する感覚を身につけます。

**確認ポイント**: ログに日時が入る。


## Knock 061: 番号付き実験ディレクトリを作る 24

**目的**: 変数を使ってディレクトリを作る。

````bash
EXP=exp_24; mkdir -p experiments/$EXP/logs experiments/$EXP/outputs; echo $EXP
````
**解説**: 手打ちミスを避け、規則的な実験管理をします。

**確認ポイント**: `find experiments/exp_24` で確認。


## Knock 062: 番号付きログを作る 24

**目的**: ログファイルを作る。

````bash
echo "exp_24 started at $(date)" | tee experiments/exp_24/logs/run.log
````
**解説**: スクリプトからログ保存する感覚を身につけます。

**確認ポイント**: ログに日時が入る。


## Knock 063: 番号付き実験ディレクトリを作る 25

**目的**: 変数を使ってディレクトリを作る。

````bash
EXP=exp_25; mkdir -p experiments/$EXP/logs experiments/$EXP/outputs; echo $EXP
````
**解説**: 手打ちミスを避け、規則的な実験管理をします。

**確認ポイント**: `find experiments/exp_25` で確認。


## Knock 064: 番号付きログを作る 25

**目的**: ログファイルを作る。

````bash
echo "exp_25 started at $(date)" | tee experiments/exp_25/logs/run.log
````
**解説**: スクリプトからログ保存する感覚を身につけます。

**確認ポイント**: ログに日時が入る。


## Knock 065: 番号付き実験ディレクトリを作る 26

**目的**: 変数を使ってディレクトリを作る。

````bash
EXP=exp_26; mkdir -p experiments/$EXP/logs experiments/$EXP/outputs; echo $EXP
````
**解説**: 手打ちミスを避け、規則的な実験管理をします。

**確認ポイント**: `find experiments/exp_26` で確認。


## Knock 066: 番号付きログを作る 26

**目的**: ログファイルを作る。

````bash
echo "exp_26 started at $(date)" | tee experiments/exp_26/logs/run.log
````
**解説**: スクリプトからログ保存する感覚を身につけます。

**確認ポイント**: ログに日時が入る。


## Knock 067: 番号付き実験ディレクトリを作る 27

**目的**: 変数を使ってディレクトリを作る。

````bash
EXP=exp_27; mkdir -p experiments/$EXP/logs experiments/$EXP/outputs; echo $EXP
````
**解説**: 手打ちミスを避け、規則的な実験管理をします。

**確認ポイント**: `find experiments/exp_27` で確認。


## Knock 068: 番号付きログを作る 27

**目的**: ログファイルを作る。

````bash
echo "exp_27 started at $(date)" | tee experiments/exp_27/logs/run.log
````
**解説**: スクリプトからログ保存する感覚を身につけます。

**確認ポイント**: ログに日時が入る。


## Knock 069: 番号付き実験ディレクトリを作る 28

**目的**: 変数を使ってディレクトリを作る。

````bash
EXP=exp_28; mkdir -p experiments/$EXP/logs experiments/$EXP/outputs; echo $EXP
````
**解説**: 手打ちミスを避け、規則的な実験管理をします。

**確認ポイント**: `find experiments/exp_28` で確認。


## Knock 070: 番号付きログを作る 28

**目的**: ログファイルを作る。

````bash
echo "exp_28 started at $(date)" | tee experiments/exp_28/logs/run.log
````
**解説**: スクリプトからログ保存する感覚を身につけます。

**確認ポイント**: ログに日時が入る。


## Knock 071: 番号付き実験ディレクトリを作る 29

**目的**: 変数を使ってディレクトリを作る。

````bash
EXP=exp_29; mkdir -p experiments/$EXP/logs experiments/$EXP/outputs; echo $EXP
````
**解説**: 手打ちミスを避け、規則的な実験管理をします。

**確認ポイント**: `find experiments/exp_29` で確認。


## Knock 072: 番号付きログを作る 29

**目的**: ログファイルを作る。

````bash
echo "exp_29 started at $(date)" | tee experiments/exp_29/logs/run.log
````
**解説**: スクリプトからログ保存する感覚を身につけます。

**確認ポイント**: ログに日時が入る。


## Knock 073: 番号付き実験ディレクトリを作る 30

**目的**: 変数を使ってディレクトリを作る。

````bash
EXP=exp_30; mkdir -p experiments/$EXP/logs experiments/$EXP/outputs; echo $EXP
````
**解説**: 手打ちミスを避け、規則的な実験管理をします。

**確認ポイント**: `find experiments/exp_30` で確認。


## Knock 074: 番号付きログを作る 30

**目的**: ログファイルを作る。

````bash
echo "exp_30 started at $(date)" | tee experiments/exp_30/logs/run.log
````
**解説**: スクリプトからログ保存する感覚を身につけます。

**確認ポイント**: ログに日時が入る。


## Knock 075: 関数を書く

**目的**: bash関数を使う。

````bash
cat > scripts/function.sh <<'EOF
#!/usr/bin/env bash
log(){ echo "[$(date +%H:%M:%S)] $*"; }
log "start"
log "finish"
EOF
chmod +x scripts/function.sh && ./scripts/function.sh
````
**解説**: 繰り返し使う処理は関数化できます。

**確認ポイント**: 時刻付きログが出る。


## Knock 076: usageを表示する

**目的**: 使い方メッセージを書く。

````bash
cat > scripts/usage.sh <<'EOF
#!/usr/bin/env bash
if [ $# -lt 1 ]; then
  echo "Usage: $0 EXP_NAME"
  exit 1
fi
echo "exp=$1"
EOF
chmod +x scripts/usage.sh; ./scripts/usage.sh || true
````
**解説**: 引数不足時に分かりやすく失敗させます。

**確認ポイント**: Usageが出る。


## Knock 077: case文を書く

**目的**: サブコマンド風に分岐する。

````bash
cat > scripts/case.sh <<'EOF
#!/usr/bin/env bash
case "${1:-}" in
  train) echo training ;;
  eval) echo evaluating ;;
  *) echo "Usage: $0 {train|eval}"; exit 1 ;;
esac
EOF
chmod +x scripts/case.sh && ./scripts/case.sh train
````
**解説**: run.sh train / run.sh eval のような形が作れます。

**確認ポイント**: trainingが出る。


## Knock 078: trapで終了処理を書く

**目的**: 終了時処理を登録する。

````bash
cat > scripts/trap.sh <<'EOF
#!/usr/bin/env bash
trap 'echo "cleanup"' EXIT
echo "main"
EOF
chmod +x scripts/trap.sh && ./scripts/trap.sh
````
**解説**: 一時ファイル削除やログ出力に使えます。

**確認ポイント**: main後にcleanupが出る。


## Knock 079: mktempを使う

**目的**: 安全な一時ファイルを作る。

````bash
tmpfile=$(mktemp); echo hello > $tmpfile; cat $tmpfile; rm $tmpfile
````
**解説**: 固定名tmpは衝突するのでmktempが安全です。

**確認ポイント**: helloが出る。


## Knock 080: shellcheck前提確認

**目的**: スクリプト静的解析ツールを確認する。

````bash
command -v shellcheck || echo "shellcheck not installed"
````
**解説**: 入っていればbashのミスを検出できます。

**確認ポイント**: パスまたは未導入表示。


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

