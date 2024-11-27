from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import pykakasi
import os

app = Flask(__name__)


class Kakashi:

    kakashi = pykakasi.kakasi()
    kakashi.setMode('H', 'a')
    kakashi.setMode('K', 'a')
    kakashi.setMode('J', 'a')
    conv = kakashi.getConverter()

    @classmethod
    def japanese_to_ascii(cls, japanese):
        return cls.conv.do(japanese)

class UserInfo:
    # コンストラクタ
    def __init__(self, last_name, first_name, job, gender, message):
        self.last_name = last_name
        self.first_name = first_name
        self.job = job
        self.gender = gender
        self.message = message

@app.route('/signup') # サインアップ画面
def sign_up():
    return render_template('signup.html')

@app.route('/home', methods=["GET", "POST"])
def home():
    # ターミナルでリクエストのパスを表示
    print(f"リクエストのパス: {request.full_path}")
    # ターミナルでリクエストのメソッドを表示
    print(f"リクエストのメソッド: {request.method}")
    # ターミナルでリクエストの引数を表示
    print(f"リクエストの引数: {request.args}")
    # user_info = UserInfo(
    #     request.args.get('last_name'),
    #     request.args.get('first_name'),
    #     request.args.get('job'),
    #     request.args.get('gender'),
    #     request.args.get('message')
    # )
    user_info = UserInfo(
        # リクエストのフォームからlast_nameを取得
        request.form.get('last_name'),
        # リクエストのフォームからfirst_nameを取得
        request.form.get('first_name'),
        # リクエストのフォームからjobを取得
        request.form.get('job'),
        # リクエストのフォームからgenderを取得
        request.form.get('gender'),
        # リクエストのフォームからmessageを取得
        request.form.get('message')
    )
    # home.htmlにuser_infoを渡して、表示する
    return render_template('home.html', user_info=user_info)


# アップロード先のディレクトリを指定
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'image')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# アップロード先のディレクトリが存在しない場合は作成
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

#  画像をアップロードする
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    # GETの場合の処理先
    if request.method == 'GET':
        # upload.htmlを表示する
        return render_template('upload.html')
    # POSTの場合の処理先
    elif request.method == 'POST':
        # POSTデータからファイルを取得
        file = request.files['file']
        # ファイルを日本語から英語に変換
        ascii_filename = Kakashi.japanese_to_ascii(file.filename)
        # ファイル名を安全な形式に変換
        save_filename = secure_filename(ascii_filename)
        # ファイルを保存
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], save_filename))
        # アップロード完了画面にリダイレクト
        return redirect(url_for('uploaded_file', filename=save_filename))

@app.route('/uploaded_file/<string:filename>')
def uploaded_file(filename):
    return render_template('uploaded_file.html', filename=filename)

if __name__ == '__main__':
    app.run(debug=True)
