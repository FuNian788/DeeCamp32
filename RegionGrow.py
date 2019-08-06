import numpy as np
import random
import cv2 

class grow():
    def __init__(self, img, ColorThreshold, RegionAreaThreshold):
        # 'Seed' is a list which consists of random seeds, it gives only ONE seed to 'OpenList' once.
        self.Seed = []
        # 'OpenList' is a list which consists of a seed from List(Seed) and its near points, 
        #           near points must meet color-threshold conditions.
        self.OpenList = []
        # Eight connected.
        self.Connect = [(-1,-1), (-1,0), (-1,1), 
                        (0, -1),         (0, 1),
                        (1, -1), (1, 0), (1, 1)]
        self.width = img.shape[1]
        self.height = img.shape[0]
        # self.new_img: save region labels.
        self.new_img = np.zeros([self.height, self.width])
        # self.img_mask: save existing areas and blank areas.
        self.img_mask = np.zeros([self.height, self.width], dtype=np.uint8)
        # self.img_edge: save the final edges.
        self.img_edge = np.zeros([self.height, self.width], dtype=np.uint8)

        self.ColorThreshold = ColorThreshold
        self.RegionAreaThreshold = RegionAreaThreshold
        self.RegionNum = 0
        self.Save_Folder = "None"


    ''' Set the save folder.'''
    def Set_Save_Folder(self, folder_path):
        self.Save_Folder = folder_path


    ''' Decide whether the RGB values of two pixels meet the color-threshold condition.'''
    def ColorDifferent(self, x, y):
        color1 = img[x[0]][x[1]]
        color2 = img[y[0]][y[1]]
        difference = np.sqrt(np.sum(np.square(color1-color2)))
        if difference <= self.ColorThreshold:
            return True
        else:
            return False


    ''' Generate many seeds randomly / uniformly.'''
    def GenerateSeed(self, seedtype, parameter):
        if seedtype == "Random":
            for i in range(parameter):
                x = random.randint(0, self.height-1)
                y = random.randint(0, self.width-1)
                self.Seed.append( (x, y) )
        if seedtype == "Uniform":
            x_unit = int(self.height / parameter)
            y_unit = int(self.width / parameter)
            for i in range(parameter):
                for j in range(parameter):
                    self.Seed.append( (i * x_unit, j * y_unit) )
        if seedtype == "all":
            for i in range(self.height):
                for j in range(self.width):
                    self.Seed.append( (i,j) )


    ''' The process of Region-Growing.'''
    def RegionGrow(self):
        self.RegionNum = 1
        print("Let's begin.")
        while (len(self.Seed)>0):
            if( len(self.Seed) % 5 == 0):
                print("There are still {} seeds.".format(len(self.Seed)) ) 
            # 1. Give a seed to 'OpenList' and decide whether it belongs to an existing region.
            OneSeed = self.Seed.pop(-1)
            if self.new_img[OneSeed[0]][OneSeed[1]] == 0:
                self.new_img[OneSeed[0]][OneSeed[1]] = self.RegionNum
                self.OpenList.append(OneSeed)
                # print("Now add a new region.")
            # 2. 'OpenList' first receive a random seed, then add its near pixels(meet color-threshlod condition) to be new seeds.
            #     NOTE: each pixel just use once.
                while(len(self.OpenList)>0):
                    SourceSeed = self.OpenList.pop(-1)
                    x = SourceSeed[0]
                    y = SourceSeed[1]
                    if (x < 0 or y < 0 or x >= self.height or y >= self.width):
                        continue
                    for i in range(8):
                        new_x = x + self.Connect[i][0]
                        new_y = y + self.Connect[i][1]
                        if (new_x >= 0 and new_y >= 0 and new_x < self.height and new_y < self.width):
                            if self.new_img[new_x][new_y] == 0:
                                if self.ColorDifferent(SourceSeed, (new_x, new_y)):
                                    self.new_img[new_x][new_y] = self.RegionNum
                                    self.AddNearPoint(new_x, new_y)  
            # 3. the region whose area belows threshold will be eliminated.
                actual_threshold = int(self.RegionAreaThreshold * self.width * self.height)
                if (np.sum(self.new_img == self.RegionNum) < actual_threshold):
                    self.new_img = np.where(self.new_img == self.RegionNum, 0, self.new_img)
                    continue
            # 4. When the pixels in 'OpenList' run out, use a new random seed to create a new region. 
                self.RegionNum = self.RegionNum + 1
            # print("Now is the {} region.".format(self.RegionNum))
        print("There are {} regions in total.".format(self.RegionNum))


    '''Add near pixels to 'OpenList', which shouldn't be traversed.'''
    def AddNearPoint(self, x, y):
        for i in range(-1,2,1):
            for j in range(-1,2,1):
                if (x+i >= 0 and y+j >= 0 and x+i < self.height and y+j < self.width):
                    if self.new_img[x+i][y+j] == 0:
                        self.OpenList.append( (x, y) )


    ''' Randomly paint all regions.'''
    def AddRandomColor(self, __RegionNum):
        color_img = np.zeros((img.shape[0],img.shape[1],3), np.uint8)
        color_list = [(255,255,255)] * (__RegionNum+1)
        # Create random color.
        for i in range(__RegionNum):
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            color_list[i+1] = (r,g,b)
        # color each region.
        for i in range(len(self.new_img)):
            for j in range(len(self.new_img[0])):
                color = int(self.new_img[i][j])
                for k in range(3):
                    color_img[i][j][k] = color_list[color][k]
        cv2.namedWindow('closed-region image', cv2.WINDOW_NORMAL)
        cv2.imshow('closed-region image', color_img)
        cv2.waitKey(0)


    ''' Color each area using the color of the original image.'''
    def AddSourceColor(self, __RegionNum):
        color_img = np.zeros((img.shape[0],img.shape[1],3), np.uint8)
        color_list = [(255,255,255)] * (__RegionNum+1)
        # 3 channels mean certain color's R/G/B values.
        Certain_Color = np.array([0, 0, 0])

        '''Find the source color. ''' 
        # 'i' means how many regions.
        for i in range(__RegionNum):
            color_tuple = np.where(self.new_img == i+1)
        # 'j' means how many pixels are there in certain region.
            for j in range(len(color_tuple[0])):
        # 'k' means 3 channels.
                for k in range(3):
                    Certain_Color[k] = Certain_Color[k] + img[color_tuple[0][j]][color_tuple[1][j]][k]
            length = max(len(color_tuple[0]), 1)
            Certain_Color = Certain_Color // length
            color_list[i+1] = (Certain_Color[0], Certain_Color[1], Certain_Color[2])
            
        '''Color each region. '''
        for i in range(len(self.new_img)):
            for j in range(len(self.new_img[0])):
                color = int(self.new_img[i][j])
                for k in range(3):
                    color_img[i][j][k] = color_list[color][k]
        cv2.namedWindow('closed-region image', cv2.WINDOW_NORMAL)
        cv2.imshow('closed-region image', color_img)
        print("Now save a image.")
        cv2.imwrite(self.Save_Folder + str(self.RegionNum) + ".jpg", color_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


    ''' Add some remain pixels to be new seeds because one traversal can't detect all regions.'''
    def AddNewSeed(self):
        RemainPixel = np.where(self.new_img == 0)
        for i in range(1000):
            x = random.randint(0, len(RemainPixel[0])-1)
            self.Seed.append((RemainPixel[0][x], RemainPixel[1][x]))

    
    ''' 
        After spreading seeds several times, we think the remaining blank regions belong to 2 types.
            (1) Small blank regions:
                They are too to small to expand to a region.(because of the region-size-threshold.)
                So we just paint them their near region's color.
            (2) Big blank regions:
                They are probably connected regions with complex textures, can't expand well because 
                textures divide the image to many pieces.
                So we just see the blank region as a new region, ignoring its textures.    
    '''
    def NearInfection(self):
        self.img_mask = np.array(np.where(self.new_img == 0, 1, 0), dtype = np.uint8)
        _, labels = cv2.connectedComponents(self.img_mask, connectivity=4)
        # There are 'AreaNum' blank regions at all.
        AreaNum = np.max(labels)
        actual_threshold = int(self.RegionAreaThreshold * self.height * self.width)
        for k in range(AreaNum):
            if ( (k+1) % 100 == 0 ):
                print("Now we paint NO.{}/{} region. Please don't cry.".format(k+1, AreaNum) )
            if np.sum(labels == k+1) < actual_threshold:
                near_pixel = (np.where(labels == k+1)[0][0], np.where(labels == k+1)[1][0])
                near_pixel_region = self.new_img[near_pixel[0]][near_pixel[1]-1]
                self.new_img = self.new_img + (np.where(labels == k+1, near_pixel_region, 0))
            else:
                self.RegionNum = self.RegionNum + 1
                self.new_img = self.new_img + (np.where(labels == k+1, self.RegionNum, 0))

        
    '''Draw edges by traversing 8 neighborhoods.'''
    def DrawEdge(self):
        for i in range(1, self.height-1, 1):
            for j in range(1, self.width-1, 1):
                for m in range(-1, 2, 1):
                    for n in range(-1, 2, 1):
                        if self.new_img[i+m][j+n] != self.new_img[i][j]:
                            self.img_edge[i][j] = 255
                            continue
                    continue
        cv2.imshow("final edge", self.img_edge)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        cv2.imwrite(self.Save_Folder + "final.jpg", self.img_edge)




if __name__ == "__main__":
    img = cv2.imread("G:/Deecamp/1.jpg")
    print("The image shape is {}.".format(img.shape))

    '''
        First parameter: the source image.
        Second parameter: color threshold.
        Third parameter: the region whose area belows threshold will be eliminated.
                         actual_threshold = RegionAreaThreshold * img_height * img_width)      
    '''
    Op = grow(img, 9, 0.001)
    Op.Set_Save_Folder("G:/Deecamp/cat/")

    '''
        There are 3 type of seed-generate methods. "random", "unform" and "all".
            if seedtype == "random", parameter means "the number of seeds."
            if seedtype == "uniform", parameter means "the image has parameter*parameter blocks/seeds."
            if seedtype == "all", parameter means "all the pixels are seeds."
    '''
    Op.GenerateSeed("Uniform", 40)
    # Op.GenerateSeed("random", 1000)
    # Op.GenerateSeed("all", "None")

    Op.RegionGrow()
    Op.AddSourceColor(Op.RegionNum)
    # The image has 'i' chances to find all regions.
    for i in range(2):
        Op.AddNewSeed()
        Op.RegionGrow()
        Op.AddSourceColor(Op.RegionNum-1)

    print("Now we deal with small empty regions.")
    Op.NearInfection()
    Op.AddSourceColor(Op.RegionNum)
    print("there are {} pixels still no region.".format(np.sum(Op.new_img == 0)))
    Op.DrawEdge()
    
 

