车辆段项目模块组

## 一 项目说明：
###		简介：***

## 二 代码规范说明

###		1) 命名规范
a: odoo字段功能函数compute、search 、default分别以下划线 (_) 和具体功能开头，例如: _compute_name_</br>  
b: 普通变量采用单词加下划线(_)隔开命名,单词不可以采用缩写形式，函数局部变量除外， 例如：name_project   c: 全局变量及其类变量必须大写  
d: 私有变量和函数采用python规范,下划线开头  
e: 相关常用属性变量变量命名采用 ”变量属性_变量具体含义“形式，例如： name_project, number_project, count_project等,这样有利于变量具体查找和使用  
f: 函数尽量采用动词作为前缀,后接名词表示具体用处命名方式,例如: make_name, search_name

###	  2) 函数规范
a: 注释应当添加,但是更应该尽量让代码有自解释(自解释的含义是指函数可以更具上下变量及其函数命名说明函数功能，这比注释更加有效，注释会因为代码反复修改而不及时更新，导致注释错误)  
b: 函数的功能应该单一，不应该一个函数出现多个功能，多个功能函数应该拆分几个函数，这样有利于以更小的代价去维护代码  
c: 一个函数应该有少量的return  
e: 函数代码的行数最多应该是显示器一屏能看完，大概六十行，这样有利于代码的阅读  
f: 函数因该保持尽量少的嵌  
g: 项目中不能出现两个工功能相同的函数,必须保证函数功能的唯一性
###  3) 类
***
###  4)注释
***
###  5) 项目结构
a) 通用功能应该采用共用的py文件  
b）根据功能为每一个功能建立package,各个部分之间必须隔离  
c) 一个py文件应该只包含相同的class及其函数  
d) 导入包应该先import 然后 import xxx from排列
### 6) odoo使用规范
a) record的id必须加功能前缀,例如action_xxxx, tree_xxxx, form_xxx  
b) 记录数据安全必须采用dooo记录安全过滤机制,不可以仅仅进行简单的domain过滤  
c) __manifest__ datexml数据顺序必须按照加载先后排序, __init__ py文件加载同样如此  
[其余代码规范参考google python规范](https://google.github.io/styleguide/pyguide.html)  



##三 项目结构说明  
项目模块主要分别为 知识产权模块(intellectual_property) 、研究经费模块(research_funds) 、研究项目模块(research_projetc)、科研成果模块(research_achievements) 和基础数据模块(funenc_base)  


## 四 开发说明  
a)  模块项目文件应当保证项目文件结构按类分割  
b)  项目模块开发同时需将测试用例增加相应模块test下  



