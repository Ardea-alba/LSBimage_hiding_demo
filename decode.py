import binascii
import numpy as np
from PIL import Image
import argparse

def decode(pic,origin_pic):
    # 图片展平成一维数组
    w,h=pic.size
    pic=np.array(pic).ravel()
    origin_pic=np.array(origin_pic).ravel()

    # 异或读取数据
    xor_result=np.bitwise_xor(origin_pic,pic)

    # 读取数据长度
    length=0
    t=xor_result[-4:]
    for i in range(4):
        length+=t[-1-i]*(16**(i))

    # 读取数据
    string=""
    for i in xor_result:
        string+=hex(i)[2:]
    string=string[:length]
    string=binascii.a2b_hex(string).decode('utf-8')
    return string

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='从图片中提取隐藏信息')

    # 添加位置参数
    parser.add_argument('-img', default='encoded.png', type=str, help='待解码的图片的地址')
    parser.add_argument('-refer', default='img.png', type=str, help='原图片地址')
    parser.add_argument('-result', default='output.txt', type=str, help='解码后文字的保存地址')

    # 解析参数
    args = parser.parse_args()

    # 解码
    pic=Image.open(args.img)
    picin=Image.open(args.refer)
    decoded_str=decode(picin,pic)
    print(decoded_str)
    with open(args.result, 'w', encoding='utf-8') as f:
        f.write(decoded_str)