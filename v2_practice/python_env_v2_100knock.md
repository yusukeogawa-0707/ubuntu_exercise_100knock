# Python研究環境100本ノック — v2 応用・実践編

## 位置づけ

Python/uv/venv/pip/VSCode/環境変数を、研究実装前提で扱う。

- v1入門編: まず壊さず、意味を確認しながら手を動かす。
- v2応用・実践編: 研究実務で使う形に近づける。

## 使い方

1. まず各Knockのコマンドを読む。
2. 練習用ディレクトリで実行する。
3. 解説と確認ポイントを見て、何が起きたか確認する。

注意: `myserver`, `your_username`, `git@example.com:USER/REPO.git` などは仮の名前です。実環境に合わせて置き換えてください。

## Knock 001: プロジェクト雛形を作る

**目的**: 研究プロジェクトの基本構造を作る。

````bash
mkdir -p airan_project/{src,configs,data,outputs,logs,tests}
````
**解説**: コード、設定、データ、出力、ログを分けると迷子になりにくいです。

**確認ポイント**: `find airan_project -maxdepth 2 -type d` で確認。


## Knock 002: pyprojectを作る

**目的**: 依存関係をpyprojectに書く。

````bash
cat > airan_project/pyproject.toml <<EOF
[project]
name = "airan-project"
version = "0.1.0"
dependencies = ["numpy", "pandas", "pyyaml", "tqdm"]
EOF
````
**解説**: requirementsだけでなく、プロジェクト定義として依存を持てます。

**確認ポイント**: `cat airan_project/pyproject.toml` で確認。


## Knock 003: uv syncの前提確認

**目的**: uvが使えるか確認する。

````bash
cd airan_project && command -v uv && uv --version
````
**解説**: 会社PCでは導入可否が環境依存なので、まず確認します。

**確認ポイント**: uvのパスとバージョンが出る。


## Knock 004: uvで環境同期する

**目的**: pyprojectから環境を作る。

````bash
cd airan_project && uv sync
````
**解説**: uvを使うと依存解決と環境作成を一気に行えます。

**確認ポイント**: `.venv` とlockファイルが作られる。


## Knock 005: venvフォールバックを用意する

**目的**: uvが使えない場合の標準手順を持つ。

````bash
cd airan_project && python3 -m venv .venv && source .venv/bin/activate && python -m pip install -U pip
````
**解説**: どの環境でも使える標準venv手順です。

**確認ポイント**: `.venv` 配下のpythonを確認。


## Knock 006: requirementsを用意する

**目的**: venv用の依存ファイルを作る。

````bash
cd airan_project && cat > requirements.txt <<EOF
numpy
pandas
pyyaml
tqdm
EOF
````
**解説**: 簡単な共有にはrequirementsが今でも便利です。

**確認ポイント**: `wc -l requirements.txt` で確認。


## Knock 007: requirementsから入れる

**目的**: 依存を一括導入する。

````bash
cd airan_project && source .venv/bin/activate && python -m pip install -r requirements.txt
````
**解説**: サーバで環境再現するときの基本です。

**確認ポイント**: `pip list` で確認。


## Knock 008: 設定ファイルを作る

**目的**: 実験設定をファイル管理する。

````bash
cat > airan_project/configs/base.yaml <<EOF
seed: 42
model: rqn
epochs: 3
lr: 0.001
EOF
````
**解説**: CLI引数だけでなく設定ファイルに残すと再現しやすいです。

**確認ポイント**: `cat configs/base.yaml` で確認。


## Knock 009: 実験スクリプトを作る

**目的**: ログを出す学習スクリプトを作る。

````bash
cat > airan_project/src/train.py <<'EOF
import os, yaml, random, time
from pathlib import Path
config = yaml.safe_load(open("configs/base.yaml"))
Path("outputs").mkdir(exist_ok=True)
print("config", config)
for e in range(1, config["epochs"]+1):
    print(f"epoch={e} loss={1/e:.3f} acc={0.7+e*0.03:.3f}")
    time.sleep(0.1)
open("outputs/result.txt", "w").write("done\n")
EOF
````
**解説**: 実験運用練習用の安全なダミースクリプトです。

**確認ポイント**: `python src/train.py` で動く。


## Knock 010: 実験をログ保存実行する

**目的**: 実験ログを日時付きで保存する。

````bash
cd airan_project && source .venv/bin/activate && python src/train.py 2>&1 | tee logs/train_$(date +%Y%m%d_%H%M%S).log
````
**解説**: 上書きを避け、あとで追跡できます。

