# Python研究環境100本ノック — 入門編

## 位置づけ

Python/uv/venv/pip/VSCode/環境変数を、研究実装前提で扱う。

- 入門編: まず壊さず、意味を確認しながら手を動かす。
- 実践編: 研究実務で使う形に近づける。

## 使い方

1. まず各Knockのコマンドを読む。
2. 練習用ディレクトリで実行する。
3. 解説と確認ポイントを見て、何が起きたか確認する。

注意: `myserver`, `your_username`, `git@example.com:USER/REPO.git` などは仮の名前です。実環境に合わせて置き換えてください。

## Knock 001: Pythonの場所を確認する

**目的**: VSCodeやターミナルがどのPythonを見ているか確認する。

````bash
which python3
````
**解説**: `which` はPATH上で最初に見つかった実行ファイルを表示します。Python環境の混乱はここから確認します。

**確認ポイント**: `/usr/bin/python3` や `.venv/bin/python` のようなパスが出る。


## Knock 002: Pythonのバージョンを確認する

**目的**: 使っているPythonのバージョンを把握する。

````bash
python3 --version
````
**解説**: ライブラリによってはPythonの対応バージョンが違います。最初に確認する癖をつけます。

**確認ポイント**: `Python 3.x.x` が表示される。


## Knock 003: pipの場所を確認する

**目的**: pipがどのPython環境に紐づいているか確認する。

````bash
which pip3
````
**解説**: `pip` と `python` が別環境を指すと、インストールしたのにimportできない問題が起きます。

**確認ポイント**: Pythonと近い場所のpipなら安全度が高い。


## Knock 004: pipのバージョンを確認する

**目的**: pipが紐づくPythonを確認する。

````bash
pip3 --version
````
**解説**: `pip --version` には、pip自体のバージョンだけでなくPythonのパスも表示されます。

**確認ポイント**: 出力の末尾にPythonバージョンやパスが出る。


## Knock 005: python経由でpipを呼ぶ

**目的**: pipとPythonの対応を安全に確認する。

````bash
python3 -m pip --version
````
**解説**: 初心者は `pip install` より `python -m pip install` の方が環境ズレを避けやすいです。

**確認ポイント**: `python3` に紐づいたpip情報が表示される。


## Knock 006: 仮想環境を作る

**目的**: 標準機能venvでプロジェクト専用環境を作る。

````bash
python3 -m venv .venv
````
**解説**: `.venv` はそのプロジェクト専用のPython環境です。グローバル環境を汚さないために使います。

**確認ポイント**: `.venv/` ディレクトリができる。


## Knock 007: 仮想環境を有効化する

**目的**: 作成した仮想環境に入る。

````bash
source .venv/bin/activate
````
**解説**: 有効化すると、`python` や `pip` が `.venv` 側を向きます。

**確認ポイント**: プロンプトの先頭に `(.venv)` が付くことが多い。


## Knock 008: 仮想環境内のPythonを確認する

**目的**: 今のPythonが仮想環境のものか確認する。

````bash
which python && python --version
````
**解説**: 仮想環境を有効化したら、必ず `which python` で確認します。

**確認ポイント**: パスに `.venv/bin/python` が含まれる。


## Knock 009: 仮想環境内のpipを確認する

**目的**: pipも仮想環境側か確認する。

````bash
python -m pip --version
````
**解説**: Pythonとpipの対応確認は環境構築の基本です。

**確認ポイント**: 出力パスに `.venv` が含まれる。


## Knock 010: 仮想環境を抜ける

**目的**: 現在の仮想環境から抜ける。

````bash
deactivate
````
**解説**: 仮想環境から抜けると、通常のPythonに戻ります。

**確認ポイント**: プロンプトの `(.venv)` が消える。


## Knock 011: パッケージ一覧を見る

**目的**: 現在の環境に入っているパッケージを確認する。

````bash
python -m pip list
````
**解説**: 「何が入っているか分からない」を避ける基本操作です。

**確認ポイント**: `pip`, `setuptools` などが表示される。


## Knock 012: numpyを入れる

