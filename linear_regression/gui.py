#!/usr/bin/python3

import numpy as np
import cv2
import linear_regression as lr

WINDOWS_NAME = 'regression'

def createCanva(canvaY,canvaX):
    return np.zeros((canvaY,canvaX), dtype='uint8')
#
def mouseControl(event,x,y,flags,param):
    global x_graph, y_graph, canva,learning_rate
    if event == cv2.EVENT_LBUTTONDOWN:
        canva[y,x,cGREEN]     = 255
        x_graph = np.append(x_graph, x)
        y_graph = np.append(y_graph, y)
        learning_rate = learning_rate * 10

def nothing(**args):
    pass

try:
    global x_graph, y_graph, canva, learning_rate
    cBLUE=0
    cGREEN=1
    cRED=2
    x_graph = np.array([],dtype = 'int' )
    y_graph = np.array([],dtype = 'int' )
    canva = createCanva(300,300)
    canva = cv2.cvtColor(canva.astype('uint8'), cv2.COLOR_GRAY2RGB)

    x = np.arange(0,300,1)
    
    thetas = []
    costs = []
    theta = lr.init_theta(2)    
    
    cv2.namedWindow(WINDOWS_NAME)
    cv2.setMouseCallback(WINDOWS_NAME,mouseControl)
    
    learning_rate = 0.001
    while True:
        
        cv2.imshow(WINDOWS_NAME,canva)
            
        y_h = lr.hyp_func(x, theta)
        canva[:,:, cRED] = 0
        for i in range(x.size):
            if y_h[i] <= 299 and y_h[i] >= 0 :
                canva[int(y_h[i]),x[i], cRED] = 250
        
        if len(x_graph):
            theta =  lr.gradient_descent(x_graph, y_graph, theta, learning_rate)
            print(lr.cost_function(lr.hyp_func(x_graph, theta), y_graph))
            print(learning_rate)
            thetas.append(theta)
            costs.append(lr.cost_function(lr.hyp_func(x_graph, theta), y_graph))
        
        
        if len(costs) >=10 and costs[-1] == max(costs[-3:]):
            learning_rate = learning_rate / 5
        elif len(costs) >=10 and costs[-1] == min(costs[-5:]):
            learning_rate = learning_rate * 2 
            
        if learning_rate <= 0.000001:
            learning_rate = 0.000001
#        elif len(costs) >=3 and costs[-1] <= costs[-2]:
#            learning_rate = learning_rate * 3

        k = cv2.waitKey(1) & 0xFF
        if k == ord('q'):
            cv2.destroyAllWindows()
            break
    
except Exception as error:
    print('Error: ' + str(type(error)) + ' - ' + str(error.args))
    cv2.destroyAllWindows()
    
from matplotlib import pyplot as plt
thetass = np.array(thetas) 
costss = np.array(costs)
plt.scatter(thetass[:,0],thetass[:,1])
plt.plot(costss)

plt.plot(thetass[:,0])
plt.plot(thetass[:,1])
        