**確認ポイント**: `ls logs` でログを見る。


## Knock 011: 実験IDを変数にする

**目的**: 実験IDを自動生成する。

````bash
cd airan_project && EXP=exp_$(date +%Y%m%d_%H%M%S) && mkdir -p outputs/$EXP logs/$EXP && echo $EXP
````
**解説**: 実験ごとに出力先を分けると上書きを防げます。

**確認ポイント**: EXP名が表示される。


## Knock 012: 環境レポートを保存する

**目的**: 実験時の環境を保存する。

````bash
cd airan_project && { date; hostname; which python; python --version; python -m pip freeze; } > outputs/env_report.txt
````
**解説**: 再現性に効く最低限の情報です。

**確認ポイント**: `head outputs/env_report.txt` で確認。


## Knock 013: GPU指定の実行形を使う

**目的**: GPU番号指定の型を覚える。

````bash
cd airan_project && CUDA_VISIBLE_DEVICES=0 python src/train.py 2>&1 | tee logs/gpu0_train.log
````
**解説**: PyTorch/TensorFlow実験で頻出です。

**確認ポイント**: ログが生成される。


## Knock 014: 環境変数で実験名を渡す

**目的**: 環境変数を実験に渡す。

````bash
cd airan_project && EXP_NAME=test001 python -c "import os; print(os.environ.get("EXP_NAME"))"
````
**解説**: スクリプト側で設定を読みたいときに使います。

**確認ポイント**: `test001` が出る。


## Knock 015: .env例を作る

**目的**: 環境変数の見本を残す。

````bash
cd airan_project && cat > .env.example <<EOF
CUDA_VISIBLE_DEVICES=0
EXP_NAME=debug
EOF
````
**解説**: 秘密情報は入れず、必要な変数名だけ共有します。

**確認ポイント**: `.env.example` を確認。


## Knock 016: 秘密情報をgitignoreする

**目的**: 不要・秘密・巨大ファイルをGit管理から外す。

````bash
cd airan_project && cat > .gitignore <<EOF
.env
.venv/
outputs/
logs/
__pycache__/
EOF
````
**解説**: APIキーや出力ファイルを誤コミットしないために重要です。

**確認ポイント**: `cat .gitignore` で確認。


## Knock 017: import時間を計測する

**目的**: ライブラリ読み込みが極端に遅くないか見る。

````bash
cd airan_project && time python -c "import numpy, pandas, yaml; print("ok")"
````
**解説**: 環境異常やネットワークファイルシステム問題の手がかりになります。

**確認ポイント**: 実行時間が表示される。


## Knock 018: site-packages容量を見る

**目的**: 仮想環境の容量感を掴む。

````bash
cd airan_project && du -sh .venv/lib/python*/site-packages 2>/dev/null || true
````
**解説**: 大きなライブラリが入るとvenvも重くなります。

**確認ポイント**: 容量が表示される。


## Knock 019: 環境をtarで固めない判断をする

**目的**: 仮想環境の持ち運び前に容量を見る。

````bash
cd airan_project && du -sh .venv
````
**解説**: venv丸ごと転送は重く壊れやすいので、基本は再構築します。

**確認ポイント**: 容量を確認する。


## Knock 020: pip freeze差分を見る

**目的**: 要求ファイルと実環境の差分を見る。

````bash
cd airan_project && python -m pip freeze | sort > outputs/freeze_now.txt && diff -u requirements.txt outputs/freeze_now.txt || true
````
**解説**: 入れたつもりが足りない・余計に入っているを確認できます。

**確認ポイント**: diffが出る場合がある。


## Knock 021: 設定ファイルvariant 01を作る

**目的**: 複数実験設定をCLIで複製する。

````bash
cd airan_project && cp configs/base.yaml configs/exp_01.yaml && sed -i "s/epochs: 3/epochs: 2/" configs/exp_01.yaml
````
**解説**: 設定差分をファイルに残すと、実験管理が楽になります。

**確認ポイント**: `cat configs/exp_01.yaml` で確認。


## Knock 022: variant 01をログ保存実行する

**目的**: 設定別に実験を実行する。

````bash
cd airan_project && cp configs/exp_01.yaml configs/base.yaml && python src/train.py 2>&1 | tee logs/exp_01.log
````
**解説**: 実験名とログ名を一致させると後で探しやすいです。

**確認ポイント**: `grep acc logs/exp_01.log` で確認。


## Knock 023: 設定ファイルvariant 02を作る

**目的**: 複数実験設定をCLIで複製する。