**目的**: 代表的なパッケージを仮想環境に入れる。

````bash
python -m pip install numpy
````
**解説**: 仮想環境を有効化した状態で入れるのが大事です。

**確認ポイント**: 最後に `Successfully installed` が出る。


## Knock 013: numpyをimport確認する

**目的**: 入れたパッケージが本当に使えるか確認する。

````bash
python -c "import numpy as np; print(np.__version__)"
````
**解説**: インストール後はimport確認までやると安心です。

**確認ポイント**: numpyのバージョンが表示される。


## Knock 014: requirementsを書き出す

**目的**: 現在の環境を再現用ファイルに保存する。

````bash
python -m pip freeze > requirements.txt
````
**解説**: `requirements.txt` は他人や未来の自分が同じ環境を作るためのメモです。

**確認ポイント**: `cat requirements.txt` でnumpy等が見える。


## Knock 015: requirementsから入れる

**目的**: 環境再現の基本を体験する。

````bash
python -m pip install -r requirements.txt
````
**解説**: 別PCやサーバで同じライブラリを入れる時に使います。

**確認ポイント**: エラーなく終了する。


## Knock 016: パッケージ詳細を見る

**目的**: 特定パッケージの情報を見る。

````bash
python -m pip show numpy
````
**解説**: バージョン、インストール場所、依存関係を確認できます。

**確認ポイント**: `Location:` に環境内パスが出る。


## Knock 017: パッケージを更新する

**目的**: pip自体を更新する。

````bash
python -m pip install -U pip
````
**解説**: 古すぎるpipはインストール失敗の原因になることがあります。

**確認ポイント**: pipのバージョンが変わる場合がある。


## Knock 018: パッケージを削除する

**目的**: 不要パッケージを消す練習をする。

````bash
python -m pip uninstall -y numpy
````
**解説**: `-y` は確認に自動でyesを入れます。練習環境だけで使いましょう。

**確認ポイント**: `pip list | grep numpy` で出なければ削除済み。


## Knock 019: 再度numpyを入れる

**目的**: 削除後に再インストールする。

````bash
python -m pip install numpy
````
**解説**: 消す・入れる・確認する流れを覚えます。

**確認ポイント**: import確認が通る。


## Knock 020: Pythonの検索パスを見る

**目的**: Pythonがどこからモジュールを探すか見る。

````bash
python -c "import sys; print(*sys.path, sep="
")"
````
**解説**: importエラーの原因調査で役に立ちます。

**確認ポイント**: カレントディレクトリやsite-packagesが見える。


## Knock 021: 実行ファイルの場所をPythonから見る

**目的**: 現在のPython実体をPython内部から確認する。

````bash
python -c "import sys; print(sys.executable)"
````
**解説**: VSCodeのInterpreter確認にも近い発想です。

**確認ポイント**: `.venv/bin/python` などが出る。


## Knock 022: 作業ディレクトリをPythonから見る

**目的**: Python実行時の現在地を確認する。

````bash
python -c "import os; print(os.getcwd())"
````
**解説**: 相対パスでファイルが見つからない問題の原因を確認できます。

**確認ポイント**: ターミナルの `pwd` と一致する。


## Knock 023: 簡単なスクリプトを作る

**目的**: スクリプトファイルを作る。

````bash
mkdir -p src && echo "print("hello python env")" > src/check.py
````
**解説**: CLIからコードファイルを作り、実行する流れを確認します。

**確認ポイント**: `src/check.py` ができる。


## Knock 024: スクリプトを実行する

**目的**: PythonファイルをCLIから実行する。

````bash
python src/check.py
````
**解説**: VSCodeの実行ボタンだけでなく、CLI実行もできるようにします。

**確認ポイント**: `hello python env` が表示される。


## Knock 025: PYTHONPATHを一時指定する

**目的**: 環境変数を付けてPythonを実行する。

````bash
PYTHONPATH=. python src/check.py
````
**解説**: `VAR=value command` の形で、そのコマンドだけ環境変数を設定できます。

