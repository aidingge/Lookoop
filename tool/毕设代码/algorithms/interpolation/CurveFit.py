# coding:utf-8
# 2019/11/25
"""多元二次响应面拟合"""
import sys
sys.path.append("../../")

from util import io 
from util import tool

# 使用非线性最小二乘法拟合
from scipy.optimize import curve_fit
import numpy as np

dataFilePath = "../../data/samples-data.data"
labelsFilePath = "../../data/samples-data-labels.data"
curveFitModelSavingPath = "../../data/quadraticRegression.model"

def getTrainData():
    """获取训练数据"""
    X = io.getData(dataFilePath)
    Y = io.getData(labelsFilePath)

    return X, Y

class CurveFitHandler():
    """模板"""
    def __init__(self):
        self.y = None
        self.pdtResult = None

    def adaptData(self, X):
        """将数据变形为系数矩阵"""
        newData = []
        for data in X:
            # x1 = data[0]
            # x2 = data[1]
            # x3 = data[2]
            # x4 = data[3]
            # x5 = data[4]
            # tmp = [ 1, x1, x2, x3, x4, x5, 
            #         x1*x2, x1*x3, x1*x4, x1*x5, x2*x3, 
            #         x2*x4, x2*x5, x3*x4, x3*x5, x4*x5, 
            #         x1**2, x2**2, x3**2, x4**2, x5**2 ]
            var = [1]   # 常数系数
            for v in data:
                var.append(v)

            tmp = []
            for i in range(len(var)):
                for j in range(i, len(var)):
                    tmp.append(var[i]*var[j])
                    
            newData.append(tmp)
        newData = np.array(newData)

        return newData

    def fit(self, X, y):
        """训练"""
        pass

    def amiFunc(self, x, *args):
        """目标函数"""
        pass

    def predict(self, X):
        """预测"""
        pass

    def getMSE(self):
        """计算均方误差"""
        m = np.shape(self.y)[0]
        tmpSum = 0
        for i in range(m):
            tmpSum += abs(self.y[i] - self.pdtResult[i])

        return tmpSum / m

class CurveFit(CurveFitHandler):
    """针对五个变量的例子"""
    def __init__(self):
        super(CurveFit, self).__init__()
        self.coef = None    # 二次项系数

    def fit(self, X, y):
        """训练
        @param X mxn维数组，训练数据
        @param y 1xm or mx1 维数组，标签
        """
        if np.shape(y)[0] != 1:
            y = y.reshape(1, len(y))[0]
        self.y = y

        self.coef, pcov = curve_fit(self.amiFunc, X, y)

    def amiFunc(self, x, c0, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10,
                c11, c12, c13, c14, c15, c16, c17, c18, c19, c20):
        """目标函数"""
        newData = self.adaptData(x)
        c = np.array([c0, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10,
             c11, c12, c13, c14, c15, c16, c17, c18, c19, c20])
        c = c.reshape(len(c), 1)
        ret = np.dot(newData, c)
        ret = ret.reshape(1, len(ret))[0]   # 转为一维

        return ret

    def predict(self, X):
        """预测
        @param X mxn维数组

        @returns pdt mx1维预测值
        """
        c0, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13, c14, c15, c16, c17, c18, c19, c20 = self.coef
        self.pdtResult = self.amiFunc(X, c0, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10,
             c11, c12, c13, c14, c15, c16, c17, c18, c19, c20)

        return self.pdtResult

if __name__ == '__main__':
    X, Y = getTrainData()
    y = Y.reshape(1, len(Y))[0]
    curveFit = CurveFit()
    curveFit.fit(X, y)
    io.saveData(curveFit, curveFitModelSavingPath)  # 保存当前模型
    # curveFit = io.getData(curveFitModelSavingPath)
    # pdtVDiff = curveFit.predict(X) - y
    # print("[INFO] predict mse : {}".format(curveFit.getMSE()))
    mse = tool.crossValueScore(curveFit, X, y)
    print("MSE: {}".format(mse))