````bash
cd airan_project && cp configs/base.yaml configs/exp_02.yaml && sed -i "s/epochs: 3/epochs: 3/" configs/exp_02.yaml
````
**解説**: 設定差分をファイルに残すと、実験管理が楽になります。

**確認ポイント**: `cat configs/exp_02.yaml` で確認。


## Knock 024: variant 02をログ保存実行する

**目的**: 設定別に実験を実行する。

````bash
cd airan_project && cp configs/exp_02.yaml configs/base.yaml && python src/train.py 2>&1 | tee logs/exp_02.log
````
**解説**: 実験名とログ名を一致させると後で探しやすいです。

**確認ポイント**: `grep acc logs/exp_02.log` で確認。


## Knock 025: 設定ファイルvariant 03を作る

**目的**: 複数実験設定をCLIで複製する。

````bash
cd airan_project && cp configs/base.yaml configs/exp_03.yaml && sed -i "s/epochs: 3/epochs: 4/" configs/exp_03.yaml
````
**解説**: 設定差分をファイルに残すと、実験管理が楽になります。

**確認ポイント**: `cat configs/exp_03.yaml` で確認。


## Knock 026: variant 03をログ保存実行する

**目的**: 設定別に実験を実行する。

````bash
cd airan_project && cp configs/exp_03.yaml configs/base.yaml && python src/train.py 2>&1 | tee logs/exp_03.log
````
**解説**: 実験名とログ名を一致させると後で探しやすいです。

**確認ポイント**: `grep acc logs/exp_03.log` で確認。


## Knock 027: 設定ファイルvariant 04を作る

**目的**: 複数実験設定をCLIで複製する。

````bash
cd airan_project && cp configs/base.yaml configs/exp_04.yaml && sed -i "s/epochs: 3/epochs: 5/" configs/exp_04.yaml
````
**解説**: 設定差分をファイルに残すと、実験管理が楽になります。

**確認ポイント**: `cat configs/exp_04.yaml` で確認。


## Knock 028: variant 04をログ保存実行する

**目的**: 設定別に実験を実行する。

````bash
cd airan_project && cp configs/exp_04.yaml configs/base.yaml && python src/train.py 2>&1 | tee logs/exp_04.log
````
**解説**: 実験名とログ名を一致させると後で探しやすいです。

**確認ポイント**: `grep acc logs/exp_04.log` で確認。


## Knock 029: 設定ファイルvariant 05を作る

**目的**: 複数実験設定をCLIで複製する。

````bash
cd airan_project && cp configs/base.yaml configs/exp_05.yaml && sed -i "s/epochs: 3/epochs: 1/" configs/exp_05.yaml
````
**解説**: 設定差分をファイルに残すと、実験管理が楽になります。

**確認ポイント**: `cat configs/exp_05.yaml` で確認。


## Knock 030: variant 05をログ保存実行する

**目的**: 設定別に実験を実行する。

````bash
cd airan_project && cp configs/exp_05.yaml configs/base.yaml && python src/train.py 2>&1 | tee logs/exp_05.log
````
**解説**: 実験名とログ名を一致させると後で探しやすいです。

**確認ポイント**: `grep acc logs/exp_05.log` で確認。


## Knock 031: 設定ファイルvariant 06を作る

**目的**: 複数実験設定をCLIで複製する。

````bash
cd airan_project && cp configs/base.yaml configs/exp_06.yaml && sed -i "s/epochs: 3/epochs: 2/" configs/exp_06.yaml
````
**解説**: 設定差分をファイルに残すと、実験管理が楽になります。

**確認ポイント**: `cat configs/exp_06.yaml` で確認。


## Knock 032: variant 06をログ保存実行する

**目的**: 設定別に実験を実行する。

````bash
cd airan_project && cp configs/exp_06.yaml configs/base.yaml && python src/train.py 2>&1 | tee logs/exp_06.log
````
**解説**: 実験名とログ名を一致させると後で探しやすいです。

**確認ポイント**: `grep acc logs/exp_06.log` で確認。


## Knock 033: 設定ファイルvariant 07を作る

**目的**: 複数実験設定をCLIで複製する。

````bash
cd airan_project && cp configs/base.yaml configs/exp_07.yaml && sed -i "s/epochs: 3/epochs: 3/" configs/exp_07.yaml
````
**解説**: 設定差分をファイルに残すと、実験管理が楽になります。

**確認ポイント**: `cat configs/exp_07.yaml` で確認。


## Knock 034: variant 07をログ保存実行する

**目的**: 設定別に実験を実行する。

