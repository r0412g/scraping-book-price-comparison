import csv

from playwright.sync_api import Page, sync_playwright

import config


def scrape_books():
    url = config.PAPER_URL

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # get data in relative page
        for page_num in range(1, 4):

            # empty list
            book_title_list = []
            book_price_list = []
            book_isbn_list = []

            if page_num == 1:
                # go to page base url (page1)
                page.goto(url)
            else:
                # go to relative page
                page.get_by_role("button", name=f"{page_num}").click()


            # make sure page loaded
            page.wait_for_selector(f'.item.active[data-position="{page_num}"]')

            # list of page
            book_title_list = get_book_title(page, page_num)
            book_price_list = get_book_price(page, page_num)
            book_isbn_list = get_book_isbn(page, book_title_list, page_num)[0]
            ebook_price_list = get_book_isbn(page, book_title_list, page_num)[1]

            # zip list data to tuple
            data_rows = zip(book_title_list, book_isbn_list, book_price_list, ebook_price_list)

            # write data into csv file
            write_data_to_csv(data_rows, page_num)


        # close browser
        browser.close()


''' get book title '''
def get_book_title(page: Page, page_num: int) -> list:

    title_list = page.locator(".search-product-block").locator(".product-name").all_text_contents()

    # only get 10 data in page 3
    if page_num == 3:
        return title_list[0:10]

    return title_list

''' get paper book price '''
def get_book_price(page: Page, page_num: int) -> list:

    # make sure price selector shows
    page.wait_for_selector(".product-price")

    # get price text
    price_and_discount_list = page.locator(".product-price").all_text_contents()

    # only get 10 data in page 3
    if page_num == 3:
        return price_and_discount_list[0:10]
    
    return price_and_discount_list

''' get book ISBN'''
def get_book_isbn(page: Page, book_title_list: list, page_num: int):

    isbn_list = []
    ebook_price_list = []
            
    # get ISBN in book's page
    for book_title in book_title_list:

        # click button to redirect to book's product page
        # page.get_by_role("link", name=f"{book_title}", description=f"{book_title}", exact=True).click()
        page.locator("a").filter(has_text=f"{book_title}").click()

        # make sure enter product page
        page.wait_for_url("**product**")

        # get book's ISBN
        isbn = page.get_by_text("ISBN13 /").inner_text()
        isbn_list.append(isbn)

        # get ebook's price
        if page.get_by_text("電子書$").count() > 0:
            ebook_price = page.get_by_text("電子書$").inner_text()
        else:
            ebook_price = 0
        ebook_price_list.append(ebook_price)

        # go back to best sellers page
        page.go_back()

        if page_num != 1:            
            page.get_by_role("button", name=f"{page_num}").click()

            # make sure page loaded
            page.wait_for_selector(f'.item.active[data-position="{page_num}"]')

        # make sure go back to best sellers page
        page.wait_for_url("**best-sellers**")

    return isbn_list, ebook_price_list


''' write book's data into books_paper.csv'''
def write_data_to_csv(data: tuple, page: int):
    
    file_path = f"{config.RAW_DIR}/books_combined.csv"

    with open(file_path, 'a+', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)

        # write header when on page 1
        if page == 1:
            writer.writerow(['Title', 'ISBN', 'Paper book price', 'e-book price'])

        # write data into file
        writer.writerows(data)