import streamlit as st 
from streamlit_option_menu import option_menu
import pandas as pd 
import psycopg2
import plotly.express as px
import plotly.io as pio
import requests
import json

# data framr creation   
mydb = psycopg2.connect(host="localhost",
                        user="postgres",
                        password="0040",
                        database="phonepe_data",
                        port="5432")
cursor = mydb.cursor()

#aggregated insurance table
cursor.execute("select * from aggregated_insurance")
mydb.commit()
Table1 = cursor.fetchall()

Aggregated_insurance = pd.DataFrame(Table1,columns=("States","Years","Quarter","Transaction_type","Transaction_count","Transaction_amount"))

#aggregated Transaction table
cursor.execute("select * from aggregated_transaction")
mydb.commit()
Table2 = cursor.fetchall()

Aggregated_Transaction = pd.DataFrame(Table2,columns=("States","Years","Quarter","Transaction_type","Transaction_count","Transaction_amount"))

#aggregated USER table
cursor.execute("select * from aggregated_user")
mydb.commit()
Table3 = cursor.fetchall()

Aggregated_USER = pd.DataFrame(Table3,columns=("States","Years","Quarter","Brands","Transaction_count","Percentage"))


#map_transaction table
cursor.execute("select * from map_transaction")
mydb.commit()
Table4 = cursor.fetchall()

Map_Transaction = pd.DataFrame(Table4,columns=("States","Years","Quarter","District","Transaction_count","Transaction_amount"))

#Map_insruence table
cursor.execute("select * from map_insruence")
mydb.commit()
Table5 = cursor.fetchall()

Map_insruence = pd.DataFrame(Table5,columns=("States","Years","Quarter","District","Transaction_count","Transaction_amount"))


#Map_USER table
cursor.execute("select * from map_user")
mydb.commit()
Table6 = cursor.fetchall()

Map_user = pd.DataFrame(Table6,columns=("States","Years","Quarter","District","RegisteredUsers","AppOpens"))


#Top_transaction table
cursor.execute("select * from top_transaction")
mydb.commit()
Table7 = cursor.fetchall()

Top_transaction = pd.DataFrame(Table7,columns=("States","Years","Quarter","Pincodes","Transaction_count","Transaction_amount"))

#TOP_insruence table
cursor.execute("select * from top_insrurence") 
mydb.commit()
Table8 = cursor.fetchall()

TOP_insruence = pd.DataFrame(Table8,columns=("States","Years","Quarter","Pincodes","Transaction_count","Transaction_amount"))


#TOP_USER table
cursor.execute("select * from top_user")
mydb.commit()
Table9 = cursor.fetchall()

TOP_USER = pd.DataFrame(Table9,columns=("States","Years","Quarter","Pincodes","RegisteredUsers"))


def Transaction_Amout_Count_Year(df, year):
    Tran_Am_Cot_Ye = df[df["Years"]==year]
    Tran_Am_Cot_Ye.reset_index(drop=True, inplace=True)

    Tran_Am_Cot_Ye_Group = Tran_Am_Cot_Ye.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    Tran_Am_Cot_Ye_Group.reset_index(inplace=True)

    col1,col2  = st.columns(2)
    with col1:
        
        ammout = px.bar(Tran_Am_Cot_Ye_Group, x="States",y="Transaction_amount",title=f"{year} - Transaction Amount",
                        color_discrete_sequence=px.colors.sequential.Blackbody,height=650,width=600)
        st.plotly_chart(ammout)
    with col2:

        Cout = px.bar(Tran_Am_Cot_Ye_Group, x="States",y="Transaction_count",title=f"{year} - Transaction Count",
                        color_discrete_sequence=px.colors.sequential.Bluyl_r,height=650,width=600)
        st.plotly_chart(Cout)

    col1,col2 = st.columns(2)

    with col1:

        url  = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"

        response = requests.get(url)
        data1 = json.loads(response.content)

        stat_name = []

        for feature in data1["features"]:
            stat_name.append(feature["properties"]["ST_NM"])

        stat_name.sort()

        indiaMar = px.choropleth(Tran_Am_Cot_Ye_Group,  geojson=data1, locations= "States", featureidkey="properties.ST_NM",
                                color="Transaction_amount",color_continuous_scale="Rainbow",
                                range_color=(Tran_Am_Cot_Ye_Group["Transaction_amount"].min(),Tran_Am_Cot_Ye_Group["Transaction_amount"].max()),
                                hover_name="States",title=f"{year} - Transaction Amount", fitbounds="locations",
                                height=600,width=600)
        indiaMar.update_geos(visible=False)
        st.plotly_chart(indiaMar)

    with col2:

        indiaMar2 = px.choropleth(Tran_Am_Cot_Ye_Group,  geojson=data1, locations= "States", featureidkey="properties.ST_NM",
                                color="Transaction_count",color_continuous_scale="Rainbow",
                                range_color=(Tran_Am_Cot_Ye_Group["Transaction_count"].min(),Tran_Am_Cot_Ye_Group["Transaction_count"].max()),
                                hover_name="States",title=f"{year} - Transaction Count", fitbounds="locations",
                                height=600,width=600)
        indiaMar2.update_geos(visible=False)
        st.plotly_chart(indiaMar2)

    return Tran_Am_Cot_Ye
    
    

