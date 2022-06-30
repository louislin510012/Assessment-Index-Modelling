import datetime as dt
import pandas as pd


# reading the CSV file
#df = pd.read_csv('Assessment-Index-Modelling-master\data_sources\stock_prices.csv', index_col='Date',parse_dates=True)
df = pd.read_csv('data_sources\stock_prices.csv')
# displaying the first row of the CSV file
print(df.head(1))

# calculate the daily percentage change
df_01012020 = df.iloc[2:]
df_01012020 = df_01012020.set_index('Date')
data_returns = df_01012020.pct_change(1)
# calculate the cumulative daily growth
data_cum_returns = (1 + data_returns).cumprod() - 1


date_column = df.iloc[:,0]
print(date_column)

# start_date = dt.date(year=2020, month=1, day=1)
# end_date= dt.date(year=2020, month=12, day=31)

start_date = '01/01/2020'
end_date = '31/12/2020'
#find first business day on the month
FBD = pd.date_range(start_date,end_date,freq='BMS')
#last business day of the month
LBD = pd.date_range('31/12/2019', end_date,freq='BM')


#FBD = pd.DatetimeIndex.to_series(FBD)
FBD = FBD.strftime('%d/%m/%Y')
LBD = LBD.strftime('%d/%m/%Y')
FBD = FBD.to_series()
LBD = LBD.to_series()
#FBD = list(FBD.values)

# date_column = df.index
# date_column = date_column.strftime('%Y/%m/%d')
# date_column = df.index.to_series()



#stock prices on the first business day in data set
FBD_dataframe = pd.DataFrame()
for i in FBD:
    FBD_dataframe = FBD_dataframe.append(df[df['Date'] == i])
    print(FBD_dataframe)

# stock prices on the first business day in data set
LBD_dataframe = pd.DataFrame()
for i in LBD:
    LBD_dataframe = LBD_dataframe.append(df[df['Date'] == i])
    print(LBD_dataframe)

# LBD_top_three_DF = pd.DataFrame()
# for i in range(0,13):
#    LBD_sort = LBD_dataframe.iloc[i,1:].sort_values(axis=0,ascending=False)
#    LBD_top_three = LBD_sort.iloc[0:3]
#    LBD_top_three_index = LBD_top_three.index
#    LBD_top_three_index = LBD_top_three_index.to_list()
#    LBD_top_three_DF = LBD_top_three_DF.append(LBD_top_three_index)




#Select Top three stock in portfolio
    FBD_index = FBD_dataframe.index
    index_level_daily_final = pd.DataFrame()
    x = 0

    for i in range(0,12):
        LBD_sort = LBD_dataframe.iloc[i, 1:].sort_values(axis=0, ascending=False)
        LBD_top_three = LBD_sort.iloc[0:3]  #B,C,H
        # LBD_top_three = LBD_top_three.reset_index()
        # LBD_top_three = pd.Series.to_frame(LBD_top_three)
        LBD_top_three_index = LBD_top_three.index
        LBD_top_three_index = LBD_top_three_index.to_series()
        # data_cum_returns_top_three = data_cum_returns[LBD_top_three_index]
        # weight = [0.5,0.25,0.25]
        # data_cum_returns_W_adj = data_cum_returns_top_three * weight
        # index_return_daily = data_cum_returns_W_adj.sum(axis=1)
        # index_level_daily = 100* (1+index_return_daily)
        # index_level_daily = pd.Series.to_frame(index_level_daily)
        k = FBD_index[i]
        df_top_three = df.iloc[k:]
        df_top_three = df_top_three.set_index('Date')
        data_returns = df_top_three.pct_change(1)
        # calculate the cumulative daily growth
        data_cum_returns = (1 + data_returns).cumprod() - 1
        data_cum_returns_top_three = data_cum_returns[LBD_top_three_index]
        weight = [0.5, 0.25, 0.25]
        data_cum_returns_W_adj = data_cum_returns_top_three * weight
        index_return_daily = data_cum_returns_W_adj.sum(axis=1)

        if i==0:
            index_level_daily = 100 * (1 + index_return_daily)
            index_level_daily = pd.Series.to_frame(index_level_daily)
            index_level_daily_final = index_level_daily_final.append(index_level_daily)
        else:

            index_level_daily.iloc[k-2:][0]= (index_level_daily.iloc[k-2][0])* (1 + index_return_daily)


index_level_daily.columns = ['Index_level']
index_level_daily = round(index_level_daily,2)











