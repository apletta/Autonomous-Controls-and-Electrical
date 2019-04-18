import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import numpy as np
from dataclasses import dataclass
import pandas as pd

# Path object to store path information
class Path:

    # Point data class object to contain {x,y} points
    @dataclass
    class Point:
        x: float
        y: float

    points = []

    def __init__(self):
        pass

    def add_point(self,x,y):
        self.points.append(self.Point(x,y))

    def get_path(self):
        return self.points

# Creates a user defined path
def cone_generation(file_name='data/test_data.csv'):
    fig = plt.figure()
    ax = plt.subplot(111)
    ax.set_xlim([0,50])
    ax.set_ylim([0,50])

    # Path is a dataclass with fields {x,y}
    path = Path()

    # The mouse click handler method
    def onclick(event):
        if event.inaxes==axsave:
            return

        [x,y] = [round(event.xdata,2),round(event.ydata,2)]
        path.add_point(x,y)
        ax.plot(x,y,'ob')
        fig.canvas.draw()

    # Saves path to file test_data.csv
    def save_path(event):
        p = path.get_path()

        columns = ['x','y']
        points = {'x':[point.x for point in path.points],'y':[point.y for point in path.points]}
        
        df = pd.DataFrame(points,columns=columns)
        df.to_csv(file_name, sep=',',index=False)
        plt.close()

    def exit_without_saving(event):
        plt.close()

    # Creates a save button
    plt.subplots_adjust(bottom=0.2)
    axsave = plt.axes([0.81, 0.05, 0.1, 0.075])
    bsave = Button(axsave, 'Save')
    bsave.on_clicked(save_path)
    
    # Creates an exit button
    axexit = plt.axes([0.1, 0.05, 0.1, 0.075])
    bexit = Button(axexit, 'Exit')
    bexit.on_clicked(exit_without_saving)

    # Creates figure with specified onclick event
    plt.connect('button_press_event', onclick)

    plt.show()

