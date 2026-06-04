# Docker慎重入門100本ノック — 実践編

## 位置づけ

Dockerを怖がらず、容量・コンテナ・イメージを見ながら安全に扱う。

- 入門編: まず壊さず、意味を確認しながら手を動かす。
- 実践編: 研究実務で使う形に近づける。

## 使い方

1. まず各Knockのコマンドを読む。
2. 練習用ディレクトリで実行する。
3. 解説と確認ポイントを見て、何が起きたか確認する。

注意: `myserver`, `your_username`, `git@example.com:USER/REPO.git` などは仮の名前です。実環境に合わせて置き換えてください。

## Knock 001: Dockerがあるか確認する

**目的**: Docker利用可否を確認する。

````bash
command -v docker || echo "docker not installed"
````
**解説**: 会社PCではインストールや起動権限が制限されることがあります。

**確認ポイント**: パスまたは未導入表示。


## Knock 002: Dockerバージョンを見る

**目的**: Docker CLIのバージョンを見る。

````bash
docker --version
````
**解説**: まずCLIが動くか確認します。

**確認ポイント**: Docker versionが出る。


## Knock 003: Docker daemon疎通確認

**目的**: Docker本体が起動しているか確認する。

````bash
docker info | head -n 20
````
**解説**: CLIがあってもdaemonが止まっていると使えません。

**確認ポイント**: 情報または接続エラーが出る。


## Knock 004: イメージ一覧を見る

**目的**: ローカルのDockerイメージを見る。

````bash
docker images
````
**解説**: イメージはディスク容量を食います。

**確認ポイント**: 一覧が出る。


## Knock 005: コンテナ一覧を見る

**目的**: 動いているコンテナを見る。

````bash
docker ps
````
**解説**: メモリやCPUを使うのは主に実行中コンテナです。

**確認ポイント**: 一覧が出る。


## Knock 006: 停止中も含めて見る

**目的**: 過去に作ったコンテナも見る。

````bash
docker ps -a
````
**解説**: 停止コンテナもディスクを使います。

**確認ポイント**: 全コンテナ一覧が出る。


## Knock 007: 容量を見る

**目的**: Dockerが使う容量を見る。

````bash
docker system df
````
**解説**: Dockerへの苦手意識があるなら最重要コマンドです。

**確認ポイント**: Images/Containers/Volumesの容量が出る。


## Knock 008: Dockerfile用ディレクトリを作る

**目的**: Dockerビルド練習場所を作る。

````bash
mkdir -p ~/docker100app && cd ~/docker100app
````
**解説**: 実プロジェクトから分けて練習します。

**確認ポイント**: 作業場所ができる。


## Knock 009: 最小Dockerfileを作る

**目的**: Python入りイメージ定義を書く。

````bash
cat > Dockerfile <<EOF
FROM python:3.11-slim
WORKDIR /app
CMD ["python", "--version"]
EOF
````
**解説**: Dockerfileは環境のレシピです。

**確認ポイント**: `cat Dockerfile` で確認。


## Knock 010: イメージをビルドする

**目的**: Dockerfileからイメージを作る。

````bash
docker build -t ubuntu100-python:0.1 .
````
**解説**: タグ名を付けると管理しやすいです。

**確認ポイント**: Successfully builtが出る。


## Knock 011: 作ったイメージを実行する

**目的**: 自作イメージを実行する。

````bash
docker run --rm ubuntu100-python:0.1
````
**解説**: DockerfileのCMDが実行されます。

**確認ポイント**: Pythonバージョンが出る。


## Knock 012: app.pyを作る

**目的**: コンテナで動かすアプリを作る。

````bash
cat > app.py <<EOF
print("hello from container app")
EOF
````
**解説**: ホストのファイルをイメージに含める練習です。

**確認ポイント**: app.pyができる。


## Knock 013: COPY入りDockerfileにする

**目的**: ファイルをイメージ内へコピーする。

````bash
cat > Dockerfile <<EOF
FROM python:3.11-slim
WORKDIR /app
COPY app.py /app/app.py
CMD ["python", "app.py"]
EOF
````
**解説**: COPYでビルド時にファイルを取り込みます。

**確認ポイント**: Dockerfileを確認。


## Knock 014: 再ビルドする

**目的**: 更新したDockerfileでビルドする。

