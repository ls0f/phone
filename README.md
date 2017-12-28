[![Build Status](https://travis-ci.org/lovedboy/phone.svg?branch=master)](https://travis-ci.org/lovedboy/phone)

## 手机号码库

#### 安装

使用pip安装:

```
pip install phone

```
或者直接clone源码。

使用：

```
from phone import Phone
p  = Phone()
p.find(1888888)
```

### 支持号段
13\*,15\*,18\*,14[5,7],17[0,6,7,8]

#### 记录条数

360569 (updated:2017年4月)

#### 其他语言支持

下载[phone.dat](https://github.com/lovedboy/phone/raw/master/phone/phone.dat)文件，用其他语言解析即可。

* [lua解析](https://gist.github.com/lovedboy/bbff19c91e3d98388d52)，如果不支持bit32，用[这个](https://gist.github.com/lovedboy/fe7750e202572712615a)。
* [go解析](https://github.com/xluohome/phonedata)。
* [Node解析](https://github.com/conzi/phone)。


#### phone.dat文件格式

```

        | 4 bytes |                     <- phone.dat 版本号
        ------------
        | 4 bytes |                     <-  第一个索引的偏移
        -----------------------
        |  offset - 8            |      <-  记录区
        -----------------------
        |  index                 |      <-  索引区
        -----------------------

```

* `头部` 头部为8个字节，版本号为4个字节，第一个索引的偏移为4个字节(<4si)。      
* `记录区` 中每条记录的格式为"\<省份\>|\<城市\>|\<邮编\>|\<长途区号\>\0"。 每条记录以'\0'结束。  
* `索引区` 中每条记录的格式为"<手机号前七位><记录区的偏移><卡类型>"，每个索引的长度为9个字节(`<iiB`)。

解析步骤:

 * 解析头部8个字节，得到索引区的第一条索引的偏移。
 * 在索引区用二分查找得出手机号在记录区的记录偏移。
 * 在记录区从上一步得到的记录偏移处取数据，直到遇到'\0'。
 
我定义的卡类型为:

* 1 移动
* 2 联通
* 3 电信
* 4 电信虚拟运营商
* 5 联通虚拟运营商
* 6 移动虚拟运营商

## License
#### [MIT](https://opensource.org/licenses/mit-license.php)
