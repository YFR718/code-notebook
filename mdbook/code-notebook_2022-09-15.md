# Javascript
## 前端
### 10进制转k进制
**123**
```Javascript
123
```
# Python
## list
### 列表定义
**列表是有序集合，没有固定大小，能够保存任意数量任意类型的 Python 对象，语法为 [元素1, 元素2, ..., 元素n] **
```Python
# 直接定义
x = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
# 利用乘号
x= [0] * 3
# 利用range() 创建列表
x = list(range(10))
# 利用推导式创建列表
x = [i for i in range(100) if (i % 2) != 0 and (i % 3) == 0]
# 列表推导式创建二维列表
x = [[0 for j in range(5)] for i in range(5)]
# 魔法命令创建二维列表
x=[[0]*5 for i in range(5)]
```
### 列表添加、删除、获取
**- 尾插、固定位置插入
- 尾删、固定位置删除
- 索引、切片**
```Python
# 尾插一个元素
list.append(obj) 
# 尾插一个list
list.extend(seq)
# 固定位置插入
list.insert(index, obj) 

# 移除列表中某个值的第一个匹配项
list.remove(obj) 
# 移除列表中的一个元素（默认最后一个元素），并且返回该元素的值
list.pop([index=-1]) 
# 删除单个或多个对象
del var1[, var2 ……] 

# 通过元素的索引值
list[index]
# 切片
list[start : stop : step]
```
## 异常处理
### try - except 
**try 语句按照如下方式工作：
1. 首先，执行try 子句（在关键字try 和关键字except 之间的语句）
2. 如果没有异常发生，忽略except 子句， try 子句执行后结束。
3. 如果在执行try 子句的过程中发生了异常，那么try 子句余下的部分将被忽略。如果异常的类型和except 之后的名称相符，那么对应的except 子句将被执行。最后执行try 语句之后的代码。
4. 如果一个异常没有与任何的except 匹配，那么这个异常将会传递给上层的try 中。**
```Python
try:
    int("abc")
    s = 1 + '1'
    f = open('test.txt')
    print(f.read())
    f.close()
except OSError as error:
        print('打开文件出错\n原因是：' + str(error))
except TypeError as error:
        print('类型出错\n原因是：' + str(error))
except ValueError as error:
        print('数值出错\n原因是：' + str(error))
# 数值出错
# 原因是：invalid literal for int() with base 10: 'abc'

dict1 = {'a': 1, 'b': 2, 'v': 22}
try:
        x = dict1['y']
except KeyError:
        print('键错误')
except LookupError:
        print('查询错误')
else:
        print(x)
# 键错误
```
### try - except - finally、else
**不管try子句里面有没有发生异常，finally 子句都会执行。
如果在try子句执行时没有发生异常，Python将执行else 语句后的语句。**
```Python
try:
        检测范围
except Exception[as reason]:
        出现异常后的处理代码
finally:
        无论如何都会被执行的代码

# 如果在try 子句执行时没有发生异常，Python将执行else 语句后的语句。
try:
        检测范围
except(Exception1[, Exception2[,...ExceptionN]]]):
        发生以上多个异常中的一个，执行这块代码
else:
        如果没有异常执行这块代码
```
## 迭代
### enumerate()函数
**enumerate(sequence, [start=0])
1. sequence -- 一个序列、迭代器或其他支持迭代对象。
2. start -- 下标起始位置。
3. 返回 enumerate(枚举) 对象**
```Python
seasons = ['Spring', 'Summer', 'Fall', 'Winter']
lst = list(enumerate(seasons))
print(lst)
# [(0, 'Spring'), (1, 'Summer'), (2, 'Fall'), (3, 'Winter')]

# enumerate() 与 for 循环的结合使用
for i, a in enumerate(A)
        do something with a
```
### 推导式
**可以便捷生成一个列表、元组、字典
[ expr for value in collection [if condition] ]**
```Python
x = [i for i in range(100) if (i % 2) != 0 and (i % 3) == 0]
print(x)
# [3, 9, 15, 21, 27, 33, 39, 45, 51, 57, 63, 69, 75, 81, 87, 93, 99]

a = [(i, j) for i in range(0, 3) if i < 1 for j in range(0, 3) if j > 1]
print(a)
# [(0, 2)]

# 元组推导式
( expr for value in collection [if condition] )
# 字典推导式
{ key_expr: value_expr for value in collection [if condition] }
# 复合推导式
{ expr for value in collection [if condition] }
```
123