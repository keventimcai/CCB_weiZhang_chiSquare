import numpy as np
from matplotlib import pyplot as plt

class roc:
    def rocFigure(self,probabilityArray,realArray):
        """
        :param probabilityArray: list，所输出的阳性概率
        :param realArray: list，对应真实值
        :return: null
        """
        trueSum=sum(realArray)
        falseSum=len(realArray)-trueSum
        data=zip(probabilityArray,realArray)
        sortData=sorted(data,key=lambda student: student[0],reverse=True)
        xAxis=[]
        yAxis=[]
        for i in range(len(sortData)):
            count=0
            for j in range(i):
                if sortData[j][1]==0:
                    count+=1
            falsePositiveRate=count/falseSum
            xAxis.append(falsePositiveRate)
            truePositive=i-count
            truePositiveRate=truePositive/trueSum
            yAxis.append(truePositiveRate)
        xAxis.append(1)
        yAxis.append(1)
        x=np.array(xAxis)
        y=np.array(yAxis)
        plt.xlabel("false positive rate")
        plt.ylabel("true positive rate")
        plt.title("ROC")
        for a, b in zip(x, y):
            plt.text(a-0.02,b,"({:.2f} {:.2f})".format(a,b) ,ha='center', va='bottom', fontsize=5)
        plt.plot(x,y)
        plt.legend()
        plt.show()

kk=roc()
real=[1,1,0,1,1,1,0,0,1,0,
      1,0,1,0,0,0,1,0,1,0]
pp=[0.9,0.8,0.7,0.6,0.55,0.54,0.53,0.52,0.51,0.505,
    0.4,0.39,0.38,0.37,0.36,0.35,0.34,0.33,0.30,0.1]
rr=kk.rocFigure(pp,real)



