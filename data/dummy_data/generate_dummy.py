import pandas as pd
import numpy as np

# 元データの読み込み（ファイル名は適宜変更）
df = pd.read_csv("original_data.csv")

# シード固定（再現性のため）
np.random.seed(42)

# ninzu: 1〜5の整数
df["ninzu"] = np.random.randint(1, 6, size=len(df))

# amount: 1,000〜300,000円の範囲で連続ランダム
df["amount"] = np.round(np.random.uniform(1000, 300000, size=len(df)), 2)

# gender: 1 or 2
df["gender"] = np.random.choice([1, 2], size=len(df))

# age: 10〜80の範囲で10刻み（10, 20, ..., 80）
df["age"] = np.random.choice(range(10, 81, 10), size=len(df))

# 保存
df.to_csv("dummy_data.csv", index=False, encoding='shift-jis')