````bash
docker build -t ubuntu100-python:0.2 .
````
**解説**: タグを変えると比較しやすいです。

**確認ポイント**: ビルド成功。


## Knock 015: 再実行する

**目的**: app.pyをコンテナ内で実行する。

````bash
docker run --rm ubuntu100-python:0.2
````
**解説**: 環境を固定してアプリを動かせます。

**確認ポイント**: helloが出る。


## Knock 016: ビルドコンテキストを確認

**目的**: ビルドに送るディレクトリサイズを確認する。

````bash
du -sh .
````
**解説**: 不要な巨大ファイルがあるとビルドが遅くなります。

**確認ポイント**: 容量が表示される。


## Knock 017: .dockerignoreを作る

**目的**: ビルド対象から除外する。

````bash
cat > .dockerignore <<EOF
.venv
__pycache__
outputs
logs
.git
EOF
````
**解説**: Dockerの容量・速度対策で重要です。

**確認ポイント**: .dockerignoreを確認。


## Knock 018: タグ 0.3 でビルドする

**目的**: タグ運用に慣れる。

````bash
docker build -t ubuntu100-python:0.3 .
````
**解説**: 実験環境はタグで区別すると便利です。

**確認ポイント**: `docker images ubuntu100-python` で0.3確認。


## Knock 019: タグ 0.4 でビルドする

**目的**: タグ運用に慣れる。

````bash
docker build -t ubuntu100-python:0.4 .
````
**解説**: 実験環境はタグで区別すると便利です。

**確認ポイント**: `docker images ubuntu100-python` で0.4確認。


## Knock 020: タグ debug でビルドする

**目的**: タグ運用に慣れる。

````bash
docker build -t ubuntu100-python:debug .
````
**解説**: 実験環境はタグで区別すると便利です。

**確認ポイント**: `docker images ubuntu100-python` でdebug確認。


## Knock 021: タグ cpu でビルドする

**目的**: タグ運用に慣れる。

````bash
docker build -t ubuntu100-python:cpu .
````
**解説**: 実験環境はタグで区別すると便利です。

**確認ポイント**: `docker images ubuntu100-python` でcpu確認。


## Knock 022: タグ slim でビルドする

**目的**: タグ運用に慣れる。

````bash
docker build -t ubuntu100-python:slim .
````
**解説**: 実験環境はタグで区別すると便利です。

**確認ポイント**: `docker images ubuntu100-python` でslim確認。


## Knock 023: タグ latest でビルドする

**目的**: タグ運用に慣れる。

````bash
docker build -t ubuntu100-python:latest .
````
**解説**: 実験環境はタグで区別すると便利です。

**確認ポイント**: `docker images ubuntu100-python` でlatest確認。


## Knock 024: 環境変数 EXP=debug を渡す

**目的**: コンテナに環境変数を渡す。

````bash
docker run --rm -e EXP=debug ubuntu100-python:0.2 bash -lc "env | grep EXP"
````
**解説**: 実験設定やログ設定を外から注入できます。

**確認ポイント**: 変数が表示される。


## Knock 025: 環境変数 SEED=42 を渡す

**目的**: コンテナに環境変数を渡す。

````bash
docker run --rm -e SEED=42 ubuntu100-python:0.2 bash -lc "env | grep SEED"
````
**解説**: 実験設定やログ設定を外から注入できます。

**確認ポイント**: 変数が表示される。


## Knock 026: 環境変数 CUDA_VISIBLE_DEVICES=0 を渡す

**目的**: コンテナに環境変数を渡す。

````bash
docker run --rm -e CUDA_VISIBLE_DEVICES=0 ubuntu100-python:0.2 bash -lc "env | grep CUDA_VISIBLE_DEVICES"
````
**解説**: 実験設定やログ設定を外から注入できます。

**確認ポイント**: 変数が表示される。


## Knock 027: 環境変数 LOG_LEVEL=INFO を渡す

**目的**: コンテナに環境変数を渡す。

````bash
docker run --rm -e LOG_LEVEL=INFO ubuntu100-python:0.2 bash -lc "env | grep LOG_LEVEL"
````
**解説**: 実験設定やログ設定を外から注入できます。

**確認ポイント**: 変数が表示される。


## Knock 028: 環境変数 PYTHONUNBUFFERED=1 を渡す

