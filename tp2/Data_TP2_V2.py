# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 20:17:53 2020

@author: robert_normand
"""
import pandas as pd

#Moving Average   
def MA(df,ser, n): 
    # df: Dataframe
    # ser: 
    MA_ser = pd.Series(df[ser].rolling(n).mean(), name = 'MA_' + str(n))  
    df = df.join(MA_ser)  
    return df
# Exemple
#Signal=MA(df,"Adj Close",40) # 40 jours
   
#Exponential Moving Average
def EMA(df,ser, M): 
    # df: Dataframe
    # ser: Nom de la série Adj Close ou Close etc.
    # n : Facteur pour la pondération: alpha=(2/(M+1))
    EMA_ser = pd.Series(df[ser].ewm(span=M, adjust=False).mean(), name = 'EMA_' + str(M))  
    df = df.join(EMA_ser)  
    return df
  # Exemple
#Signal=EMA(df,"Adj Close",10) # Moyenne mobile 10 jours

#Momentum  
def MOM(df,ser, n):  
    M = pd.Series(df[ser].pct_change(periods=n), name = 'Momentum_' + str(n))  
    df = df.join(M)  
    return df

#Signal=MOM(df,"Adj Close",250 ) # NB 250 jours est environ 1 an.

#Rate of Change  
def ROC(df,ser, n):  
    M = df[ser].diff(n)  
    N = df[ser].shift(n)  
    ROC = pd.Series(M / N, name = 'ROC_' + str(n))
    df = df.join(ROC)  
    return df
  
#Signal=ROC(df,"Adj Close",1) # Variation quotidienne             
               
#Average True Range  
def ATR(df, n):
    tempo = df
    tempo["Close_P"]=tempo["Close"].shift(1) # Add a lag of closing price
    temp1=pd.Series(tempo["High"]-tempo["Low"]) # High_t - Low_t
    temp2=pd.Series(abs(tempo["High"]-tempo["Close_P"])) # High_t - Close_t-1
    temp3= pd.Series(abs(tempo["Low"]-tempo["Close_P"])) # Low_t - Close_t-1
    frame = { 'temp1': temp1, 'temp2': temp2, 'temp3' : temp3 } 
    temp4 = pd.DataFrame(frame) 
    temp5= pd.Series(temp4.max(axis=1), name= "TR" ) # Max(temp1,temp2,temp3)
    temp6 = pd.Series(temp5.ewm(span=n, adjust=False).mean(),
                      name = "ATR_" + str(n)) # ATR : Moving Average of n days
    df = df.join(temp6)  
    return df

#Tech=ATR(df,10) # MOyenne mobile sur 10 jours

#Bollinger Bands  
def BBANDS(df,ser, win, n):
    MA = df["Close"].rolling(win).mean()
    MSD = df["Close"].rolling(win).std() 
    BOL_H =pd.Series(MA + (MSD * n),name = 'BOL_H_' + str(win) + '_' + str(n))
    BOL_L =pd.Series(MA - (MSD * n),name = 'BOL_L_' + str(win) + '_' + str(n))
    df = df.join(BOL_H)
    df = df.join(BOL_L)
    return df

#Signal = BBANDS(df,"Close",21,2) # Moyenne mobile 21 jours et 2 écart-types

#Pivot Points, Supports and Resistances  
def PPSR(df):  
    PP = pd.Series((df['High'] + df['Low'] + df['Close']) / 3)  
    R1 = pd.Series(2 * PP - df['Low'])  
    S1 = pd.Series(2 * PP - df['High'])  
    R2 = pd.Series(PP + df['High'] - df['Low'])  
    S2 = pd.Series(PP - df['High'] + df['Low'])  
    R3 = pd.Series(df['High'] + 2 * (PP - df['Low']))  
    S3 = pd.Series(df['Low'] - 2 * (df['High'] - PP))  
    psr = {'PP':PP, 'R1':R1, 'S1':S1, 'R2':R2, 'S2':S2, 'R3':R3, 'S3':S3}  
    PSR = pd.DataFrame(psr)  
    df = df.join(PSR)  
    return df

#Signal - PPSR(df) # Supports et Résistances


#Stochastic oscillator %K  
def STOK(df):  
    SOk = pd.Series((df['Close'] - df['Low']) / (df['High'] - df['Low']), name = 'SO%k')  
    df = df.join(SOk)  
    return df

#Signal = STOK(df)


# Stochastic Oscillator, EMA smoothing, nS = slowing (1 if no slowing)  
def STO(df,  nK, nD, nS=1):  
    SOk = pd.Series((df['Close'] - df['Low'].rolling(nK).min()) / (df['High'].rolling(nK).max() - df['Low'].rolling(nK).min()), name = 'SO%k'+str(nK))  
    SOd = pd.Series(SOk.ewm(ignore_na=False, span=nD, min_periods=nD-1, adjust=True).mean(), name = 'SO%d'+str(nD))  
    SOk = SOk.ewm(ignore_na=False, span=nS, min_periods=nS-1, adjust=True).mean()  
    SOd = SOd.ewm(ignore_na=False, span=nS, min_periods=nS-1, adjust=True).mean()  
    df = df.join(SOk)  
    df = df.join(SOd)  
    return df  

#Signal = STO(df, 14, 3, 1) # 14 jours avev un lissage de 3 jours est souvent utilisé

#Trix  
def TRIX(df, ser, n):  
    EX1 = pd.Series(df[ser].ewm(span=n, adjust=False).mean(), name = 'EX1') 
    EX2 = pd.Series(EX1.ewm(span=n, adjust=False).mean(), name = 'EX2') 
    EX3 = pd.Series(EX2.ewm(span=n, adjust=False).mean(), name = 'EX3') 
    temp = {'EX1':EX1, 'EX2':EX2, 'EX3':EX3}
    EX = pd.DataFrame(temp)  
    EX["EX4"]=EX["EX3"].shift(1)
    Trix=pd.Series((EX["EX3"]-EX["EX4"])/EX["EX4"], name = "TRIX_" + str(n))
    df = df.join(Trix)  
    return df
 
#Signal = TRIX(df,"Adj Close",14)        
#Signal["TRIX_14"].plot(grid=True)

#Average Directional Movement Index  
def ADX(df, n, n_ADX): 
    temp = df
    temp1= pd.Series(temp["Close"].shift(1), name="Close_Pr") # Add a lag of Close price
    temp = temp.join(temp1)
    temp2= pd.Series(temp["High"].shift(1), name="High_Pr") # Add a lag of High price
    temp = temp.join(temp2)
    temp3= pd.Series(temp["Low"].shift(1), name="Low_Pr") # Add a lag of Low price
    temp = temp.join(temp3)
    
    # Up Move and Down Move
    UpMove = pd.Series(temp["High"]-temp["High_Pr"], name = "UpMove")
    DoMove = pd.Series(temp["Low_Pr"]-temp["Low"], name = "DoMove")
    ser = {'UpMove':UpMove, 'DoMove':DoMove}
    UpDo = pd.DataFrame(ser)
    def Upfunc(x):
        x1 = x[0]
        x2 = x[1]
        if x1 >= x2 and x1 >0:
            return x1
        else:
            return 0
    Up_sig = UpDo.apply(lambda UpDo: Upfunc(UpDo), axis=1)
    def Dofunc(x):
        x1 = x.UpMove
        x2 = x.DoMove
        if x2 >= x1 and x2 >0:
            return x2
        else:
            return 0
    Do_sig = UpDo.apply(lambda UpDo: Dofunc(UpDo), axis=1)
    
    # True Range
    temp1=pd.Series(temp["High"]-temp["Low"]) # High_t - Low_t
    temp2=pd.Series(abs(temp["High"]-temp["Close_Pr"])) # High_t - Close_t-1
    temp3= pd.Series(abs(temp["Low"]-temp["Close_Pr"])) # Low_t - Close_t-1
    frame = { 'temp1': temp1, 'temp2': temp2, 'temp3' : temp3 } 
    temp4 = pd.DataFrame(frame) 
    temp5= pd.Series(temp4.max(axis=1), name= "TR" ) # Max(temp1,temp2,temp3) 
    ATR = pd.Series(temp5.ewm(span=n, adjust=False).mean(), name = 'ATR')  
    # Calcul de l'ADX
    PosDI = pd.Series(Up_sig.ewm(span = n, adjust=False).mean()/ ATR, name = 'PosDI') 
    NegDI = pd.Series(Do_sig.ewm(span = n, adjust=False).mean()/ ATR, name = 'NegDI')
    temp6 = pd.Series(abs((PosDI - NegDI) / (PosDI + NegDI)))
    ADX = pd.Series(temp6.ewm(span = n, adjust=False).mean(), name = 'ADX_' + str(n) + '_'+str(n_ADX)) 
    df = df.join(ADX)  
    return df

#Signal = ADX(df,14,14)
#Signal["ADX_14_14"].plot(Grid=True)   

#MACD, MACD Signal and MACD difference  
def MACD(df,ser, n_fast, n_slow, n_sign): 
    EMAfast= pd.Series(df[ser].ewm(span=n_fast, adjust=False).mean(), name = 'EMAfast') 
    EMAslow= pd.Series(df[ser].ewm(span=n_slow, adjust=False).mean(), name = 'EMAslow')
    MACD = pd.Series(EMAfast - EMAslow, name = 'MACD_' + str(n_fast) + '_' + str(n_slow))
    MACDsign = pd.Series(MACD.ewm(span = n_sign, adjust=False).mean(), name = 'MACDsign_' + str(n_fast) + '_' + str(n_slow))
    MACDdiff = pd.Series(MACD - MACDsign, name = 'MACDdiff_' + str(n_fast) + '_' + str(n_slow))  
    df = df.join(MACD)  
    df = df.join(MACDsign)  
    df = df.join(MACDdiff) 
    return df

#Signal = MACD(df,"Adj Close",5,25,9)

#Mass Index  
def MassI(df):  
    Range = df['High'] - df['Low']  
    EX1 = pd.Series(Range.ewm(span=9, adjust=False).mean(), name = 'EX1') 
    EX2 = pd.Series(EX1.ewm(span=9, adjust=False).mean(), name = 'EX2')
    Mass = EX1 / EX2
    MassI = pd.Series(Mass.rolling(25).sum(), name = 'MassI') 
    df = df.join(MassI)  
    return df   

#Signal = MassI(df)
#Signal["MassI"].plot(grid=True)


#Vortex Indicator: http://www.vortexindicator.com/VFX_VORTEX.PDF  
def Vortex(df, n): 
        temp = df
        temp1= pd.Series(temp["Close"].shift(1), name="Close_Pr") # Add a lag of Close price
        temp = temp.join(temp1)
        temp2= pd.Series(temp["High"].shift(1), name="High_Pr") # Add a lag of High price
        temp = temp.join(temp2)
        temp3= pd.Series(temp["Low"].shift(1), name="Low_Pr") # Add a lag of Low price
        temp = temp.join(temp3)
        # True Range
        temp1=pd.Series(temp["High"]-temp["Low"]) # High_t - Low_t
        temp2=pd.Series(abs(temp["High"]-temp["Close_Pr"])) # High_t - Close_t-1
        temp3= pd.Series(abs(temp["Low"]-temp["Close_Pr"])) # Low_t - Close_t-1
        frame = { 'temp1': temp1, 'temp2': temp2, 'temp3' : temp3 } 
        temp4 = pd.DataFrame(frame) 
        temp5= pd.Series(temp4.max(axis=1), name= "TR" ) # Max(temp1,temp2,temp3) 
        TR_sum = pd.Series(temp5.rolling(n).sum(), name = 'TR_sum') 
        # Vortex Signal
        VM_plus=pd.Series(abs(temp["High"]-temp["Low_Pr"])) # High_t - Low_t-1
        VM_neg= pd.Series(abs(temp["Low"]-temp["High_Pr"])) # Low_t - High_t-1
        VM_p_sum = pd.Series(VM_plus.rolling(n).sum(), name = 'VM_p_sum') 
        VM_n_sum = pd.Series(VM_neg.rolling(n).sum(), name = 'VM_n_sum') 
        VMI_plus = pd.Series(VM_p_sum / TR_sum, name = 'VI_plus_' + str(n)) 
        VMI_neg = pd.Series(VM_n_sum / TR_sum, name = 'VI_neg_' + str(n)) 
        df = df.join(VMI_plus)  
        df = df.join(VMI_neg)
        return(df)
    
#Signal = Vortex(df,14) # On utilise généralement 14 ou 30 jours
#Signal["VI_plus_14"].plot(grid=True)   
    
#KST Oscillator  
def KST(df, r1, r2, r3, r4, n1, n2, n3, n4):  
    ROC1 = pd.Series(df['Close'].pct_change(periods=r1) , name='ROC1')
    ROC2 = pd.Series(df['Close'].pct_change(periods=r2) , name='ROC2')
    ROC3 = pd.Series(df['Close'].pct_change(periods=r3) , name='ROC3')
    ROC4 = pd.Series(df['Close'].pct_change(periods=r4) , name='ROC4')
    KST = pd.Series(ROC1.rolling(n1).mean() + ROC2.rolling(n2).mean() * 2 + ROC3.rolling(n3).mean() * 3 + ROC4.rolling(n4).mean() * 4, name = 'KST')  
    df = df.join(KST)  
    return df

#Signal = KST(df,10,15,20,30,10,10,15,15) # on utilise les combinaisons usuelles
#Signal["KST"].plot(grid=True)   

#Relative Strength Index  
def RSI(df, n):
    rsi_period = n
    chg = df["Close"].diff(1)
    gain = chg.mask(chg < 0, 0)
    loss = chg.mask(chg > 0, 0)
    avg_gain = gain.ewm(com=rsi_period-1, min_periods=rsi_period).mean()
    avg_loss = loss.ewm(com=rsi_period-1, min_periods=rsi_period).mean()
    rs = abs(avg_gain / avg_loss)
    rsi = pd.Series(100 - (100/(1+rs)), name = "RSI_" + str(n))
    df = df.join(rsi)
    return df

#Signal = RSI(df,14) # on utilise 14 jours
#Signal["RSI_14"].plot(grid=True)

#True Strength Index  
def TSI(df, r, s):  
    M = pd.Series(df['Close'].diff(1))  
    aM = abs(M)  
    EMA1 = pd.Series(M.ewm(com = r, min_periods = r).mean(), name = "EMA1")  
    aEMA1 = pd.Series(aM.ewm(com = r, min_periods = r).mean(), name = "aEM1")  
    EMA2 = pd.Series(EMA1.ewm(com= s, min_periods = s).mean(), name = "EMA2")  
    aEMA2 = pd.Series(aEMA1.ewm(com = s, min_periods = s).mean(), name = "aEMA2")  
    TSI = pd.Series(EMA2 / aEMA2, name = 'TSI_' + str(r) + '_' + str(s))  
    df = df.join(TSI)  
    return df

#Signal = TSI(df, 13, 25) # Selon Investopedia
#Signal["TSI_13_25"].plot(grid=True)

#Accumulation/Distribution  
def ACCDIST(df, n):  
    ad = (2 * df['Close'] - df['High'] - df['Low']) / (df['High'] - df['Low']) * df['Volume']  
    AD = pd.Series(ad.rolling(window=n, min_periods=1).sum(), name = 'AD')  
    df = df.join(AD)  
    return df

#Signal = ACCDIST(df, 250) #C'est ma version de cet indicateur alors que j<ajoute une fenetre
#Signal["AD"].plot(grid=True)

#Chaikin Oscillator  
def Chaikin(df):  
    ad = (2 * df['Close'] - df['High'] - df['Low']) / (df['High'] - df['Low']) * df['Volume']  
    Chaikin = pd.Series(ad.ewm(com = 3, min_periods = 3).mean()- ad.ewm(com = 10, min_periods = 10).mean(), name = 'Chaikin')
    df = df.join(Chaikin)  
    return df

#Signal = Chaikin(df) 
#Signal["Chaikin"].plot(grid=True)

#Money Flow Index and Ratio  
def MFI(df, n): 
    PP = pd.Series((df['High'] + df['Low'] + df['Close']) / 3, name = "PP")
    tempo = df.join(PP)
    tempo["PP_Pr"]=tempo["PP"].shift()
    def MF_plus(x):        
        if x["PP"] > x["PP_Pr"]:
            return x["PP"]*x["Volume"]
        else:
            return 0
    def MF_neg(x):
        if x["PP"] < x["PP_Pr"]:
            return x["PP"]*x["Volume"]
        else:
            return 0
    
    MF_p = pd.Series(tempo.apply(lambda tempo: MF_plus(tempo), axis=1), name = "MF_plus")
    MF_n = pd.Series(tempo.apply(lambda tempo: MF_neg(tempo), axis=1), name = "MF_neg")
    S_MF_plus = pd.Series(MF_p.rolling(n).sum(), name="V1")
    S_MF_neg = pd.Series(MF_n.rolling(n).sum(), name="V2")
    mf = {'V1':S_MF_plus, 'V2':S_MF_neg}  
    mfr = pd.DataFrame(mf)  
    def MF_ratio(x):
        if x["V2"] > 0:
            return x['V1'] / x["V2"]
        else:
            return 99 # Hypothese si le Flot est nul
    mf_ratio = mfr.apply(lambda mfr: MF_ratio(mfr), axis=1)
    MFI = pd.Series(100-(100/(1+mf_ratio)), name = 'MFI_' + str(n))
    df = df.join(MFI)
    return(df)

#Signal = MFI(df,14)
#Signal["MFI_14"].plot(grid=True)    
  
#On-balance Volume  
def OBV(df, n): 
    temp1= pd.Series(df["Close"].shift(1), name="Close_Pr") # Add a lag of Close price
    temp = df.join(temp1)
    def Vol_Sign(x):
        if x["Close"] < x["Close_Pr"]:
            return x["Volume"]
        else:
            return -x["Volume"]
    
    obv = pd.Series(temp.apply(lambda temp: Vol_Sign(temp), axis=1), name = "Vol_Sign")
    OBV_ma = pd.Series(obv.rolling(window=n,min_periods=1).mean(), name = 'OBV_' + str(n))  
    df = df.join(OBV_ma)  
    return df

#Signal = OBV(df,250)
#Signal["OBV_250"].plot(grid=True)  

#Force Index  
def FORCE(df, n, n_per):  
    F = pd.Series(df['Close'].diff(n) * df['Volume'].diff(n), name = 'Force') 
    FI = pd.Series(F.ewm(com = n_per, min_periods = 1).mean(), name = 'FI')
    df = df.join(FI)  
    return df

#Signal = FORCE(df,1,13) # Valeurs usuelles
#Signal["FI"].plot(grid=True)  

#Ease of Movement  
def EOM(df, n): 
    temp1= pd.Series(df["High"].shift(1), name="High_Pr")
    temp2= pd.Series(df["Low"].shift(1), name="Low_Pr")
    temp = df.join(temp1)
    temp = temp.join(temp2)
    EoM = ((temp['High'] + temp['Low'])/2 -(temp['High_Pr'] + temp['Low_Pr'])/2 / temp["Volume"] /scale / ((temp['High'] + temp['Low'])/2)  )  
    Eom_ma = pd.Series(EoM.rolling(window=n, min_periods=1).mean(), name = 'EoM_' + str(n))                                                                                   
    df = df.join(Eom_ma)  
    return df

#Signal = EOM(df,14) # Valeurs usuelles
#Signal["EoM_14"].plot(grid=True)  

#Commodity Channel Index  
def CCI(df, n):  
    PP = (df['High'] + df['Low'] + df['Close']) / 3  
    PP_mav = PP.rolling(window=n, min_periods=10).mean()
    PP_dev = abs(PP - PP_mav)
    PP_dev_MAV = PP_dev.rolling(window=n, min_periods=10).mean()
    CCI = pd.Series((PP-PP_mav)/(0.15*PP_dev_MAV), name = 'CCI_' + str(n))
    df = df.join(CCI)  
    return df

#Signal = CCI(df,20) # Valeurs usuelles
#Signal["CCI_20"].plot(grid=True)


#Signal = CCI(df,14) # Valeurs usuelles
#Signal["CCI_14"].plot(grid=True)  


