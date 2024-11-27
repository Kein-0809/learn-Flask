from flask import Flask, render_template, redirect, url_for, abort
from custom_filters import reverse, calculate_birth_year


# app = Flask(__name__, static_folder="custom_static")
app = Flask(__name__)

# カスタムテンプレートフィルター(自作のフィルター)を追加
# 1つ目の引数にはフィルターを適用する関数を指定 (custom_filters.pyのreverse関数)
# 2つ目の引数にはフィルターの名前を指定 (reverse_name)。この名前をHTMLで使ってフィルターを適用する
app.add_template_filter(reverse, 'reverse_name')
# custom_filters.pyのcalculate_birth_year関数をフィルターとして追加
# フィルターの名前を指定 (birth_year)。この名前をHTMLで使ってフィルターを適用する
app.add_template_filter(calculate_birth_year, 'birth_year')

# @app.template_filter('reverse_name')
# def reverse(name):
#     return name[::-1]

# @app.template_filter('birth_year')
# def calculate_birth_year(age):
#     current_year = datetime.datetime.now().year
#     birth_year = current_year - age
#     return birth_year

@app.route('/')
def index():
    # userの値をUpperし、index.htmlにその値を渡して、表示する
    return render_template('index.html', user="John".upper())

# User情報のクラスを定義
class UserInfo:
    # コンストラクタ
    def __init__(self, name, age):
        self.name = name
        self.age = age
        
    def greet(self, message=""):
        return f"{self.name}です。よろしくお願い申し上げます。{message}"

# ホーム画面のルート (例: http://localhost:5000/home/Taro/20)
@app.route('/home/<string:user_name>/<int:age>')
# URLからのパラメータ"user_name"と"age"を受け取って引数にする
def home(user_name, age):
    # login_user = user_name
    # user_info = {
    #     'name': user_name,
    #     'age': age
    # }
    # 引数を使ってUserInfoクラスのインスタンスを生成
    user_info = UserInfo(user_name, age)
    # home.htmlにuser_infoを渡して、表示する
    return render_template('home.html', user_info=user_info)

@app.route('/userlist')
def user_list():
    users = [
        'Taro', 'Jiro', 'Saburo', 'Shiro'
    ]
    is_login = False
    # userlist.htmlにusersとis_loginを渡して、表示する
    return render_template('userlist.html', users=users, is_login=is_login)

@app.route('/user/<user_name>/<int:age>')
# URLからのパラメータ"user_name"と"age"を受け取って引数にする
def user(user_name, age):
    if user_name in ['Taro', 'Jiro', 'Saburo']:
        # ホーム画面にリダイレクト
        return redirect(url_for('home', user_name=user_name, age=age))
    elif user_name == 'Shiro':
        # Googleにリダイレクト
        return redirect('https://google.com')
    else:
        abort(500, 'そのユーザーはリダイレクトできません')

@app.errorhandler(500)
def system_error(error):
    # エラーの説明を取得
    error_description = error.description
    # system_error.htmlにerror_descriptionを渡して、表示する
    return render_template('system_error.html', error_description=error_description), 500

@app.errorhandler(404)  
def page_not_found(error):
    # エラーの説明を取得
    error_description = error.description
    # not_found.htmlにerror_descriptionを渡して、表示する
    return render_template('not_found.html', error_description=error_description), 404


if __name__ == '__main__':
    app.run(debug=True)