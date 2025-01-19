import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('agg')
class PlottingMixin:

    def plot(self, x, y, x_label='Time (Months)', y_label='Net Savings (GBP)'):
        plt.plot(x, y)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        return plt.gcf()

