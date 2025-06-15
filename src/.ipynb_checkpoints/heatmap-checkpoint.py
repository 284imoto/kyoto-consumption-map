import folium
import numpy as np
from branca.colormap import linear

def create_map_with_heatmap(matched_area, value_column, log_scale=True):
    """
    GeoDataFrame の value_column に基づき、
    オプションで対数変換（log1p）をかけた連続カラースケールを用いたヒートマップ風ビジュアライゼーションを作成する。

    Parameters:
    matched_area: GeoDataFrame
        可視化対象の地理データ
    value_column: str
        色分けの基準となる数値列名
    log_scale: bool, optional
        True の場合、np.log1p を適用してから色分け（デフォルト True）

    Returns:
    folium.Map または None
    """
    if matched_area is None or matched_area.empty:
        print("該当するエリア無し")
        return None

    # 地図の中心を京都市に設定
    m = folium.Map(location=[35.0116, 135.7681], zoom_start=12)

    # データコピー＆値の準備
    df = matched_area.copy()
    # 郵便番号を文字列化してカンマ区切りを無効化
    df['post_code'] = df['post_code'].astype(str)
    target_col = value_column
    if log_scale:
        df['log_val'] = np.log1p(df[value_column])
        target_col = 'log_val'

    # 値の最小・最大を取得
    min_val = df[target_col].min()
    max_val = df[target_col].max()

    # 連続カラーマップを作成
    colormap = linear.YlOrRd_09.scale(min_val, max_val)
    colormap.caption = f"{'log1p(' + value_column + ')' if log_scale else value_column} の値"
    m.add_child(colormap)

    # GeoJSON にスタイル関数とツールチップを適用
    folium.GeoJson(
        df,
        style_function=lambda feature: {
            'fillColor': colormap(feature['properties'][target_col]),
            'color': 'black',
            'weight': 1,
            'fillOpacity': 0.8
        },
        tooltip=folium.GeoJsonTooltip(
            fields=['post_code', 'full_address', value_column, target_col],
            aliases=['郵便番号', '住所', '元の値', '表示値'],
            localize=True,
            sticky=True
        )
    ).add_to(m)

    print("該当エリアを地図上に表示")
    return m


def save_map(map_object, filename="local_map.html"):
    """
    マップオブジェクトを保存する。
    """
    if map_object is None:
        print("抽出条件が間違っています")
    else:
        map_object.save(filename)