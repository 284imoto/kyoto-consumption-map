import pandas as pd

#sort_columnを指定する関数
def get_sort_column():
    sort_column = input("並び替えの基準を選択してください（a: amount / n: ninzu）：")
    
    if sort_column == "a":
        return "amount"
    elif sort_column == "n":
        return "ninzu"
    else:
        return "amount"  # デフォルト値

#引数でsort_columnを受け取るように変更
#ユーザー入力が有効か確認し、降順で並び替え
def sort_by_ninzu_amount(df,sort_column):
    if sort_column in df.columns:
        sorted_df = df.sort_values(by=sort_column,ascending=False).reset_index()
        sorted_df = sorted_df.drop('index',axis=1)
        # rank列を追加（amount列を基準に降順で順位を付ける）
        sorted_df['rank'] = sorted_df[sort_column].rank(method="first", ascending=False).astype(int)
        return sorted_df
    else:
        print(f"入力された列名'{sort_column}'は存在しません。ninzu/amountを入力してください")