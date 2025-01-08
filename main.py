from app import app
from flask import render_template

@app.route('/')
def index():
    return render_template('dashboard.html', title='Home')

@app.route('/test')
def test():
    return "Servidor funcionando"

if __name__ == "__main__":
    app.run()