````bash
cd airan_project && cp configs/exp_07.yaml configs/base.yaml && python src/train.py 2>&1 | tee logs/exp_07.log
````
**解説**: 実験名とログ名を一致させると後で探しやすいです。

**確認ポイント**: `grep acc logs/exp_07.log` で確認。


## Knock 035: 設定ファイルvariant 08を作る

**目的**: 複数実験設定をCLIで複製する。

````bash
cd airan_project && cp configs/base.yaml configs/exp_08.yaml && sed -i "s/epochs: 3/epochs: 4/" configs/exp_08.yaml
````
**解説**: 設定差分をファイルに残すと、実験管理が楽になります。

**確認ポイント**: `cat configs/exp_08.yaml` で確認。


## Knock 036: variant 08をログ保存実行する

**目的**: 設定別に実験を実行する。

````bash
cd airan_project && cp configs/exp_08.yaml configs/base.yaml && python src/train.py 2>&1 | tee logs/exp_08.log
````
**解説**: 実験名とログ名を一致させると後で探しやすいです。

**確認ポイント**: `grep acc logs/exp_08.log` で確認。


## Knock 037: 設定ファイルvariant 09を作る

**目的**: 複数実験設定をCLIで複製する。

````bash
cd airan_project && cp configs/base.yaml configs/exp_09.yaml && sed -i "s/epochs: 3/epochs: 5/" configs/exp_09.yaml
````
**解説**: 設定差分をファイルに残すと、実験管理が楽になります。

**確認ポイント**: `cat configs/exp_09.yaml` で確認。


## Knock 038: variant 09をログ保存実行する

**目的**: 設定別に実験を実行する。

````bash
cd airan_project && cp configs/exp_09.yaml configs/base.yaml && python src/train.py 2>&1 | tee logs/exp_09.log
````
**解説**: 実験名とログ名を一致させると後で探しやすいです。

**確認ポイント**: `grep acc logs/exp_09.log` で確認。


## Knock 039: 設定ファイルvariant 10を作る

**目的**: 複数実験設定をCLIで複製する。

````bash
cd airan_project && cp configs/base.yaml configs/exp_10.yaml && sed -i "s/epochs: 3/epochs: 1/" configs/exp_10.yaml
````
**解説**: 設定差分をファイルに残すと、実験管理が楽になります。

**確認ポイント**: `cat configs/exp_10.yaml` で確認。


## Knock 040: variant 10をログ保存実行する

**目的**: 設定別に実験を実行する。

````bash
cd airan_project && cp configs/exp_10.yaml configs/base.yaml && python src/train.py 2>&1 | tee logs/exp_10.log
````
**解説**: 実験名とログ名を一致させると後で探しやすいです。

**確認ポイント**: `grep acc logs/exp_10.log` で確認。


## Knock 041: 設定ファイルvariant 11を作る

**目的**: 複数実験設定をCLIで複製する。

````bash
cd airan_project && cp configs/base.yaml configs/exp_11.yaml && sed -i "s/epochs: 3/epochs: 2/" configs/exp_11.yaml
````
**解説**: 設定差分をファイルに残すと、実験管理が楽になります。

**確認ポイント**: `cat configs/exp_11.yaml` で確認。


## Knock 042: variant 11をログ保存実行する

**目的**: 設定別に実験を実行する。

````bash
cd airan_project && cp configs/exp_11.yaml configs/base.yaml && python src/train.py 2>&1 | tee logs/exp_11.log
````
**解説**: 実験名とログ名を一致させると後で探しやすいです。

**確認ポイント**: `grep acc logs/exp_11.log` で確認。


## Knock 043: 設定ファイルvariant 12を作る

**目的**: 複数実験設定をCLIで複製する。

````bash
cd airan_project && cp configs/base.yaml configs/exp_12.yaml && sed -i "s/epochs: 3/epochs: 3/" configs/exp_12.yaml
````
**解説**: 設定差分をファイルに残すと、実験管理が楽になります。

**確認ポイント**: `cat configs/exp_12.yaml` で確認。


## Knock 044: variant 12をログ保存実行する

**目的**: 設定別に実験を実行する。

````bash
cd airan_project && cp configs/exp_12.yaml configs/base.yaml && python src/train.py 2>&1 | tee logs/exp_12.log
````
**解説**: 実験名とログ名を一致させると後で探しやすいです。

**確認ポイント**: `grep acc logs/exp_12.log` で確認。


## Knock 045: 設定ファイルvariant 13を作る

**目的**: 複数実験設定をCLIで複製する。

