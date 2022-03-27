from __future__ import division, print_function
import os
import pandas as pd
import pdfplumber
from flask import Flask, redirect, url_for, request, render_template,Response
import io
app = Flask(__name__)
global f

@app.route('/extractor123', methods=['GET', 'POST'])
def pdf_extractor():
    global f
    file = 'static/uploads/Current.pdf'

    df1 = pd.DataFrame(
        columns=['Doc Type', 'Document.No', 'Posting Date', 'Bill.No', 'Bill.Date', 'Gross', 'Net.Amt Deductions',
                 'TDS'])
    k = 0
    with open(file, 'rb') as f:
        content = io.BytesIO(f.read())
    with pdfplumber.open(content) as pdf:
        page0 = pdf.pages[0]
    for i in range(0, len(pdf.pages)):
        with pdfplumber.open(content) as pdf:
            page = pdf.pages[i]
            text = page.extract_table()
            if i != len(pdf.pages) - 1:
                for j in range(0, len(text[-1][0].split('C\n'))):
                    lst = text[-1][0].split('C\n')[j].replace('\n', '').split(" ")
                    try:
                        while True:
                            lst.remove('')
                    except ValueError:
                        pass
                    if len(lst) == 8:
                        print(lst)
                        df1.loc[k] = lst
                        k = k + 1
                    elif len(lst) == 9:
                        print(lst[0:-1])
                        df1.loc[k] = lst[0:-1]
                        k = k + 1

            elif i == len(pdf.pages) - 1:
                for j in range(0, len(text[-4][0].split('C\n '))):
                    lst = text[-4][0].split('C\n ')[j].replace('\n', '').split(" ")
                    try:
                        while True:
                            lst.remove('')
                    except ValueError:
                        pass
                    if len(lst) == 8:
                        print(lst)
                        df1.loc[k] = lst
                        k = k + 1
                    elif len(lst) == 9:
                        print(lst[0:-1])
                        df1.loc[k] = lst[0:-1]
                        k = k + 1
    df1['D/C'] = 'C'
    csv_raw = df1.to_csv(index=False)
    return Response(
        csv_raw,
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename= {}.csv".format("ABC")})



@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/extractor', methods=['GET', 'POST'])
def upload():
    global f
    if request.method == 'POST':
        f = request.files['file']

        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'static/uploads', f.filename)
        f.save('static/uploads/Current.pdf')
        print(file_path)
        return 'Success'
    return 'Success'
if __name__ == '__main__':
    app.run(debug=True)
