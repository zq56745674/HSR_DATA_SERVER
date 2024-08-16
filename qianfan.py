import os
import qianfan

#【推荐】使用安全认证AK/SK鉴权，通过环境变量初始化认证信息
# 替换下列示例中参数，安全认证Access Key替换your_iam_ak，Secret Key替换your_iam_sk
# os.environ["QIANFAN_ACCESS_KEY"] = "ALTAK8UtQciV2cLNZZaG5E0EYB"
# os.environ["QIANFAN_SECRET_KEY"] = "82d9ab569eeb4aa8945ca08e90f2ec37"

chat_comp = qianfan.ChatCompletion()

# 指定特定模型
resp = chat_comp.do(model="ERNIE-Speed-128K", messages=[{
    "role": "user",
    "content": """ANDROID	6.606914212548015	1.295774647887324	3124
            PC	7.730145175064048	1.1323654995730146	1171
            IOS	7.44015444015444	1.2007722007722008	518
            CLOUD_ANDROID	6.407216494845361	1.4896907216494846	194
            CLOUD_WEB_ANDROID	4.959183673469388	1.3061224489795917	49
            CLOUD_IOS	6.433962264150943	1.509433962264151	53
            CLOUD_WEB_PC	5.904761904761905	1.4285714285714286	42
            CLOUD_WEB_IOS	7.090909090909091	1.4545454545454546	11
            CLOUD_WEB_MAC	4.0	0.0	2请分析已上数据"""
}])

print(resp["body"])