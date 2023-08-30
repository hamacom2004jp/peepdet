# Peep Detection App

ノートパソコンで作業中にのぞき見されていることを検知するアプリです。

1. 起動するとタスクトレイにアイコンが表示されます。
2. トレイアイコンを右クリックして`Setting`を押すことで自分の顔を登録します。
3. トレイアイコンを右クリックして`Start`を押すことで監視を開始します。
4. 監視中に他人がのぞき見していることを検知するとトースト表示します。
5. トーストをクリックすると画像を保存しているフォルダを開きます。
6. トレイアイコンを右クリックして`Stop`を押すことで監視を終了します。
7. トレイアイコンを右クリックして`Quit`を押すことでアプリが終了します。 

## 動作確認OS
- `Windows 11 Pro`

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
