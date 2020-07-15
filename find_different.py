import pandas as pd


def find_difference_to_between_two_dataframe(df1, df2):
    df_diffrent = df2[~(df2['link'].isin(df1['link']) &
                        df2['title'].isin(df1['title']) &
                        df2['description'].isin(df1['description']) &
                        df2['location'].isin(df1['location']))].reset_index(drop=True)

    df_diffrent.to_csv('different.csv', encoding="utf-8")
