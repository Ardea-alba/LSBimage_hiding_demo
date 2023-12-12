import numpy as np
from PIL import Image
import argparse

def encode(pic,string):
    w,h=pic.size

    # 将数据转换为十六进制
    by =bytes(string,encoding='utf8')#将字符串以UTF8方式转换为字节
    data=by.hex()

    # 两个展开的数组做异或运算
    picarray=np.array(pic).ravel()
    dataarray=np.zeros((w,h,3),dtype='uint8').ravel()
    assert len(data)<16**4 or len(data)<len(picarray)-4, "文本编码长度大于图片容量"
    for i in range(len(data)):
        dataarray[i]+=int(data[i],base=16)
    picarray=np.bitwise_xor(dataarray,picarray)

    # 尾部记录数据长度
    length=len(data)
    for i in range(4):
        if len(hex(length))-2<i+1:
            break
        picarray[-i-1]=np.bitwise_xor(picarray[-i-1],int(hex(length)[-i-1],base=16))

    # 将数组转换为图像
    picout=Image.fromarray(picarray.reshape(h,w,3))
    return picout

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='将txt文本藏入png图片')

    # 添加位置参数
    parser.add_argument('-img', default='img.png', type=str, help='原图片地址')
    parser.add_argument('-txt', default='input.txt', type=str, help='待编码文本地址')
    parser.add_argument('-result', default='encoded.png', type=str, help='编码后图片地址')

    # 解析参数
    args = parser.parse_args()

    # 读取数据
    pic=Image.open(args.img)
    string=open(args.txt,"r",encoding="utf-8").read()

    # 编码
    picout=encode(pic,string)
    picout.save(args.result)