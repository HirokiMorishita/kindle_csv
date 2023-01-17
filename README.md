## 概要
購入したkindle本の一覧をまとめたcsvファイルを生成します。

## 使用方法
1. kindle for pcが生成するキャッシュファイルをkindle_csv.pyと同じディレクトリに入れてください。キャッシュファイルは以下のパスに存在します。
    - windows
      - ~/AppData/Local/Amazon/Kindle/Cache/KindleSyncMetadataCache.xml
      - シンボリックリンクを張るコマンド
      ```bash
        ln -s $(wslpath "$(wslvar USERPROFILE)")/AppData/Local/Amazon/Kindle/Cache/KindleSyncMetadataCache.xml ./
      ```
    - mac
      - ~/Library/Containers/com.amazon.Kindle/Data/Library/Application Support/Kindle/Cache/KindleSyncMetadataCache.xml

2. 実行すると./kindle_book_list.csvにcsvファイルが生成されます
    ```bash
    python kindle_csv.py
    ```

## csvファイルの内容
生成されるcsvファイルには以下の情報が含まれます。
- title
  - 書名
- ASIN
  - Amazonが発行する識別子。Amazon Standard Item Number.
- url
  - Amazonの商品ページへのリンク
- image_url
  - 書影画像へのリンク
- authors
  - 著者名
- publishers
  - 出版社名
- publication_date
  - 出版日
- purchase_date
  - 購入日

## 参考にしたURL
https://note.com/nanigashi/n/n8a1e590d2ea3

## 物理本の取り込み
物理本をkindle本と同じ形式で管理するには以下のコマンドを叩いてください。
その物理本のcsvレコード１行がクリップボードにコピーされます。
```bash
# url: 物理本のamazonページへのurl. ターミナルでは&のエスケープが必要になるので""で括るとよいです
# purchase_date: 物理本の購入日。省略した場合、空文字列が記録されます
python3 amazon_url_to_csv_row.py "$url" [$purchase_date] | pbcopy
```
-p tsvを指定するとtsv形式で出力します。
スプレッドシートに貼る場合はtsvでないとうまく認識できませんでした
```bash
python3 amazon_url_to_csv_row.py -p tsv "$url" [$purchase_date]  | pbcopy
```