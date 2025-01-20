from typing import Optional, Literal
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
    
    def cum_yearly(self, number_of_years:int):
        years = range(0,number_of_years)
        cum_array=[0]*number_of_years
        for i,_ in enumerate(years):
            yearly = self.YEARLY + self.INCREASE*i 
            if i==0:
                yearly+=self.OFFSET
            cum = yearly+cum_array[i-1]
            cum_array[i]=cum
        return np.array(cum_array, np.float64)

    def cum_monthly(self, number_of_months:int):
        months = range(0,number_of_months)
        cum_array=[0]*number_of_months
        for i,_ in enumerate(months):
            monthly = self.MONTHLY + self.INCREASE_MONTHLY*i 
            if i==0:
                monthly+=self.OFFSET
            cum = monthly+cum_array[i-1]
            cum_array[i]=cum
        return np.array(cum_array, np.float64)
    
    def cum_weekly(self, number_of_years:int):
        raise NotImplementedError

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
        return savgol_filter(arr, interval, polyorder=2)
    

    def net(self,expense:list[BaseEntity], plot:bool=True, smooth_interval = 0, income:Optional[list[BaseEntity]]=None, unit:Literal['yearly', 'monthly', 'weekly']='yearly', length:int=5):
        """
        Calculate monthly net income after expense deductions 
        """
        net = np.array([0]*length, np.float64)
        net_expense_list = np.array([0]*length, np.float64)
        net_income_list =np.array([0]*length, np.float64)
        if unit=='yearly':
            self_cum=self.cum_yearly(length)
        elif unit=='monthly':
            self_cum=self.cum_monthly(length)
        elif unit=='weekly':
            self_cum=self.cum_weekly(length)
        else:
            raise TypeError(f"'{unit}' is not a correct argument for unit")

       
        for exp in expense:
            if unit=='yearly':
                net_expense_list+=exp.cum_yearly(length)
            elif unit=='monthly':
                net_expense_list+=exp.cum_monthly(length)
            elif unit=='weekly':
                net_expense_list+=exp.cum_weekly(length)

        if income:
            for inc in income:
                if unit=='yearly':
                    net_income_list+=inc.cum_yearly(length)
                elif unit=='monthly':
                    net_income_list+=inc.cum_monthly(length)
                elif unit=='weekly':
                    net_income_list+=inc.cum_weekly(length)
        net_income_list+=self_cum
            
        net = net_income_list - net_expense_list
        if smooth_interval:
            net = self.smooth(net,smooth_interval)
            
        print(f"net_exp_list:{net_expense_list}, net_income_list: {net_income_list}, self_cum: {self_cum} net: {net}")
        if plot:
            return self.plot(range(1,length+1), net, f'Time ({unit})', 'Net Savings (GBP)')
        else:
            return net
    

        



if __name__=='__main__':
    rent = Expense(monthly_cost=2000)
    bills = Expense(monthly_cost=117)
    travel = Expense(monthly_cost=24*4)
    food = Expense(monthly_cost=150)
    car = Expense(monthly_cost=500)
    income=Income(yearly=27000, offset=11000, yearly_increase=2500)
    oils_income=Income(yearly=1000, yearly_increase=0)
    tutor_income=Income(yearly=1000, yearly_increase=0)
    income.net([rent, bills],plot=True,smooth_interval= 0, income=[oils_income, tutor_income], unit='yearly', length=4)
    
    


        
        