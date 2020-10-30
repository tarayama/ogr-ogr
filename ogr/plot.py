import matplotlib
import matplotlib.pyplot as plt
import io

class FriendEvent():
    def __init__(self, friendevent):
        self.event = friendevent
    
    def getDatelist(self):
        datelist = []
        for i in self.event:
            datelist.append(str(i.date))
        return datelist
        
    def getMoneyList(self):
        moneylist = []
        result = 0
        for i in self.event:
            result += int(i.money)
            m = result + int(i.money)
            moneylist.append(i.money)
        return moneylist
    
    def getTotalMoney(self):
        result = 0
        for i in self.event:
            result += int(i.money)
        return result
    
    def plot(self, datelist, moneylist, friendname):
        plt.rcParams['font.family'] = 'Yu Mincho'
        matplotlib.use('Agg')
        plt.plot(datelist, moneylist)
        plt.xlabel("日付")
        plt.ylabel("金額")
        title = "{}さんとの記録".format(friendname)
        plt.title(title)
        img = io.BytesIO()
        plt.savefig(img, format='png', dpi=200)
        png = img.getvalue()
        img.close()
        plt.cla()
        return png

