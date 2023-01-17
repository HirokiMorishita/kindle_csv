import argparse
import re
import urllib.request as request
import json
import csv
import io
import sys
from datetime import datetime 

parser = argparse.ArgumentParser(
  prog = "amazon_url_to_csv_row",
  description = "convert amazon url to csv row (kindle csv format)"
)
parser.add_argument("url")
parser.add_argument("purchase_date", nargs="?", default= "")
parser.add_argument("-p","--print_format", choices=["csv","tsv"], default= "csv")

def main(args):
  if args.purchase_date:
    purchase_date = parse_purchase_date(args.purchase_date)
  else:
    purchase_date = ""
  asin = parse_asin(args.url)
  book_info = get_book_info(asin)
  amazon_urls = generate_amazon_urls(asin)
  csv_info = dict(book_info, **{
    "ASIN": asin,
    "purchase_date": purchase_date
  }, **amazon_urls)
  print_csv_row(csv_info, args.print_format)

def get_book_info(asin):
  api_url = f"https://api.openbd.jp/v1/get?isbn={asin}"
  req = request.Request(api_url)
  book_info ={}
  with request.urlopen(req) as response:
    book_info_json = json.loads(response.read().decode("utf-8"))
    book_info["title"] = book_info_json[0]["onix"]["DescriptiveDetail"]["TitleDetail"]["TitleElement"]["TitleText"]["content"]
    book_info["authors"] = ";".join(map(lambda author: author["PersonName"]["content"],book_info_json[0]["onix"]["DescriptiveDetail"]["Contributor"])) 
    book_info["publishers"] = book_info_json[0]["onix"]["PublishingDetail"]["Publisher"]["PublisherName"]
    book_info["publication_date"] = datetime.strptime(book_info_json[0]["onix"]["PublishingDetail"]["PublishingDate"][0]["Date"], "%Y%m%d").strftime("%Y/%m/%d")
  return book_info

def parse_asin(url):
  matched = re.search('/([0-9]+)/', url)
  if not matched :
    print("failed. may be url for kindle or not amazon url")
  return matched.group(1)

def parse_purchase_date(purchase_date):
  return datetime.strptime(purchase_date, "%Y年%m月%d日").strftime("%Y/%m/%d")

def generate_amazon_urls(asin):
  return {
    "url":
        f"https://amazon.co.jp/dp/{asin}",
    "image_url":
        f"https://images-na.ssl-images-amazon.com/images/P/{asin}.09.LZZZZZZZ.jpg",
  }
  
def print_csv_row(csv_info, print_format):
  csv_headers = [
      "title", "ASIN", "url", "image_url", "authors", "publishers",
      "publication_date", "purchase_date"
  ]
  row = list(map(lambda header: csv_info[header], csv_headers))
  delimiter =","
  if print_format == "tsv":
    delimiter = "\t"
  config = {'encoding': 'utf-8', 'newline': '', 'write_through': True}
  writer = csv.writer(io.TextIOWrapper(sys.stdout.buffer, **config), delimiter=delimiter)
  writer.writerow(row)
  
main(parser.parse_args())
