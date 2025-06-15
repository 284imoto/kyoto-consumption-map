import pandas as pd

#2025/02/25追加
def process_data_by_ind_block(df):
    # 産業ブロック別で集計を行い、出力する関数
    df['date'] = pd.to_datetime(df['date'], format='%Y%m%d', errors='coerce')
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
    df['ninzu'] = pd.to_numeric(df['ninzu'], errors='coerce')
    grouped_df = df.groupby(['date', 'ind_block']).agg({'ninzu': 'sum', 'amount': 'sum'}).unstack(fill_value=0)
    grouped_df.columns = [f'{col[1]}_{col[0]}' for col in grouped_df.columns]
    return grouped_df.reset_index()

#2025/02/25追加
def process_data_by_agesegment_gender(df):
    # 年代と性別で集計を行い、出力する関数
    df['date'] = pd.to_datetime(df['date'], format='%Y%m%d', errors='coerce')
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
    df['ninzu'] = pd.to_numeric(df['ninzu'], errors='coerce')
    df['age_segment'] = (df['age'] // 10)*10
    df['age_gender'] = df['age_segment'].astype(str) + "_" + df['gender'].astype(str)
    grouped_df = df.groupby(['date', 'age_gender']).agg({'ninzu': 'sum', 'amount': 'sum'}).unstack(fill_value=0)
    grouped_df.columns = [f'{col[1]}_{col[0]}' for col in grouped_df.columns]
    return grouped_df.reset_index()

#2025/02/25追加
def make_ind_age_gender(df):
    df['date'] = pd.to_datetime(df['date'], format='%Y%m%d', errors='coerce')
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
    df['ninzu'] = pd.to_numeric(df['ninzu'], errors='coerce')
    # 新しい分類列を作成
    df['age'] = (df['age'] // 10)*10 #年齢別を10年区切りに加工
    df["category"] = df["ind_block"] + "_" + df["age"].astype(str) + "_" + df["gender"].astype(str)

    # 各カテゴリごとにデータを抽出して分類
    categories = df["category"].unique()  # ユニークなカテゴリ一覧を取得
    category_dict = {cat: df[df["category"] == cat] for cat in categories}  # カテゴリごとにDataFrameを辞書に保存

    # すべてのカテゴリを1つの DataFrame に統合
    merged_df = pd.concat(category_dict.values(), ignore_index=True)
    result_df = merged_df.groupby(['date', 'category']).agg({'ninzu': 'sum', 'amount': 'sum'}).unstack(fill_value=0)
    result_df.columns = [f"{col[1]}_{col[0]}" for col in result_df.columns]
    return result_df

#2025/04/25追加 入力した時系列データの業種ごとの男女別の人数と金額の値を集計する関数
def compute_gender_ratio_by_date_ind(df):
    # date × ind_block × genderで集計
    grouped_df = df.groupby(['date','ind_block','gender'], as_index=False)[['ninzu','amount']].sum()

    #同一date × ind_blockごとの合計をtransformで取得
    day_totals = grouped_df.groupby(['date','ind_block'])[['ninzu','amount']].transform('sum')

    #構成比を算出
    grouped_df['ninzu_ratio'] = (grouped_df['ninzu'] / day_totals['ninzu'] * 100).round(2)
    grouped_df['amount_ratio'] = (grouped_df['amount'] / day_totals['amount'] * 100).round(2)

    return grouped_df

def compute_age_gender_ratio_by_date_ind(df):
    # date × ind_block × genderで集計
    grouped_df = df.groupby(['date','ind_block','age_gender'], as_index=False)[['ninzu','amount']].sum()

    #同一date × ind_blockごとの合計をtransformで取得
    day_totals = grouped_df.groupby(['date','ind_block'])[['ninzu','amount']].transform('sum')

    #構成比を算出
    grouped_df['ninzu_ratio'] = (grouped_df['ninzu'] / day_totals['ninzu'] * 100).round(2)
    grouped_df['amount_ratio'] = (grouped_df['amount'] / day_totals['amount'] * 100).round(2)

    return grouped_df

def split_by_resi1(df, prefecture="京都府"):
    
    prefecture_df = df[df['resi1'] == prefecture]
    non_prefecture_df = df[df['resi1'] != prefecture]
    
    return prefecture_df, non_prefecture_df

#2025/04/06追加
#2025/05/05編集
#指定した期間のみ抽出できるように変更
# 欠損値を0で補完した時系列データを作成する関数
def create_time_series_df(df, date_col, group_col, agg_cols, start_date, end_date, freq="D", fill_value=0, round_digits=2):
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])

    #全組み合わせのインデックス作成
    all_dates = pd.date_range(start=start_date, end=end_date, freq=freq)
    all_groups = df[group_col].unique()
    full_index = pd.MultiIndex.from_product([all_dates, all_groups], names=[date_col, group_col])

    grouped = df.groupby([date_col, group_col])[agg_cols].sum()
    filled = grouped.reindex(full_index, fill_value=fill_value)
    filled = filled.round(round_digits)

    return filled.unstack(fill_value=fill_value)

#郵便番号（post_code）別で集計を行う関数
def aggregate_by_code(df):
    #'date','amount','ninzu'列を適切なデータタイプとして扱う
    df.loc[:, 'date'] = pd.to_datetime(df['date'],format='%Y%m%d',errors='coerce')
    df.loc[:,'amount'] = pd.to_numeric(df['amount'], errors='coerce')
    df.loc[:,'ninzu'] = pd.to_numeric(df['ninzu'], errors='coerce')
    #'code'でまとめる
    grouped_df = df.groupby('post_code').agg({'ninzu': 'sum', 'amount': 'sum'})
    output_df = grouped_df.reset_index()
    return output_df