**目的**: コンテナに環境変数を渡す。

````bash
docker run --rm -e PYTHONUNBUFFERED=1 ubuntu100-python:0.2 bash -lc "env | grep PYTHONUNBUFFERED"
````
**解説**: 実験設定やログ設定を外から注入できます。

**確認ポイント**: 変数が表示される。


## Knock 029: dataをマウントする

**目的**: ホストディレクトリをコンテナへ見せる。

````bash
mkdir -p data && docker run --rm -v "$PWD/data:/work/data" ubuntu:22.04 ls -ld /work/data
````
**解説**: データや出力をコンテナ外に残すために重要です。

**確認ポイント**: マウント先が表示される。


## Knock 030: outputsをマウントする

**目的**: ホストディレクトリをコンテナへ見せる。

````bash
mkdir -p outputs && docker run --rm -v "$PWD/outputs:/work/outputs" ubuntu:22.04 ls -ld /work/outputs
````
**解説**: データや出力をコンテナ外に残すために重要です。

**確認ポイント**: マウント先が表示される。


## Knock 031: logsをマウントする

**目的**: ホストディレクトリをコンテナへ見せる。

````bash
mkdir -p logs && docker run --rm -v "$PWD/logs:/work/logs" ubuntu:22.04 ls -ld /work/logs
````
**解説**: データや出力をコンテナ外に残すために重要です。

**確認ポイント**: マウント先が表示される。


## Knock 032: configsをマウントする

**目的**: ホストディレクトリをコンテナへ見せる。

````bash
mkdir -p configs && docker run --rm -v "$PWD/configs:/work/configs" ubuntu:22.04 ls -ld /work/configs
````
**解説**: データや出力をコンテナ外に残すために重要です。

**確認ポイント**: マウント先が表示される。


## Knock 033: tmpをマウントする

**目的**: ホストディレクトリをコンテナへ見せる。

````bash
mkdir -p tmp && docker run --rm -v "$PWD/tmp:/work/tmp" ubuntu:22.04 ls -ld /work/tmp
````
**解説**: データや出力をコンテナ外に残すために重要です。

**確認ポイント**: マウント先が表示される。


## Knock 034: 実用確認: docker ps --format "table {{.N

**目的**: Docker状態を読みやすく確認する。

````bash
docker ps --format "table {{.Names}}	{{.Status}}	{{.Ports}}"
````
**解説**: 容量・状態・履歴を読めると安心して使えます。

**確認ポイント**: 表やJSONが出る。


## Knock 035: 実用確認: docker images --format "table 

**目的**: Docker状態を読みやすく確認する。

````bash
docker images --format "table {{.Repository}}	{{.Tag}}	{{.Size}}"
````
**解説**: 容量・状態・履歴を読めると安心して使えます。

**確認ポイント**: 表やJSONが出る。


## Knock 036: 実用確認: docker system df -v

**目的**: Docker状態を読みやすく確認する。

````bash
docker system df -v
````
**解説**: 容量・状態・履歴を読めると安心して使えます。

**確認ポイント**: 表やJSONが出る。


## Knock 037: 実用確認: docker stats --no-stream

**目的**: Docker状態を読みやすく確認する。

````bash
docker stats --no-stream
````
**解説**: 容量・状態・履歴を読めると安心して使えます。

**確認ポイント**: 表やJSONが出る。


## Knock 038: 実用確認: docker inspect ubuntu100-pytho

**目的**: Docker状態を読みやすく確認する。

````bash
docker inspect ubuntu100-python:0.2 | head -n 40
````
**解説**: 容量・状態・履歴を読めると安心して使えます。

**確認ポイント**: 表やJSONが出る。


## Knock 039: 実用確認: docker history ubuntu100-pytho

**目的**: Docker状態を読みやすく確認する。

````bash
docker history ubuntu100-python:0.2
````
**解説**: 容量・状態・履歴を読めると安心して使えます。

**確認ポイント**: 表やJSONが出る。


## Knock 040: 掃除の予行演習: container

**目的**: 削除前に何が消えるか確認する。

````bash
docker container prune --dry-run 2>/dev/null || echo "dry-run unsupported"
````
**解説**: Docker掃除は慎重に。まずdry-runやhelpで確認します。

**確認ポイント**: 削除候補または非対応表示。


