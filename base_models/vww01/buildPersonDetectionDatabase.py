from pycocotools.coco import COCO
import numpy as np
import skimage.io as io
from skimage.color import gray2rgb
from skimage.transform import resize
import matplotlib.pyplot as plt
import os

# Parameters, change directories for a local run
useLocalCoco=True
debugCats=False
debugPlot=False
dataDir='/Users/antorrin/Desktop'
annDir='/Users/antorrin/Desktop/annotations'

# Looking for people as wakeword, 2.5% area of image for a person, be careful with other parameters
wakeword='person'
areaRatio=.025
useBoundingBoxArea=True
imgSize = 96

# Generation function for each dataset portion
def generateInstance(dataType, outputDataDir):

    # initialize COCO api for instance annotations
    annFile='{}/instances_{}.json'.format(annDir,dataType)
    print(dataType + ', starting processing');
    coco=COCO(annFile)

    # display COCO categories and supercategories
    if( debugCats ):
        cats = coco.loadCats(coco.getCatIds())
        nms=[cat['name'] for cat in cats]
        print('COCO categories: \n{}\n'.format(' '.join(nms)))

        nms = set([cat['supercategory'] for cat in cats])
        print('COCO supercategories: \n{}'.format(' '.join(nms)))

    # Get all images containing given categories
    catIds = coco.getCatIds(catNms=wakeword);

    # Create the output directories
    if not os.path.exists(outputDataDir):
        os.makedirs(outputDataDir)
    if not os.path.exists('%s/%s'%(outputDataDir,wakeword)):
        os.makedirs('%s/%s'%(outputDataDir,wakeword))
    if not os.path.exists('%s/non_%s'%(outputDataDir,wakeword)):
        os.makedirs('%s/non_%s'%(outputDataDir,wakeword))

    # Loop over all images and process
    print(dataType + ', wrinting ' + str(len(coco.imgs)) + ' images...');
    index = 0
    for image in coco.imgs:
        # Read image
        img = coco.loadImgs(image)[0]
        if( useLocalCoco ):
            I = io.imread('%s/%s/%s'%(dataDir,dataType,img['file_name']))
        else:
            I = io.imread(img['coco_url'])
        
        # Convert to RGB if needed
        if( I.ndim == 2 ):
            I = gray2rgb(I)

        # Get annotation
        annIds = coco.getAnnIds(imgIds=img['id'], catIds=catIds, iscrowd=False)
        anns = coco.loadAnns(annIds)

        # Debug plot
        if( debugPlot ):
            plt.imshow(I); plt.axis('off')
            coco.showAnns(anns)
            plt.show()

        # Area of image for ratio calculations
        imageArea = I.shape[0]*I.shape[1]

        # Check if at least a person is present
        fullFileName = ''
        if( len(anns) > 0 ):
            for ann in anns:
                # Check if annotation's area is large enough
                # If not skip image altogether
                if( useBoundingBoxArea ):
                    annArea = ann['bbox'][2]*ann['bbox'][3]
                else:
                    annArea = ann['area']

                if( annArea/imageArea > areaRatio ):
                    fullFileName = '%s/%s/%s'%(outputDataDir,wakeword,img['file_name'])
                    break
        else:
            fullFileName = '%s/non_%s/%s'%(outputDataDir,wakeword,img['file_name'])

        # Resize and write only we didn't skip
        if( len(fullFileName) ):
            I = resize(I, (imgSize, imgSize), anti_aliasing=True)
            io.imsave(fullFileName, (255*I).astype(np.uint8), check_contrast=False)
        
        # Show progress
        index += 1
        if( (index % 1000) == 0 ):
            print(dataType + ', index=' + str(index))


# Generate for training set, COCO2014
outputDataDir = './vw_coco2014_96_2p5b'
dataType='train2014'
generateInstance(dataType, outputDataDir)

# Then for validation set, COCO2014
outputDataDir = './vw_coco2014_96_2p5b'
dataType='val2014'
generateInstance(dataType, outputDataDir)