def Transaction_Amout_Count_Year_Quarter(df, Quarter): 
    Tran_Am_Cot_Ye = df[df["Quarter"]==Quarter]
    Tran_Am_Cot_Ye.reset_index(drop=True, inplace=True)

    Tran_Am_Cot_Ye_Group = Tran_Am_Cot_Ye.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    Tran_Am_Cot_Ye_Group.reset_index(inplace=True)

    col1,col2  = st.columns(2)  

    with col1:
        ammout = px.bar(Tran_Am_Cot_Ye_Group, x="States",y="Transaction_amount",title=f"{Tran_Am_Cot_Ye['Years'].unique()} Year {Quarter} Quarter- Transaction Amount",
                        color_discrete_sequence=px.colors.sequential.Blackbody,height=650,width=600)
        st.plotly_chart(ammout)
    with col2:
        Cout = px.bar(Tran_Am_Cot_Ye_Group, x="States",y="Transaction_count",title=f"{Tran_Am_Cot_Ye['Years'].unique()} Year {Quarter} Quarter - Transaction Count",
                        color_discrete_sequence=px.colors.sequential.Bluyl_r,height=650,width=600)
        st.plotly_chart(Cout)

    col1,col2 = st.columns(2)

    with col1:
        url  = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"

        response = requests.get(url)
        data1 = json.loads(response.content)

        stat_name = []

        for feature in data1["features"]:
            stat_name.append(feature["properties"]["ST_NM"])

        stat_name.sort()

        indiaMar = px.choropleth(Tran_Am_Cot_Ye_Group,  geojson=data1, locations= "States", featureidkey="properties.ST_NM",
                                color="Transaction_amount",color_continuous_scale="Rainbow",
                                range_color=(Tran_Am_Cot_Ye_Group["Transaction_amount"].min(),Tran_Am_Cot_Ye_Group["Transaction_amount"].max()),
                                hover_name="States",title=f"{Tran_Am_Cot_Ye['Years'].unique()} Year {Quarter} Quarter- Transaction Amount", fitbounds="locations",
                                height=600,width=600)
        indiaMar.update_geos(visible=False)    
        st.plotly_chart(indiaMar)

    with col2:
        indiaMar2 = px.choropleth(Tran_Am_Cot_Ye_Group,  geojson=data1, locations= "States", featureidkey="properties.ST_NM",
                                color="Transaction_count",color_continuous_scale="Rainbow",
                                range_color=(Tran_Am_Cot_Ye_Group["Transaction_count"].min(),Tran_Am_Cot_Ye_Group["Transaction_count"].max()),
                                hover_name="States",title=f"{Tran_Am_Cot_Ye['Years'].unique()} Year {Quarter} Quarter- Transaction Count", fitbounds="locations",
                                height=600,width=600)
        indiaMar2.update_geos(visible=False)   
        st.plotly_chart(indiaMar2)

    return Tran_Am_Cot_Ye

    
def aggre_transa_type(df,state):
    Tran_Am_Cot_Ye = df[df["States"]==state]
    Tran_Am_Cot_Ye.reset_index(drop=True, inplace=True)

    Tran_Am_Cot_Ye_Group = Tran_Am_Cot_Ye.groupby("Transaction_type")[["Transaction_count","Transaction_amount"]].sum()
    Tran_Am_Cot_Ye_Group.reset_index(inplace=True)

    col1,col2  = st.columns(2)

    with col1:
            
        pie_1 = px.pie(data_frame= Tran_Am_Cot_Ye_Group, names="Transaction_type", values="Transaction_amount", width=600,title=f"{state.upper()} Transaction Amount", hole=0.3)
        st.plotly_chart(pie_1)  

    with col2:        
        pie_2 = px.pie(data_frame= Tran_Am_Cot_Ye_Group, names="Transaction_type", values="Transaction_count", width=600,title=f"{state.upper()} Transaction Count", hole=0.3)
        st.plotly_chart(pie_2)

#Aggregated USER Analysis _1 
def Agger_User_plot_1(df, year): 
    agger_user_year = df[df["Years"]==year]
    agger_user_year.reset_index(drop=True, inplace=True)

    agger_user_year_Group = pd.DataFrame(agger_user_year.groupby("Brands")[["Transaction_count","Percentage"]].sum())
    agger_user_year_Group.reset_index(inplace=True)

    user_bar_1 =  px.bar(agger_user_year_Group, x= "Brands", y= "Transaction_count", title=f"{year} Brands and Transaction Count",
                        width=600,color_discrete_sequence=px.colors.sequential.haline,hover_name="Brands")
    #user_bar_1.show()
    st.plotly_chart(user_bar_1) 
    return agger_user_year


#Aggregated USER Analysis _2 
def Agger_User_plot_2(df,Quarter):
    agger_user_Quarter  = df[df["Quarter"]==Quarter]
    agger_user_Quarter.reset_index(drop=True, inplace=True)

    agger_user_Quarter_group = pd.DataFrame(agger_user_Quarter.groupby("Brands")["Transaction_count"].sum())
    agger_user_Quarter_group.reset_index(inplace=True)

    user_bar_2 =  px.bar(agger_user_Quarter_group, x= "Brands", y= "Transaction_count", title=f"{Quarter} (Quarter) Brands and Transaction Count",
                        width=600,color_discrete_sequence=px.colors.sequential.algae_r,hover_name="Brands")
    st.plotly_chart(user_bar_2)
    return agger_user_Quarter

