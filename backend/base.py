import matplotlib.pyplot as plt

class Expense:
    YEARLY_COST=None
    MONTHLY_COST=None
    WEEKLY_COST=None
    MONTHS = range(1,12*5)

    def __init__(self,yearly_cost=0,monthly_cost=0,weekly_cost=0):
        self.YEARLY_COST=yearly_cost
        self.MONTHLY_COST=monthly_cost
        self.WEEKLY_COST=weekly_cost
        
        if not self.MONTHLY_COST:
            self.MONTHLY_COST = int(yearly_cost)/12
        
        if not self.WEEKLY_COST:
            self.WEEKLY_COST = int(yearly_cost)/52
        
    def plot(self):
        plt.plot(self.MONTHS, [self.MONTHLY_COST]*12)
        plt.show()
    
class Income:
    MONTHS = range(1,12*5)
    def __init__(self,yearly=0,monthly=0,weekly=0, offset=0):
        self.YEARLY=yearly
        self.MONTHLY=monthly
        self.WEEKLY=weekly
        self.OFFSET=offset
        
        if not self.MONTHLY:
            self.MONTHLY = int(yearly)/12
        
        if not self.WEEKLY:
            self.WEEKLY = int(yearly)/52
        
    def plot(self):
        plt.plot(self.MONTHS, [self.MONTHLY]*12)
        plt.show()
    
    def net(self,expense:Expense|list[Expense], plot:bool=True):
        # TODO: use numpy
        net = []
        if type(expense) is list:
            net_expense_list = []
            for _ in self.MONTHS:
                net_exp=0
                for exp in expense:
                    net_exp+=exp.MONTHLY_COST
                    print(net_exp)
                new=(self.OFFSET+self.MONTHLY)-net_exp
                print(self.MONTHLY)
                net_expense_list.append(new)
                self.OFFSET=new
            print(net_expense_list)
            print(self.MONTHS)
            
            if plot:
                plt.plot(self.MONTHS, net_expense_list)
                plt.show()
            else:
                return net
        else:
            for x,y in zip([expense.MONTHLY_COST]*12, [self.MONTHLY]*12):
                net.append(y-x)
            if plot:
                plt.plot(self.MONTHS, net)
                plt.show()
            else:
                return net
        





rent = Expense(monthly_cost=875)
bills = Expense(monthly_cost=117)
travel = Expense(monthly_cost=24*4)
food = Expense(monthly_cost=60)
income=Income(yearly=44603, offset=0)
income.net([rent, bills, travel, food])


        
        