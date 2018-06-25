#from shutil import copytree
import os
import cv2
import csv
import face_detection as fd

path = os.getcwd()
oldDir = os.path.join(path, 'Research_Datasets\Radbound')
newDir = os.path.join(path, 'RadboundConverted')

'''
#Testing face detection with JAFFE dataset
oldDir = os.path.join(path, 'Research_Datasets\jaffe')
newDir = os.path.join(path, 'JAFFEConverted')
'''
os.mkdir(newDir)

#load cascade classifier training file for haarcascade
#Either need to find or make model for side-face detection in generalized/Radbound datasets
haar_face_cascade = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')

def squarePicFaceDetected(image):
    face_img = fd.crop_faces(haar_face_cascade, image)
    resized = cv2.resize(face_img, (48, 48), interpolation = cv2.INTER_AREA)
    return resized

#crops image to a square crops half the difference off wider axis
def squarePic(image):
    height, width = image.shape[:2] #height then width because numpy
    difference = (height - width)/2
    difference = int(difference)
    if difference < 0: #width is bigger
        cropped = image[0:height, difference:(width - difference)]
    elif difference > 0: #height is bigger
        cropped = image[difference:(height-difference), 0:width]

    return cropped

#makes new name for converted image with emotion as a number
def newNameFromJaffe(name, number):
    num = str(number)
    if name.find('AN') > -1:
        return 'img-'+num+'-0.jpg'
    elif name.find('DI') > -1:
        return 'img-'+num+'-1.jpg'
    elif name.find('FE') > -1:
        return 'img-'+num+'-2.jpg'
    elif name.find('HA') > -1:
        return 'img-'+num+'-3.jpg'
    elif name.find('SA') > -1:
        return 'img-'+num+'-4.jpg'
    elif name.find('SU') > -1:
        return 'img-'+num+'-5.jpg'
    elif name.find('NE') > -1:
        return 'img-'+num+'-6.jpg'
    else:
        #what do we do if it's not one of the 6 basic emotions?
        return 'skip-'+num+'.jpg'

#makes new name for converted image with emotion as a number
def newName(name, number):
    num = str(number)
    if name.find('angry') > -1:
        return 'img-'+num+'-0.jpg'
    elif name.find('disgusted') > -1:
        return 'img-'+num+'-1.jpg'
    elif name.find('fearful') > -1:
        return 'img-'+num+'-2.jpg'
    elif name.find('happy') > -1:
        return 'img-'+num+'-3.jpg'
    elif name.find('sad') > -1:
        return 'img-'+num+'-4.jpg'
    elif name.find('surprised') > -1:
        return 'img-'+num+'-5.jpg'
    elif name.find('neutral') > -1:
        return 'img-'+num+'-6.jpg'
    else:
        #what do we do if it's not one of the 6 basic emotions?
        return 'skip-'+num+'.jpg'

#scans image name for emotion number (last number before extention) returns it as int
def emoNum(name):
    if name.find('0.') > -1: #does the '.' need an escape character?
        return 0
    elif name.find('1.') > -1:
        return 1
    elif name.find('2.') > -1:
        return 2
    elif name.find('3.') > -1:
        return 3
    elif name.find('4.') > -1:
        return 4
    elif name.find('5.') > -1:
        return 5
    elif name.find('6.') > -1:
        return 6
    else:
        return -1 #this will probably cause mistakes later...

#crops images to equal width and height, resizes to 48x48 renames, puts in new directory
def processImages(img_dir, new_dir):
    numPic = 0
    for img_path in os.listdir(img_dir):
        numPic+=1
        img = cv2.imread(os.path.join(img_dir, img_path), -1) #-1 is imread_unchanged
        #warning: even if image path is wrong, no error will be thrown

        resized = cv2.resize(squarePic(img), (48, 48), interpolation = cv2.INTER_AREA)
        #not sure what 3rd param does...

        #resized= squarePicFaceDetected(img)

        #os.rename(img, newName(img_path, numPic)) #should this be img or img_path??
        new_name = newName(img_path, numPic)

        #new_name = newNameFromJaffe(img_path, numPic)

        cv2.imwrite(os.path.join(new_dir, new_name), resized)
        if numPic% 100 == 0:
            print (str((numPic/8040.0)*100)+'%')

def createCSV(name, categories, img_dir):
    with open(name, 'wb') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|',
                                quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(categories)
        for img_path in os.listdir(img_dir):
            img = cv2.imread(os.path.join(img_dir, img_path), -1)
            img_pixels = ' '.join(map(str,img.flatten().tolist()))
            filewriter.writerow([emoNum(img_path), img_pixels])

processImages(oldDir, newDir)
createCSV('RadboundConverted.csv', ['emotion', 'pixels'], newDir)