````bash
cd airan_project && cp configs/base.yaml configs/exp_13.yaml && sed -i "s/epochs: 3/epochs: 4/" configs/exp_13.yaml
````
**解説**: 設定差分をファイルに残すと、実験管理が楽になります。

**確認ポイント**: `cat configs/exp_13.yaml` で確認。


## Knock 046: variant 13をログ保存実行する

**目的**: 設定別に実験を実行する。

````bash
cd airan_project && cp configs/exp_13.yaml configs/base.yaml && python src/train.py 2>&1 | tee logs/exp_13.log
````
**解説**: 実験名とログ名を一致させると後で探しやすいです。

**確認ポイント**: `grep acc logs/exp_13.log` で確認。


## Knock 047: 設定ファイルvariant 14を作る

**目的**: 複数実験設定をCLIで複製する。

````bash
cd airan_project && cp configs/base.yaml configs/exp_14.yaml && sed -i "s/epochs: 3/epochs: 5/" configs/exp_14.yaml
````
**解説**: 設定差分をファイルに残すと、実験管理が楽になります。

**確認ポイント**: `cat configs/exp_14.yaml` で確認。


## Knock 048: variant 14をログ保存実行する

**目的**: 設定別に実験を実行する。

````bash
cd airan_project && cp configs/exp_14.yaml configs/base.yaml && python src/train.py 2>&1 | tee logs/exp_14.log
````
**解説**: 実験名とログ名を一致させると後で探しやすいです。

**確認ポイント**: `grep acc logs/exp_14.log` で確認。


## Knock 049: 設定ファイルvariant 15を作る

**目的**: 複数実験設定をCLIで複製する。

````bash
cd airan_project && cp configs/base.yaml configs/exp_15.yaml && sed -i "s/epochs: 3/epochs: 1/" configs/exp_15.yaml
````
**解説**: 設定差分をファイルに残すと、実験管理が楽になります。

**確認ポイント**: `cat configs/exp_15.yaml` で確認。


## Knock 050: variant 15をログ保存実行する

**目的**: 設定別に実験を実行する。

````bash
cd airan_project && cp configs/exp_15.yaml configs/base.yaml && python src/train.py 2>&1 | tee logs/exp_15.log
````
**解説**: 実験名とログ名を一致させると後で探しやすいです。

**確認ポイント**: `grep acc logs/exp_15.log` で確認。


## Knock 051: 設定ファイルvariant 16を作る

**目的**: 複数実験設定をCLIで複製する。

````bash
cd airan_project && cp configs/base.yaml configs/exp_16.yaml && sed -i "s/epochs: 3/epochs: 2/" configs/exp_16.yaml
````
**解説**: 設定差分をファイルに残すと、実験管理が楽になります。

**確認ポイント**: `cat configs/exp_16.yaml` で確認。


## Knock 052: variant 16をログ保存実行する

**目的**: 設定別に実験を実行する。

````bash
cd airan_project && cp configs/exp_16.yaml configs/base.yaml && python src/train.py 2>&1 | tee logs/exp_16.log
````
**解説**: 実験名とログ名を一致させると後で探しやすいです。

**確認ポイント**: `grep acc logs/exp_16.log` で確認。


## Knock 053: 設定ファイルvariant 17を作る

**目的**: 複数実験設定をCLIで複製する。

````bash
cd airan_project && cp configs/base.yaml configs/exp_17.yaml && sed -i "s/epochs: 3/epochs: 3/" configs/exp_17.yaml
````
**解説**: 設定差分をファイルに残すと、実験管理が楽になります。

**確認ポイント**: `cat configs/exp_17.yaml` で確認。


## Knock 054: variant 17をログ保存実行する

**目的**: 設定別に実験を実行する。

````bash
cd airan_project && cp configs/exp_17.yaml configs/base.yaml && python src/train.py 2>&1 | tee logs/exp_17.log
````
**解説**: 実験名とログ名を一致させると後で探しやすいです。

**確認ポイント**: `grep acc logs/exp_17.log` で確認。


## Knock 055: 設定ファイルvariant 18を作る

**目的**: 複数実験設定をCLIで複製する。

````bash
cd airan_project && cp configs/base.yaml configs/exp_18.yaml && sed -i "s/epochs: 3/epochs: 4/" configs/exp_18.yaml
````
**解説**: 設定差分をファイルに残すと、実験管理が楽になります。

**確認ポイント**: `cat configs/exp_18.yaml` で確認。


## Knock 056: variant 18をログ保存実行する

**目的**: 設定別に実験を実行する。

