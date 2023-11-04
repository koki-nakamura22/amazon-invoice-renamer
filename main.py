import glob
import os
import re

from pdfminer.high_level import extract_text

# PDFからテキストを抽出する関数
def extract_info_from_pdf(pdf_path):
    text = extract_text(pdf_path)

    # 発行者と年月日を見つけるための正規表現パターン
    date_pattern1 = r'請求書発行日\s*(\d{4}-\d{2}-\d{2})'
    date_pattern2 = r'請求日:\s*(\d{4}/\d{2}/\d{2})'
    price_pattern1 = r'合計￥([\d,]+)購入明細'
    price_pattern2 = r'￥(\d+,\d+)(?=\s*\n*\s*合計\s*\n*\s*\(税込\))'

    # テキストから発行者と年月日を抽出
    date1 = re.search(date_pattern1, text)
    date2 = re.search(date_pattern2, text)
    prices1 = re.findall(price_pattern1, text)
    prices2 = re.findall(price_pattern2, text)

    def sum(prices):
        total_price = 0
        for p in prices:
            total_price += int(p.replace(',', ''))
        return total_price

    # 見つかった場合はそれぞれのグループを返す
    if date1 and prices1:
        return date1.group(1).replace('-', ''), 'Amazon', sum(prices1)
    if date2 and prices2:
        return date2.group(1).replace('/', ''), 'Amazon', sum(prices2)

    raise ValueError("Could not find the issuer or date")

# ファイル名を変更する関数
def rename_pdf_file(pdf_path, new_name):
    # ファイルのディレクトリと拡張子を取得
    directory = os.path.dirname(pdf_path)
    extension = os.path.splitext(pdf_path)[1]

    # 新しいファイルパスを作成
    new_path = os.path.join(directory, f"{new_name}{extension}")

    # ファイル名を変更
    os.rename(pdf_path, new_path)
    print(f"Renamed '{pdf_path}' to '{new_path}'")

def main():
    current_dir = os.path.dirname(__file__)
    files = glob.glob(os.path.join(current_dir, 'target_files', '*'))
    for file in files:
        try:
            date, issuer, price = extract_info_from_pdf(file)
            new_name = f"{date}-{issuer}-{price}-請求書"
            rename_pdf_file(file, new_name)
        except Exception as e:
            print(f"Error: {e}")


if __name__ == '__main__':
    main()
