"""
@author: Obehi Georgina Dibua

Script to project a 2D image into a 3D thermal profile
for selective sintering of a powder bed
using a previously developed sintering simulation
"""

from PIL import Image
from array import array as ARRAY


# This function creates a meshgrid from dimensions xSize and ySize
# if xSize = 4 and ySize  = 4, meshgrid returns
# x = 
# 0 1 2 3
# 0 1 2 3
# 0 1 2 3
# 0 1 2 3
# and 
# y = 
# 0 0 0 0
# 1 1 1 1
# 2 2 2 2
# 3 3 3 3
def meshgrid(xsize,ysize):

    y = []
    
    xValues = list(range(xsize))
    x = xValues*ysize
    for ct in range(ysize):
        y += [ct]*xsize
        
    return x, y
        
# cast2Dto3D takes in a temperature array and extrudes the temperature array
# in the z direction to give a 3D temperature profile
def cast2Dto3D(tempArray, xsize, ysize, zsize):
    
    x, y = meshgrid(xsize, ysize)
    
    x = x*zsize
    y = y*zsize
    
    z = []
    for ct in range(zsize):
        z += [ct]*xsize*ysize
    
    tempArray3D = tempArray*zsize
    
    return tempArray3D, x, y, z

# convertTemptoColor maps a temperature array to colors for visualization
def convertTemptoColor(tempArray):
   
    colorDic = {0:'white', 450:'yellow', 500:'orange', 550:'red'}
    
    colorArray = []
    for temp in tempArray:
        colorArray.append(colorDic[temp])
    
    return colorArray

# plotFromTemperatureMap makes a 2D plot of a temperature array
# having dimensions of xsize by ysize
# figName is the name of the file to save the plot to
def plotFromTemperatureMap(tempArray,xsize,ysize, figName = 'TemperatureArray.png'):
    
    import matplotlib.pyplot as plt
    
    colorArray = convertTemptoColor(tempArray)
        
    x, y = meshgrid(xsize, ysize)
    
    fig = plt.figure()
    plt.scatter(x, y, c = colorArray)
    plt.xlim([0, ysize])
    plt.ylim([0, xsize])
    fig.savefig(figName)
    plt.close()

# plotFrom3DTemperature Array takes in the temperature, x, y, and z arrays and makes a
# 3D plot of the results cut at position yCut so that internal image details can be seen
# plotSize sets the axis limits
# figName sets the name of the output file
def plotFrom3DTemperatureArray(tempArray3D, x3D, y3D, z3D, yCut = 104, plotSize = 104, figName = 'TemperatureArray3D.png'):
    
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    import numpy as np

    # Get color array from the input temperatures    
    colorArray = convertTemptoColor(tempArray3D)
    
    # convert list to np arrays, necessary for slicing 
    colorArray = np.array(colorArray)
    x3D = np.array(x3D)
    y3D = np.array(y3D)
    z3D = np.array(z3D)
    
    # Find the indices that have y values less than the given yCut cutting plane
    y3D_idx = np.where(y3D < yCut)
    
    # Get the values corresponding to these indices
    x3D = x3D[y3D_idx]
    y3D = y3D[y3D_idx]
    z3D = z3D[y3D_idx]
    colorArray = colorArray[y3D_idx]
    
    # Plot the points
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.set_xlim([0, plotSize])
    ax.set_ylim([0, plotSize])
    ax.scatter(x3D,y3D,z3D,s = 9.8,c='w',marker='o',edgecolor=colorArray)
    ax.view_init(elev=50,azim=45)
    fig.savefig(figName)
    plt.close()
    
# colorToTemperature maps the rgb values from the image file to temperatures passed
# into the sintering simulation. This function can be changed to allow certain color
# ranges map to certain temperatures. In the current scheme the function determines
# if the white area should be sintered or not and the temperatures are determined
# from each pixel's color's proximity to white
# sinterWhite should be True if the white area in the image is the desired sintered area
# otherwise the default of False should be kept
def colorToTemperature(colorArray, sinterWhite = False):
    
    tempArray = []
    
    if sinterWhite:
        # the white area in the image is to be sintered
        for rgb in colorArray:
            color = sum(rgb)
            if color > 750:
                temp = 550
            elif 650 < color < 750:
                temp = 500
            elif 550 < color < 650:
                temp = 450
            else:
                temp = 0
            tempArray.append(temp)
    else:
        # sinter the colored area
        if type(colorArray[0]) == int:
            scale = max(colorArray)
        else:
            scale = sum(max(colorArray))

        for rgb in colorArray:
            if type(rgb) == int:
                color = rgb
            else:
                color = sum(rgb)
                
            if color > 0.7*scale:
                temp = 0
            elif 0.6*scale < color < 0.7*scale:
                temp = 450
            elif 0.5*scale < color < 0.6*scale:
                temp = 500
            else:
                temp = 550
            tempArray.append(temp)        
    
    return tempArray
        
