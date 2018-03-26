from BayesianSmoothing import BayesianSmoothing
def ctr_PH(df_train,df,column,iter_num, epsilon):    
    
    #-------------------------------------
    print('开始统计平滑')
    bs = BayesianSmoothing(1, 1)    
    dic_i = df_train[column].value_counts().to_dict() 
    dic_cov = df_train.loc[df_train['is_trade']==1,column].value_counts().to_dict()
    l = df_train[column].unique()
    I=[]
    C=[]
    for value in l:
        I.append(dic_i[value])
    for value in l:
        if value not in dic_cov:
            C.append(0)
        else:
            C.append(dic_cov[value])        
    print('开始平滑操作')           
    bs.update(I, C, iter_num, epsilon)
    print(bs.alpha, bs.beta)  
    print('构建平滑转化率')
    
    
    dic_PH={}
    for value in df[column].values:
        if value not in dic_i:
            dic_PH[value]=(bs.alpha)/(bs.alpha+bs.beta)
        elif value not in dic_cov:
            dic_PH[value]=(bs.alpha)/(dic_i[value]+bs.alpha+bs.beta)
        else:
            dic_PH[value]=(dic_cov[value]+bs.alpha)/(dic_i[value]+bs.alpha+bs.beta)   
    return dic_PH