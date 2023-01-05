## 概要
購入したkindle本の一覧をまとめたcsvファイルを生成します。

## 使用方法
1. kindle for pcが生成するキャッシュファイルをkindle_csv.pyと同じディレクトリに入れてください。キャッシュファイルは以下のパスに存在します。
    - windows
      - ~/AppData/Local/Amazon/Kindle/Cache/KindleSyncMetadataCache.xml
    - mac
      - ~/Library/Containers/com.amazon.Kindle/Data/Library/Application Support/Kindle/Cache/KindleSyncMetadataCache.xml

2. 実行するとcsvファイルが生成されます
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