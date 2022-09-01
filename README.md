# Spoofing Designer

VLP-16に対するChosen Pattern Injectionを3Dで実現するためのデータ作成のためのスクリプトたち

## データ形式(深度画像)

FGに入力するのは1次元の波形データだが、それを生成するための中間表現として2次元のcsvデータを用意。
要は深度画像。

- row: 垂直角ごとのデータ(16本)
- column: 水平角(0.2°)ごとのデータ

セルの値は0を基準として奥行方向につけたい遅延量(整数)である。単位あたりの遅延距離はFG入力データの
時間間隔に依存するが、32nsであれば値1あたり0.15m奥にずれる。
点を出したくないセルには数字でない何かを入れておく("-"でも空白でもよい)。

## main.py: データ作成

```
usage: main.py [-h] [--no_editor] [-d DISTANCE_M] path

positional arguments:
  path                  Path to the file to watch

optional arguments:
  -h, --help            show this help message and exit
  --no_editor           don't open editor
  -d DISTANCE_M, --distance_m DISTANCE_M
                        distance in meters
```

深度画像を脳内で作るのはつらいので、CSVを編集するとリアルタイムに3Dで表示してくれる環境を用意する。
csvを用意し、main.pyを実行するとOpen3Dのウィンドウとcsvの編集ウィンドウ(恐らくExcel)が開く。
この状態でcsvを編集し、保存するとOpen3Dの画面が更新される。

csvの編集画面を開きたくない場合は--no_editorオプションを付ける。

オブジェクトを出す距離を指定したい場合は--distance_mで指定可能(デフォルトは100m)。

## img_to_bin_csv.py

2次元の白黒画像からmain.pyで使う深度画像を生成するスクリプト
