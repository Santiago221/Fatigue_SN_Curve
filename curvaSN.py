#import 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os 

class SN:
    def __init__(self,material,Sut,T,Supvalue,Confvalue,ciclomax):
        self.material   = material
        self.Supvalue   = Supvalue
        self.Confvalue	= Confvalue
        self.Sut        = Sut
        self.T          = T
        self.Csup       = SN.Sup(self)
        self.Ctemp      = SN.Temp(self)
        self.Cconf      = SN.Conf(self)
        self.Sm         = 0.9*self.Sut
        print('Sm = {:04.3f} MPa'.format(self.Sm))
        self.Se         = 0.5*self.Sut*self.Csup*self.Ctemp*self.Cconf
        print('Se = {:04.3f} MPa'.format(self.Se))
        self.N1         = 1e3
        self.N2         = 1e6
        if ciclomax < self.N2:
            self.ciclomax   = ciclomax
        else:
            self.ciclomax   = self.N2 
        self.z          = np.log10(self.N1) - np.log10(self.N2)
        self.b          = (1/self.z)*np.log10(self.Sm/self.Se)
        self.a          = 10**((np.log10(self.Sm)) - 3*self.b)
        self.Sn = []
        self.ciclo = []
        SN.CurvaSn(self)
        SN.WriteFile(self)
        SN.Image(self)
        SN.MOVE(self)
        plt.show()

    def Conf(self):
        if self.Confvalue == '50%':
            self.Cconf = 1
        elif self.Confvalue == '90%':
            self.Cconf = 0.897
        elif self.Confvalue == '95%':
            self.Cconf = 0.868
        elif self.Confvalue == '99%':
            self.Cconf = 0.814
        elif self.Confvalue == '99.9%':
            self.Cconf = 0.753
        elif self.Confvalue == '99.99%':
            self.Cconf = 0.702
        elif self.Confvalue == '99.999%':
            self.Cconf = 0.659
        elif self.Confvalue == '99.9999%':
            self.Cconf = 0.620
        else:
            self.Cconf = 1 
        print('Cconf = {:04.3f}'.format(self.Cconf))
        return self.Cconf	

    def Sup(self):
        try:
            if self.Supvalue     == 'Rectified':
                self.Csup   = 1.58*self.Sut**(-0.085)
            elif self.Supvalue   == 'Machined or cold drawn':
                self.Csup   = 4.51*self.Sut**(-0.265)     
            elif self.Supvalue   == 'Hot Rolled':
                self.Csup   = 57.7*self.Sut**(-0.708) 
            elif self.Supvalue   == 'Forged':
                self.Csup   = 272*self.Sut**(-0.995) 
        except:
            self.Csup = 1
            print('Surface Condition not specified')
        print('Csup = {:04.3f}'.format(self.Csup))
        return self.Csup

    def Temp(self):
        try:
            if self.T<=450:
                self.Ctemp = 1
            elif 450<self.T<=550:
                self.Ctemp = 1-0.0058*(self.T-450)
            if self.T>550:
                self.Ctemp = 1-0.0058*(550-450)
                print('Temperature above to 550°C')
        except:
            self.Ctemp = 1
            print('Condition not specified')
        print('Ctemp = {:04.3f}'.format(self.Ctemp))
        return self.Ctemp  

    def CurvaSn(self):
        for c in range(int(self.N1),10000,1000):
            self.ciclo.append(c)
            self.Sn.append((self.a)*c**(self.b))
        if self.ciclomax < 100000:
            for c2 in range(10000,int(self.ciclomax),10000):
                self.ciclo.append(c2)
                self.Sn.append((self.a)*(c2)**(self.b))
            self.ciclo.append(self.ciclomax)
            self.Sn.append((self.a)*(self.ciclomax)**(self.b))
        else: 
            for c2 in range(10000,100000,10000):
                self.ciclo.append(c2)
                self.Sn.append((self.a)*(c2)**(self.b))
            for c3 in range(100000,int(self.ciclomax),100000):
                self.ciclo.append(c3)
                self.Sn.append((self.a)*(c3)**(self.b))
            self.ciclo.append(self.ciclomax)
            self.Sn.append(((self.a)*(self.ciclomax)**(self.b)))
    
    def WriteFile(self):
        sn = np.zeros(len(self.Sn))
        for i in range(len(self.Sn)):
            sn[i] = (int(self.Sn[i]))
            #sn[i] = (np.round(self.Sn[i],3))
        #print(b)
        self.df = pd.DataFrame({'N': self.ciclo,'S':sn})
        self.df.to_csv(self.material+'.csv')
        self.df.to_csv(self.material+'.txt',sep = '\t')

    def Image(self):
        x = self.df[['N']].values.T[0]
        y = self.df[['S']].values.T[0]
        fig, ax = plt.subplots()    
        ax.loglog(x,y,'k--')
        ax.grid()
        ax.set_xlabel('Cycles')
        ax.set_ylabel('Strength [MPa]')
        plt.savefig(self.material + '.tiff')

    def MOVE(self):
        f = self.material
        cwd = os.getcwd()
        print(cwd)
        fwd = os.path.expanduser("~")+ '/desktop'
        print(fwd)
        extension = ['.txt','.csv', '.tiff']
        for i in extension:
            os.replace( cwd + '/' + f + i,fwd +'/'+ f + i)
            
        
material = str(input('Material Name:'))
sut = float(input('Sut [MPa]:'))
T = float(input('Temperature [ºC]:'))
s = str(input('Surface Finish [Rectified, Machined or cold drawn , Hot Rolled, Forged]:'))
c = str(input('Reliability [50,90,95,99,99.9,99.99,99.999,99.9999 - sem o %]:'))
aco = SN(material,sut,T,s,c+'%',1E6)
aco.WriteFile()
input()
