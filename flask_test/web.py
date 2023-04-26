from flask import Flask,render_template

app = Flask(__name__)
# app = Flask(__name__,render_template = '')
@app.route('/show/info')
def index():
    # return '中国联通'
    return render_template('aa.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5100, debug=False)
# http://120.229.24.75:5100/show/info