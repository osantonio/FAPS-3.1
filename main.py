from app import app
from flask import Flask, render_template

@app.route('/')
def index():
    return render_template('dashboard.html', title='Home')

if __name__ == '__main__':
    app.run(debug=False)