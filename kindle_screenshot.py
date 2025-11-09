# PythonでWebブラウザを自動操作するためのライブラリをインポートします。
# asyncio: 非同期処理を扱うための標準ライブラリ。Playwrightは非同期に動作するため必須です。
import asyncio
# playwright.async_api から sync_playwright をインポート。
# これにより、Playwrightの非同期APIを、よりPythonらしい同期的なコードのように扱うことができます。
from playwright.async_api import sync_playwright

# Kindle Cloud Readerからスクリーンショットを取得する非同期関数を定義します。
# 'async def' は、この関数が非同期処理を行うことを示しています。
async def take_kindle_screenshot():
    # Playwrightのブラウザ操作コンテキストを開始します。
    # 'async with' を使用することで、処理の開始と終了時に必要なリソース管理（ブラウザの起動・終了など）を自動で行ってくれます。
    async with sync_playwright() as p:
        # Chromiumブラウザ（Google Chromeのオープンソース版）を起動します。
        # headless=False: ブラウザが実際に画面に表示されるモードで起動します。
        #                デバッグ中にブラウザの動きを目で確認するのに便利です。
        #                最終的にはheadless=Trueに設定して、バックグラウンドで実行することも可能です。
        browser = await p.chromium.launch(headless=False)
        # 新しいブラウザページ（タブ）を作成します。
        # このページオブジェクトを使って、ウェブページへの操作を行います。
        page = await browser.new_page()

        # Kindle Cloud Readerのウェブサイトにアクセスします。
        # 指定されたURLへページを移動するコマンドです。
        await page.goto("https://read.amazon.com/")

        # ここからログイン処理を開始します。
        # 環境変数からユーザー名とパスワードを取得するためにosモジュールをインポートします。
        # プログラムコードに直接認証情報を書くのはセキュリティ上非常に危険なため、
        # 環境変数として外部から読み込む方法を採用しています。
        import os
        # ユーザーにメールアドレス（ユーザー名）とパスワードの入力を求めます。
        # input()関数を使うと、プログラムの実行中にキーボードからの入力を受け取ることができます。
        email = input("Kindleにログインするためのメールアドレスを入力してください: ")
        password = input("Kindleにログインするためのパスワードを入力してください: ")

        # 入力された情報が空でないかを確認します。
        # もし入力がなかったら、エラーメッセージを表示してプログラムを終了します。
        if not email or not password:
            print("エラー: メールアドレスとパスワードの両方を入力してください。")
            await browser.close()
            return

        # メールアドレス入力フィールドを探して、環境変数から取得したメールアドレスを入力します。
        # 'input[type="email"]' はCSSセレクタと呼ばれるもので、HTML要素を特定するための記述方法です。
        # 今回はtype属性が"email"のinputタグを探しています。
        await page.fill('input[type="email"]', email)
        # 「続行」ボタンをクリックします。
        # Amazonのログインフローでは、メールアドレス入力後に「続行」ボタンをクリックするステップがあるため、これも自動化します。
        await page.click('input[id="continue"]')

        # パスワード入力フィールドを探して、環境変数から取得したパスワードを入力します。
        # 同様に、CSSセレクタでtype属性が"password"のinputタグを探しています。
        await page.fill('input[type="password"]', password)

        # ログインボタンをクリックします。
        # id属性が"signInSubmit"のinputタグを探しています。
        await page.click('input[id="signInSubmit"]')

        # ログインが成功し、Kindleライブラリページにリダイレクトされるまで待機します。
        # 'wait_for_url' は、指定したURLパターンにページが遷移するまで待つメソッドです。
        # ここでは、URLが"https://read.amazon.com/kindle-library"で始まることを期待しています。
        await page.wait_for_url("https://read.amazon.com/kindle-library*")

        # ログイン後のKindleライブラリページのスクリーンショットを撮影し、ファイルとして保存します。
        # path引数で保存するファイル名を指定します。
        await page.screenshot(path="kindle_after_login.png")
        print("ログイン後の画面のスクリーンショットを保存しました: kindle_after_login.png")

        # 今後のステップとして、ここから個々の本を開き、ページをめくりながらスクリーンショットを撮影し、
        # 最終的にそれらを結合してPDFを生成する処理を追加していく予定です。

        # 全ての処理が完了したので、開いていたブラウザを閉じます。
        await browser.close()

# このPythonスクリプトが直接実行された場合にのみ、
# take_kindle_screenshot関数を非同期に実行します。
# asyncio.run() は非同期関数を実行するためのエントリーポイントです。
if __name__ == "__main__":
    asyncio.run(take_kindle_screenshot())

# --- 参考：Playwrightの同期APIを使った場合の例 --- 
# 上記の非同期コードとは異なり、async/awaitキーワードを使わずに書けます。
# ただし、非同期APIの方が現代のWebスクレイピングや自動化では推奨されることが多いです。
# from playwright.sync_api import sync_playwright as sync_playwright_sync

# def take_kindle_screenshot_sync():
#     with sync_playwright_sync() as p:
#         browser = p.chromium.launch(headless=False)
#         page = browser.new_page()
#         page.goto("https://read.amazon.com/")
#         page.screenshot(path="kindle_login_page_sync.png")
#         browser.close()

# # 同期関数はasyncio.run()を使わずに直接呼び出せます。
# # if __name__ == "__main__":
# #     take_kindle_screenshot_sync()