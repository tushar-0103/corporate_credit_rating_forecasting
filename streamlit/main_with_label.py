import streamlit as st
import pickle
import pandas as pd
import json
from urllib.request import urlopen
#import pymongo


pickle_in = open('/home/talentum/spark/Untitled Folder/corporateCreditRating_project/streamlit/XGB_model.pkl','rb')
classifier = pickle.load(pickle_in)

def get_jsonparsed_data(url):
    response = urlopen(url)
    data = response.read().decode("utf-8")
    return json.loads(data)

def fin_ratios(symbol,S):
    financial_ratios_df = pd.DataFrame()
    financial_ratios_df.head()
    
    
    df_company_ratios = pd.DataFrame.from_dict(
            get_jsonparsed_data("https://financialmodelingprep.com/api/v3/ratios/" 
                                + symbol + 
                                "?apikey=c283e7eb3ddc10dcc0ed8146046dff97"))
    col_df_company_ratios = df_company_ratios.columns.tolist() 
   
    col_x_org = ['Sector', 'Year', 'assetTurnover', 'cashFlowToDebtRatio', 'cashPerShare', 'cashRatio', 'currentRatio',
 	'daysOfSalesOutstanding', 'debtRatio', 'ebitPerRevenue', 'effectiveTaxRate', 'enterpriseValueMultiple', 'freeCashFlowOperatingCashFlowRatio', 'freeCashFlowPerShare', 'grossProfitMargin',
 	'interestCoverage', 'netProfitMargin', 'operatingCashFlowPerShare', 'operatingCashFlowSalesRatio', 'operatingProfitMargin', 'payoutRatio', 'pretaxProfitMargin', 'priceEarningsToGrowthRatio',
 	'quickRatio', 'returnOnAssets', 'returnOnCapitalEmployed']
    
    col_x_test = [ 'date', 'assetTurnover', 'cashFlowToDebtRatio', 'cashPerShare', 'cashRatio', 'currentRatio',
 	'daysOfSalesOutstanding', 'debtRatio', 'ebitPerRevenue', 'effectiveTaxRate', 'enterpriseValueMultiple', 'freeCashFlowOperatingCashFlowRatio', 'freeCashFlowPerShare', 'grossProfitMargin',
 	'interestCoverage', 'netProfitMargin', 'operatingCashFlowPerShare', 'operatingCashFlowSalesRatio', 'operatingProfitMargin', 'payoutRatio', 'pretaxProfitMargin', 'priceEarningsToGrowthRatio',
 	'quickRatio', 'returnOnAssets', 'returnOnCapitalEmployed']
    
    for col in col_df_company_ratios:
        if col not in col_x_test:
            df_company_ratios.drop(col,axis=1,inplace=True)
    df_company_ratios['Year'] = df_company_ratios['date'].astype('datetime64[ns]').dt.year
    df_company_ratios.drop('date',axis=1,inplace=True)
    df_company_ratios['Sector'] = S
    df = df_company_ratios[col_x_org]
    return df
    
def predict_note_authentication(symbol,sector):
    test_df = fin_ratios(symbol,sector)
    pred = classifier.predict(test_df)
    #print(pred)
    return pred


def sec_choose(s):
	lable= [10,7,11,4,1,9,0,3,5,12,8,2,6]
	sec = ['Public Utilities', 'Health Care', 'Technology',
       'Consumer Services', 'Capital Goods', 'Not Known', 'Basic Industries',
       'Consumer Non-Durables', 'Energy', 'Transportation',
       'Miscellaneous', 'Consumer Durables', 'Finance']
	ind = sec.index(s)
	return lable[ind]


def main():

    st.title("Welcome to Corporate Credit Rating Prediction!")
    html_temp ="""    
    <div style="background-color:tomato; padding:10px">
    <h2 style="color:white; text-align: center;">Corporate Credit Rating Prediction ML App </h2>
    </div>
    """  
    
    st.markdown(html_temp, unsafe_allow_html=True)
    
    symbol = st.text_input("Symbol", "Type Here") 
    sector_txt = st.selectbox( 'Choose The Sector',('Public Utilities', 'Health Care', 'Technology',
      									 'Consumer Services', 'Capital Goods', 'Not Known', 'Basic Industries',
    									   'Consumer Non-Durables', 'Energy', 'Transportation',
      										 'Miscellaneous', 'Consumer Durables', 'Finance'))

  
    sector = sec_choose(sector_txt)
    
    
    if st.button("Predict"):
        result=predict_note_authentication(symbol,int(sector))
        lbl=[2,0,3,1]
        rating = ['Low Risk','High Risk','Medium Risk','Highest Risk']
        final = []
        for i in result:
         if i in lbl:
           ind = lbl.index(i)
           final.append(rating[ind])
        df = pd.DataFrame({'Symbol':symbol,'Year':range(2017,2022),'Risk':final})
    
    
        st.success('The output is')
        st.dataframe(df)

    if st.button("About"):
        st.text("Corporate Credit Rating Prediction")
        st.text("Built by Group 9 (DBDA , CDAC)")
        st.text("You Need to provide company Symbol and Sector of there domain , This Page will predict the last 5 year risk for the same")


if __name__=='__main__':
    main()