## Knock 041: 掃除の予行演習: image

**目的**: 削除前に何が消えるか確認する。

````bash
docker image prune --dry-run 2>/dev/null || echo "dry-run unsupported"
````
**解説**: Docker掃除は慎重に。まずdry-runやhelpで確認します。

**確認ポイント**: 削除候補または非対応表示。


## Knock 042: 掃除の予行演習: builder

**目的**: 削除前に何が消えるか確認する。

````bash
docker builder prune --dry-run 2>/dev/null || echo "dry-run unsupported"
````
**解説**: Docker掃除は慎重に。まずdry-runやhelpで確認します。

**確認ポイント**: 削除候補または非対応表示。


## Knock 043: 掃除の予行演習: system

**目的**: 削除前に何が消えるか確認する。

````bash
docker system prune --dry-run 2>/dev/null || echo "dry-run unsupported"
````
**解説**: Docker掃除は慎重に。まずdry-runやhelpで確認します。

**確認ポイント**: 削除候補または非対応表示。


## Knock 044: コンテナ実験名を付けて実行 01

**目的**: 名前付き一時コンテナを動かす。

````bash
docker run --rm --name exp_container_01 ubuntu:22.04 bash -lc "echo exp_container_01"
````
**解説**: ログやpsで区別しやすくなります。

**確認ポイント**: exp_container_01が出る。


## Knock 045: コンテナ実験名を付けて実行 02

**目的**: 名前付き一時コンテナを動かす。

````bash
docker run --rm --name exp_container_02 ubuntu:22.04 bash -lc "echo exp_container_02"
````
**解説**: ログやpsで区別しやすくなります。

**確認ポイント**: exp_container_02が出る。


## Knock 046: コンテナ実験名を付けて実行 03

**目的**: 名前付き一時コンテナを動かす。

````bash
docker run --rm --name exp_container_03 ubuntu:22.04 bash -lc "echo exp_container_03"
````
**解説**: ログやpsで区別しやすくなります。

**確認ポイント**: exp_container_03が出る。


## Knock 047: コンテナ実験名を付けて実行 04

**目的**: 名前付き一時コンテナを動かす。

````bash
docker run --rm --name exp_container_04 ubuntu:22.04 bash -lc "echo exp_container_04"
````
**解説**: ログやpsで区別しやすくなります。

**確認ポイント**: exp_container_04が出る。


## Knock 048: コンテナ実験名を付けて実行 05

**目的**: 名前付き一時コンテナを動かす。

````bash
docker run --rm --name exp_container_05 ubuntu:22.04 bash -lc "echo exp_container_05"
````
**解説**: ログやpsで区別しやすくなります。

**確認ポイント**: exp_container_05が出る。


## Knock 049: コンテナ実験名を付けて実行 06

**目的**: 名前付き一時コンテナを動かす。

````bash
docker run --rm --name exp_container_06 ubuntu:22.04 bash -lc "echo exp_container_06"
````
**解説**: ログやpsで区別しやすくなります。

**確認ポイント**: exp_container_06が出る。


## Knock 050: コンテナ実験名を付けて実行 07

**目的**: 名前付き一時コンテナを動かす。

````bash
docker run --rm --name exp_container_07 ubuntu:22.04 bash -lc "echo exp_container_07"
````
**解説**: ログやpsで区別しやすくなります。

**確認ポイント**: exp_container_07が出る。


## Knock 051: コンテナ実験名を付けて実行 08

**目的**: 名前付き一時コンテナを動かす。

````bash
docker run --rm --name exp_container_08 ubuntu:22.04 bash -lc "echo exp_container_08"
````
**解説**: ログやpsで区別しやすくなります。

**確認ポイント**: exp_container_08が出る。


## Knock 052: コンテナ実験名を付けて実行 09

**目的**: 名前付き一時コンテナを動かす。

````bash
docker run --rm --name exp_container_09 ubuntu:22.04 bash -lc "echo exp_container_09"
````
**解説**: ログやpsで区別しやすくなります。

**確認ポイント**: exp_container_09が出る。


## Knock 053: コンテナ実験名を付けて実行 10

**目的**: 名前付き一時コンテナを動かす。

````bash
docker run --rm --name exp_container_10 ubuntu:22.04 bash -lc "echo exp_container_10"
````
**解説**: ログやpsで区別しやすくなります。

