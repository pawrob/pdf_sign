import os


from flask import Flask, request, send_file

from sign import sign

app = Flask(__name__)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'pdf' not in request.files:
            return 'No pdf file found in form, try again', 400
        pdf = request.files['pdf']
        path = os.path.join('./', pdf.filename)
        print(path)
        pdf.save(path)
        return send_file(sign(path), as_attachment=True)
    else:
        return 'POST file to proceed', 200


if __name__ == '__main__':
    app.run()