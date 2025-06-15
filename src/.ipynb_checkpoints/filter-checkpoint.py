import pandas as pd

#2025/01/07追加
#1日単位、週単位、月単位、曜日単位で絞り込む関数
def filter_by_date(df, start_date=None, end_date=None, dates=None, weeks=None, months=None, weekdays=None):
    filtered_df = df.copy()
    
    #条件ごとにフィルタリング
    if start_date and end_date:
        # マスクを作成して条件に合致する行を抽出
        mask = (df['date'] >= start_date) & (df['date'] <= end_date)
        filtered_df = df.loc[mask]
    if dates:
        #文字列のリストをdatetimeに変換
        dates = pd.to_datetime(dates)
        filtered_df = filtered_df[filtered_df["date"].isin(dates)]
    if weeks:
        week_ranges = [(pd.to_datetime(week), pd.to_datetime(week) + pd.Timedelta(days=6)) for week in weeks]
        week_mask = pd.Series(False, index=filtered_df.index)
        for start, end in week_ranges:
            week_mask |= (filtered_df["date"] >= start) & (filtered_df["date"] <= end)
        filtered_df = filtered_df[week_mask]
    if months:
        filtered_df = filtered_df[filtered_df["date"].dt.month.isin(months)]
    if weekdays:
        filtered_df = filtered_df[filtered_df["date"].dt.weekday.isin(weekdays)] #月曜日-0,日曜日-6
    return filtered_df

#業種ブロックで絞り込む関数
def filter_by_ind_blocks(df, ind_blocks):
    if not ind_blocks:
        return df
    if isinstance(ind_blocks, str):
        # カンマで分割してリストに変換
        ind_blocks = [s.strip() for s in ind_blocks.split(",")]
    elif not isinstance(ind_blocks, list):
        raise ValueError("ind_blocksは文字列またはリストである必要があります")
    if ind_blocks:
        return df[df["ind_block"].isin(ind_blocks)]

#居住地ブロックで絞り込む関数
def filter_by_resi_blocks(df, resi_blocks):
    if not resi_blocks:
        return df
    if isinstance(resi_blocks, str):
        # カンマで分割してリストに変換
        resi_blocks = [s.strip() for s in resi_blocks.split(",")]
    if resi_blocks:
        return df[df["residence_block"].isin(resi_blocks)]

#resi2で更に絞り込む関数
def filter_by_resi2_blocks(df, resi2_blocks):
    if not resi2_blocks:
        return df
    if isinstance(resi2_blocks, str):
        # カンマで分割してリストに変換
        resi2_blocks = [s.strip() for s in resi2_blocks.split(",")]
    if resi2_blocks:
        return df[df["resi2"].isin(resi2_blocks)]

#業種で絞り込む関数
def filter_by_ind(df,ind):
    if ind:
        return df[df["ind"].str.contains(ind,na=False)]
    return df

#性別で絞り込む関数
def filter_by_gender(df,gender):
    if gender:
        return df[df["gender"] == int(gender)]
    return df

#年齢で絞り込む関数
def filter_by_age(df,age_range):
    if age_range:
        min_age,max_age = map(int,age_range.split("-"))
        return df[(df["age"] >= min_age) & (df["age"] <= max_age)]
    return df