**確認ポイント**: exp_container_10が出る。


## Knock 054: コンテナ実験名を付けて実行 11

**目的**: 名前付き一時コンテナを動かす。

````bash
docker run --rm --name exp_container_11 ubuntu:22.04 bash -lc "echo exp_container_11"
````
**解説**: ログやpsで区別しやすくなります。

**確認ポイント**: exp_container_11が出る。


## Knock 055: コンテナ実験名を付けて実行 12

**目的**: 名前付き一時コンテナを動かす。

````bash
docker run --rm --name exp_container_12 ubuntu:22.04 bash -lc "echo exp_container_12"
````
**解説**: ログやpsで区別しやすくなります。

**確認ポイント**: exp_container_12が出る。


## Knock 056: コンテナ実験名を付けて実行 13

**目的**: 名前付き一時コンテナを動かす。

````bash
docker run --rm --name exp_container_13 ubuntu:22.04 bash -lc "echo exp_container_13"
````
**解説**: ログやpsで区別しやすくなります。

**確認ポイント**: exp_container_13が出る。


## Knock 057: コンテナ実験名を付けて実行 14

**目的**: 名前付き一時コンテナを動かす。

````bash
docker run --rm --name exp_container_14 ubuntu:22.04 bash -lc "echo exp_container_14"
````
**解説**: ログやpsで区別しやすくなります。

**確認ポイント**: exp_container_14が出る。


## Knock 058: コンテナ実験名を付けて実行 15

**目的**: 名前付き一時コンテナを動かす。

````bash
docker run --rm --name exp_container_15 ubuntu:22.04 bash -lc "echo exp_container_15"
````
**解説**: ログやpsで区別しやすくなります。

**確認ポイント**: exp_container_15が出る。


## Knock 059: コンテナ実験名を付けて実行 16

**目的**: 名前付き一時コンテナを動かす。

````bash
docker run --rm --name exp_container_16 ubuntu:22.04 bash -lc "echo exp_container_16"
````
**解説**: ログやpsで区別しやすくなります。

**確認ポイント**: exp_container_16が出る。


## Knock 060: コンテナ実験名を付けて実行 17

**目的**: 名前付き一時コンテナを動かす。

````bash
docker run --rm --name exp_container_17 ubuntu:22.04 bash -lc "echo exp_container_17"
````
**解説**: ログやpsで区別しやすくなります。

**確認ポイント**: exp_container_17が出る。


## Knock 061: コンテナ実験名を付けて実行 18

**目的**: 名前付き一時コンテナを動かす。

````bash
docker run --rm --name exp_container_18 ubuntu:22.04 bash -lc "echo exp_container_18"
````
**解説**: ログやpsで区別しやすくなります。

**確認ポイント**: exp_container_18が出る。


## Knock 062: コンテナ実験名を付けて実行 19

**目的**: 名前付き一時コンテナを動かす。

````bash
docker run --rm --name exp_container_19 ubuntu:22.04 bash -lc "echo exp_container_19"
````
**解説**: ログやpsで区別しやすくなります。

**確認ポイント**: exp_container_19が出る。


## Knock 063: コンテナ実験名を付けて実行 20

**目的**: 名前付き一時コンテナを動かす。

````bash
docker run --rm --name exp_container_20 ubuntu:22.04 bash -lc "echo exp_container_20"
````
**解説**: ログやpsで区別しやすくなります。

**確認ポイント**: exp_container_20が出る。


## Knock 064: 総復習チェック 064

**目的**: その領域の練習前後で現在地・時刻・ファイル状態を確認する。

````bash
pwd && date && ls -lah | head
````
**解説**: 初心者ほど、現在地と対象ファイルを確認する癖が重要です。迷ったらまずこの確認セットに戻ります。

**確認ポイント**: 現在地、日時、ファイル一覧の先頭が表示される。


## Knock 065: 総復習チェック 065

**目的**: その領域の練習前後で現在地・時刻・ファイル状態を確認する。

````bash
pwd && date && ls -lah | head
````
**解説**: 初心者ほど、現在地と対象ファイルを確認する癖が重要です。迷ったらまずこの確認セットに戻ります。

**確認ポイント**: 現在地、日時、ファイル一覧の先頭が表示される。


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

