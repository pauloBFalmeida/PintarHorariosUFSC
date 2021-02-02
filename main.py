import argparse
import numpy as np
import cv2

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
    
def main(args):
    fileName = args.fileName
    fileCores = args.fileCores if args.fileCores else 'cores.txt'
    transparencia, cores = readCores(fileCores)

    #
    img = cv2.imread(fileName)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    _,threshLinhas = cv2.threshold(gray,20,255,cv2.THRESH_BINARY)
    _,threshPalavras = cv2.threshold(gray,150,255,cv2.THRESH_BINARY)
    
    contours, hier = cv2.findContours(threshLinhas, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    
    cccc = []
    width, height = gray.shape
    # per_contours = []
    area_contours = []
    for i in range(len(contours)):
        cnt = contours[i]
        area = cv2.contourArea(cnt)
        # perimeter = cv2.arcLength(cnt,True)
        # if hier[0,i,3] == -1 and perimeter > width//2 and perimeter < width*11//12:
        # 	per_contours.append( (perimeter, cnt) )
        if hier[0,i,3] == -1 and area > 0:
            cccc.append(cnt)
            area_contours.append( (area, cnt) )
    # sort by perimeter
    area_contours.sort(key=(lambda x: x[0]))
    # find the 8 contours with the min difference between
    seq_i = 0
    seq_difference = 9999
    for i in range(len(area_contours)-8):
        difference = area_contours[i+8][0] - area_contours[i][0]
        # divide by the high value, so difference is related to the number
        # otherwise the first values would be the smallest
        difference /= area_contours[i][0]
        if difference < seq_difference:
	        seq_i = i
	        seq_difference = difference
    # select just the digital rects
    rect_contours = area_contours[seq_i:seq_i+8]
    # remove the perimeter
    for i in range(len(rect_contours)): rect_contours[i] = rect_contours[i][1]

    # show the image
    # draw the contours in the original image # test
    for cnt in cccc:
        cv2.drawContours(img, cnt, -1, (200, 200, 0), 2)
    cv2.imshow('Contours', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

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