````bash
cd airan_project && cp configs/exp_18.yaml configs/base.yaml && python src/train.py 2>&1 | tee logs/exp_18.log
````
**解説**: 実験名とログ名を一致させると後で探しやすいです。

**確認ポイント**: `grep acc logs/exp_18.log` で確認。


## Knock 057: 設定ファイルvariant 19を作る

**目的**: 複数実験設定をCLIで複製する。

````bash
cd airan_project && cp configs/base.yaml configs/exp_19.yaml && sed -i "s/epochs: 3/epochs: 5/" configs/exp_19.yaml
````
**解説**: 設定差分をファイルに残すと、実験管理が楽になります。

**確認ポイント**: `cat configs/exp_19.yaml` で確認。


## Knock 058: variant 19をログ保存実行する

**目的**: 設定別に実験を実行する。

````bash
cd airan_project && cp configs/exp_19.yaml configs/base.yaml && python src/train.py 2>&1 | tee logs/exp_19.log
````
**解説**: 実験名とログ名を一致させると後で探しやすいです。

**確認ポイント**: `grep acc logs/exp_19.log` で確認。


## Knock 059: 設定ファイルvariant 20を作る

**目的**: 複数実験設定をCLIで複製する。

````bash
cd airan_project && cp configs/base.yaml configs/exp_20.yaml && sed -i "s/epochs: 3/epochs: 1/" configs/exp_20.yaml
````
**解説**: 設定差分をファイルに残すと、実験管理が楽になります。

**確認ポイント**: `cat configs/exp_20.yaml` で確認。


## Knock 060: variant 20をログ保存実行する

**目的**: 設定別に実験を実行する。

````bash
cd airan_project && cp configs/exp_20.yaml configs/base.yaml && python src/train.py 2>&1 | tee logs/exp_20.log
````
**解説**: 実験名とログ名を一致させると後で探しやすいです。

**確認ポイント**: `grep acc logs/exp_20.log` で確認。


## Knock 061: 設定ファイルvariant 21を作る

**目的**: 複数実験設定をCLIで複製する。

````bash
cd airan_project && cp configs/base.yaml configs/exp_21.yaml && sed -i "s/epochs: 3/epochs: 2/" configs/exp_21.yaml
````
**解説**: 設定差分をファイルに残すと、実験管理が楽になります。

**確認ポイント**: `cat configs/exp_21.yaml` で確認。


## Knock 062: variant 21をログ保存実行する

**目的**: 設定別に実験を実行する。

````bash
cd airan_project && cp configs/exp_21.yaml configs/base.yaml && python src/train.py 2>&1 | tee logs/exp_21.log
````
**解説**: 実験名とログ名を一致させると後で探しやすいです。

**確認ポイント**: `grep acc logs/exp_21.log` で確認。


## Knock 063: 設定ファイルvariant 22を作る

**目的**: 複数実験設定をCLIで複製する。

````bash
cd airan_project && cp configs/base.yaml configs/exp_22.yaml && sed -i "s/epochs: 3/epochs: 3/" configs/exp_22.yaml
````
**解説**: 設定差分をファイルに残すと、実験管理が楽になります。

**確認ポイント**: `cat configs/exp_22.yaml` で確認。


## Knock 064: variant 22をログ保存実行する

**目的**: 設定別に実験を実行する。

````bash
cd airan_project && cp configs/exp_22.yaml configs/base.yaml && python src/train.py 2>&1 | tee logs/exp_22.log
````
**解説**: 実験名とログ名を一致させると後で探しやすいです。

**確認ポイント**: `grep acc logs/exp_22.log` で確認。


## Knock 065: 設定ファイルvariant 23を作る

**目的**: 複数実験設定をCLIで複製する。

````bash
cd airan_project && cp configs/base.yaml configs/exp_23.yaml && sed -i "s/epochs: 3/epochs: 4/" configs/exp_23.yaml
````
**解説**: 設定差分をファイルに残すと、実験管理が楽になります。

**確認ポイント**: `cat configs/exp_23.yaml` で確認。


## Knock 066: variant 23をログ保存実行する

**目的**: 設定別に実験を実行する。

````bash
cd airan_project && cp configs/exp_23.yaml configs/base.yaml && python src/train.py 2>&1 | tee logs/exp_23.log
````
**解説**: 実験名とログ名を一致させると後で探しやすいです。

**確認ポイント**: `grep acc logs/exp_23.log` で確認。


## Knock 067: 設定ファイルvariant 24を作る

**目的**: 複数実験設定をCLIで複製する。

