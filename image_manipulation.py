import sys
import os
import numpy as np
import glob as glob
import matplotlib.pyplot
import pandas as pd
from pathlib import Path
import PIL
from PIL import Image,ImageDraw,ImageFont
import csv
import cv2
from itertools import chain


def image_read():
    #os.makedirs('C:\\Amrita\\Pythoncodes\\images\\results')
    file_path = 'C:\\Amrita\\Pythoncodes\\images\\imagefolder'
    file_list = [files for files in os.listdir(file_path) if files.endswith(".jpg")]

    raw_data = {'xmin': [70,70,70,70,70],
            'ymin': [50,50,50,50,50],
            'xmax': [240,240,240,240,240],
            'ymax': [140,140,140,140,140]}
    df = pd.DataFrame(raw_data, columns = [ 'xmin', 'ymin', 'xmax', 'ymax'])
    df.to_csv('C:/Amrita/Pythoncodes/images/txt_csv/pxl.csv')
    data = pd.read_csv('C:/Amrita/Pythoncodes/images/txt_csv/pxl.csv')

    for each_file in file_list:
        txt_file(each_file, file_path)
        maskblack_file(each_file, file_path)
        bbox_image(each_file, file_path)
        crop_image(each_file, file_path)


#image pixels
def txt_file(image_name, file_path):
    image_path = file_path+'\\'+image_name
    images = Image.open(image_path)
    #print(images)
    size = width, height = images.size
    #print(size)
    coordinates= x,y = 50,80
    #print(images.getpixel(coordinates))

#pixel coordinate list
data_list = [['xmin','ymin','xmax','ymax'],['70', '50', '240', '140'], ['70', '50', '240', '140'], ['70', '50', '240', '140'], ['70', '50', '240', '140'], ['70', '50', '240', '140']]
with open('C:/Amrita/Pythoncodes/images/list_txt/listfile.txt', 'w') as f:
    for listitem in data_list:
        f.write('%s\n' % listitem)


#list to csvfile
def WriteListToCSV(csv_file,csv_columns,data_list):
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.writer(csvfile, dialect='excel',lineterminator='\n', quoting=csv.QUOTE_NONE)
            writer.writerow(csv_columns)
            for data in data_list:
                writer.writerow(data)
    except IOError as error:
        print(error)

csv_columns = ['Imageid','xmin','ymin','xmax','ymax']
csv_data_list = [['dalia','70', '50', '240', '140'], ['lotus','70', '50', '240', '140'], ['rose','70', '50', '240', '140'], ['sflower','70', '50', '240', '140'], ['tulip','70', '50', '240', '140']]

currentPath = "C:/Amrita/Pythoncodes/images/txt_csv"
csv_file = currentPath + "/pixels.csv"
WriteListToCSV(csv_file,csv_columns,csv_data_list)


# large csv file to single csv file with each differnt names
def split_file(filename, pattern, size):
 with open(filename, 'rb') as f:
        header = next(f)
        for index, line in enumerate(f, start=1):
            with open(pattern.format(index), 'wb') as out:
                out.write(header)
                n = 0
                for line in chain([line], f):
                    out.write(line)
                    n += len(line)
                    if n >= size:
                        break

split_file('C:/Amrita/Pythoncodes/images/txt_csv/pixels.csv', 'C:/Amrita/Pythoncodes/images/txt_csv/each_csv/image_{0:03d}.csv', 1)


#Create the basic black image
def maskblack_file(image_name, file_path):
    image_path = file_path+'\\'+image_name
    save_file_name = str(image_name.split(".")[0])
    path = 'C:\\Amrita\\Pythoncodes\\images\\txt_csv\\each_csv'
    #image size array
    rect = np.array([[0,0,260,190],[0,0,500,500],[0,0,260,190],[0,0,180,270],[0,0,260,190],[0,0,220,220]])
    #plane black masking
    mask = np.zeros((256,256,3), dtype="uint8")
    for (x1,y1,x2,y2) in rect:
      img = cv2.rectangle(mask,(x1,y1),(x2,y2), -1)
      with open('C:/Amrita/Pythoncodes/images/txt_csv/pxl.csv', 'r') as csvfile:
          so = csv.reader(csvfile, delimiter=',',quotechar='"')
          so_data = []
          for row in so:
              so_data.append(row[1:])
              #print('rows=',row)
          #print('so data=',so_data)
          values =so_data[1:]
          #print('values=',values)
          for (xmin,ymin,xmax,ymax) in values:
              #print(typr(xmin)) 'type is str so make it int'
      #non filled retangle
              cv2.rectangle(img,(int(xmin),int(ymin)),(int(xmax),int(ymax)),(0,255,0),3)
      #filled retangle
              cv2.rectangle(img,(int(xmin),int(ymin)),(int(xmax),int(ymax)),(255,255,255),-1)
              cv2.imwrite("C:\\Amrita\\Pythoncodes\\images\\masks\\"+ save_file_name +'_masked.jpg',mask)

#image bounding box
def bbox_image(image_name, file_path):
    image_path = file_path+'\\'+image_name
    save_file_name = str(image_name.split(".")[0])
    source_img = Image.open(image_path).convert('RGB')
    draw = ImageDraw.Draw(source_img)
    with open('C:/Amrita/Pythoncodes/images/txt_csv/pxl.csv', 'r') as csvfile:
        so = csv.reader(csvfile, delimiter=',',quotechar='"')
        so_data = []
        for row in so:
            so_data.append(row[1:])
            #print('rows=',row)
        #print('so data=',so_data)
        values =so_data[1:]
        #print('values=',values)
        for (xmin,ymin,xmax,ymax) in values:
            draw.rectangle(((int(xmin), int(ymin)), (int(xmax), int(ymax))), outline="yellow")
            source_img.save("C:\\Amrita\\Pythoncodes\\images\\bbox\\"+ save_file_name +'_bbox.jpg',"JPEG")


#image cropping
def crop_image(image_name, file_path):
    image_path = file_path+'\\'+image_name
    image = Image.open(image_path)
    with open('C:/Amrita/Pythoncodes/images/txt_csv/pxl.csv', 'r') as csvfile:
        so = csv.reader(csvfile, delimiter=',',quotechar='"')
        so_data = []
        for row in so:
            so_data.append(row[1:])
            #print('rows=',row)
        #print('so data=',so_data)
        values =so_data[1:]
        #print('values=',values)
        for (xmin,ymin,xmax,ymax) in values:
            image2 = image.crop((int(xmin),int(ymin),int(xmax),int(ymax) ))
            image2.save("C:\\Amrita\\Pythoncodes\\images\\cropped\\"+ str(image_name.split(".")[0]) +'_cropped.jpg')

#call main read function here
image_read()