#Agger_User_plot_3 
def Agger_User_plot_3(df,state): 
    Agger_User_yer_quo_stat = df[df["States"]==state]
    Agger_User_yer_quo_stat.reset_index(drop=True,inplace=True)

    line_1  = px.line(Agger_User_yer_quo_stat, x = "Brands", y= "Transaction_count", hover_data="Percentage",title=f"{state} Brands and Transaction Count and Percentage",
                    width=700,markers=True)
    st.plotly_chart(line_1)


    #Map insurcence District
def Map_insru_Distric_type(df,state):
    Tran_Am_Cot_Ye = df[df["States"]==state]
    Tran_Am_Cot_Ye.reset_index(drop=True, inplace=True)

    Tran_Am_Cot_Ye_Group = Tran_Am_Cot_Ye.groupby("District")[["Transaction_count","Transaction_amount"]].sum()
    Tran_Am_Cot_Ye_Group.reset_index(inplace=True)
    col1,col2 = st.columns(2)

    with col1:
        pie_bar_1 = px.bar(Tran_Am_Cot_Ye_Group, x="Transaction_amount",y="District",orientation="h",height=600,
                        title=f"{state} District and Transaction Amount",color_discrete_sequence=px.colors.sequential.Peach_r)   
        st.plotly_chart(pie_bar_1)
    with col2:

        pie_bar_2 = px.bar(Tran_Am_Cot_Ye_Group, x="Transaction_count",y="District",orientation="h",height=600,
                        title=f"{state} District and Transaction Count",color_discrete_sequence=px.colors.sequential.Plasma_r)
        st.plotly_chart(pie_bar_2)


#map user plot _1
def map_user_plot_1(df,year):
    map_user_year = df[df["Years"]==year]
    map_user_year.reset_index(drop=True, inplace=True)

    Map_user_year_Group = map_user_year.groupby("States")[["RegisteredUsers","AppOpens"]].sum()
    Map_user_year_Group.reset_index(inplace=True)
    
    line_1_Map  = px.line(Map_user_year_Group, x = "States", y= ["RegisteredUsers","AppOpens"], title=f"{year} Registered Users and AppOpens",
                    width=900,height=900,markers=True,color_discrete_sequence=px.colors.sequential.Rainbow)    
    st.plotly_chart(line_1_Map)
    return map_user_year


#map user plot _2
def map_user_plot_2 (df,Quarter):
    map_user_year_Quarter = df[df["Quarter"]==Quarter]
    map_user_year_Quarter.reset_index(drop=True, inplace=True)

    Map_user_year_Group_Quarter = map_user_year_Quarter.groupby("States")[["RegisteredUsers","AppOpens"]].sum()
    Map_user_year_Group_Quarter.reset_index(inplace=True)
    

    line_1_Map  = px.line(Map_user_year_Group_Quarter, x = "States", y= ["RegisteredUsers","AppOpens"], title=f"{df['Years'].max()} Year {Quarter} (Quarter) Registered Users and AppOpens",
                    width=1000,height=900,markers=True,color_discrete_sequence=px.colors.sequential.Rainbow )
    st.plotly_chart(line_1_Map)

    return map_user_year_Quarter


#map_user_plot_2
def map_user_plot_3(df,States):
    map_user_Year_Quarter  = df[df["States"]==States]
    map_user_Year_Quarter.reset_index(drop=True, inplace=True)

    col1,col2  = st.columns(2)
    with col1:
        map_user_bar1 = px.bar(map_user_Year_Quarter, x = "RegisteredUsers", y = "District",orientation="h",
                            title= f"{States} Registered Users",height=800,color_discrete_sequence=px.colors.sequential.Aggrnyl)
        st.plotly_chart(map_user_bar1)
    with col2:
            
        map_user_bar2 = px.bar(map_user_Year_Quarter, x = "AppOpens", y = "District",orientation="h",
                            title= f"{States} AppOpens",height=800,color_discrete_sequence=px.colors.sequential.RdBu_r)
        st.plotly_chart(map_user_bar2)


#top_insruence_plot_1
def top_insruence_plot_1(df,state):
    top_user_insruenc_year_Quarter = df[df["States"]==state]
    top_user_insruenc_year_Quarter.reset_index(drop=True, inplace=True)
    
    col1,col2  = st.columns(2)

    with col1:
        top_user_bar1 = px.bar(top_user_insruenc_year_Quarter, x = "Quarter", y = "Transaction_amount", hover_data= "Pincodes",
                            title= "Transaction Amount",width=500, height=600,color_discrete_sequence=px.colors.sequential.Redor_r)
        st.plotly_chart(top_user_bar1)

    with col2:
        top_user_bar2 = px.bar(top_user_insruenc_year_Quarter, x = "Quarter", y = "Transaction_count", hover_data= "Pincodes",
                        title= "Transaction Count",width=500 ,height=600,color_discrete_sequence=px.colors.sequential.YlGnBu_r)    
        st.plotly_chart(top_user_bar2)



