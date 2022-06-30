import datetime as dt


class IndexModel:
    def __init__(self):
        pass

    def calc_index_level(self,start_date, end_date):
        import pandas as pd
        global index_level_daily
        # reading the CSV file
        df = pd.read_csv('data_sources\stock_prices.csv')
        # displaying the first row of the CSV file
        print(df.head(1))

        # calculate the daily percentage change
        df_01012020 = df.iloc[2:]
        df_01012020 = df_01012020.set_index('Date')
        data_returns = df_01012020.pct_change(1)
        # calculate the cumulative daily return
        data_cum_returns = (1 + data_returns).cumprod() - 1

        date_column = df.iloc[:,0]
        print(date_column)


        #first business day on the month during the given time period
        FBD = pd.date_range(start_date,end_date,freq='BMS')
        #last business day of the month during the given time period
        LBD = pd.date_range('31/12/2019',end_date,freq='BM')


        #define date format
        FBD = FBD.strftime('%d/%m/%Y')
        LBD = LBD.strftime('%d/%m/%Y')
        FBD = FBD.to_series()
        LBD = LBD.to_series()



        #stock prices on the first business days in data set
        FBD_dataframe = pd.DataFrame()
        for i in FBD:
            FBD_dataframe = FBD_dataframe.append(df[df['Date'] == i])
            print(FBD_dataframe)

        #stock prices on the last business days in data set
        LBD_dataframe = pd.DataFrame()
        for i in LBD:
            LBD_dataframe = LBD_dataframe.append(df[df['Date'] == i])
            print(LBD_dataframe)



        FBD_index = FBD_dataframe.index
        index_level_daily_final = pd.DataFrame()

        # Select Top three stock in portfolio and rebalance monthly
        for i in range(0,12):
            LBD_sort = LBD_dataframe.iloc[i, 1:].sort_values(axis=0, ascending=False)
            LBD_top_three = LBD_sort.iloc[0:3]  #Select Top three stock

            LBD_top_three_index = LBD_top_three.index
            LBD_top_three_index = LBD_top_three_index.to_series()

            #calculate monthly return
            k = FBD_index[i]
            df_top_three = df.iloc[k:]
            df_top_three = df_top_three.set_index('Date')
            data_returns = df_top_three.pct_change(1)
            data_cum_returns = (1 + data_returns).cumprod() - 1
            data_cum_returns_top_three = data_cum_returns[LBD_top_three_index]
            weight = [0.5, 0.25, 0.25] #assign weight to the top three stocks
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
        print(index_level_daily)







    def export_values(self, file_name: str):

        index_level_daily.to_csv('file_name.csv')