````bash
cd airan_project && cp configs/base.yaml configs/exp_24.yaml && sed -i "s/epochs: 3/epochs: 5/" configs/exp_24.yaml
````
**解説**: 設定差分をファイルに残すと、実験管理が楽になります。

**確認ポイント**: `cat configs/exp_24.yaml` で確認。


## Knock 068: variant 24をログ保存実行する

**目的**: 設定別に実験を実行する。

````bash
cd airan_project && cp configs/exp_24.yaml configs/base.yaml && python src/train.py 2>&1 | tee logs/exp_24.log
````
**解説**: 実験名とログ名を一致させると後で探しやすいです。

**確認ポイント**: `grep acc logs/exp_24.log` で確認。


## Knock 069: 設定ファイルvariant 25を作る

**目的**: 複数実験設定をCLIで複製する。

````bash
cd airan_project && cp configs/base.yaml configs/exp_25.yaml && sed -i "s/epochs: 3/epochs: 1/" configs/exp_25.yaml
````
**解説**: 設定差分をファイルに残すと、実験管理が楽になります。

**確認ポイント**: `cat configs/exp_25.yaml` で確認。


## Knock 070: variant 25をログ保存実行する

**目的**: 設定別に実験を実行する。

````bash
cd airan_project && cp configs/exp_25.yaml configs/base.yaml && python src/train.py 2>&1 | tee logs/exp_25.log
````
**解説**: 実験名とログ名を一致させると後で探しやすいです。

**確認ポイント**: `grep acc logs/exp_25.log` で確認。


## Knock 071: 設定ファイルvariant 26を作る

**目的**: 複数実験設定をCLIで複製する。

````bash
cd airan_project && cp configs/base.yaml configs/exp_26.yaml && sed -i "s/epochs: 3/epochs: 2/" configs/exp_26.yaml
````
**解説**: 設定差分をファイルに残すと、実験管理が楽になります。

**確認ポイント**: `cat configs/exp_26.yaml` で確認。


## Knock 072: variant 26をログ保存実行する

**目的**: 設定別に実験を実行する。

````bash
cd airan_project && cp configs/exp_26.yaml configs/base.yaml && python src/train.py 2>&1 | tee logs/exp_26.log
````
**解説**: 実験名とログ名を一致させると後で探しやすいです。

**確認ポイント**: `grep acc logs/exp_26.log` で確認。


## Knock 073: 設定ファイルvariant 27を作る

**目的**: 複数実験設定をCLIで複製する。

````bash
cd airan_project && cp configs/base.yaml configs/exp_27.yaml && sed -i "s/epochs: 3/epochs: 3/" configs/exp_27.yaml
````
**解説**: 設定差分をファイルに残すと、実験管理が楽になります。

**確認ポイント**: `cat configs/exp_27.yaml` で確認。


## Knock 074: variant 27をログ保存実行する

**目的**: 設定別に実験を実行する。

````bash
cd airan_project && cp configs/exp_27.yaml configs/base.yaml && python src/train.py 2>&1 | tee logs/exp_27.log
````
**解説**: 実験名とログ名を一致させると後で探しやすいです。

**確認ポイント**: `grep acc logs/exp_27.log` で確認。


## Knock 075: 設定ファイルvariant 28を作る

**目的**: 複数実験設定をCLIで複製する。

````bash
cd airan_project && cp configs/base.yaml configs/exp_28.yaml && sed -i "s/epochs: 3/epochs: 4/" configs/exp_28.yaml
````
**解説**: 設定差分をファイルに残すと、実験管理が楽になります。

**確認ポイント**: `cat configs/exp_28.yaml` で確認。


## Knock 076: variant 28をログ保存実行する

**目的**: 設定別に実験を実行する。

````bash
cd airan_project && cp configs/exp_28.yaml configs/base.yaml && python src/train.py 2>&1 | tee logs/exp_28.log
````
**解説**: 実験名とログ名を一致させると後で探しやすいです。

**確認ポイント**: `grep acc logs/exp_28.log` で確認。


## Knock 077: 設定ファイルvariant 29を作る

**目的**: 複数実験設定をCLIで複製する。

````bash
cd airan_project && cp configs/base.yaml configs/exp_29.yaml && sed -i "s/epochs: 3/epochs: 5/" configs/exp_29.yaml
````
**解説**: 設定差分をファイルに残すと、実験管理が楽になります。

**確認ポイント**: `cat configs/exp_29.yaml` で確認。


## Knock 078: variant 29をログ保存実行する

**目的**: 設定別に実験を実行する。