def top_user_plot_1(df, year):
    top_user_year = df[df["Years"]==year]
    top_user_year.reset_index(drop=True, inplace=True)

    top_user_year_Group = pd.DataFrame(top_user_year.groupby(["States","Quarter"])[["RegisteredUsers"]].sum())
    top_user_year_Group.reset_index(inplace=True)


    top_plot1 = px.bar(top_user_year_Group, x="States", y="RegisteredUsers", color="Quarter", width=1000, height=800, 
                    color_discrete_sequence=px.colors.sequential.Bluered_r,hover_name="States",title=f"{year} Registered Users")
    #top_plot1.show()
    st.plotly_chart(top_plot1)
    return top_user_year
  

#top_user_plot_2
def top_user_plot_2(df,state):
    top_user_state_year = df[df["States"]==state]
    top_user_state_year.reset_index(drop=True, inplace=True)

    top_plot_2  = px.bar(top_user_state_year, x= "Quarter", y  = "RegisteredUsers", title=f"{state} Registered Users and Pincodes with Quarter",
                        width=1000,height=700,color="RegisteredUsers", hover_data="Pincodes",
                        color_continuous_scale= px.colors.sequential.RdBu)
    st.plotly_chart(top_plot_2)


def top_chart_transactionAmount(table_name):
    mydb = psycopg2.connect(host="localhost",
                            user="postgres",
                            password="0040",
                            database="phonepe_data",
                            port="5432")
    cursor = mydb.cursor()

    #plot 1
    query1 = f'''SELECT states, SUM(transaction_amount) AS transaction_amount
                FROM {table_name}
                GROUP BY states 
                ORDER BY transaction_amount DESC
                LIMIT 10;'''

    cursor.execute(query1)
    table = cursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table,columns= ("states","transaction_amount"))

    col1, col2 = st.columns(2)

    with col1:
        ammout = px.bar(df_1, x="states",y="transaction_amount",title="Top 10 Of Transaction Amount", hover_name="states",
                        color_discrete_sequence=px.colors.sequential.YlGnBu_r,height=650,width=600)
        #ammout.show()
        st.plotly_chart(ammout)
    # plot2 
    query2 = f'''SELECT states, SUM(transaction_amount) AS transaction_amount
                FROM {table_name}
                GROUP BY states 
                ORDER BY transaction_amount 
                LIMIT 10;'''

    cursor.execute(query2)
    table2 = cursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table2,columns= ("states","transaction_amount"))

    with col2:
        ammout2 = px.bar(df_2, x="states",y="transaction_amount",title="Last 10 of Transaction Amount", hover_name="states",
                        color_discrete_sequence=px.colors.sequential.Rainbow,height=650,width=600)
        #ammout2.show()
        st.plotly_chart(ammout2)
    #plot 3 
    query3 = f'''SELECT states, AVG(transaction_amount) AS transaction_amount
                FROM {table_name}
                GROUP BY states 
                ORDER BY transaction_amount ;'''

    cursor.execute(query3)
    table3 = cursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table3,columns= ("states","transaction_amount"))


    ammout3 = px.bar(df_3, y="states",x="transaction_amount",title="Average of Transaction Amount", hover_name="states",orientation="h",
                    color_discrete_sequence=px.colors.sequential.Darkmint_r,height=800,width=1000)
    #ammout3.show()
    st.plotly_chart(ammout3)



def top_chart_transactionCount(table_name):
    mydb = psycopg2.connect(host="localhost",
                            user="postgres",
                            password="0040",
                            database="phonepe_data",
                            port="5432")
    cursor = mydb.cursor()

    #plot 1
    query1 = f'''SELECT states, SUM(Transaction_count) AS Transaction_count
                FROM {table_name}
                GROUP BY states 
                ORDER BY Transaction_count DESC
                LIMIT 10;'''

    cursor.execute(query1)
    table = cursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table,columns= ("states","Transaction_count"))
    col1, col2 = st.columns(2)
    with col1:
        ammout = px.bar(df_1, x="states",y="Transaction_count",title="Top 10 of Transaction count", hover_name="states",
                        color_discrete_sequence=px.colors.sequential.YlGnBu_r,height=650,width=600)
        #ammout.show()
        st.plotly_chart(ammout)

    # plot2 
    query2 = f'''SELECT states, SUM(Transaction_count) AS Transaction_count
                FROM {table_name}
                GROUP BY states 
                ORDER BY Transaction_count 
                LIMIT 10;'''

    cursor.execute(query2)
    table2 = cursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table2,columns= ("states","Transaction_count"))
    with col2:

        ammout2 = px.bar(df_2, x="states",y="Transaction_count",title="last 10 of Transaction Count", hover_name="states",
                        color_discrete_sequence=px.colors.sequential.Rainbow,height=650,width=600)
        #ammout2.show()
        st.plotly_chart(ammout2)
    #plot 3 
    query3 = f'''SELECT states, AVG(Transaction_count) AS Transaction_count
                FROM {table_name}
                GROUP BY states 
                ORDER BY Transaction_count ;'''

    cursor.execute(query3)
    table3 = cursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table3,columns= ("states","Transaction_count"))


    ammout3 = px.bar(df_3, y="states",x="Transaction_count",title="Avaerage of Transaction count", hover_name="states",orientation="h",
                    color_discrete_sequence=px.colors.sequential.Darkmint_r,height=800,width=1000)
    #ammout3.show()
    st.plotly_chart(ammout3)


