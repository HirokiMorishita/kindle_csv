# original from https://note.com/nanigashi/n/n8a1e590d2ea3
# kindle Pc cashe file => kindle book list csv
import xml.etree.ElementTree as ET
import csv
import datetime
import re

# windows
# ~/AppData/Local/Amazon/Kindle/Cache/KindleSyncMetadataCache.xml
# mac
# ~/Library/Containers/com.amazon.Kindle/Data/Library/Application Support/Kindle/Cache/KindleSyncMetadataCache.xml
input_file_str = "./KindleSyncMetadataCache.xml"
output_file_str = "./kindle_book_list.csv"
tags = ["ASIN", "title", "authors", "publishers",
        "publication_date", "purchase_date"]
tree = ET.parse(input_file_str)
root = tree.getroot()
books = []

for book_info in root[2]:
    book = {}
    for info in book_info:
        if not info.tag in tags:
            continue
        # authers publishers are nested
        if len(info) == 0:
            book[info.tag] = info.text
        else:
            info_list = [s.text for s in info if s.text]
            book[info.tag] = ';'.join(info_list)
    books.append(book)

converted_books = list(
    map(
        lambda book: book | {
            "url":
                f"https://amazon.co.jp/dp/{book['ASIN']}",
            "image_url":
                f"https://images-na.ssl-images-amazon.com/images/P/{book['ASIN']}.09.LZZZZZZZ.jpg",
            "publication_date":
                datetime.datetime.fromisoformat(
                    re.sub("\+([0-9]{2})([0-9]{2})$",r"+\1:\2",book["publication_date"]) 
                ).strftime("%Y/%m/%d") if book["publication_date"] else "",
            "purchase_date":
                datetime.datetime.fromisoformat(
                    re.sub("\+([0-9]{2})([0-9]{2})$",r"+\1:\2",book["purchase_date"]) 
                ).strftime("%Y/%m/%d") if book["purchase_date"] else "",
        },
        books
    )
)

csv_headers = [
    "title", "ASIN", "url", "image_url", "authors", "publishers",
    "publication_date", "purchase_date"
]
csv_rows = [
    csv_headers
] + list(
    map(
        lambda book: list(map(lambda header: book[header], csv_headers)),
        converted_books
    )
)
with open(output_file_str, 'w', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(csv_rows)
