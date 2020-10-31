# -*-coding:utf-8 -*-
# Author: w61
# Date: 2020.10.27

import os
import shutil
import xml.etree.ElementTree as ET
import glob
import cv2

class ImgProcess():
    def renameImgAndXml(self,img_path,xml_path):
        '''Rename pictures and XMLs at the same time 
        (for marked VOC format downloaded from the Internet)
        param: img_path: the path of imgs
        param: xml_path: the path of xmls
        '''
        img_filelist = os.listdir(img_path)
        img_filelist.sort()
        img_total_num = len(img_filelist)
        print('img_num:{}'.format(img_total_num))

        xml_filelist = os.listdir(xml_path)
        xml_filelist.sort()
        xml_total_num = len(xml_filelist)
        print('xml_num:{}'.format(xml_total_num))

        new_ann = xml_path + '_new'
        new_img = img_path + '_new'
        if not os.path.exists(new_ann):
            os.mkdir(new_ann)
        if not os.path.exists(new_img):
            os.mkdir(new_img)

        for i, item in enumerate(img_filelist):
            try:
                src = os.path.join(os.path.abspath(img_path), item)
                # img = cv2.imread(src)
                # if img == None:
                #     print(src)
                #     continue
                name = item[:-4] 
                xml_name = os.path.join(xml_path,name+'.xml')
                if os.path.exists(xml_name):
                    s = str(i)
                    s = s.zfill(6)
                    #print(os.path.abspath(img_path + '_new'))
                    dst = os.path.join(os.path.abspath(new_img), s + '.jpg')

                    xml_src = os.path.join(os.path.abspath(xml_path),name+'.xml')
                    xml_dst = os.path.join(os.path.abspath(new_ann),s+'.xml')
                    try:
                        tree = ET.parse(xml_src)
                        root = tree.getroot()
                        node_filename = root.find("filename")
                        node_path = root.find("path")

                        node_filename.text = s + '.jpg'
                        node_path.text = dst

                        tree.write(xml_src)
                    
                        os.rename(src, dst) 
                        os.rename(xml_src,xml_dst) 
                        
                    except Exception as e:
                        print('{} is not existed.'.format(xml_src))

                    #print ('total %d to rename & converted %d jpgs' % (img_total_num, i+1))
            
            except Exception as e:
                pass

    def rename(self,path):
        '''folder batch rename
        Args:
            path: the folder path you want to rename
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
        '''move specified suffix to the specified folder
        param:
        endsname: suffix. e.g. ".jpg"
        source_dir: source path 
        target_dir: target path
        '''
        filelist = os.listdir(source_dir)
        filelist.sort()
        for i,item in enumerate(filelist):
            src = os.path.join(os.path.abspath(source_dir),item)
            print(src)
            if item.endswith(endsname):
                shutil.move(src,target_dir)
    
    def changeXmlObjName(self,xml_path,obj_name):
        '''modify xml files with <object>-<name> exception
        param:
        xml_path: xml path
        obj_name: the name of the object should be. e.g. "smoke"
        '''
        xml_files = glob.glob(os.path.join(xml_path,'*.xml'))
        names= []
        for i,item in enumerate(xml_files):
            tree = ET.parse(item)
            root = tree.getroot()
            node_obj = root.find("object")
            node_obj_name = node_obj.find("name")
            if node_obj_name.text != obj_name:
                node_obj_name.text = obj_name
                tree.write(item)
        for i,item in enumerate(xml_files):
            tree = ET.parse(item)
            root = tree.getroot()
            node_obj = root.find("object")
            node_obj_name = node_obj.find("name")
            if node_obj_name.text not in names:
                names.append(node_obj_name.text)
        print(names)
    
    def delWrongImg(self,img_path,xml_path):
        '''delete broken images
        '''
        img_filelist = os.listdir(img_path)
        img_filelist.sort()
        for item in img_filelist:
            src = os.path.join(os.path.abspath(img_path), item)
            name = item[:-4]
            try:
                img = cv2.imread(src)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
            except:
                print(src)
                xml = os.path.join(os.path.abspath(xml_path), name+'.xml')
                os.remove(src)
                os.remove(xml)

if __name__ == '__main__':
    img_path = '/home/w61/PatternRecognition/smoke/images/images_new'
    xml_path = '/home/w61/PatternRecognition/smoke/Annotations/Annotations_new'
    demo = ImgProcess()
    #demo.moveDir(endsname,source_dir,target_dir)
    demo.delWrongImg(img_path,xml_path)