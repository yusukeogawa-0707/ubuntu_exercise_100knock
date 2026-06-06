# Windows PC 1台から始める環境準備

この教材は Ubuntu / Linux CLI の練習用ですが、最初から研究サーバ、SSH接続先、GPU環境、Docker環境がそろっている前提にはしません。手元に Windows PC が1台だけある場合は、まず **WSL上のUbuntuだけでローカル練習**を始め、サーバが必要なKnockは後回しにします。

## 0. まず決めること

| 状況 | 進め方 |
|---|---|
| Windows PC 1台だけ | WSLのUbuntuを入れて、ローカルで `intro_100knock.md` から進める |
| SSH先サーバがない | `myserver` が出るKnockは「サーバ必須」として後回しにする |
| 操作用データがない | `scripts/setup_local_practice_env.sh` で練習用データを作る |
| Docker/GPUがない | Docker/GPU系Knockは読んで意味を確認し、環境ができてから実行する |

## 1. WindowsにWSL Ubuntuを用意する

PowerShellを管理者権限で開き、WSLをセットアップします。

```powershell
wsl --install -d Ubuntu
```

インストール後、Ubuntuを起動してユーザー名とパスワードを設定します。以降のKnockは、原則として **WindowsのPowerShellではなく、WSLのUbuntuターミナル**で実行します。

## 2. 最低限のツールを入れる

Ubuntuターミナルで次を実行します。

```bash
sudo apt update
sudo apt install -y git curl wget rsync python3 python3-venv
```

SSHクライアントは通常入っていますが、なければ次を入れます。

```bash
sudo apt install -y openssh-client
```

## 3. 教材リポジトリを置く

```bash
mkdir -p ~/work
cd ~/work
git clone <このリポジトリのURL> ubuntu_exercise_100knock
cd ubuntu_exercise_100knock
```

まだGitHub上のURLがない場合は、ZIPを展開して `cd` しても構いません。

## 4. 練習用データを作る

このリポジトリには、ローカル練習に必要なディレクトリとサンプルデータを作るスクリプトを用意しています。

```bash
bash scripts/setup_local_practice_env.sh
cd ~/ubuntu100knock
```

作成される主なものは次の通りです。

- `data/members.csv`：CSV操作、`cut`、`sort`、`awk` などの練習用
- `logs/app.log`：`tail`、`grep`、ログ調査の練習用
- `data/metrics.jsonl`：JSONL形式の実験結果を想定した練習用
- `src/train.py`：Python実行、リダイレクト、ログ保存の練習用
- `notes/research.md`：コピーや転送コマンドの練習用
- `mock_server/`：SSH先がないときに、転送先サーバの代わりとして使うローカルディレクトリ

## 5. 最初に実行するKnock

最初はサーバ不要の範囲だけで十分です。

```bash
cd ~/ubuntu100knock
```

そのうえで、教材リポジトリ側の次のファイルを見ながら進めます。

1. `cli_foundation/intro_100knock.md`
2. `python_env/intro_100knock.md`
3. `git/intro_100knock.md`
4. `shell/intro_100knock.md`

## 6. `myserver` が出るKnockの扱い

`ssh myserver ...` や `rsync ... myserver:...` は、実際の研究サーバやSSH接続先がある人向けです。Windows PC 1台だけの段階では、無理に実行しなくて構いません。

| 教材内の例 | SSH先がないときの練習方法 |
|---|---|
| `ssh myserver "hostname && pwd && free -h"` | `hostname && pwd && free -h` をローカルで実行して、コマンド連結と確認項目を学ぶ |
| `rsync -avP data/ myserver:~/ubuntu100_data_rsync/` | `rsync -avP data/ ~/ubuntu100knock/mock_server/ubuntu100_data_rsync/` でローカル同期を練習する |
| `scp notes/research.md myserver:~/research.md` | `cp notes/research.md mock_server/research.md` でコピー元・コピー先の考え方だけ先に練習する |
| `ssh myserver "tail -n 50 ..."` | ローカルの `tail -n 50 logs/app.log` でログ確認の型を練習する |

ポイントは、**サーバがないから全部止めるのではなく、ローカルで同じ考え方を先に練習する**ことです。SSH先が手に入ったら、`myserver` を実際の接続先に置き換えて同じKnockをやり直します。

## 7. 本物のSSH先ができたら設定する

大学・研究室・クラウドVMなどのSSH先ができたら、`~/.ssh/config` に短縮名を登録します。

```sshconfig
Host myserver
  HostName example.com
  User your_username
  Port 22
```

設定後、次で確認します。

```bash
ssh myserver "hostname && pwd"
```

ここで接続できるようになってから、SSH・scp・rsync・長時間実験系のKnockを実行してください。
