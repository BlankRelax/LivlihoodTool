from typing import Optional
import numpy as np
from scipy.signal import savgol_filter  
from apps.livelihood.backend.plotting import PlottingMixin

class Expense(PlottingMixin):
    YEARLY_COST=None
    MONTHLY_COST=None
    WEEKLY_COST=None
    YEARS = 5
    MONTHS = range(1,12*YEARS+1)

    def __init__(self,yearly_cost=0,monthly_cost=0,weekly_cost=0):
        self.YEARLY_COST=yearly_cost
        self.MONTHLY_COST=monthly_cost
        self.WEEKLY_COST=weekly_cost
        
        if not self.MONTHLY_COST:
            self.MONTHLY_COST = int(yearly_cost)/12
        
        if not self.WEEKLY_COST:
            self.WEEKLY_COST = int(yearly_cost)/52
        
    def plot(self):
        super().plot(self.MONTHS, [self.MONTHLY_COST]*12*self.YEARS)
    
class Income(PlottingMixin):
    MONTHS = range(1,(12*5)+1)
    def __init__(self,yearly=0,monthly=0,weekly=0, offset=0,  yearly_increase=0):
        self.YEARLY=yearly
        self.MONTHLY=monthly
        self.WEEKLY=weekly
        self.OFFSET=offset
        self.YEARLY_INCREASE=yearly_increase
        self.MONTHLY_INCREASE=yearly_increase/12
        
        if not self.MONTHLY:
            self.MONTHLY = int(yearly)/12
        
        if not self.WEEKLY:
            self.WEEKLY = int(yearly)/52
    
    def smooth(self,y, interval)->list:
        arr = np.array(y)
        return savgol_filter(arr, interval, polyorder=3)
    
    def iterate_income(self):
        for month in enumerate(self.MONTHS):
            if month==1:
                yield self.MONTHLY
            else:
                yield self.MONTHLY+(month*self.MONTHLY_INCREASE)

    @staticmethod
    def mod_int_div(x,y):
        if not x%y:
            return x//y
        else:
            return 0

    def net(self,expense:list[Expense], plot:bool=True, smooth_interval = 0, income:Optional[list]=None):
        """
        Calculate monthly net income after expense deductions 
        """
        net = []
        net_expense_list = []
        if not income:
            #init empty Income object
            income=[Income()]
            
        for month in self.MONTHS:
            net_exp=0
            net_income=0
            current_yearly = self.YEARLY_INCREASE*(month//12)+self.YEARLY
            current_monthly = current_yearly/12
            for exp in expense:
                #calculate net expenses 
                net_exp+=exp.MONTHLY_COST
            for inc in income:
                net_income+=inc.MONTHLY+(month*inc.MONTHLY_INCREASE)
            
            new=(self.OFFSET+current_monthly)-net_exp

            net_expense_list.append(new)
            self.OFFSET=new
        if smooth_interval:
            net_expense_list = self.smooth(net_expense_list,smooth_interval)
            
        
        if plot:
            self.plot(self.MONTHS, net_expense_list, 'Time (Months)', 'Net Savings (GBP)')
        else:
            return net
    

        



if __name__=='__main__':
    rent = Expense(monthly_cost=1600)
    bills = Expense(monthly_cost=117)
    travel = Expense(monthly_cost=24*4)
    food = Expense(monthly_cost=150)
    car = Expense(monthly_cost=500)
    income=Income(yearly=27000, offset=11000, yearly_increase=2500)
    side_income=Income(yearly=1000, yearly_increase=0)
    income.net([rent, bills, travel, food, car],plot=True,smooth_interval= 24, income=[side_income])
    


        
        