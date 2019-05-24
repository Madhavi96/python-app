import csv
import numpy as np
from sklearn.svm import SVR

files=['OutputDTM0.csv','OutputDTM1.csv','OutputDTM2.csv','OutputDTM3.csv','OutputDTM4.csv']
topic_number=1

times = ["201810", "201811", "201812", "201901", "201902", "201903", "201904"]
monthsdict = {"201810": "October 2018", "201811": "November 2018", "201812": "Decemebr 2018", "201901": "January 2019",
               "201902": "February 2019", "201903": "March 2019", "201904": "April 2019"}
months=["October 2018","November 2018","December 2018","January 2019","February 2019","March 2019","April 2019"]
monthsdictionary={"October 2018":0,"November 2018":1,"December 2018":2,"January 2019":3,"February 2019":4,"March 2019":5,"April 2019":6}

def getFuturePlot(end=None,topic_number=None):
    with open(files[topic_number] , 'r') as csvfile:
        dates = []
        prob = []
        topic_chain = []
        dates_prob_annotes_dict={}
        csvFileReader= csv.reader(csvfile)
        next(csvFileReader)
        next(csvFileReader)
        for row in csvFileReader:
            dates.append(row[2])

            prob.append(float('%.16f'%(float(row[3]))))
            topic_chain.append(row[1])
            next(csvFileReader)
        start_old=months.index(dates[0])
        end_old = months.index(dates[-1])

        old_dates=months[start_old:end_old+1]
        end_new=times.index(end)
        if end_old >= end_new :
            return ""
        x=months[end_old+1:end_new+1]
        x_numeric=[i for i in range(monthsdictionary[x[0]],monthsdictionary[x[-1]]+1)]
        old_dates_numeric=[i for i in range(monthsdictionary[old_dates[0]],monthsdictionary[old_dates[-1]]+1)]

        empty_annote_amt=end_new-end_old
        for i in range(empty_annote_amt):
            topic_chain.append("")

        all_months=months[start_old:end_new+1]
        old_dates_num_reshape = np.reshape(old_dates_numeric, (len(old_dates_numeric), 1))
        svr_rbf = SVR(kernel='rbf', C=100,gamma=0.1,epsilon=0.000000000001)


        svr_rbf.fit(old_dates_num_reshape, prob)


        x_num_reshape = np.reshape(x_numeric, (len(x), 1))
        new=np.concatenate((old_dates_num_reshape,x_num_reshape))

        predictions=svr_rbf.predict(new)

        ydata=[]
        for ele in predictions:
            ydata.append(ele)
        csvfile.close()
        dates_prob_annotes_dict["dates"]=all_months
        dates_prob_annotes_dict["prob"]=ydata
        dates_prob_annotes_dict["annotes"]=topic_chain

        return dates_prob_annotes_dict