def top_chart_register_user(table_name, state):
    mydb = psycopg2.connect(host="localhost",
                            user="postgres",
                            password="0040",
                            database="phonepe_data",
                            port="5432")
    cursor = mydb.cursor()

    #plot 1
    query1 = f'''SELECT districts,sum(registeredUsers) as registeredUsers
                    from {table_name}
                    where states = '{state}'
                    group by districts
                    order by registeredUsers DESC
                    limit 10;'''

    cursor.execute(query1)
    table = cursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table,columns= ("districts","registeredUsers"))

    col1, col2 = st.columns(2)

    with col1:
        ammout = px.bar(df_1, x="districts",y="registeredUsers",title="Top 10 of Registered Users", hover_name="districts",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=600)     
        st.plotly_chart(ammout)

    # plot2 
    query2 = f'''SELECT districts,sum(registeredUsers) as registeredUsers
                    from {table_name}
                    where states = '{state}'
                    group by districts
                    order by registeredUsers 
                    limit 10;'''

    cursor.execute(query2)
    table2 = cursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table2,columns= ("districts","registeredUsers"))

    with col2:
        ammout2 = px.bar(df_2, x="districts",y="registeredUsers",title="Last 10 of Registered Users", hover_name="districts",
                        color_discrete_sequence=px.colors.sequential.Rainbow,height=650,width=600)
        st.plotly_chart(ammout2)
   
    query3 = f'''SELECT districts,AVG(registeredUsers) as registeredUsers
                from {table_name}
                where states = '{state}'
                group by districts
                order by registeredUsers;'''

    cursor.execute(query3)
    table3 = cursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table3,columns= ("districts","registeredUsers"))


    ammout3 = px.bar(df_3, y="districts",x="registeredUsers",title="Average of Registered Users", hover_name="districts",orientation="h",
                    color_discrete_sequence=px.colors.sequential.Darkmint_r,height=800,width=1000)
    st.plotly_chart(ammout3)
   

def top_chart_appopen(table_name, state):
    mydb = psycopg2.connect(host="localhost",
                            user="postgres",
                            password="0040",
                            database="phonepe_data",
                            port="5432")
    cursor = mydb.cursor()

    #plot 1
    query1 = f'''SELECT districts,sum(AppOpens) as AppOpens
                    from {table_name}
                    where states = '{state}'
                    group by districts
                    order by AppOpens DESC
                    limit 10'''

    cursor.execute(query1)
    table = cursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table,columns= ("districts","AppOpens"))

    col1, col2 = st.columns(2)

    with col1:
        ammout = px.bar(df_1, x="districts",y="AppOpens",title="Top 10 of AppOpens", hover_name="districts",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=600)
        st.plotly_chart(ammout)
    
    # plot2 
    query2 = f'''SELECT districts,sum(AppOpens) as AppOpens
                    from {table_name}
                    where states = '{state}'
                    group by districts
                    order by AppOpens 
                    limit 10'''

    cursor.execute(query2)
    table2 = cursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table2,columns= ("districts","AppOpens"))

    with col2:
        ammout2 = px.bar(df_2, x="districts",y="AppOpens",title="Last 10 of AppOpens", hover_name="districts",
                        color_discrete_sequence=px.colors.sequential.Rainbow,height=650,width=600)
        st.plotly_chart(ammout2)
   
    query3 = f'''SELECT districts,AVG(AppOpens) as AppOpens
                from {table_name}
                where states = '{state}'
                group by districts
                order by AppOpens'''

    cursor.execute(query3)
    table3 = cursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table3,columns= ("districts","AppOpens"))


    ammout3 = px.bar(df_3, y="districts",x="AppOpens",title="Average of AppOpens", hover_name="districts",orientation="h",
                    color_discrete_sequence=px.colors.sequential.Darkmint_r,height=800,width=1000)
    st.plotly_chart(ammout3)


def top_chart_Top_user(table_name):
    mydb = psycopg2.connect(host="localhost",
                            user="postgres",
                            password="0040",
                            database="phonepe_data",
                            port="5432")
    cursor = mydb.cursor()

    #plot 1
    query1 = f'''select states, sum(registeredUsers) as registeredUsers
                from {table_name}
                group by states
                order by registeredUsers
                limit 10;'''

    cursor.execute(query1)
    table = cursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table,columns= ("states","registeredUsers"))

    col1, col2 = st.columns(2)

    with col1:
        ammout = px.bar(df_1, x="states",y="registeredUsers",title="Top 10 of Registered Users", hover_name="states",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=600)
        st.plotly_chart(ammout)
    
    # plot2 
    query2 = f'''select states, sum(registeredUsers) as registeredUsers
            from {table_name}
            group by states
            order by registeredUsers Desc
            limit 10;'''

    cursor.execute(query2)
    table2 = cursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table2,columns= ("states","registeredUsers"))

    with col2:
        ammout2 = px.bar(df_2, x="states",y="registeredUsers",title="Last 10 of Registered Users", hover_name="states",
                        color_discrete_sequence=px.colors.sequential.Rainbow,height=650,width=600)
        st.plotly_chart(ammout2)
   
    query3 = f'''select states, AVG(registeredUsers) as registeredUsers
                from {table_name}
                group by states
                order by registeredUsers;'''

    cursor.execute(query3)
    table3 = cursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table3,columns= ("states","registeredUsers"))


    ammout3 = px.bar(df_3, y="states",x="registeredUsers",title="Average of Registered Users", hover_name="states",orientation="h",
                    color_discrete_sequence=px.colors.sequential.Darkmint_r,height=800,width=1000)
    st.plotly_chart(ammout3)
   
   

