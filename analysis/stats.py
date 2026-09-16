def compute_stats(df):

    # df data which retain ebook data
    df_has_ebook = df[df["has_ebook"] == True]

    stats = {}
    stats.update(price_diff_summary(df_has_ebook))
    stats.update(avg_price_comparison(df, df_has_ebook))
    stats["more_expensive_ebooks"] = more_expensive_ebooks(df_has_ebook)
    # print(stats)

    return stats

# 價差百分比的平均與中位數
def price_diff_summary(df_has_ebook):
    return {
        "mean_price_diff_pct": df_has_ebook["price_diff_pct"].mean(),
        "median_price_diff_pct": df_has_ebook["price_diff_pct"].median(),
    }

# 紙本與電子書平均價格
def avg_price_comparison(df, df_has_ebook):
    return {
        "avg_paper_price": df["paper_price"].mean(),
        "avg_ebook_price": df_has_ebook["ebook_price"].mean(),
    }

# 電子書比紙本貴的數量與比例
def more_expensive_ebooks(df_has_ebook):
    more_expensive = df_has_ebook[df_has_ebook["price_diff"] < 0]
    return {
        "count": len(more_expensive),
        "total": len(df_has_ebook),
        "pct": len(more_expensive) / len(df_has_ebook) * 100,
        "titles": more_expensive["title"].tolist(),
    }