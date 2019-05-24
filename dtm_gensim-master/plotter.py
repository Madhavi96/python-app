
import numpy as np

np.random.seed(9615)
import csv


#topics=[0,1,2,3,4]
files = ['OutputDTM0.csv', 'OutputDTM1.csv', 'OutputDTM2.csv', 'OutputDTM3.csv', 'OutputDTM4.csv']

mydict={}

xdates=[]
def getPlot():

    datalist = []

    for number in range(5):
        with open(files[number], 'r') as csvfile:
            dates = []
            datadict = {}
            reader = csv.reader(csvfile, delimiter='\n')
            next(reader)# skip 'TopicID,Word,Year,Probability' -first row/heading
            datadict["name"] = "topic" + str(number+1)

            dicty=[]
            dictannotes=[]
            for line in reader:
                if len(line)!=0:
                    res=[word for word in line[0].split(',')]

                    dicty.append(float('%.16f'%(float(res[3]))))

                    #dates.append(int(res[2]))
                    dates.append(res[2])
                    dictannotes.append(res[1])
            xdates=dates
            datadict["data"]=dicty
            datadict["annotes"]=dictannotes

            datalist.append(datadict)





    returndict={}
    returndict["datalist"]=datalist
    returndict["xdates"]=xdates




    return returndict
