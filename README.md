# amazon-invoice-renamer

Amazon の請求書ファイル名を電子帳簿保存法に対応した名前に一気に変換するプログラム

## 使い方

1. Amazon からダウンロードした請求書を target_files ディレクトリに保存する。
2. main.py を実行する。

上記の作業で、target_files ディレクトリ内のファイルが
yyyyMMdd-Amazon-金額-請求書.pdf
という名前でリネームされる。