# Given the length of the actual simulation axis (bigSize) and the length of the corresponding 
# side of the image (smallSize). getSpacing determines the area of white space between the 
# edges of the simulation and the edges of the image
def getSpacing(bigSize, smallSize):
    
    spacing = (bigSize - smallSize)//2
    
    return 0, spacing, smallSize + spacing, bigSize


# Main implementation
if __name__ == '__main__':
    
    # Define properties:

    imgName = 'UTLogo.jpg' # Image file name

    # Dimensions of the actual simulation bed
    xsize = 192 
    ysize = 192 
    zsize = 52 
    
    image_width = 180 # size to project image to, should be less than xsize
        
    # Open and read in image file
    img = Image.open(imgName,'r')
    
    # Shrink the image to the size set    
    newSize = (image_width, image_width) # width and height
    img = img.resize(newSize, Image.ANTIALIAS)
    
    # Rotate the image so that it fits properly
    img = img.rotate(180, Image.ANTIALIAS, expand = 1)
    
    # CHECK!
    # Save the image to check resizing
    img.save('ImageScaleAntialias.jpg', quality = image_width)
    
    # Get the pixel rgb values from the resized image
    pixel_values = list(img.getdata())

    # Convert rgb values to temperature
    pixel_values = colorToTemperature(pixel_values, sinterWhite = False)
    
    # Fill in the rest of the 2 by 2 area between the resized image
    # and the x-y dimensions of the bed
    xDivisions = getSpacing(xsize, newSize[0])
    yDivisions = getSpacing(ysize, newSize[1])
    
    fullTempArray = []
    
    for y in range(ysize):
        iy = y - yDivisions[1]
        for x in range(xsize):
            if xDivisions[1] <= x < xDivisions[2] and yDivisions[1] <= y < yDivisions[2]:
                ix = x - xDivisions[1]
                idx = iy*newSize[0] + ix
                fullTempArray.append(pixel_values[idx])
            else:
                fullTempArray.append(0)  
    
    # CHECK!
    # Plot 2D temperature array to check resizing
    plotFromTemperatureMap(fullTempArray, xsize, ysize)
 
    #%% This Section takes the 2D image and extrudes it to 3D
    
    # Expand from 2D to 3D
    fullTempArray3D, x3D, y3D, z3D = cast2Dto3D(fullTempArray, xsize, ysize, zsize)
    
    # # CHECK!
    # # Plot 3D temperature array
    # # This can be commented out to plot the temperature array at different y cut planes
    # plotFrom3DTemperatureArray(fullTempArray3D, x3D, y3D, z3D)
    # plotFrom3DTemperatureArray(fullTempArray3D, x3D, y3D, z3D, yCut = 60, figName = 'TemperatureArray3D_y60Cut.png')
    # plotFrom3DTemperatureArray(fullTempArray3D, x3D, y3D, z3D, yCut = 65, figName = 'TemperatureArray3D_y65Cut.png')
    
    # Change the order/arrangement for parallelization
    # This is necessary because in the parallel sintering simulation
    # the smallest direction is x. So for efficiency the x and z axes are switched
    # so that the temperature distribution matches the simulation bed
    xzfullTempArray3D = []
    x3D = []
    y3D = []
    z3D = []
    
    for iz in range(xsize):
        for iy in range(ysize):
            for ix in range(zsize):
                l = ix*xsize*ysize + iy*xsize + iz
                z3D.append(iz)
                y3D.append(iy)
                x3D.append(ix)
                xzfullTempArray3D.append(fullTempArray3D[l])
    
    # CHECK!
    # Plot to check
    plotFrom3DTemperatureArray(xzfullTempArray3D, x3D, y3D, z3D, ysize, ysize, figName = 'TemperatureArray3D_RotateCheckAll.png')
    
    # Write the temperature array to dat file
    tempProfileFileName = 'tempProfile.dat'
    fill = open(tempProfileFileName,'wb')
    s = ARRAY('d',xzfullTempArray3D)
    s.tofile(fill)
    fill.close()    
    
    #%% This section tests the data out as it will appear when read into the sintering simulation
    
    # Use same order as parallelization
    boxSize = [zsize, ysize, xsize]
    
    pos = [[],[],[],[]]
    
    for iz in range(boxSize[2]):
        for iy in range(boxSize[1]):
            for ix in range(boxSize[0]):
                l = iz*boxSize[0]*boxSize[1] + iy*boxSize[0] + ix
                val = xzfullTempArray3D[l]
                if val:
                    pos[0].append(ix)
                    pos[1].append(iy)
                    pos[2].append(iz)
                    pos[3].append(val)
    
    # CHECK!
    # Plot to check, plotting temperature points
    plotFrom3DTemperatureArray(pos[3], pos[0], pos[1], pos[2], figName = 'TemperatureArray3D_RotateCheckOnlyTemp.png')
                    
    