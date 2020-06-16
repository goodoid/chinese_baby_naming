# 根据康熙字典 起名

using step
===========

step1: 根据笔画数，获取康熙字典的字和五行属性

```python
python kx_word_extract.py 5  #这里获取的5划的字, 输出到文件
```

step2: 根据候选字文件生成名字

```python
# 比如生成第二个字1笔画，第三个字5笔画的所有组合
python naming.py tid3_wd1.agg tid3_wd5.agg
```
    
