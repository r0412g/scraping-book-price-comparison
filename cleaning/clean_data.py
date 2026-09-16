import numpy as np
import pandas as pd

import config


def clean_data():
    # fix Chinese width count
    pd.set_option('display.unicode.east_asian_width', True)

    raw_data_path = f"{config.RAW_DIR}/books_combined.csv"
    save_data_path = f"{config.PROCESSED_DIR}/comparison_result.csv"

    # read raw data
    df = pd.read_csv(raw_data_path)

    ''' regex column '''
    df = paper_book_regex(df)
    df = ebook_price_regex(df)
    df = isbn_regex(df)


    # if ebook price is NA, it means the book doesn't has ebook version
    df["has_ebook"] = df["ebook_price"].notna()

    # price difference between paper book and ebook
    df["price_diff"] = df["paper_price"] - df["ebook_price"]

    # price difference percentage between paper book and ebook
    df["price_diff_pct"] = (df["price_diff"] / df["paper_price"]) * 100

    # save clean data to csv file
    df.to_csv(save_data_path, index=False, encoding='utf-8-sig')

    return df


def paper_book_regex(df):

    # remove ","
    df["paper_price"] = df["paper_price"].str.replace(r"\,", "", regex=True)

    # check if paper price column has Chinese word "折"
    has_discount = df["paper_price"].str.contains("折", na=False)

    # using np.where to replace the string having "折" and the word before it to "", or stay original value
    df["paper_price"] = np.where(
        has_discount, pd.to_numeric(
            df["paper_price"].astype(str).str.replace(r'\d+[\u4e00-\u9fa5]{1}', '', regex=True),
            errors="coerce"
        ), df["paper_price"]
    )

    return df


def paper_book_discount_regex(df):

    # check if paper price column has Chinese word "折"
    has_discount = df["paper_price"].str.contains("折", na=False)

    # using np.where to replace the string having "折" and the word after it to "", or replace to "0"
    df["paper_discount"] = np.where(
        has_discount, df["paper_price"].str.replace(r'[\u4e00-\u9fa5]{1}.+', '', regex=True), "0"
    )

    # replace with "NaN" where paper book hs no discount
    df["paper_discount"] = df["paper_discount"].replace(0, pd.NA)

    return df


def ebook_price_regex(df):

    # replace with "NaN" where ebook price is '0'
    df["ebook_price"] = df["ebook_price"].replace('0', pd.NA)

    # ebook price regex
    df["ebook_price"] = pd.to_numeric(
        df["ebook_price"].astype(str).str.replace(r'\D+', '', regex=True),
        errors="coerce"
    )

    return df

def isbn_regex(df):
        
    # remove "ISBN 13 /"
    df["ISBN"] = df["ISBN"].str.replace(r'([ISBN]{4}.+)/', '', regex=True).astype(str)
    # empty field replace with "NaN"
    df["ISBN"] = df["ISBN"].replace('', pd.NA).astype(str)

    return df
