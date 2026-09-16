import matplotlib.pyplot as plt

import config


def plot_all(df, stats):

    # make sure visualize can shows Chinese font
    plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
    # 正常顯示負號
    plt.rcParams['axes.unicode_minus'] = False

    plot_ebook_ratio(df)
    plot_price_diff_histogram(df)
    plot_price_diff_mean_median(stats)
    plot_avg_price_comparison(stats)
    plot_more_expensive_count(stats)
    plot_price_vs_diff(df)
    plot_price_distribution(df)
    plot_price_boxplot(df)
    

# 圓餅圖：有電子書比例
def plot_ebook_ratio(df):
    counts = df["has_ebook"].value_counts()
    plt.figure()
    plt.pie(counts, labels=["有電子書", "無電子書"], autopct="%1.1f%%")
    plt.title("書籍有電子書版本的比例")
    plt.savefig(f"{config.OUTPUT_DIR}/ebook_ratio_pie.png")
    plt.close()


# 直方圖：價差百分比分布
def plot_price_diff_histogram(df):
    df_has_ebook = df[df["has_ebook"] == True]
    plt.figure()
    plt.hist(df_has_ebook["price_diff_pct"], bins=15)
    plt.xlabel("價差百分比 (%)")
    plt.ylabel("書籍數量")
    plt.title("電子書與紙本價格的價差分布")
    plt.savefig(f"{config.OUTPUT_DIR}/price_diff_histogram.png")
    plt.close()

# 長條圖：平均與中位數價差百分比
def plot_price_diff_mean_median(stats):
    plt.figure()
    plt.bar(["平均值", "中位數"], [stats["mean_price_diff_pct"], stats["median_price_diff_pct"]])
    plt.ylabel("價差百分比 (%)")
    plt.title("電子書與紙本價格的平均/中位數價差")
    plt.savefig(f"{config.OUTPUT_DIR}/price_diff_mean_median_bar.png")
    plt.close()

# 長條圖：紙本 vs 電子書平均價格
def plot_avg_price_comparison(stats):
    plt.figure()
    plt.bar(["紙本平均價", "電子書平均價"], [stats["avg_paper_price"], stats["avg_ebook_price"]])
    plt.ylabel("價格")
    plt.title("紙本與電子書平均價格比較")
    plt.savefig(f"{config.OUTPUT_DIR}/avg_price_comparison_bar.png")
    plt.close()

# 長條圖：電子書較貴 vs 較便宜 的數量
def plot_more_expensive_count(stats):
    more_expensive = stats["more_expensive_ebooks"]["count"]
    cheaper = stats["more_expensive_ebooks"]["total"] - more_expensive
    plt.figure()
    plt.bar(["電子書較貴", "電子書較便宜"], [more_expensive, cheaper])
    plt.ylabel("書籍數量")
    plt.title("電子書相對紙本的價格高低分布")
    plt.savefig(f"{config.OUTPUT_DIR}/more_expensive_count_bar.png")
    plt.close()

# 散佈圖：紙本價 vs 價差百分比關聯
def plot_price_vs_diff(df):
    df_has_ebook = df[df["has_ebook"] == True]
    plt.figure()
    plt.scatter(df_has_ebook["paper_price"], df_has_ebook["price_diff_pct"])
    plt.xlabel("紙本原價")
    plt.ylabel("價差百分比 (%)")
    plt.title("紙本價格與電子書價差的關聯")
    plt.savefig(f"{config.OUTPUT_DIR}/price_vs_diff_scatter.png")
    plt.close()

# 疊加直方圖：紙本 vs 電子書價格分布
def plot_price_distribution(df):
    df_has_ebook = df[df["has_ebook"] == True]
    plt.figure()
    plt.hist(df["paper_price"], alpha=0.5, label="紙本")
    plt.hist(df_has_ebook["ebook_price"], alpha=0.5, label="電子書")
    plt.xlabel("價格")
    plt.ylabel("書籍數量")
    plt.legend()
    plt.title("紙本與電子書價格分布對比")
    plt.savefig(f"{config.OUTPUT_DIR}/price_distribution_overlay.png")
    plt.close()

# 箱型圖：有無電子書兩組的紙本價格分布
def plot_price_boxplot(df):
    has_ebook_prices = df[df["has_ebook"] == True]["paper_price"]
    no_ebook_prices = df[df["has_ebook"] == False]["paper_price"]
    plt.figure()
    plt.boxplot([has_ebook_prices, no_ebook_prices], label=["有電子書", "無電子書"])
    plt.ylabel("紙本原價")
    plt.title("有無電子書版本的紙本價格分布比較")
    plt.savefig(f"{config.OUTPUT_DIR}/price_boxplot.png")
    plt.close()