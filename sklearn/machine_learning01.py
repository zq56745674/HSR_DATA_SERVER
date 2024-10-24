from sklearn import datasets
from sklearn.model_selection import train_test_split
import jieba
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.decomposition import PCA
import pandas as pd
from sklearn.feature_selection import VarianceThreshold
from scipy.stats import pearsonr
import matplotlib.pyplot as plt

def datasets_demo():
    # 加载 Iris 数据集
    iris = datasets.load_iris()
    # print(iris.data)
    # print(iris.target)
    # print(iris['DESCR'])

    # 划分数据集，80% 训练集，20% 测试集
    X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size=0.2, random_state=42)

    print("训练集特征数据：", X_train)
    print("训练集标签数据：", y_train)
    print("测试集特征数据：", X_test)
    print("测试集标签数据：", y_test)

def cut_word(text):
    return " ".join(list(jieba.cut(text)))

def datasets_chinese_demo():
    data = [
        '我爱北京天安门',
        '天安门上太阳升',
        '我爱北京天安门',
        '太阳升，天安门',
    ]
    data_new = []
    for text in data:
        data_new.append(cut_word(text))
    
    # transfer = CountVectorizer(stop_words=['我爱',])
    transfer = TfidfVectorizer()
    data_final = transfer.fit_transform(data_new)
    print("文本特征抽取结果：", data_final.toarray())
    print("特征名字：", transfer.get_feature_names_out())
    
def minmax_demo():
    """
    归一化处理
    归一化适用于数据的分布较为均匀的情况
    """
    data = pd.read_csv("D:\\pytest\\HSR_DATA_SERVER\\doc\\temp.csv")
    data = data.iloc[:, 1:4]

    transfer = MinMaxScaler()
    # 设置特征属性的取值范围
    # transfer = MinMaxScaler(feature_range=(2, 3))
    data_new = transfer.fit_transform(data)
    print(data_new)

def standard_demo():
    data = pd.read_csv("D:\\pytest\\HSR_DATA_SERVER\\doc\\temp.csv")
    data = data.iloc[:, 1:4]
    """
    低方差特征过滤
    """
    data_new = VarianceThreshold(threshold=0.5).fit_transform(data)
    print(data_new)
    """
    计算相关系数
    statistic：相关系数
    pvalue：p值 p值越小，相关系数越大
    """
    r1 = pearsonr(data["GS"], data["HSR"])
    print("GS和HSR相关系数：", r1)
    r2 = pearsonr(data["GS"], data["ZZZ"])
    print("GS和ZZZ相关系数：", r2)
    r3 = pearsonr(data["HSR"], data["ZZZ"])
    print("HSR和ZZZ相关系数：", r3)

    plt.figure(figsize=(20, 8), dpi=80)
    # 画折线图
    plt.plot(data["GS"], label="GS")
    plt.plot(data["HSR"], label="HSR")
    plt.plot(data["ZZZ"], label="ZZZ")
    # 显示图例
    plt.legend(loc="best")
    # 显示网格
    plt.grid()
    # 显示图像
    # plt.show()


    """
    标准化处理
    标准化适用于数据的分布不均匀的情况
    """
    transfer = StandardScaler()
    # 设置特征属性的取值范围
    # transfer = MinMaxScaler(feature_range=(2, 3))
    data_new = transfer.fit_transform(data_new)
    # print(data_new)

def pca_demo():
    """
    PCA 降维
    """
    data = pd.read_csv("D:\\pytest\\HSR_DATA_SERVER\\doc\\temp.csv")
    data = data.iloc[:, 1:4]
    # n_components：小数，表示保留的信息量 整数，表示保留的特征个数
    transfer = PCA(n_components=2)
    data_new = transfer.fit_transform(data)
    print(data_new)

    return data_new

if __name__ == '__main__':
    # datasets_demo()
    # datasets_chinese_demo()
    # minmax_demo()
    # standard_demo()
    pca_demo()