**確認ポイント**: 通常通り実行される。


## Knock 026: 環境変数を表示する

**目的**: 環境変数の一覧を見る。

````bash
env | sort | head
````
**解説**: PythonやCUDA、プロキシ設定のトラブル調査に使います。

**確認ポイント**: 複数の `KEY=value` が表示される。


## Knock 027: PATHを確認する

**目的**: コマンド探索パスを見やすく表示する。

````bash
echo $PATH | tr ":" "
"
````
**解説**: `which python` の裏側にある探索順です。

**確認ポイント**: ディレクトリが1行ずつ表示される。


## Knock 028: CUDA_VISIBLE_DEVICESの形を覚える

**目的**: GPU番号を指定する書き方を覚える。

````bash
CUDA_VISIBLE_DEVICES=0 python -c "import os; print(os.environ.get("CUDA_VISIBLE_DEVICES"))"
````
**解説**: GPU実験ではこの形を非常によく使います。

**確認ポイント**: `0` が表示される。


## Knock 029: uvが入っているか確認する

**目的**: uvコマンドの有無を確認する。

````bash
command -v uv || echo "uv is not installed"
````
**解説**: uvは高速なPythonパッケージ・環境管理ツールですが、入っていない環境もあります。

**確認ポイント**: パスまたは未インストール表示が出る。


## Knock 030: uvのバージョンを見る

**目的**: uvが使える場合のバージョン確認をする。

````bash
uv --version
````
**解説**: 使える環境では、pip/venvの代替として便利です。

**確認ポイント**: `uv` のバージョンが出る。


## Knock 031: uvで仮想環境を作る

**目的**: uvによる仮想環境作成を体験する。

````bash
uv venv .venv_uv
````
**解説**: 標準venvより高速に作れることが多いです。

**確認ポイント**: `.venv_uv/` ができる。


## Knock 032: uv環境を有効化する

**目的**: uvで作ったvenvに入る。

````bash
source .venv_uv/bin/activate
````
**解説**: uv venvで作っても有効化方法は通常のvenvと同じです。

**確認ポイント**: `which python` に `.venv_uv` が出る。


## Knock 033: uv pipでnumpyを入れる

**目的**: uv経由でパッケージを入れる。

````bash
uv pip install numpy
````
**解説**: `uv pip install` はpip互換の操作です。

**確認ポイント**: numpyがインストールされる。


## Knock 034: uv pip listを見る

**目的**: uv管理環境のパッケージを見る。

````bash
uv pip list
````
**解説**: pip listと似た感覚で使えます。

**確認ポイント**: numpyが一覧に出る。


## Knock 035: 依存関係をファイル出力する

**目的**: uv環境の依存関係を書き出す。

````bash
uv pip freeze > requirements_uv.txt
````
**解説**: サーバ再現用に残すと便利です。

**確認ポイント**: `requirements_uv.txt` ができる。


## Knock 036: pyproject.tomlを最小作成する

**目的**: 現代的なPythonプロジェクト設定ファイルを作る。

````bash
cat > pyproject.toml <<EOF
[project]
name = "ubuntu100-python-env"
version = "0.1.0"
dependencies = ["numpy"]
EOF
````
**解説**: `pyproject.toml` は最近のPythonプロジェクト管理の中心です。

**確認ポイント**: `cat pyproject.toml` で中身を確認する。


## Knock 037: VSCode用設定ディレクトリを作る

**目的**: VSCodeのプロジェクト設定置き場を作る。

````bash
mkdir -p .vscode
````
**解説**: Python interpreter指定や設定をプロジェクトに置けます。

