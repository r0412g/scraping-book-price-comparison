# from analysis.stats import compute_stats
# from analysis.visualize import plot_all
# from cleaning.clean_data import clean_data
from scrapers.book_scraper import scrape_books

if __name__ == "__main__":
    scrape_books()
    # df = clean_data()
    # compute_stats(df)
    # plot_all(df)