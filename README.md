# Ubuntu CLI 100Knock Series

研究実装者向けの Ubuntu / Linux CLI 練習リポジトリです。

## 構成

- `v0_foundation/`：最初に作った2本。CLI基礎と研究サーバSSH実務の土台。
- `v1_intro/`：各領域の入門編。
- `v2_practice/`：各領域の応用・実践編。
- `progress/`：3周するための進捗管理。

## 推奨学習順

1. `v0_foundation/local_cli_v0_100knock.md`
2. `v0_foundation/server_cli_v0_100knock.md`
3. `v1_intro/python_env_v1_100knock.md`
4. `v1_intro/git_v1_100knock.md`
5. `v1_intro/shell_v1_100knock.md`
6. 必要に応じて `permissions`, `network`, `jobs`, `archive_cron`, `docker`
7. 対応する `v2_practice/` に進む

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
