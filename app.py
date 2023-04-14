import os
from flask import Flask, render_template, request, send_from_directory
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField
from werkzeug.utils import secure_filename
from text_to_column import text_to_columns
from flask import jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'uploads/'

class UploadForm(FlaskForm):
    excel_file = FileField('Excel File')
    column_name = StringField('Column Name')
    delimiter = StringField('Delimiter')
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        file = request.files['excel_file']
        column_name = form.column_name.data
        delimiter = form.delimiter.data

        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            text_to_columns(os.path.join(app.config['UPLOAD_FOLDER'], filename), column_name, delimiter)
            return send_from_directory(app.config['UPLOAD_FOLDER'], filename.replace(".xlsx", "_modified.xlsx"), as_attachment=True)

    return render_template('upload.html', form=form)

if __name__ == "__main__":
    app.run(debug=True)


def preview():
    file = request.files['excel_file']
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Read the Excel file and convert it to an HTML table
        df = pd.read_excel(file_path)
        html_table = df.to_html(index=False, classes=["table", "table-striped", "table-bordered"])

        # Send the HTML table as a JSON response
        return jsonify({'html_table': html_table})

    return jsonify({'error': 'No file provided'})