from flask import Flask, render_template, url_for, send_from_directory, send_file

app = Flask(__name__)

@app.route('/')
def hello_world():
    name = ['Harsh Gupta', 'Anish Nuni']
    return render_template('index.html', persons=name)
    # return 'Hello World!'

if __name__ == '__main__':
    app.run()
