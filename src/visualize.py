import folium
import pandas as pd

def create_map_with_graduation(matched_area, value_column,gender):
    # matched_area: GeoDataFrame, 可視化する地理データ
    # value_column: str, 色分けの基準となる列名
    if matched_area is None or matched_area.empty:
        print("該当するエリア無し")
        return None

    # 京都市の中心を地図の中心に設定
    m = folium.Map(location=[35.0116, 135.7681], zoom_start=12)

    # 色のリストを定義（上位10件のために10色用意
    top_colors = [
        "#ff4500",  # orange-red: rank 1 (情熱)
        "#ff7f00",  # dark orange: rank 2 (活力)
        "#ffd700",  # gold: rank 3 (輝き)
        "#32cd32",  # lime green: rank 4 (元気)
        "#00fa9a",  # medium spring green: rank 5 (新鮮)
        "#00ced1",  # dark turquoise: rank 6 (知的)
        "#1e90ff",  # dodger blue: rank 7 (冷静)
        "#6a5acd",  # slate blue: rank 8 (安定)
        "#9932cc",  # dark orchid: rank 9 (優雅)
        "#8b008b"   # dark magenta: rank 10 (個性)
    ]
    other_color = "#d3d3d3"  # dark gray: 11位以降

    # value_column を基準に順位を計算
    matched_area = matched_area.sort_values(by=value_column, ascending=False)
    matched_area["rank"] = matched_area[value_column].rank(method="first", ascending=False)
    
    # 最大rankを事前に計算
    max_rank = matched_area["rank"].max()

    # スタイル関数
    def style_function(feature):
        rank = feature["properties"].get("rank", 0)
        
        #Noneチェック
        if rank is None:
            rank = max_rank + 1
        
        if rank <= 10:
            color = top_colors[int(rank) - 1]  # 1位が0番目の色に対応
        else:
            color = other_color
        return {
            "fillColor": color,  # 順位に応じた色
            "color": "black",    # 境界線の色
            "weight": 1,         # 境界線の太さ
            "fillOpacity": 0.7     # 塗りつぶし透明度
        }

    # GeoJSONを地図に追加
    folium.GeoJson(
        matched_area,
        style_function=style_function,
        tooltip=folium.features.GeoJsonTooltip(
            fields=["post_code", "full_address", value_column, "rank"],  # ツールチップに順位も表示
            labels=True,
            sticky=True
        )
    ).add_to(m)

    # カラースケールの説明を追加
    legend_html = f"""
    <div style="
        position: fixed; 
        bottom: 2px; left: 2px; width: 250px; height: 100px; 
        background-color: white; z-index:9999; font-size:12px; 
        border:2px solid grey; padding:5px;">
        <i style="background:#ff4500; width:20px; height:20px; display:inline-block;"></i> 1位
        <i style="background:#ff7f00; width:20px; height:20px; display:inline-block;"></i> 2位
        <i style="background:#ffd700; width:20px; height:20px; display:inline-block;"></i> 3位
        <i style="background:#32cd32; width:20px; height:20px; display:inline-block;"></i> 4位
        <i style="background:#00fa9a; width:20px; height:20px; display:inline-block;"></i> 5位<br>
        <i style="background:#00ced1; width:20px; height:20px; display:inline-block;"></i> 6位
        <i style="background:#1e90ff; width:20px; height:20px; display:inline-block;"></i> 7位
        <i style="background:#6a5acd; width:20px; height:20px; display:inline-block;"></i> 8位
        <i style="background:#9932cc; width:20px; height:20px; display:inline-block;"></i> 9位
        <i style="background:#8b008b; width:20px; height:20px; display:inline-block;"></i> 10位<br>
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))

    print("該当エリアを地図上に表示")
    return m

def save_map(map_object, filename="local_map.html"):
    """
    マップオブジェクトを保存する関数。
    map_object が None の場合は警告メッセージを出力する。

    Parameters:
    map_object : folium.Map または None
        作成したマップオブジェクト
    filename : str, optional
        保存するファイル名（デフォルトは "local_map.html"）
    """
    if map_object is None:
        print("抽出条件が間違っています")
    else:
        map_object.save(filename)