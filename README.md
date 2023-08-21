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

## 開発環境構築メモ

```
python -m venv .venv
.venv\Scripts\activate
python.exe -m pip install --upgrade pip
pip install -r requirements.txt
python -m peepdet
pyinstaller peepdet/__main__.py -n peepdet --onefile --collect-all peepdet -i peepdet/start.ico -w --clean
deactivate
```