````bash
cd airan_project && cp configs/exp_29.yaml configs/base.yaml && python src/train.py 2>&1 | tee logs/exp_29.log
````
**解説**: 実験名とログ名を一致させると後で探しやすいです。

**確認ポイント**: `grep acc logs/exp_29.log` で確認。


## Knock 079: 設定ファイルvariant 30を作る

**目的**: 複数実験設定をCLIで複製する。

````bash
cd airan_project && cp configs/base.yaml configs/exp_30.yaml && sed -i "s/epochs: 3/epochs: 1/" configs/exp_30.yaml
````
**解説**: 設定差分をファイルに残すと、実験管理が楽になります。

**確認ポイント**: `cat configs/exp_30.yaml` で確認。


## Knock 080: variant 30をログ保存実行する

**目的**: 設定別に実験を実行する。

````bash
cd airan_project && cp configs/exp_30.yaml configs/base.yaml && python src/train.py 2>&1 | tee logs/exp_30.log
````
**解説**: 実験名とログ名を一致させると後で探しやすいです。

**確認ポイント**: `grep acc logs/exp_30.log` で確認。


## Knock 081: 全ログからlossを検索する

**目的**: ログ中のlossを横断検索する。

````bash
cd airan_project && grep -R "loss" logs || true
````
**解説**: 実験が増えるほどgrepの便利さが増します。

**確認ポイント**: 該当行が一覧表示される。


## Knock 082: 全ログからaccを検索する

**目的**: ログ中のaccを横断検索する。

````bash
cd airan_project && grep -R "acc" logs || true
````
**解説**: 実験が増えるほどgrepの便利さが増します。

**確認ポイント**: 該当行が一覧表示される。


## Knock 083: 全ログからepochを検索する

**目的**: ログ中のepochを横断検索する。

````bash
cd airan_project && grep -R "epoch" logs || true
````
**解説**: 実験が増えるほどgrepの便利さが増します。

**確認ポイント**: 該当行が一覧表示される。


## Knock 084: 全ログからconfigを検索する

**目的**: ログ中のconfigを横断検索する。

````bash
cd airan_project && grep -R "config" logs || true
````
**解説**: 実験が増えるほどgrepの便利さが増します。

**確認ポイント**: 該当行が一覧表示される。


## Knock 085: 全ログからERRORを検索する

**目的**: ログ中のERRORを横断検索する。

````bash
cd airan_project && grep -R "ERROR" logs || true
````
**解説**: 実験が増えるほどgrepの便利さが増します。

**確認ポイント**: 該当行が一覧表示される。


## Knock 086: 全ログからWARNを検索する

**目的**: ログ中のWARNを横断検索する。

````bash
cd airan_project && grep -R "WARN" logs || true
````
**解説**: 実験が増えるほどgrepの便利さが増します。

**確認ポイント**: 該当行が一覧表示される。


## Knock 087: ログをacc行だけCSV化する

**目的**: ログから指標を抽出する。

````bash
cd airan_project && grep -R "acc=" logs | sed -E "s/.*epoch=([0-9]+).*acc=([0-9.]+).*/epoch,\1,acc,\2/" | head
````
**解説**: 完璧なパーサでなくても、軽い確認ならCLIで十分です。

**確認ポイント**: epochとaccが見える。


## Knock 088: 最新ログを開く

**目的**: 最新ログの末尾を見る。

````bash
cd airan_project && ls -t logs/*.log | head -n 1 | xargs tail -n 20
````
**解説**: どのログが最新か探してからtailする流れを1行化しています。

**確認ポイント**: 最新ログ末尾が表示される。


## Knock 089: 全ログのサイズを見る

**目的**: ログが膨らみすぎていないか確認する。

````bash
cd airan_project && du -h logs | sort -hr | head
````
**解説**: 学習ログは意外と容量を食います。

**確認ポイント**: 大きい順に表示される。


## Knock 090: outputsを確認する

**目的**: 出力ファイルを一覧する。

````bash
cd airan_project && find outputs -maxdepth 2 -type f -exec ls -lh {} \;
````
**解説**: 実験後に何が生成されたか必ず確認します。

**確認ポイント**: 出力ファイル一覧が出る。


## Knock 091: 環境再作成手順をREADMEに書く

**目的**: 未来の自分用に環境手順を残す。

````bash
cd airan_project && cat > README_ENV.md <<EOF
# Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python src/train.py
```
EOF
````
**解説**: READMEがあるとサーバ移行時に迷いません。

**確認ポイント**: `cat README_ENV.md` で確認。


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

