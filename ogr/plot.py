import matplotlib
import matplotlib.pyplot as plt
import io

class FriendEvent():
    def __init__(self, friendevent):
        self.event = friendevent
    
    def getMoneyDateDict(self):
        result = {}
        for i in self.event:
            if (i.date in result):
                result[i.date] += i.money
            else:
                result[i.date] = i.money
        return result
    
    def getDatelist(self):
        dict = self.getMoneyDateDict()
        datelist = list(dict.keys())
        return datelist
        
    def getMoneyList(self):
        dict = self.getMoneyDateDict()
        moneylist = list(dict.values())
        return moneylist
    
    def getTotalMoney(self):
        result = 0
        for i in self.event:
            result += int(i.money)
        return result
    
    def plot(self, datelist, moneylist, friendname):
        plt.rcParams['font.family'] = 'Yu Mincho'
        matplotlib.use('Agg')
        plt.bar(datelist, moneylist)
        plt.xlabel("Date")
        plt.ylabel("Money")
        plt.xticks(rolation=90)
        title = "{} money log".format(friendname)
        plt.title(title)
        img = io.BytesIO()
        plt.savefig(img, format='png', dpi=200)
        png = img.getvalue()
        img.close()
        plt.cla()
        return png

