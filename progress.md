# 课设进展

1. pip安装 blind-watermark库

   ![image-20211213144858340](https://gitee.com/Wuuconix/image_host/raw/master/image-20211213144858340.png)

2. 运行范例

   ```python
   from blind_watermark import WaterMark
   
   bwm1 = WaterMark(password_wm=1, password_img=1)
   # read original image
   bwm1.read_img('ori_img.jpg')
   # read watermark
   bwm1.read_wm('watermark.png')
   # embed
   bwm1.embed('embedded.png')
   ```

   发现报错

   ![image-20211213145745540](https://gitee.com/Wuuconix/image_host/raw/master/image-20211213145745540.png)

3. 需要安装PyWavelets

   ![image-20211213150026457](https://gitee.com/Wuuconix/image_host/raw/master/image-20211213150026457.png)

4. 原图需要比水印的图片大一些，不然会报错

   ![image-20211213150547026](https://gitee.com/Wuuconix/image_host/raw/master/image-20211213150547026.png)

5. 成功生成出一张嵌入后的图片

   ![image-20211213150621383](https://gitee.com/Wuuconix/image_host/raw/master/image-20211213150621383.png)

   相比原图模糊了许多，但是确实看不到水印的存在。

6. 成功将文本存入图片

   ```python
   from blind_watermark import WaterMark
   import sys
   
   if (sys.argv[1] == "embed"):
       bwm1 = WaterMark(password_img=1, password_wm=1)
       bwm1.read_img('origin/origin.jpg')
       wm = 'flag{wuuconix yyds!}'
       bwm1.read_wm(wm, mode='str')
       bwm1.embed('embedded/embedded_str.png')
       len_wm = len(bwm1.wm_bit)
       print('Put down the length of wm_bit {len_wm}'.format(len_wm=len_wm))
   
   elif (sys.argv[1] == "extract"):
       bwm1 = WaterMark(password_img=1, password_wm=1)
       wm_extract = bwm1.extract('embedded/embedded_str.png', wm_shape=159, mode='str')
       print(wm_extract)
   
   else:
       print("try like python3 str.py embed/extract")
   ```

   ![image-20211213161325393](https://gitee.com/Wuuconix/image_host/raw/master/image-20211213161325393.png)

## 代码学习

### numpy库下的array

![](https://gitee.com/Wuuconix/image_host/raw/master/image-20211214084542256.png)

数组，放的不光是数。

![image-20211214085155544](https://gitee.com/Wuuconix/image_host/raw/master/image-20211214085155544.png)

### YUV

![image-20211214084741213](https://gitee.com/Wuuconix/image_host/raw/master/image-20211214084741213.png)

指的应该是色彩空间。

代码中有类似这样的操作。

![image-20211214095016430](https://gitee.com/Wuuconix/image_host/raw/master/image-20211214095016430.png)

它利用了cv2库中的cvtColor函数将图片从BGR模式转到了YUV模式。

那什么是BGR模式呢，我们可以发现它和RGB长的很像。

![image-20211214095213087](https://gitee.com/Wuuconix/image_host/raw/master/image-20211214095213087.png)

至于为什么cv库中为什么用BGR而不用RGB这种更常见的模式，大概是因为历史遗留问题。

![image-20211214095333311](https://gitee.com/Wuuconix/image_host/raw/master/image-20211214095333311.png)

### cv2

是opencv python二进制拓展库

### cv2中的imraed函数

![image-20211214090452459](https://gitee.com/Wuuconix/image_host/raw/master/image-20211214090452459.png)

![image-20211214090558962](https://gitee.com/Wuuconix/image_host/raw/master/image-20211214090558962.png)

读入一张图片后，其返回值是一个四维数组。且原本的类型都是uint8，即整形。程序中利用astype函数全部转成了小数。

![image-20211214090733022](https://gitee.com/Wuuconix/image_host/raw/master/image-20211214090733022.png)

利用a.shape可以查看图片的尺寸分别是宽和长，但是不知道第三个参数是什么。大概表示有三个通道。

![image-20211214090822415](https://gitee.com/Wuuconix/image_host/raw/master/image-20211214090822415.png)

shape实际上是 np.array的属性，所以这些值代表了array长的样子。

![image-20211214092530478](https://gitee.com/Wuuconix/image_host/raw/master/image-20211214092530478.png)

array 实际上是个函数，它的返回值是ndarry “类”。

![image-20211214092633908](https://gitee.com/Wuuconix/image_host/raw/master/image-20211214092633908.png)

而这个ndarry 就定义了shape这个函数。

### ca

代码中的ca不知道是什么意思，这里设置了它的长宽都为原图的一半。

![image-20211214093900797](https://gitee.com/Wuuconix/image_host/raw/master/image-20211214093900797.png)

![image-20211214093850163](https://gitee.com/Wuuconix/image_host/raw/master/image-20211214093850163.png)

### echo！

```python
def read_img(self, filename):
    # 读入图片->YUV化->加白边使像素变偶数->四维分块
    self.img = cv2.imread(filename).astype(np.float32)
    self.img_shape = self.img.shape[:2]

    # 如果不是偶数，那么补上白边
    self.img_YUV = cv2.copyMakeBorder(cv2.cvtColor(self.img, cv2.COLOR_BGR2YUV),
    0, self.img.shape[0] % 2, 0, self.img.shape[1] % 2,
    cv2.BORDER_CONSTANT, value=(0, 0, 0))

    self.ca_shape = [(i + 1) // 2 for i in self.img_shape]

    self.ca_block_shape = (self.ca_shape[0] // self.block_shape[0], self.ca_shape[1] // self.block_shape[1],
    self.block_shape[0], self.block_shape[1])
    strides = 4 * np.array([self.ca_shape[1] * self.block_shape[0], self.block_shape[1], self.ca_shape[1], 1])

    for channel in range(3):
        self.ca[channel], self.hvd[channel] = dwt2(self.img_YUV[:, :, channel], 'haar')
        # 转为4维度
        self.ca_block[channel] = np.lib.stride_tricks.as_strided(self.ca[channel].astype(np.float32),
        self.ca_block_shape, strides)
```

其中self.img 可能是 一个三维数组。前两位分别是宽和长，如1080*1920。

第三维有三个值，分别代表三个通道的信息，BGR通道和YUV都是三个通道。

![image-20211214110310710](https://gitee.com/Wuuconix/image_host/raw/master/image-20211214110310710.png)

self.img_YUV是将BGR通道转换位YUV通道并 白边补齐后的结果（白边补齐指的是像素不为偶数则补为偶数）

![image-20211214110705940](https://gitee.com/Wuuconix/image_host/raw/master/image-20211214110705940.png)

 self.img_shape 很简单，就是把img的 宽和长截取了出来。

![image-20211214110814463](https://gitee.com/Wuuconix/image_host/raw/master/image-20211214110814463.png)

self.ca_shape 不知道代表什么含义，实际效果就是在原图的基础上把宽和长除以2

![image-20211214110913713](https://gitee.com/Wuuconix/image_host/raw/master/image-20211214110913713.png)

self.ca_block_shape 和 self.block_shape 有关，后者默认为(4.4)

![image-20211214111104968](https://gitee.com/Wuuconix/image_host/raw/master/image-20211214111104968.png)

![image-20211214111010914](https://gitee.com/Wuuconix/image_host/raw/master/image-20211214111010914.png)

135和240分别是ca_shape除以block_shape得来的。后面的两个4就是block_shape。

strides 是在 [960 * 4, 4, 960, 1]的基础上再乘以4，这里可以学习到array可以通过乘一个数，把内部每个数字都乘上这个数。

![image-20211214111735295](https://gitee.com/Wuuconix/image_host/raw/master/image-20211214111735295.png)

self.ca中存放了每个通道的在经历离散小波变换后的近似系数。

![image-20211214162244054](https://gitee.com/Wuuconix/image_host/raw/master/image-20211214162244054.png)

它是一个二维数组，540 * 960。

self.hvd 中存放了某个通道 经历DWT后 其他三个 水平系数、垂直系数、对角线系数。

![image-20211214162533478](https://gitee.com/Wuuconix/image_host/raw/master/image-20211214162533478.png)

相当于 hvd里包含了三个array，分别用 来存储 ch  cv 和cd。

而这些ch cv cd的shape和ca是一样的，都是560 * 960。

self.ca_block 即为二维数字近似系数ca在升到四维后的结果。

它的形状是 (135, 240, 4, 4)

![image-20211214162714707](https://gitee.com/Wuuconix/image_host/raw/master/image-20211214162714707.png)

### array中类似 [:, 0] 的强大用法

这种类似的用法之前在字符串截取中见到过。

![image-20211214150442596](https://gitee.com/Wuuconix/image_host/raw/master/image-20211214150442596.png)

然后numpy中的array实现的效果如下。

![image-20211214150510390](https://gitee.com/Wuuconix/image_host/raw/master/image-20211214150510390.png)

因为是一个二维数组， [:, 0]就把里层数组的第一个数字取出来了。

水印代码中也用到了类似操作。

![image-20211214150630138](https://gitee.com/Wuuconix/image_host/raw/master/image-20211214150630138.png)

self.img_YUV[:, :, 0]相当于就获得了Y通道的所有数据。

![image-20211214150757456](https://gitee.com/Wuuconix/image_host/raw/master/image-20211214150757456.png)

![image-20211214150727406](https://gitee.com/Wuuconix/image_host/raw/master/image-20211214150727406.png)

## dwt2

2d的离散小波变换。 discrete wavelet transformation

![image-20211214151016633](https://gitee.com/Wuuconix/image_host/raw/master/image-20211214151016633.png)

![image-20211214151148381](https://gitee.com/Wuuconix/image_host/raw/master/image-20211214151148381.png)

第一个参数需要一个二维数组。我们传入的是每个通道的数据，正好是二维的。因为有长和宽。

第二个参数大概可以理解为一个小波的种子。

模式就不管了。

第四个参数大概是设定计算DWT的迭代次数？

这个dwt2的返回值是一个元组，它的第一个值 是 近似系数, Approximation coefficients

第二个值还是一个元组，他有三个元素，分别是  水平细节系数 horizontal detail coefficients   垂直细节系数  vertical detail coefficients 对角细节系数 diagonal detail coefficients。

这里就可以解释之前对变量 self.ca 和 self.hvd的疑惑了。

![image-20211214152237323](https://gitee.com/Wuuconix/image_host/raw/master/image-20211214152237323.png)

程序中注释是不是有点问题呢2333，大概是DWT？

## stride 步幅的概念

是numpy中array的一个属性。它是一个元组，存放着每个维度中，一个元素到下一个元素的所需的字节数，即步幅。

例子如下。

![image-20211214154420405](https://gitee.com/Wuuconix/image_host/raw/master/image-20211214154420405.png)

默认array的dtype是64位的int类型，即每个数值都占8个字节。

然后它的步幅是一个元组(16, 8)。元组的第一个元素即表示第一维度的元素的步幅，比如1到3，就需要跨越两个数字，即16个字节。

第二个元素即第二维下两个元素的间隔，很显然就是1个数字，即8个字节。

##  np.lib.stride_tricks.as_strided

利用as_strided函数，我们可以实现将一个数组变维度的操作。

![image-20211214155754090](https://gitee.com/Wuuconix/image_host/raw/master/image-20211214155754090.png)

第一个参数就是我们需要变维的array，第二个参数是设置它的形状，第二个参数是设置它各个 维度的步幅。

![image-20211214155848479](https://gitee.com/Wuuconix/image_host/raw/master/image-20211214155848479.png)

比如这个例子中，我便通过设置一维素组的形状和一维数组的步幅，将a从一个二维数组变成了一个一维数组。

代码中 的升4维便是这样实现的。

![image-20211214160213440](https://gitee.com/Wuuconix/image_host/raw/master/image-20211214160213440.png)

升维或者降维，总的元素个数是不会改变的。

比如ca本来是一个二维数组，它的shape是这样的。

![image-20211214110913713](https://gitee.com/Wuuconix/image_host/raw/master/image-20211214110913713.png)

在生成4维度后，程序后手动设置的形状是这样的。

![image-20211214111010914](https://gitee.com/Wuuconix/image_host/raw/master/image-20211214111010914.png)

而它们的总个数是一致的。

![image-20211214161720369](https://gitee.com/Wuuconix/image_host/raw/master/image-20211214161720369.png)









