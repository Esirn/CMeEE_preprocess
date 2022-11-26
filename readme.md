# 简介
[CMeEE数据集](https://tianchi.aliyun.com/dataset/dataDetail?dataId=95414#1)处理的工具。功能：
- stats：统计数据集的句子与实体信息，写到csv文件中。
- wash：数据清洗，将错误数据删除。
- trans: json与bmes格式的数据或文件相互转换。（bmes格式参考RESUME）
- reshape：将原始train集与dev集合并、按比例划分为train-dev-test集。

# 使用
在`main.py`中调用各方法并执行。目录结构为：
- ./*.py：实现代码
- ./i/：输入文件: CMeEE_train.json, CMeEE_dev.json
- ./o/{stats|wash|reshape|trans}/：输出文件：统计、清洗、划分、转化。

### requirements
~~~
conda install scikit-learn
~~~

# 数据分析情况
### 存在问题
- 有两处实体**start_idx > end_idx**，wash删除。
- 删除上述两个实体后，仍有一处的实体排序不是**优先end_idx升序，其次start_idx降序**，wash重排序。
- 存在非sym类型的实体互相嵌套，stat时会打印warning。
- 医学数据集中有嵌套问题，而bmes标注无法保留嵌套信息，暂时的解决方案是当有嵌套关系时，舍弃前面的，保留后面的。
