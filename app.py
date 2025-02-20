import convertor as convert
from flask import request, render_template, Flask, send_file
import os

app = Flask('Convertor')

UPLOAD_FOLDER = convert.FOLDER
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = '1234567890'

ALLOWED_EXTENSIONS = ['pdf', 'txt', 'jpg', 'png', 'csv', 'xlsx']

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

def clear_files_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

@app.route('/submit', methods=['POST'])
def submit():
    clear_files_folder(app.config['UPLOAD_FOLDER'])
    file = request.files['file']
    conversion_type = request.form['conversion']
  
    file_extension = os.path.splitext(file.filename)[1]


    if file_extension[1:] not in ALLOWED_EXTENSIONS:
        return 'Файл не підтримується нашою системою', 400


    if conversion_type == 'png_to_jpg' and file_extension[1:] != 'png':
        return 'Для конвертації в JPG необхідно завантажити PNG файл', 400
    elif conversion_type == 'jpg_to_png' and file_extension[1:] != 'jpg':
        return 'Для конвертації в PNG необхідно завантажити JPG файл', 400
    elif conversion_type == 'txt_to_pdf' and file_extension[1:] != 'txt':
        return 'Для конвертації в PDF необхідно завантажити TXT файл', 400
    elif conversion_type == 'excel_to_csv' and file_extension[1:] != 'xlsx':
        return 'Для конвертації в CSV необхідно завантажити XLSX файл', 400
    elif conversion_type == 'csv_to_excel' and file_extension[1:] != 'csv':
        return 'Для конвертації в XLSX необхідно завантажити CSV файл', 400

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)


    if conversion_type == 'png_to_jpg':
        converted_filename = convert.png_to_jpg(file_path)
    elif conversion_type == 'jpg_to_png':
        converted_filename = convert.jpg_to_png(file_path)
    elif conversion_type == 'txt_to_pdf':
        converted_filename = convert.txt_to_pdf(file_path)
    elif conversion_type == 'excel_to_csv':
        converted_filename = convert.excel_to_csv(file_path)
    elif conversion_type == 'csv_to_excel':
        converted_filename = convert.csv_to_excel(file_path)

    
    
    return send_file(converted_filename, as_attachment=True)
if __name__ == '__main__':
    app.run(debug=True)
