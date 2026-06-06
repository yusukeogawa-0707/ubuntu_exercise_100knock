# Ubuntu CLI 100Knock Series

研究実装者向けの Ubuntu / Linux CLI 練習リポジトリです。

## 最初に環境を作る

Windows PC 1台だけでも始められるように、WSL Ubuntu前提のセットアップ手順と、ローカル練習用データ作成スクリプトを用意しています。研究サーバやSSH接続先がない場合は、まずローカルで入門編を進め、`myserver` が出る実践Knockは後回しにしてください。

```bash
bash scripts/setup_local_practice_env.sh
cd ~/ubuntu100knock
```

詳しくは [`docs/setup_windows_single_pc.md`](docs/setup_windows_single_pc.md) を参照してください。

## 構成方針

このリポジトリは、**領域（分野）ごとのディレクトリ**に整理しています。
各領域の中には、次の2本を置きます。

- `intro_100knock.md`：入門編。まず壊さず、意味を確認しながら手を動かす。
- `practice_100knock.md`：実践編。研究実務で使う形に近づける。

## ディレクトリ構成

| 領域 | 入門編 | 実践編 |
|---|---|---|
| Ubuntu CLI基礎 | [`cli_foundation/intro_100knock.md`](cli_foundation/intro_100knock.md) | [`cli_foundation/practice_100knock.md`](cli_foundation/practice_100knock.md) |
| Python研究環境 | [`python_env/intro_100knock.md`](python_env/intro_100knock.md) | [`python_env/practice_100knock.md`](python_env/practice_100knock.md) |
| Git | [`git/intro_100knock.md`](git/intro_100knock.md) | [`git/practice_100knock.md`](git/practice_100knock.md) |
| シェルスクリプト | [`shell/intro_100knock.md`](shell/intro_100knock.md) | [`shell/practice_100knock.md`](shell/practice_100knock.md) |
| Linux権限・トラブルシュート | [`permissions/intro_100knock.md`](permissions/intro_100knock.md) | [`permissions/practice_100knock.md`](permissions/practice_100knock.md) |
| Docker | [`docker/intro_100knock.md`](docker/intro_100knock.md) | [`docker/practice_100knock.md`](docker/practice_100knock.md) |
| ネットワーク・SSH | [`network/intro_100knock.md`](network/intro_100knock.md) | [`network/practice_100knock.md`](network/practice_100knock.md) |
| ジョブ管理・長時間実験 | [`jobs/intro_100knock.md`](jobs/intro_100knock.md) | [`jobs/practice_100knock.md`](jobs/practice_100knock.md) |
| 圧縮・バックアップ・cron | [`archive_cron/intro_100knock.md`](archive_cron/intro_100knock.md) | [`archive_cron/practice_100knock.md`](archive_cron/practice_100knock.md) |

補助ファイル：

- `00_ALL_KNOCK_INDEX.md`：全領域・全Knockの索引。
- `manifest.json`：領域、入門編・実践編、Knock数の機械可読な一覧。
- `progress/`：3周するための進捗管理。
- `cheatsheets/`：重要コマンドの早見表。
- `docs/setup_windows_single_pc.md`：Windows PC 1台から始めるためのWSL・ローカル練習環境ガイド。
- `scripts/setup_local_practice_env.sh`：CSV、ログ、Pythonスクリプト、擬似サーバ用ディレクトリを作るローカル練習環境セットアップ。

## 推奨学習順

1. `cli_foundation/intro_100knock.md` でローカルCLIの基礎を固める。
2. `cli_foundation/practice_100knock.md` で研究サーバSSH実務の土台を作る。
3. `python_env/intro_100knock.md`、`git/intro_100knock.md`、`shell/intro_100knock.md` に進む。
4. 必要に応じて `permissions/`、`network/`、`jobs/`、`archive_cron/`、`docker/` の入門編を進める。
5. 各領域の `practice_100knock.md` に進み、実務に近い形で反復する。


## 問題・解答・解説の品質方針

各Knockは、単にコマンドを並べるだけではなく、**なぜそのコマンドを使うのか**まで学べる形を目指します。特に解説は次の要素を含める方針です。

- **コマンドの役割**：何を確認・作成・検索・転送するための操作なのか。
- **主要オプションの意味**：例：`grep -c` の `-c` は count、`grep -B 3` の `-B` は before、`rsync -avP` の `-a`/`-v`/`-P` は属性保持・詳細表示・進捗/再開。
- **使う場面**：ログ調査、研究データ転送、リモートサーバ状態確認、実験結果回収など、研究・開発実務でどう役立つか。
- **次に試す派生形**：必要に応じて `tail -f`、`tail -n 50`、`grep -A`、`--dry-run` のような発展操作へつなげる。

## GitHubに置く手順

```bash
cd ubuntu-cli-100knock
git init
git add .
git commit -m "initial commit: add ubuntu cli 100knock series"
```

GitHubで空リポジトリを作った後：

```bash
git remote add origin https://github.com/YOUR_NAME/ubuntu-cli-100knock.git
git branch -M main
git push -u origin main
```

## 日々の進捗更新

```bash
git add progress/
git commit -m "study: update progress"
git push
```