#streamlit section
    

st.set_page_config(layout="wide")

st.markdown("<h1 style='color:#800080;'>PHONEPE DATA VISUALIZATION AND EXPLORATION</h1>", unsafe_allow_html=True)

st.markdown(
    """
    <style>
    .sidebar .sidebar-content {
        background-image: url('C:\\Users\\HameedS\\Desktop\\New folder\\VIdeos\\phonepe.jpg');
        background-size: cover;
    }
    .tabs .stTab {
        background-color: #0066ff;
        color: white;
        border-radius: 10px 10px 0 0;
        padding: 10px 20px;
        font-size: 18px;
        margin-right: 5px;
        cursor: pointer;
    }
    .tabs .stTab:hover {
        background-color: #0052cc;
    }
    .tabs .stTab.stTabSelected {
        background-color: #004080;
    }
    </style>
    """,
    unsafe_allow_html=True
)
with st.sidebar:
    select = option_menu("Main Menu", ["HOME", "Data Exploration", "Top Chart"])

st.sidebar.image("C:\\Users\\HameedS\\Desktop\\New folder\\VIdeos\\phonepe.jpg", use_column_width=True) 

if select == "HOME":
    col1, col2 = st.columns(2)

    with col1:
        st.header("PHONEPE")
        st.subheader("INDIA'S BEST TRANSACTION APP")
        st.markdown("PhonePe is India's leading digital payments and financial technology platform, offering a wide range of services to millions of users across the country.")
        st.markdown("With PhonePe, you can enjoy a seamless and secure way to manage your finances, make payments, and more.")

        st.write("****FEATURES****")
        st.write("- **Credit & Debit Card Linking:** Link your credit and debit cards to PhonePe for quick and secure transactions.")
        st.write("- **Bank Balance Check:** Check your bank account balance in real-time, anytime, anywhere.")
        st.write("- **Money Storage:** Keep your funds safe and easily accessible with PhonePe's digital wallet feature.")
        st.write("- **PIN Authorization:** Protect your transactions with a personal identification number (PIN) for added security.")

        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")

    with col2:
        st.video("C:\\Users\\HameedS\\Desktop\\New folder\\VIdeos\\1.mp4")

    col3, col4 = st.columns(2)

    with col3:
        st.video("C:\\Users\\HameedS\\Desktop\\New folder\\VIdeos\\2.mp4")

    with col4:
        st.write("****ADDITIONAL FEATURES****")
        st.write("- **Easy Transactions:** Conduct transactions seamlessly with PhonePe's user-friendly interface.")
        st.write("- **One App For All Your Payments:** Pay bills, recharge your mobile, shop online, and more, all within the PhonePe app.")
        st.write("- **Your Bank Account Is All You Need:** Use your bank account to make payments without the hassle of cash or cards.")
        st.write("- **Multiple Payment Modes:** Choose from a variety of payment options including UPI, debit/credit cards, and more.")
        st.write("- **PhonePe Merchants:** Discover a wide network of merchants accepting PhonePe payments, from local stores to online platforms.")
        st.write("- **Multiple Ways To Pay:** Whether it's through direct transfer or scanning QR codes, PhonePe offers multiple payment methods to suit your needs.")
        st.write("- **Earn Great Rewards:** Get rewarded for every transaction you make on PhonePe with exciting cashback offers and discounts.")

    col5, col6 = st.columns(2)

    with col5:
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.write("****BENEFITS****")
        st.write("- **No Wallet Top-Up Required:** Enjoy hassle-free transactions without the need to top up your wallet.")
        st.write("- **Pay Directly From Any Bank To Any Bank A/C:** Transfer funds instantly and securely between bank accounts.")
        st.write("- **Instant & Free:** Experience lightning-fast transactions that are completely free of charge.")

    with col6:
        st.video("C:\\Users\\HameedS\\Desktop\\New folder\\VIdeos\\3.mp4")