**確認ポイント**: .vscode/` ができる。


## Knock 038: VSCode設定を最小作成する

**目的**: VSCodeが使うPythonを明示する。

````bash
cat > .vscode/settings.json <<EOF
{
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python"
}
EOF
````
**解説**: チームや未来の自分が同じInterpreterを選びやすくなります。

**確認ポイント**: `cat .vscode/settings.json` で確認する。


## Knock 039: 環境を丸ごと削除する前に確認する

**目的**: 仮想環境の容量を確認する。

````bash
du -sh .venv .venv_uv 2>/dev/null || true
````
**解説**: 仮想環境は容量を使うので、不要になったら消せます。

**確認ポイント**: 各環境のサイズが表示される。


## Knock 040: pandasをインストールする

**目的**: pandasを現在の仮想環境に入れる。

````bash
python -m pip install pandas
````
**解説**: パッケージ名を変えるだけで同じ型を再利用できます。

**確認ポイント**: `python -m pip show pandas` で確認する。


## Knock 041: pandasのimport確認をする

**目的**: pandasがPythonから読めるか確認する。

````bash
python -c "import pandas; print("ok")"
````
**解説**: インストール成功とimport成功は別なので、import確認までやります。

**確認ポイント**: `ok` が出る。


## Knock 042: matplotlibをインストールする

**目的**: matplotlibを現在の仮想環境に入れる。

````bash
python -m pip install matplotlib
````
**解説**: パッケージ名を変えるだけで同じ型を再利用できます。

**確認ポイント**: `python -m pip show matplotlib` で確認する。


## Knock 043: matplotlibのimport確認をする

**目的**: matplotlibがPythonから読めるか確認する。

````bash
python -c "import matplotlib; print("ok")"
````
**解説**: インストール成功とimport成功は別なので、import確認までやります。

**確認ポイント**: `ok` が出る。


## Knock 044: scikit-learnをインストールする

**目的**: scikit-learnを現在の仮想環境に入れる。

````bash
python -m pip install scikit-learn
````
**解説**: パッケージ名を変えるだけで同じ型を再利用できます。

**確認ポイント**: `python -m pip show scikit-learn` で確認する。


## Knock 045: scikit-learnのimport確認をする

**目的**: scikit-learnがPythonから読めるか確認する。

````bash
python -c "import sklearn; print("ok")"
````
**解説**: インストール成功とimport成功は別なので、import確認までやります。

**確認ポイント**: `ok` が出る。


## Knock 046: jupyterをインストールする

**目的**: jupyterを現在の仮想環境に入れる。

````bash
python -m pip install jupyter
````
**解説**: パッケージ名を変えるだけで同じ型を再利用できます。

**確認ポイント**: `python -m pip show jupyter` で確認する。


## Knock 047: jupyterのimport確認をする

**目的**: jupyterがPythonから読めるか確認する。

````bash
python -c "import jupyter; print("ok")"
````
**解説**: インストール成功とimport成功は別なので、import確認までやります。

**確認ポイント**: `ok` が出る。


## Knock 048: pytestをインストールする

**目的**: pytestを現在の仮想環境に入れる。

````bash
python -m pip install pytest
````
**解説**: パッケージ名を変えるだけで同じ型を再利用できます。

**確認ポイント**: `python -m pip show pytest` で確認する。


## Knock 049: pytestのimport確認をする

**目的**: pytestがPythonから読めるか確認する。

````bash
python -c "import pytest; print("ok")"
````
**解説**: インストール成功とimport成功は別なので、import確認までやります。

**確認ポイント**: `ok` が出る。


## Knock 050: blackをインストールする

**目的**: blackを現在の仮想環境に入れる。

````bash
python -m pip install black
````
**解説**: パッケージ名を変えるだけで同じ型を再利用できます。

**確認ポイント**: `python -m pip show black` で確認する。


## Knock 051: blackのimport確認をする

**目的**: blackがPythonから読めるか確認する。

````bash
python -c "import black; print("ok")"
````
**解説**: インストール成功とimport成功は別なので、import確認までやります。

**確認ポイント**: `ok` が出る。


## Knock 052: ruffをインストールする

**目的**: ruffを現在の仮想環境に入れる。

````bash
python -m pip install ruff
````
**解説**: パッケージ名を変えるだけで同じ型を再利用できます。

**確認ポイント**: `python -m pip show ruff` で確認する。


## Knock 053: ruffのimport確認をする

**目的**: ruffがPythonから読めるか確認する。

````bash
python -c "import ruff; print("ok")"
````
**解説**: インストール成功とimport成功は別なので、import確認までやります。

**確認ポイント**: `ok` が出る。


## Knock 054: ipykernelをインストールする

**目的**: ipykernelを現在の仮想環境に入れる。

````bash
python -m pip install ipykernel
````
**解説**: パッケージ名を変えるだけで同じ型を再利用できます。

**確認ポイント**: `python -m pip show ipykernel` で確認する。


## Knock 055: ipykernelのimport確認をする

**目的**: ipykernelがPythonから読めるか確認する。

````bash
python -c "import ipykernel; print("ok")"
````
**解説**: インストール成功とimport成功は別なので、import確認までやります。

**確認ポイント**: `ok` が出る。


## Knock 056: tqdmをインストールする

**目的**: tqdmを現在の仮想環境に入れる。

````bash
python -m pip install tqdm
````
**解説**: パッケージ名を変えるだけで同じ型を再利用できます。

**確認ポイント**: `python -m pip show tqdm` で確認する。


## Knock 057: tqdmのimport確認をする

**目的**: tqdmがPythonから読めるか確認する。

````bash
python -c "import tqdm; print("ok")"
````
**解説**: インストール成功とimport成功は別なので、import確認までやります。

**確認ポイント**: `ok` が出る。


## Knock 058: pyyamlをインストールする

**目的**: pyyamlを現在の仮想環境に入れる。

````bash
python -m pip install pyyaml
````
**解説**: パッケージ名を変えるだけで同じ型を再利用できます。

**確認ポイント**: `python -m pip show pyyaml` で確認する。


## Knock 059: pyyamlのimport確認をする

**目的**: pyyamlがPythonから読めるか確認する。

````bash
python -c "import yaml; print("ok")"
````
**解説**: インストール成功とimport成功は別なので、import確認までやります。

**確認ポイント**: `ok` が出る。


## Knock 060: requestsをインストールする

**目的**: requestsを現在の仮想環境に入れる。

````bash
python -m pip install requests
````
**解説**: パッケージ名を変えるだけで同じ型を再利用できます。

**確認ポイント**: `python -m pip show requests` で確認する。


## Knock 061: requestsのimport確認をする

**目的**: requestsがPythonから読めるか確認する。

````bash
python -c "import requests; print("ok")"
````
**解説**: インストール成功とimport成功は別なので、import確認までやります。

**確認ポイント**: `ok` が出る。


## Knock 062: richをインストールする

**目的**: richを現在の仮想環境に入れる。

````bash
python -m pip install rich
````
**解説**: パッケージ名を変えるだけで同じ型を再利用できます。

**確認ポイント**: `python -m pip show rich` で確認する。


## Knock 063: richのimport確認をする

**目的**: richがPythonから読めるか確認する。

````bash
python -c "import rich; print("ok")"
````
**解説**: インストール成功とimport成功は別なので、import確認までやります。

**確認ポイント**: `ok` が出る。


## Knock 064: pip checkで依存関係を確認する

**目的**: 依存関係の破綻がないか確認する。

````bash
python -m pip check
````
**解説**: バージョン衝突があるとここで分かる場合があります。

**確認ポイント**: `No broken requirements found.` が出ればよい。


## Knock 065: pip cacheの場所を見る

**目的**: pipのキャッシュ場所を確認する。

````bash
python -m pip cache dir
````
**解説**: ディスク容量が気になるときに重要です。

**確認ポイント**: キャッシュディレクトリが表示される。


## Knock 066: pip cache容量を確認する

**目的**: pipキャッシュ容量を確認する。

````bash
du -sh $(python -m pip cache dir)
````
**解説**: pipはダウンロード済みファイルを保存するため、容量を使うことがあります。

**確認ポイント**: 容量が表示される。


## Knock 067: pip cacheを削除する

**目的**: pipキャッシュを掃除する。

````bash
python -m pip cache purge
````
**解説**: 容量不足時の選択肢です。必要なパッケージ自体は消えません。

**確認ポイント**: 削除されたファイル数が表示される。


## Knock 068: site-packagesの場所を見る

**目的**: ライブラリ配置場所を確認する。

````bash
python -c "import site; print(site.getsitepackages())"
````
**解説**: どの環境に入っているか確認する材料になります。

**確認ポイント**: `.venv` 配下が出るとよい。


## Knock 069: ユーザサイトを確認する

**目的**: Pythonのsite設定を確認する。

````bash
python -m site
````
**解説**: ユーザ領域にパッケージが混ざる問題の調査に使えます。

**確認ポイント**: site情報が表示される。


## Knock 070: モジュール実行の形を覚える

**目的**: Pythonモジュールをコマンドとして実行する。

````bash
python -m pip list | head
````
**解説**: `python -m ...` は環境ズレを避ける基本形です。

**確認ポイント**: パッケージ一覧の先頭が表示される。


## Knock 071: requirementsを行数確認する

**目的**: 依存パッケージ数を把握する。

````bash
wc -l requirements.txt
````
**解説**: 依存が増えすぎていないか見る簡易指標です。

**確認ポイント**: 行数が出る。


## Knock 072: requirementsを検索する

**目的**: 特定依存が固定されているか確認する。

````bash
grep -i numpy requirements.txt
````
**解説**: 再現性確認でよく使います。

**確認ポイント**: numpy行が出る。


## Knock 073: 実行時刻をログに残す

**目的**: Python実行ログを保存する。

````bash
python src/check.py 2>&1 | tee logs_python_check.txt
````
**解説**: 環境確認もログに残せると後で見返せます。

**確認ポイント**: ログファイルができる。


## Knock 074: Pythonとpipの対応を1行で確認する

**目的**: Python本体とpipの対応をまとめて見る。

````bash
python -c "import sys; print(sys.executable)" && python -m pip --version
````
**解説**: 環境トラブル時の最初の確認セットです。

**確認ポイント**: どちらも同じ環境配下を指す。


## Knock 075: 仮想環境名を確認する

**目的**: 有効化中のvenvパスを確認する。

````bash
echo $VIRTUAL_ENV
````
**解説**: 仮想環境に入っていない場合は空です。

**確認ポイント**: `.venv` のパスが出る。


## Knock 076: ipykernelを登録する

**目的**: Jupyterから仮想環境を選べるようにする。

````bash
python -m ipykernel install --user --name ubuntu100 --display-name "Python (ubuntu100)"
````
**解説**: Notebookを使う研究では重要です。

**確認ポイント**: JupyterのKernel一覧に出る。


## Knock 077: pytestで簡単なテストを作る

**目的**: テストファイルを作る。

````bash
mkdir -p tests && cat > tests/test_basic.py <<EOF
def test_basic():
    assert 1 + 1 == 2
EOF
````
**解説**: 環境が壊れていないか確認する最小テストです。

**確認ポイント**: `tests/test_basic.py` ができる。


## Knock 078: pytestを実行する

**目的**: テストをCLIから実行する。

````bash
pytest -q
````
**解説**: 研究コードでも小さなテストがあると安心です。

**確認ポイント**: `1 passed` が出る。


## Knock 079: ruffで構文チェックする

**目的**: Pythonコードを静的チェックする。

````bash
ruff check . || true
````
**解説**: 最初はエラーが出てもよいので、チェックの存在を体験します。

**確認ポイント**: 指摘または正常終了が表示される。


## Knock 080: blackでフォーマット確認する

**目的**: コード整形チェックをする。

````bash
black --check . || true
````
**解説**: チーム開発では整形ルールが大事になります。

**確認ポイント**: 整形が必要なファイルが表示される場合がある。


## Knock 081: 現在環境の概要を保存する

**目的**: 環境情報をレポート化する。

````bash
{ echo "Python:"; python --version; echo "Executable:"; python -c "import sys; print(sys.executable)"; echo "Packages:"; python -m pip list; } > env_report.txt
````
**解説**: トラブル相談時に渡せる情報になります。

**確認ポイント**: `env_report.txt` を確認する。


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

