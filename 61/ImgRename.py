# -*-coding:utf-8 -*-
# Author: w61
# Date: 2020.10.27

import os
import shutil
import xml.etree.ElementTree as ET

class ImgProcess():
    def renameImgAndXml(self,img_path,xml_path):
        '''图片和xml同时改名(针对网上下载好的已标注voc格式)
        param: img_path: 存图片的路径
        param: xml_path: 存xml的路径
        '''
        img_filelist = os.listdir(img_path)
        img_filelist.sort()
        img_total_num = len(img_filelist)

        xml_filelist = os.listdir(xml_path)
        xml_filelist.sort()
        xml_total_num = len(xml_filelist)

        if img_total_num != xml_total_num:
            print('图片数量:{},xml数量:{},两者不一致,请确保两者一致'.format(img_total_num,xml_total_num))
            return

        for i,item in enumerate(img_filelist):
            src = os.path.join(os.path.abspath(img_path), item)
            name = item[:-4] # 每个文件的名字(不含后缀)

            s = str(i)
            s = s.zfill(6)
            if item.endswith('.jpg'):
                dst = os.path.join(os.path.abspath(img_path), s + '.jpg')

            xml_src = os.path.join(os.path.abspath(xml_path),name+'.xml')
            xml_dst = os.path.join(os.path.abspath(xml_path),s+'.xml')
            tree = ET.parse(xml_src)
            root = tree.getroot()
            node_filename = root.find("filename")
            node_path = root.find("path")

            node_filename.text = s + '.jpg'
            node_path.text = dst

            tree.write(xml_src)
        
            os.rename(src, dst) # 改图片名字
            os.rename(xml_src,xml_dst) # 改xml名字

        print ('total %d to rename & converted %d jpgs' % (img_total_num, i+1))

    def rename(self,path):
        '''
        文件夹批量重命名
        param:
        path: 要批量重命名的文件夹名
        '''
        filelist = os.listdir(path)
        filelist.sort()
        total_num = len(filelist)
        for i,item in enumerate(filelist):
            src = os.path.join(os.path.abspath(path), item)
            s = str(i)
            s = s.zfill(6)
            if item.endswith('.png'):
                dst = os.path.join(os.path.abspath(path), s + '.png')
            elif item.endswith('.jpg'):
                dst = os.path.join(os.path.abspath(path), s + '.jpg')

            os.rename(src, dst)
        print ('total %d to rename & converted %d jpgs' % (total_num, i))
    
    def moveDir(self,endsname,source_dir,target_dir):
        '''
        指定后缀名移动到指定文件夹
        param:
        endsname: 文件后缀名
        source_dir: 源文件 
        target_dir: 目标文件
        '''
        filelist = os.listdir(source_dir)
        filelist.sort()
        for i,item in enumerate(filelist):
            src = os.path.join(os.path.abspath(source_dir),item)
            print(src)
            if item.endswith(endsname):
                shutil.move(src,target_dir)

if __name__ == '__main__':
    img_path = '/home/w61/PatternRecognition/Fire_dataset/VOC2020/JPEGImages'
    xml_path = '/home/w61/PatternRecognition/Fire_dataset/VOC2020/Annotations'
    demo = ImgProcess()
    #demo.moveDir(endsname,source_dir,target_dir)
    demo.renameImgAndXml(img_path,xml_path)