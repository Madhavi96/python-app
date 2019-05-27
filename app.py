from flask import render_template
import os
from flask import Flask, request
from werkzeug.utils import secure_filename
import json
import csv
import pandas as pd

ALLOWED_EXTENSIONS =['txt']

app = Flask(__name__)

from plotter import getPlot
from predictor import getFuturePlot
from testing_file import Handler
from matcharticles import findArticles
from preprocess import preprocessTweets

@app.route('/')
def index():
    return render_template('home.html')


@app.route('/viewpaths')
def viewpaths():
    return render_template('viewpaths.html')

@app.route('/validate',methods=['POST', 'GET'])
def validate():
    secret_key="ad123"
    if request.method == 'POST':
        result = request.form
        key=result["key"]
        if key==secret_key:
            return render_template('admin_uploadfile_check.html')
        else:
            return render_template('adminkey.html')




def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



def get_file_path(field):
    if field=="1":
        UPLOAD_FOLDER = 'politics_tweetdb'
    elif field=="2":
        UPLOAD_FOLDER = 'education_tweetdb'
    elif field=="3":
        UPLOAD_FOLDER = 'terrorism_tweetdb'


    return  UPLOAD_FOLDER

@app.route('/uploadcheck', methods = ['GET', 'POST'])
def uploadcheck():

    if request.method == 'POST':
        field = request.form["field"]
        tweetdate = request.form["tweetdate"]


        try:
            # write to permanant store
            processedfolder=get_file_path(field)
            file = open(os.path.join(processedfolder, tweetdate), 'r')
            error = "You have already uploaded dataset!"
            return render_template('admin_uploadfile_check.html', error=error)
        except FileNotFoundError:
            error = "No file was found!"
            return render_template('admin_uploadfile.html', error=error)




@app.route('/upload', methods = ['GET', 'POST'])
def upload():


    if request.method == 'POST':
        field = request.form["field"]
        tweetdate = request.form["tweetdate"]

        if field not in ["1","2","3"]:
            error="No field selected"

            return render_template('admin_uploadfile.html', error=error)
        # check if the post request has the file part

        if 'file' not in request.files:
            error="No file selected"

            return render_template('admin_uploadfile.html', error=error)


        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            error = "No file selected"
            return render_template('admin_uploadfile.html', error=error)


        if file and allowed_file(file.filename):

            app.config['TEMP_FOLDER'] = 'Temp'
            filename = secure_filename(file.filename)
            print(filename)



            file.save(os.path.join('Temp', filename))

            path=get_file_path(field)

            preprocessTweets(tweetdate=tweetdate,file=filename,storeFolder=path)

            return render_template('home.html')
        error="Invalid file type"
        return render_template('admin_uploadfile.html', error=error)



@app.route('/testpy',methods = ['POST', 'GET'])
def testpy():
    if request.method == 'POST':
        result = request.form
        field=result["field"]
        start_date=result["start"]

        end_date = result["end"]

        if int(start_date) >= int(end_date):
            error = "Invalid Month Range"
            #raise ValueError
            return render_template('viewpaths.html', error=error)
        files = ['OutputDTM0.csv', 'OutputDTM1.csv', 'OutputDTM2.csv', 'OutputDTM3.csv', 'OutputDTM4.csv']
        resultstore = start_date + end_date
        if field == '1':
            storeinfolder = 'result_topics_pol'
        elif field == '2':
            storeinfolder = 'result_topics_edu'
        elif field == '3':
            storeinfolder = 'result_topics_ter'

        try:
            # write to permanant store
            file = open(os.path.join(storeinfolder, resultstore), 'r')
            renderlist = []
            i = 0
            for line in file:
                renderlist.append(json.loads(line))
                print(renderlist[i])
                i = i + 1
            print(renderlist[2])
            # write the topics just viewd-for future plot

            xdates = renderlist[0]
            dataseries = renderlist[1]
            print("++++++++++++++++++++++++++++++++++")
            for i in range(5):
                with open(files[i], 'w', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile, delimiter=',')
                    # Write header
                    writer.writerow(['TopicID', 'Word', 'Year', 'Probability'])

                    for year_i in range(len(xdates)):
                        write=[int(i), dataseries[i]['annotes'][year_i], xdates[year_i], dataseries[i]['data'][year_i]]
                        writer.writerow(write)
                        print(write)

            return render_template('testgraph.html', xdates=renderlist[0], dataseries=renderlist[1], articles=renderlist[2])


        except FileNotFoundError:
            path = get_file_path(field)
            Handler(storeFolder=path, start=start_date, end=end_date).handle()
            getdict = getPlot()
            dataseries = getdict["datalist"]
            articles = findArticles(field, dataseries)
            print(articles)
            xdates = getdict["xdates"]
            print(xdates)
            print(dataseries)
            mylist = [xdates, dataseries, articles]
            f = open(os.path.join(storeinfolder, resultstore), 'w', encoding='utf-8')

            for jsonobj in mylist:
                jsonstr = json.dumps(jsonobj)
                f.write(jsonstr + "\n")
            f.flush()
            f.close()

        return render_template('testgraph.html', xdates=xdates, dataseries=dataseries,articles=articles)
    return


@app.route('/testfuturepy',methods = ['POST', 'GET'])
def testfuturepy():
    if request.method == 'POST':
        result = request.form
        topic=int(result["topic"])

        end_date = result["end"]
        '''
        try:
             with open('OutputDTM0.csv', 'r') as csvfile:
                csvFileReader = csv.reader(csvfile)
                for row in csvFileReader:
                    print(row)
                    if row != '\n':
                        print(row)
                        csvfile.close()
                        getdict = getFuturePlot(topic_number=topic, end=end_date)
                        if getdict == "":
                            error = "Invalid End Month"
                            # raise ValueError
                            return render_template('viewfuturepaths.html', error=error)
                        print("row exists.....................................................")
                        dataseries = getdict["prob"]
                        xdates = getdict["dates"]
                        annotes = getdict["annotes"]

        except:
            print("came.........................")
            error = "First view a topic evolution, before any predictions!"
            # raise ValueError
            return render_template('viewfuturepaths.html', error=error)
        '''

        print("trying.............................")
        with open('OutputDTM0.csv', 'r') as csvfile:
            csvFileReader = csv.reader(csvfile)
            print("woooooooooooooooooooow")
            for row in csvFileReader:
                print(row)
                if row != '\n':
                    print(row)
                    # csvfile.close()
                    getdict = getFuturePlot(topic_number=topic, end=end_date)
                    if getdict == "":
                        error = "Invalid End Month"
                        # raise ValueError
                        return render_template('viewfuturepaths.html', error=error)
                    print("row exists.....................................................")
                    dataseries = getdict["prob"]
                    xdates = getdict["dates"]
                    annotes = getdict["annotes"]
                    return render_template('testfuturegraph.html', xdates=xdates, dataseries=dataseries,
                                           annotes=annotes)

        print("came.........................")
        error = "First view a topic evolution, before any predictions!"
        # raise ValueError
        return render_template('viewfuturepaths.html', error=error)
    print("eeeeeeeeeeeeeeeeeeee")





@app.route('/viewfuturepaths')
def viewfuturepaths():
    return render_template('viewfuturepaths.html')

@app.route('/adminkey')
def adminkey():
    return render_template('adminkey.html')


@app.route('/adminupload')
def adminupload():
    return render_template('admin_uploadfile.html')




if __name__=='__main__':
    app.run()