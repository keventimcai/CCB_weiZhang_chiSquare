import numpy as np

class kmeans:
    def Kmeans(self,data,distanceCal,k,a):
        """
        :param data:dataframe,所聚类的数据
        :param distance: 函数，距离计算公式，默认为欧式距离
        :param k: int，k的数量
        :param a: double，聚类阈值
        :return: list，元素为对于数据的类编号
        """
        npdata=np.array(data)
        datalen=len(npdata)
        dimension=len(npdata[0])
        low=npdata[0][0]
        kmeansFront=self.randInit(low,k,dimension)
        kmeansIndex,kmeansBehind=self.update(npdata,datalen,distanceCal,kmeansFront,k)
        while np.mean(kmeansBehind-kmeansFront)>a:
            kmeansFront=kmeansBehind
            kmeansIndex, kmeansBehind = self.update(npdata, datalen, distanceCal, kmeansFront, k)
        return kmeansIndex

    def update(self,data,datalen,distanceCal,kmeans,k):
        kmeansIndex=[]
        kmeansAvg=[np.array(0) for i in range(k)]
        for i in range(datalen):
            mindistance=distanceCal(kmeans[0],data[i])
            flag=0
            for j in range(1,k):
                distance = distanceCal(kmeans[j],data[i])
                if distance<mindistance:
                    flag=j
            kmeansAvg[flag].append(data[i])
            kmeansIndex.append(flag)
        kmeans=np.zeros(k)
        for i in range(k):
            kmeans[i]=kmeansAvg[i].mean()
        return kmeansIndex,kmeans

    def randInit(self,low,k,dimensions):
        result=np.random.randint(low=np.argmax(low),size=(k,dimensions))
        return result