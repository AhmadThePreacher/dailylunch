from flask import Flask, render_template
from models import get_daily_menus

app = Flask(__name__)

@app.route('/')
def index():
    menus = get_daily_menus()
    return render_template('index.html', menus=menus)

if __name__ == '__main__':
    app.run(debug=True)