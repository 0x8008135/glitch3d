import numpy as np
import random

class chip():
    def __init__(self):
        self.counter = 0

        # origin
        self.offset_x = 0.0
        self.offset_y = 0.0
        
        # max value for X Y
        self.x_max = 0.0
        self.y_max = 0.0
        
        # steps
        self.steps = 0.0

        self.lr = False        
        self.reverse = False
        self.random = False
        self.vertical = False

        
    def __iter__(self):
        x=np.arange(self.offset_x,self.offset_x+self.x_max+self.steps,self.steps)
        y=np.arange(self.offset_y,self.offset_y+self.y_max+self.steps,self.steps)
        
        XX,YY =  np.meshgrid(x,y)
        
        if self.lr == False:
            ###############
            # default mode#
            # 0 >->->->-v #
            # 1 v-<-<-<-< #
            # 2 >->->->-> #
            ###############
            for x in range(0,len(XX)):
                if x%2:
                    XX[x] = XX[x][::-1]

        self.coordinates=np.vstack([XX.ravel(), YY.ravel()]).T

        if self.reverse == True and self.vertical == True:
            ###############
            # rev+ver.mode#
            # 0 v<.|v<.|v #
            # 1 v|^|v|^|v #
            # 2 .|^<.|^<. #
            ###############
            self.coordinates=np.vstack(np.fliplr(np.flipud([XX.ravel(), YY.ravel()]))).T
        else:
            if self.vertical == True:
                ################
                # vertical mode#
                # 0 .>v|.>v|^>.#
                # 1 ^|v|^|v|^|v#
                # 2 ^|.>^|.>^|v#
                ################
                self.coordinates=np.vstack(np.flipud([XX.ravel(), YY.ravel()])).T
            
            if self.reverse == True:
                ################
                # reverse  mode#
                # 0 v-<-<-<-<-<#
                # 1 .->->->->-v#
                # 2 v-<-<-<-<-.#
                ################
                self.coordinates=np.vstack(np.fliplr([XX.ravel(), YY.ravel()])).T
        
        
        if self.random == True:
            # true randomness ;)
            self.coordinates = np.random.permutation(self.coordinates)  

        self.counter = 0
        
        return iter(self.coordinates[self.counter])


    def __next__(self):
        self.counter += 1
        return self.coordinates[self.counter]
