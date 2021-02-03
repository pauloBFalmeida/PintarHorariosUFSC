import argparse
import numpy as np
import cv2
from math import ceil

def readCores(fileCores):
    transparencia = None
    cores = None
    with open(fileCores, 'r') as file:
        # retira o \n
        lines = [l[:-1] for l in file.readlines()]
        transparencia = int(lines[0])
        # transforma em tuples com int
        cores = [ tuple([int(i) for i in l.split(',')]) for l in lines[1:] ]
    return transparencia, cores

def criarImgCores(transparencia, cores):
    sizeW, sizeH = 50, 100
    qtdeW = ceil(200 / sizeW)
    qtdeH = ceil(len(cores) / qtdeW)
    width  = (sizeW+1) * qtdeW
    height = (sizeH+1) * qtdeH
    print(qtdeW,",",qtdeH)
    newImage = np.zeros((height,width,3), np.uint8)
    for y in range(1,qtdeH):
        for x in range(1,qtdeW):
            sX = x*sizeW
            sY = y*sizeH
            fX = (x-1)*sizeW
            fY = (y-1)*sizeH
            newImage[sX,sY:fX,fY] = cores[y*qtdeW + x]

    #blank_image[:,0:width//2] = (255,0,0)      # (B, G, R)
    #blank_image[:,width//2:width] = (0,255,0)
    return blank_image
    
def click_event(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            print(x,",",y)
            #refPt.append([x,y])
            #font = cv2.FONT_HERSHEY_SIMPLEX
            #strXY = str(x)+", "+str(y)
            #cv2.putText(img, strXY, (x,y), font, 0.5, (255,255,0), 2)
            cv2.imshow("image", img)

        if event == cv2.EVENT_RBUTTONDOWN:
            blue = img[y, x, 0]
            green = img[y, x, 1]
            red = img[y, x, 2]
            font = cv2.FONT_HERSHEY_SIMPLEX
            strBGR = str(blue)+", "+str(green)+","+str(red)
            cv2.putText(img, strBGR, (x,y), font, 0.5, (0,255,255), 2)
            cv2.imshow("image", img)


def main(args):
    fileName = args.fileName
    fileCores = args.fileCores if args.fileCores else 'cores.txt'
    transparencia, cores = readCores(fileCores)

    imgPicker = criarImgCores(transparencia, cores)



    # transformar jpg em png
    fileNameSplit = fileName.split('.')
    if fileNameSplit[1] in ("jpg", "JPG"):
        image = cv2.imread(fileName)
        fileName = fileNameSplit[0] + ".png"
        cv2.imwrite(fileName, image)

    img = cv2.imread(fileName)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    _,thresh = cv2.threshold(gray,20,255,cv2.THRESH_BINARY)
    contours, hier = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    
    width, height = gray.shape

    cccc = []
    for i in range(len(contours)):
        cnt = contours[i]
        perimeter = cv2.arcLength(cnt, True)
        if perimeter > 100 and perimeter < (width + height) * 1.5:
            cccc.append(cnt)

            #print(perimeter)


            area = cv2.contourArea(cnt)
        
            #valor = abs(1 - (area / ((perimeter/4) ** 2)) )
            valor = abs( area - ((perimeter/4) ** 2) )
            if valor < 0.3:
                print( '' )
                


    #    # if hier[0,i,3] == -1 and perimeter > width//2 and perimeter < width*11//12:
    #    # 	per_contours.append( (perimeter, cnt) )
    #    if hier[0,i,3] == -1 and area > 0:
    #        cccc.append(cnt)
    #        area_contours.append( (area, cnt) )
    ## sort by perimeter
    #area_contours.sort(key=(lambda x: x[0]))
    ## find the 8 contours with the min difference between
    #seq_i = 0
    #seq_difference = 9999
    #for i in range(len(area_contours)-8):
    #    difference = area_contours[i+8][0] - area_contours[i][0]
    #    # divide by the high value, so difference is related to the number
    #    # otherwise the first values would be the smallest
    #    difference /= area_contours[i][0]
    #    if difference < seq_difference:
	   #     seq_i = i
	   #     seq_difference = difference
    ## select just the digital rects
    #rect_contours = area_contours[seq_i:seq_i+8]
    ## remove the perimeter
    #for i in range(len(rect_contours)): rect_contours[i] = rect_contours[i][1]
    def click_event2(event, x, y, flags, param):
        
        if event == cv2.EVENT_LBUTTONDOWN:
            b = img[y, x, 0]
            g = img[y, x, 1]
            r = img[y, x, 2]
            #print(r,",",g,",",b)
            print(img[y, x])


        if event == cv2.EVENT_RBUTTONDOWN:
            print(x,",",y)

    def click_event(event, x, y, flags, param):
        
        if event == cv2.EVENT_LBUTTONDOWN:
            print(x,",",y)
            #refPt.append([x,y])
            #font = cv2.FONT_HERSHEY_SIMPLEX
            #strXY = str(x)+", "+str(y)
            #cv2.putText(img, strXY, (x,y), font, 0.5, (255,255,0), 2)
            cv2.imshow("image", img)

        if event == cv2.EVENT_RBUTTONDOWN:
            blue = img[y, x, 0]
            green = img[y, x, 1]
            red = img[y, x, 2]
            font = cv2.FONT_HERSHEY_SIMPLEX
            strBGR = str(blue)+", "+str(green)+","+str(red)
            cv2.putText(img, strBGR, (x,y), font, 0.5, (0,255,255), 2)
            cv2.imshow("image", img)

    # show the image
    # draw the contours in the original image # test
    for cnt in cccc:
        cv2.drawContours(img, cnt, -1, (200, 200, 0), 1)
    cv2.imshow('image', img)
    cv2.imshow("picker", imgPicker)
    

    cv2.setMouseCallback("image", click_event)
    cv2.setMouseCallback("picker", click_event2)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    events = [i for i in dir(cv2) if 'EVENT' in i]
    print(events)

    
    #cv2.imshow('image',threshLinhas)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()



# run
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("fileName", help="name of the image .jpg file (with the extension .jpg)")
    parser.add_argument('-cores', "--fileCores", help="name of the .txt file (with the extension .txt) (default 'cores.txt')")
    args = parser.parse_args()
    main(args)