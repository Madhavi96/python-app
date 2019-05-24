from flask import Flask, render_template , request,flash,Session
import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS =['txt']

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'super secret key'
sess = Session()

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
            return render_template('admin_uploadfile.html')
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


            flash('Uploading the file...')
            file.save(os.path.join('Temp', filename))

            path=get_file_path(field)

            preprocessTweets(tweetdate=tweetdate,file=filename,storeFolder=path)
            flash('successfully uploaded')
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

        path = get_file_path(field)
        Handler(storeFolder=path,start=start_date,end=end_date).handle()

        getdict = getPlot()
        dataseries = getdict["datalist"]


        articles=findArticles(field,dataseries)
        print(articles)

        xdates = getdict["xdates"]
        print(xdates)
        print(dataseries)
        return render_template('testgraph.html', xdates=xdates, dataseries=dataseries,articles=articles)
    return


@app.route('/testfuturepy',methods = ['POST', 'GET'])
def testfuturepy():
    if request.method == 'POST':
        result = request.form
        topic=int(result["topic"])

        end_date = result["end"]

        getdict = getFuturePlot(topic_number=topic,end=end_date)
        if getdict == "":
            error="Invalid End Month"
            #raise ValueError
            return render_template('viewfuturepaths.html', error=error)


        dataseries = getdict["prob"]
        xdates = getdict["dates"]
        annotes=getdict["annotes"]

    return render_template('testfuturegraph.html', xdates=xdates, dataseries= dataseries,annotes=annotes)






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
    app.run(debug='True')