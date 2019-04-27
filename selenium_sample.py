import glob
import os
import os.path
import time

from selenium import webdriver

# アクセスするURL
TARGET_URL = "https://www.16personalities.com/ja/%E6%80%A7%E6%A0%BC%E8%A8%BA%E6%96%AD%E3%83%86%E3%82%B9%E3%83%88"

# Seleniumで要素を取得するためにCSSセレクタで指定するときと同じ文字列を宣言しておく
DECISION_MAP = {
    3 : ".agree.max",
    2 : ".agree.med",
    1 : ".agree.min",
    0 : ".neutral",
    -1 : ".disagree.min",
    -2 : ".disagree.med",
    -3 : ".disagree.max",
}

# WindownsとMacでドライバーが違うのでそれぞれ定義しておく
DRIVER_WIN = "chromedriver.exe"
DRIVER_MAC = "./chromedriver"

# 各動作間の待ち時間（秒）
INTERVAL = 3

# ブラウザ起動
driver_path = DRIVER_WIN if os.name == "nt" else DRIVER_MAC
driver = webdriver.Chrome(executable_path=driver_path)
driver.maximize_window()
time.sleep(INTERVAL)


# ファイル名の配列取得
data_list = glob.glob("data/*.csv")

for csv_file in data_list:

    # 対象サイトへアクセス
    driver.get(TARGET_URL)
    time.sleep(INTERVAL)
    
    # ファイルを開く
    with open(csv_file) as f:
        # 一行ずつの値の配列にする
        lines = [int(line.strip()) for line in f.readlines()]
        # １ページ6問ずつなので６こずつループする
        for i in range(0, len(lines), 6):
            # 選択行を取得する
            decisions = driver.find_elements_by_css_selector(".decision:not(.mobile)")
            for j in range(i, i + 6):
                decisions[j % 6].find_element_by_css_selector(DECISION_MAP[lines[j]]).click()
            time.sleep(INTERVAL)
            # 6問入力したらボタンを押下する
            driver.find_element_by_tag_name("button").click()
            time.sleep(INTERVAL)

    # 結果画面のデータを取得
    type_name = driver.find_element_by_class_name("type-name").text
    type_code = driver.find_element_by_class_name("type-code").text
    url = driver.current_url

    # ファイル名から診断対象の人の名前を取得
    file_name = os.path.basename(csv_file)
    person, ext = os.path.splitext(file_name)
    print(f"{person}さんの性格タイプは{type_name}(タイプコード：{type_code})です。\n　詳細：{url}")
    time.sleep(INTERVAL)

# ブラウザを閉じる
driver.quit()
