# 京都市における地域別消費傾向の可視化ツール

## 概要

本リポジトリでは、クレジットカード決済データをもとに、京都市内の地域別消費傾向を可視化した。消費者の性別・年代・居住地・業種といった要因ごとの傾向を地図上に表示することで、地域特性を直感的に把握できることを目的としている。

可視化にはFoliumを用い、ブラウザ上での動的な地図表示を実現した。

## 技術スタック

- Python 3.x
- pandas / numpy
- folium / branca
- geopandas
- jupyter notebook

## デモ

下図は、特定期間における「衣料関連」業種の支出額を地理的に色分けした例である。

![demo](screenshots/map.png)

マウスオーバーにより、町丁目ごとの詳細な情報（業種・年代・性別・居住地など）を表示できる。

## ディレクトリ構成

kyoto-consumption-map/
├── data/
│ └── dummy_data/ # ダミー化済みの分析用データ
│
├── notebooks/
│ └── analysis.ipynb # メインの可視化ノートブック
│
├── src/
│ ├── preprocess.py # 前処理スクリプト
│ ├── visualize.py # Folium可視化モジュール
│ └── aggregate.py # 集計・分類用スクリプト
│
├── requirements.txt
└── README.md


## 実行方法

```bash
# 仮想環境の作成とパッケージインストール（例）
python -m venv venv
source venv/bin/activate   # Windowsでは venv\Scripts\activate
pip install -r requirements.txt

Jupyter Notebookを起動し、notebooks/analysis.ipynb を開くことで可視化処理を再現可能である。

補足事項
データはすべてダミー化済みであり、個人情報を含まない。

分析対象の元データからサンプルとして3万件を使用している。

データ生成手順は data/dummy_data/generate_dummy.py に記載している。
