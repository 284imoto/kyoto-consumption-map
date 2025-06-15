# 2025/05/03 作成

import pandas as pd

def preprocess(df):
    #左端1列の削除
    if 'Unnamed: 0' in df.columns:
        df = df.drop(columns=['Unnamed: 0'])
        
    #文字列 (object) 型に変換
    df['date'] = df['date'].astype(str)
    #年月日データ分析に最も適切なdatatime[ns]型に変換
    df['date'] = pd.to_datetime(df['date'])

    #5.71で割り、整数部分を代わりに代入する
    df["ninzu"] = (df["ninzu"] / 5.71).astype(int)

    return df

#post_code列を参照して該当するエリアのデータのみをJCBデータから取得する関数
#df1はエリアの郵便番号を含んだdf df2はJCBデータ
def get_areadata_from_raw(df1,df2):
    # post_code列の値から欠損値を削除、重複を排除してリストにする
    post_codes = df1['post_code'].dropna().unique()
    # post_codeがcode列に含まれる行をブール値を用いて取得
    target_df = df2[df2['code'].isin(post_codes)]
    target_df = target_df.rename({"code":"post_code"},axis=1)
    return target_df