elif select == "Data Exploration":
    
    tab1,tab2,tab3 = st.tabs(["Aggregated Analysis","Map Analysis","Top Analysis"])
    
    with tab1:
        
        st.markdown("<h2 class='custom-tabs'>Aggregated Analysis</h2>", unsafe_allow_html=True)
        method = st.radio("Please Select Method",["Insurance Analysis","Transaction Analysis","User Analysis"])

        if method == "Insurance Analysis":


            col1,col2 =st.columns(2)
        
            with col1:
                #Years = st.selectbox("Select Year",Aggregated_insurance["Years"].min(),Aggregated_insurance["Years"].max(),Aggregated_insurance["Years"].min())
                Years = st.selectbox("Select Year", Aggregated_insurance["Years"].unique())

            Tran_Am_Cot_Ye_NEW = Transaction_Amout_Count_Year(Aggregated_insurance,Years)

            col1,col2 = st.columns(2)
            with col1:
                Quarter = st.selectbox("Select Quarter",Tran_Am_Cot_Ye_NEW["Quarter"].unique())
                
            Transaction_Amout_Count_Year_Quarter(Tran_Am_Cot_Ye_NEW, Quarter)

        elif method == "Transaction Analysis":

            col1,col2 =st.columns(2)        
            with col1:
                Years = st.selectbox("Select Year",Aggregated_Transaction["Years"].unique())
            Agg_Tran_year = Transaction_Amout_Count_Year(Aggregated_Transaction,Years)

            col1,col2  = st.columns(2)
            with col1:
                states = st.selectbox("Select States",Agg_Tran_year["States"].unique())

            aggre_transa_type(Agg_Tran_year,states)

            col1,col2 = st.columns(2)
            with col1:
                Quarter = st.selectbox("Select Quarter",Agg_Tran_year["Quarter"].unique())
            Agg_Tran_year_Q  = Transaction_Amout_Count_Year_Quarter(Agg_Tran_year, Quarter)

            col1,col2  = st.columns(2)
            with col1:
                states = st.selectbox("Select States_Type",Agg_Tran_year_Q["States"].unique())

            aggre_transa_type(Agg_Tran_year_Q,states)
            

        elif method == "User Analysis": 
            
            col1,col2 =st.columns(2)        
            with col1:
                Years = st.selectbox("Select Year",Aggregated_USER["Years"].unique())
            Aggregated_USER_YEAR = Agger_User_plot_1(Aggregated_USER,Years)

            col1,col2 = st.columns(2)
            with col1:
                Quarter = st.selectbox("Select Quarter",Aggregated_USER_YEAR["Quarter"].unique())
            Agg_Tran_year_Q  = Agger_User_plot_2(Aggregated_USER_YEAR, Quarter)

            col1,col2  = st.columns(2)
            with col1:
                states = st.selectbox("Select States",Agg_Tran_year_Q["States"].unique())

            Agger_User_plot_3(Agg_Tran_year_Q,states)


    
    with tab2:
        
        method2  = st.radio("Please Select Method",["Map Insurance","Map Transaction","Map User"])

        if method2 == "Map Insurance":
                 
            col1,col2 =st.columns(2)  
            with col1:
                Years = st.selectbox("Select Year Map Insurance",Map_insruence["Years"].unique())
                MAP_Insrurence_Year = Transaction_Amout_Count_Year(Map_insruence,Years)  

            col1,col2  = st.columns(2)
            with col1:
                states = st.selectbox("Select States for Map Insurance",MAP_Insrurence_Year["States"].unique())

            Map_insru_Distric_type(MAP_Insrurence_Year,states)

            col1,col2 = st.columns(2)
            with col1:
                Quarter = st.selectbox("Select Quarter for Map Insurance",MAP_Insrurence_Year["Quarter"].unique())
            MAP_Insrurence_Year_Quarter  = Transaction_Amout_Count_Year_Quarter(MAP_Insrurence_Year, Quarter)

            col1,col2  = st.columns(2)
            with col1:
                states = st.selectbox("Select States_Type for Map Insrurence",MAP_Insrurence_Year_Quarter["States"].unique())

            Map_insru_Distric_type(MAP_Insrurence_Year_Quarter,states)
            
        elif method2 == "Map Transaction":
            col1,col2 =st.columns(2)  
            with col1:
                Years = st.selectbox("Select Year Map Transaction",Map_Transaction["Years"].unique())
                MAP_Transaction_Year = Transaction_Amout_Count_Year(Map_Transaction,Years)  

            col1,col2  = st.columns(2)
            with col1:
                states = st.selectbox("Select States for Map Transaction",MAP_Transaction_Year["States"].unique())

            Map_insru_Distric_type(MAP_Transaction_Year,states)

            col1,col2 = st.columns(2)
            with col1:
                Quarter = st.selectbox("Select Quarter for Map Transaction",MAP_Transaction_Year["Quarter"].unique())
            MAP_Transaction_Year_Quarter  = Transaction_Amout_Count_Year_Quarter(MAP_Transaction_Year, Quarter)

            col1,col2  = st.columns(2) 
            with col1:
                states = st.selectbox("Select States_Type for Map Transaction",MAP_Transaction_Year_Quarter["States"].unique())

            Map_insru_Distric_type(MAP_Transaction_Year_Quarter,states)

        elif method2== "Map User":
            col1,col2 =st.columns(2)  
            with col1:
                Years = st.selectbox("Select Year Map User",Map_user["Years"].unique())
                MAP_User_Year = map_user_plot_1(Map_user,Years)    

            col1,col2 = st.columns(2)
            with col1:
                Quarter = st.selectbox("Select Quarter for Map User",MAP_User_Year["Quarter"].unique())
            MAP_user_Year_Quarter  = map_user_plot_2(MAP_User_Year, Quarter)

            col1,col2  = st.columns(2) 
            with col1:
                states = st.selectbox("Select States for Map User",MAP_user_Year_Quarter["States"].unique())

            map_user_plot_3(MAP_user_Year_Quarter,states) 

    with tab3:     
        
        method3  = st.radio("Please Select Method",["Top Insurance","Top Transaction","Top User"])

        if method3 == "Top Insurance":

            col1,col2 =st.columns(2)  
            with col1:
                Years = st.selectbox("Select Year Top Insurance",TOP_insruence["Years"].unique())
                Top_insruence_Year = Transaction_Amout_Count_Year(TOP_insruence,Years) 

                

            col1,col2  = st.columns(2) 
            with col1:
                states = st.selectbox("Select States for Top User",Top_insruence_Year["States"].unique())

            top_insruence_plot_1(Top_insruence_Year,states)  

            col1,col2 = st.columns(2)
            with col1:
                Quarter = st.selectbox("Select Quarter for Top User",Top_insruence_Year["Quarter"].unique())
            Top_user_Year_Quarter  = Transaction_Amout_Count_Year_Quarter(Top_insruence_Year, Quarter)

        elif method3 == "Top Transaction":  
            col1,col2 =st.columns(2)  
            with col1:
                Years = st.selectbox("Select Year Top Transaction",Top_transaction["Years"].unique())
                Top_transaction_Year = Transaction_Amout_Count_Year(Top_transaction,Years) 

                

            col1,col2  = st.columns(2) 
            with col1:
                states = st.selectbox("Select States for Top Transaction",Top_transaction_Year["States"].unique())

            top_insruence_plot_1(Top_transaction_Year,states)  

            col1,col2 = st.columns(2) 
            with col1:
                Quarter = st.selectbox("Select Quarter for Top Transaction",Top_transaction_Year["Quarter"].unique())
            Top_transaction_Year_Quarter  = Transaction_Amout_Count_Year_Quarter(Top_transaction_Year, Quarter)
        elif method3 == "Top User":
            
            col1,col2 =st.columns(2)  
            with col1:
                Years = st.selectbox("Select Year Top User",TOP_USER["Years"].unique())
                top_user_Y = top_user_plot_1(TOP_USER,Years)  
            
            col1,col2  = st.columns(2) 
            with col1:
                states = st.selectbox("Select States for Top User",top_user_Y["States"].unique())

            top_user_plot_2(top_user_Y,states)       
