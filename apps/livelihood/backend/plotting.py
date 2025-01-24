import matplotlib
import matplotlib.pyplot as plt
import numpy as np
matplotlib.use('agg')
class PlottingMixin:

    def plot(self, x, y, x_label='Time (Months)', y_label='Net Savings (GBP)'):
        plt.close()
        plt.plot(x, y, '-o')
        for xitem,yitem in np.nditer([x,y]):
            y_point = "{:.1f}".format(yitem)
            plt.annotate(y_point, (xitem,yitem), textcoords="offset points",xytext=(0,10),ha="center")
        plt.grid(True)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        return plt.gcf()

