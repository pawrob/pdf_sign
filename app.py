import io

from flask import Flask, request, send_file

from data import admin_all
from sign import sign_bytes, verify

app = Flask(__name__)

@app.route('/sign', methods=['GET', 'POST'])
def sign_handler():
    if request.method == 'POST':
        if 'pdf' not in request.files:
            return 'No pdf file found in form, try again', 400
        pdf = request.files['pdf']
        return send_file(
            io.BytesIO(sign_bytes(pdf.stream.read())),
            download_name=pdf.filename.replace(".pdf", "-signed-cms.pdf"),
            as_attachment=True
        )
    else:
        return '''
        <!doctype html>
        <form method="post" enctype="multipart/form-data">
        <input type="file" name="pdf" />
        <input type="submit" value="submit" />
        </form>
        '''


@app.route('/verify', methods=['GET', 'POST'])
def verify_handler():
    if request.method == 'POST':
        if 'pdf' not in request.files:
            return 'No pdf file found in form, try again', 400
        pdf = request.files['pdf']
        return str(verify(pdf.stream.read()))
    else:
        return '''
        <!doctype html>
        <form method="post" enctype="multipart/form-data">
        <input type="file" name="pdf" />
        <input type="submit" value="submit" />
        </form>
        '''


@app.route('/all', methods=['GET'])
def all_handler():
    return str(admin_all())


if __name__ == '__main__':
    app.run(debug=True)
