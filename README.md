# Responce Recorder　治療効果判定記録ツール
術前治療効果判定をPre画像とPost画像を比較しながら記録が出来るツールです。
<img src=demo/demo_0.gif width=480 height=300>　　

----------

# Install
1. `git clone` or ダウンロード

   ```
   # git cloneの場合
   git clone git@github.com:TakedaKatsuji/ResponseRecorder.git
   ```
2. `git clone` or ダウンロード&解凍したディレクトリに移動する
3. `conda create`する

   ```
   conda env create -f env.yml
   ```
# How to use
## 1. dataディレクトリの構造
    ```sh
    data
    ├── patient_1
    │   ├── Post
    │   │   ├── 001_NBI_001.jpg
    │   │   ├── 001_NBI_002.png
    │   │   ├── 001_iod_001.jpg
    │   │   ├── 001_iod_002.jpg
    │   │   ├── 001_normal_001.jpg
    │   │   └── 001_normal_002.jpg
    │   └── Pre
    │       ├── 001_NBI_001.jpg
    │       ├── 001_NBI_002.jpg
    │       ├── 001_NBI_003.jpg
    │       ├── 001_iod_001.jpg
    │       ├── 001_iod_002.jpg
    │       ├── 001_iod_003.jpg
    │       ├── 001_nomal_003.jpg
    │       ├── 001_noraml_002.jpg
    │       └── 001_normal_001png
    ```
* 患者ごとにPre/Postフォルダを作成してください
* 患者のフォルダ名はpatient_<患者ID>としてください
* 画像名は<患者ID>_<撮影条件>_<画像番号>としてください

## 2. 以下のスクリプトを実行
 ```sh
   conda activate ResponseRecorder
   streamlit run front.py
```
# Featurs
- プロジェクト名が出力されるExcelの名前になります
- 画像をクリックすると拡大して表示されます
- 画像の表示設定から画像の列数、行数を変更できます
- 画像の表示設定から画像の名前の表示、非表示を選択できます
- Downloadボタンを押すとfront.pyと同じフォルダ内にプロジェクト名のExcelが出力されます
- Excelファイルを読み込ませれば途中から記録できます

# Tips
- 画像が見切れている場合や表示されない場合は、患者の移動ボタンを押すと治ります

## 開発履歴
- 2023/09/22 リリース