elif select == "Top Chart":
    
    question = st.selectbox("Select the Question",["1.	Transaction Amount and Count of Aggregated Insurance",
                                                        "2.	Transaction Amount and Count of Map Insurance",
                                                        "3.	Transaction Amount and Count of Top Insurance",
                                                        "4.	Transaction Amount and Count of Aggregated Transaction",
                                                        "5.	Transaction Amount and Count of Map Transaction",
                                                        "6.	Transaction Amount and Count of Top Transaction",
                                                        "7.	Transaction Count of Aggregated User",
                                                        "8.	Registered User of Map User",
                                                        "9.	App opens of Map user" ,
                                                        "10.	Registered user of Top User"])
    
    if question=="1.	Transaction Amount and Count of Aggregated Insurance":

        st.subheader("Transaction Amount")
        top_chart_transactionAmount("aggregated_insurance")
        st.subheader("Transaction Count")
        top_chart_transactionCount("aggregated_insurance")
    elif question=="2.	Transaction Amount and Count of Map Insurance":

        st.subheader("Transaction Amount")
        top_chart_transactionAmount("map_insruence")
        st.subheader("Transaction Count")
        top_chart_transactionCount("map_insruence")
    elif question=="3.	Transaction Amount and Count of Top Insurance":

        st.subheader("Transaction Amount")
        top_chart_transactionAmount("top_insrurence")
        st.subheader("Transaction Count")
        top_chart_transactionCount("top_insrurence")
    elif question=="4.	Transaction Amount and Count of Aggregated Transaction":

        st.subheader("Transaction Amount")
        top_chart_transactionAmount("aggregated_transaction")
        st.subheader("Transaction Count")
        top_chart_transactionCount("aggregated_transaction")
    elif question=="5.	Transaction Amount and Count of Map Transaction":

        st.subheader("Transaction Amount")
        top_chart_transactionAmount("map_transaction")
        st.subheader("Transaction Count")
        top_chart_transactionCount("map_transaction")
    elif question=="6.	Transaction Amount and Count of Top Transaction":

        st.subheader("Transaction Amount")
        top_chart_transactionAmount("top_transaction")
        st.subheader("Transaction Count")
        top_chart_transactionCount("top_transaction")
    elif question=="7.	Transaction Count of Aggregated User":

        st.subheader("Transaction Count")
        top_chart_transactionCount("aggregated_user") 
    elif question=="8.	Registered User of Map User":

        states = st.selectbox("Select the state",Map_user["States"].unique()) 
        st.subheader("Registered Users")
        top_chart_register_user("Map_user",states) 
    elif question=="9.	App opens of Map user":

        states = st.selectbox("Select the state",Map_user["States"].unique()) 
        st.subheader("AppOpens")
        top_chart_appopen("Map_user",states)   
    elif question=="10.	Registered user of Top User":

        st.subheader("Registered user")
        top_chart_Top_user("Map_user")    

    