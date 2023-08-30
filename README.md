# Peep Detection App

ノートパソコンで作業中にのぞき見されていることを検知するアプリです。

## 動作確認OS
- `Windows 11 Pro`


## インストール方法
- [リリースモジュール](https://github.com/hamacom2004jp/peepdet/releases)

1. ダウンロードしたzipファイルを任意のディレクトリで解凍します。
2. 解凍したディレクトリ内の`peepdet.exe`を実行します。
3. しばらくするとタスクトレイに`peepdet`のアイコンが表示されます。
4. トレイアイコンを右クリックし`Setting/Select Face`を押して自分の顔を登録します。
5. トレイアイコンを右クリックして`Start`を押すことで監視を開始します。
6. 監視中に他人がのぞき見していることを検知するとトースト表示します。
7. トーストをクリックすると画像を保存しているフォルダを開きます。
8. トレイアイコンを右クリックして`Setting/Open Folder`を押すことでも画像を保存しているフォルダを開けます。
9. トレイアイコンを右クリックして`Stop`を押すことで監視を終了します。
10. トレイアイコンを右クリックして`Quit`を押すことでアプリが終了します。 


## ビルド方法

### peepdetのビルド環境構築
```
git clone https://github.com/hamacom2004jp/peepdet.git
cd peepdet
python -m venv .venv
.venv\Scripts\activate
python.exe -m pip install --upgrade pip
pip install -r requirements.txt
```

### pyinstallerのブートローダービルド環境構築
ブートローダーをビルドしないと、peepdetがマルウエア判定されてしまう。
vc++のコンパイラを使うため、下記のツールをインストールする。
⇒管理者権限を持ったPowerShellで実行する必要がある

#### Chocolateryインストール
```
AdminPowerShell > Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
```
#### vcbuildtoolsインストール
```
AdminPowerShell > choco install -y python vcbuildtools
```

#### pyinstallerのブートローダービルド＆インストール
peepdetのビルドフォルダで新しいcmdを開いて実行する
```
cd peepdet
git clone https://github.com/pyinstaller/pyinstaller
cd pyinstaller/bootloader
python ./waf all
cd ..
pip install wheel
pip install .
```

#### peepdetのビルド
```
cd ..
pyinstaller peepdet/__main__.py -n peepdet --onefile --collect-all peepdet -i peepdet/start.ico -w --clean
deactivate
```

#### 開発環境でのpeepdetの実行方法
```
cd peepdet
.venv\Scripts\activate
python -m peepdet
```


# Lisence

This project is licensed under the MIT License, see the LICENSE.txt file for details
