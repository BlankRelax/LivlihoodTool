from typing import Optional
import numpy as np
from scipy.signal import savgol_filter  
from apps.livelihood.backend.plotting import PlottingMixin

class BaseEntity:

    def __init__(self, yearly=0, monthly=0, weekly=0, offset=0, increase=0):
        """
        offset: YEARLY offset, e.g savings or dept
        increase: YEARLY increase or decrease
        """
        self.YEARLY = yearly
        self.MONTHLY = monthly
        self.WEEKLY = weekly
        self.OFFSET =offset
        self.INCREASE = increase
        self.complete_init()
        self.complete_variables()

    def complete_variables(self):
        self.OFFSET_MONTHLY = self.OFFSET/12
        self.OFFSET_WEEKLY = self.OFFSET_MONTHLY/4

        self.INCREASE_MONTHLY = self.INCREASE/12
        self.INCREASE_WEEKLY = self.INCREASE_MONTHLY/4

    def complete_init(self):
        if not self.YEARLY:
            if self.MONTHLY:
                self.YEARLY=self.MONTHLY*12
            elif self.WEEKLY:
                self.MONTHLY = self.WEEKLY*4
                self.YEARLY = self.MONTHLY*12
        elif not self.MONTHLY:
            self.MONTHLY=self.YEARLY/12
            if not self.WEEKLY:
                self.WEEKLY=self.MONTHLY/4
        if not self.WEEKLY:
            self.WEEKLY=self.MONTHLY/4
    
    def cum_monthly(self, number_of_months:int):
        months = range(1,number_of_months+1)
        cum=[self.MONTHLY+(self.INCREASE_MONTHLY*i)+(self.OFFSET_MONTHLY*i) for i,_ in enumerate(months)]
        return np.array(cum)
    
    def cum_yearly(self, number_of_years:int):
        years = range(1,number_of_years+1)
        cum=[self.YEARLY+(self.INCREASE*i)+(self.OFFSET*i) for i,_ in enumerate(years)]
        return np.array(cum)



    @property
    def currency(self):
        return 'GBP'
    def __str__(self):
        return(f"YEARLY: {self.YEARLY}, MONTHLY: {self.MONTHLY}, WEEKLY {self.WEEKLY} {(self.currency)}")

            


class Expense(BaseEntity,PlottingMixin):
    

    def __init__(self,yearly_cost=0,monthly_cost=0,weekly_cost=0):
        super().__init__(yearly=yearly_cost, monthly=monthly_cost, weekly=weekly_cost)
        
    def plot(self):
        super().plot(self.MONTHS, [self.MONTHLY_COST]*12*self.YEARS)
    
class Income(BaseEntity, PlottingMixin):
    
    def __init__(self,yearly=0,monthly=0,weekly=0, offset=0,  yearly_increase=0):
        super().__init__(yearly=yearly, monthly=monthly, weekly=weekly, offset=offset, increase=yearly_increase)
    
    def smooth(self,y, interval)->list:
        arr = np.array(y)
        return savgol_filter(arr, interval, polyorder=3)
    

    def net(self,expense:list[BaseEntity], plot:bool=True, smooth_interval = 0, income:Optional[BaseEntity]=None):
        """
        Calculate monthly net income after expense deductions 
        """
        net = np.array([0]*5)
        net_expense_list = np.array([0]*5)
        net_income_list =np.array([0]*5)

        for expense in expense:
            net_expense_list+=expense.cum_yearly(5)
        for inc in income:
            net_income_list+=inc.cum_yearly(5)
        net = (net_income_list+self.cum_yearly(5)) - net_expense_list
        
        if smooth_interval:
            net = self.smooth(net,smooth_interval)
            
        
        if plot:
            self.plot(range(1,6), net, 'Time (Years)', 'Net Savings (GBP)')
        else:
            return net
    

        



if __name__=='__main__':
    rent = Expense(monthly_cost=2900)
    bills = Expense(monthly_cost=117)
    travel = Expense(monthly_cost=24*4)
    food = Expense(monthly_cost=150)
    car = Expense(monthly_cost=500)
    income=Income(yearly=27000, offset=11000, yearly_increase=2500)
    side_income=Income(yearly=1000, yearly_increase=0)
    income.net([rent, bills, travel, food, car],plot=True,smooth_interval= 0, income=[side_income])
    #print(BaseEntity(yearly=29000))
    
    


        
        