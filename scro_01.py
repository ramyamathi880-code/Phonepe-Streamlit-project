import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
from sqlalchemy import create_engine, text
import mysql.connector
import missingno as mx

# -------------------- DATABASE CONNECTION --------------------
con = mysql.connector.connect(
    user='root',
    host='localhost',
    password='ramya',
    database='phonepe_db'
)

cursor = con.cursor()
cursor.execute("show tables")

for i in cursor.fetchall():
    print(i)

cursor.close()
con.close()

user = 'root'
host = 'localhost'
password = 'ramya'
port = 3306
database = 'phonepe_db'

eng = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}')

# -------------------- STREAMLIT UI --------------------
st.title("📊 PhonePe Business Case Study Dashboard")
st.markdown("---")

Scenario = st.selectbox(
    "🧭 Select Business Case Study Scenario",
    [
        "scenario_1: 1️⃣ Decoding Transaction Dynamics",
        "scenario_2: 2️⃣ Device Dominance & User Engagement",
        "scenario_3: 3️⃣ Insurance Penetration & Growth",
        "scenario_4: 4️⃣ Transaction Analysis Across States & Districts",
        "scenario_5: 5️⃣ User Registration Analysis"
    ]
)

# ==================== SCENARIO 1 ====================
if Scenario == "scenario_1: 1️⃣ Decoding Transaction Dynamics":

    st.header("📍 Scenario 1: Decoding Transaction Dynamics")

    st.subheader("🏙️ State-Wise Transaction Analysis")
    qur = """
        SELECT state, year, SUM(amount) AS total_amount, SUM(count) AS total_transaction
        FROM agg_transaction
        GROUP BY state, year
        ORDER BY state, year DESC
    """
    state_wise_analysis = pd.read_sql(qur, eng)

    selected_state = st.selectbox(
        "👉 Select a State",
        state_wise_analysis['state'].value_counts().keys()
    )

    filtered_df = state_wise_analysis[state_wise_analysis['state'] == selected_state]

    fig = px.line(
        filtered_df,
        x='year',
        y='total_amount',
        title=f"📈 {selected_state} - Transaction Amount Trend",
        markers=True
    )
    st.plotly_chart(fig, use_container_width=True)

    fig_2 = px.line(
        filtered_df,
        x='year',
        y='total_transaction',
        title=f"🔄 {selected_state} - Transaction Count Trend",
        markers=True
    )
    st.plotly_chart(fig_2, use_container_width=True)

    st.subheader("💳 Payment Category Performance")
    qur = """
        SELECT name AS payment_transaction,
               SUM(amount) AS total_amount,
               SUM(count) AS total_transaction
        FROM agg_transaction
        GROUP BY payment_transaction
        ORDER BY payment_transaction
    """
    pie_df = pd.read_sql(qur, eng)

    st.subheader("🥧 Payment-Wise Total Amount Distribution")
    fig_3 = px.pie(
        pie_df,
        names='payment_transaction',
        values='total_amount',
        hole=0.4
    )
    st.plotly_chart(fig_3, use_container_width=True)

    st.subheader("🔁 Payment-Wise Transaction Count Distribution")
    fig_4 = px.pie(
        pie_df,
        names='payment_transaction',
        values='total_transaction',
        hole=0.4
    )
    st.plotly_chart(fig_4, use_container_width=True)

    st.subheader("🏆 State-Wise Payment Category Performance")
    qur = """
        SELECT state,
               name AS payment_category,
               SUM(amount) AS total_amount,
               SUM(count) AS total_transaction
        FROM agg_transaction
        GROUP BY state, payment_category
        ORDER BY state, payment_category
    """
    bar_df = pd.read_sql(qur, eng)

    selected_bar = st.selectbox("📍 Select State", bar_df['state'].unique())
    filtered_bar = bar_df[bar_df['state'] == selected_bar]

    fig_5 = px.bar(
        filtered_bar,
        x='payment_category',
        y='total_amount',
        title=f"💰 {selected_bar} - Top Payment Categories"
    )
    st.plotly_chart(fig_5, use_container_width=True)

    st.subheader("📊 Quarterly Transaction Distribution")
    qur = """
        SELECT state, SUM(count) AS transaction, quarter
        FROM agg_transaction
        GROUP BY state, quarter
        ORDER BY state, quarter
    """
    trans_type = pd.read_sql(qur, eng)

    selected_trans = st.selectbox("📌 Select State", trans_type['state'].unique())
    filtered_trans = trans_type[trans_type['state'] == selected_trans]

    fig_6 = px.bar(
        filtered_trans,
        x='quarter',
        y='transaction'
    )
    fig_6.update_layout(bargap=0.4)
    st.plotly_chart(fig_6, use_container_width=True)

    st.subheader("🧾 Payment Category Contribution Overview")
    qur = """
        SELECT name AS payment_type, SUM(amount) AS total_amount
        FROM agg_transaction
        GROUP BY payment_type
    """
    pay = pd.read_sql(qur, eng)

    fig_8 = px.pie(
        pay,
        names='payment_type',
        values='total_amount',
        hole=0.4
    )
    st.plotly_chart(fig_8, use_container_width=True)

# ==================== SCENARIO 2 ====================
elif Scenario == "scenario_2: 2️⃣ Device Dominance & User Engagement":

    st.header("📱 Scenario 2: Device Dominance & User Engagement")

    st.subheader("🔍 Missing Value Analysis")
    df = pd.read_sql("SELECT * FROM agg_user", eng)
    st.write(df.isnull().sum())

    fig, ax = plt.subplots()
    mx.matrix(df, ax=ax)
    st.pyplot(fig)

    st.subheader("📆 Year-Wise Device Brand Usage")
    qur = """
        SELECT device_brand, SUM(device_count) AS total_transaction, year
        FROM agg_user
        GROUP BY device_brand, year
        ORDER BY device_brand, year
    """
    brand = pd.read_sql(qur, eng)

    selected_brand = st.selectbox("📱 Select Device Brand", brand['device_brand'].unique())
    filtered_brand = brand[brand['device_brand'] == selected_brand]

    fig_11 = px.line(
        filtered_brand,
        x='year',
        y='total_transaction',
        markers=True
    )
    st.plotly_chart(fig_11, use_container_width=True)

    st.subheader("⏱️ Quarter-Wise Device Brand Usage")
    qur = """
        SELECT device_brand, SUM(device_count) AS total_transaction, quarter
        FROM agg_user
        GROUP BY device_brand, quarter
    """
    apps = pd.read_sql(qur, eng)

    selected_app = st.selectbox("📲 Select Device Brand", apps['device_brand'].unique())
    filtered_app = apps[apps['device_brand'] == selected_app]

    fig_12 = px.bar(
        filtered_app,
        x='quarter',
        y='total_transaction'
    )
    st.plotly_chart(fig_12, use_container_width=True)

    st.subheader("🌍 State-Wise Top Device Brands")
    qur = """
        SELECT state, device_brand, SUM(device_count) AS total_transaction
        FROM agg_user
        GROUP BY state, device_brand
    """
    statewise = pd.read_sql(qur, eng)

    selected_sts = st.selectbox("📍 Select State", statewise['state'].unique())
    filtered_sts = statewise[statewise['state'] == selected_sts]

    fig_13 = px.bar(
        filtered_sts,
        x='device_brand',
        y='total_transaction',
        color='device_brand'
    )
    st.plotly_chart(fig_13, use_container_width=True)

# ==================== SCENARIO 3 ====================
elif Scenario == "scenario_3: 3️⃣ Insurance Penetration & Growth":

    st.header("🛡️ Scenario 3: Insurance Penetration & Growth")

    st.subheader("🏙️ State-Wise Insurance Transaction Count")
    qur = """
        SELECT state, SUM(count) AS transaction, SUM(amount) AS total_amount, year
        FROM agg_insurance
        GROUP BY state, year
        ORDER BY state, year
    """
    insurance = pd.read_sql(qur, eng)

    selected_st = st.selectbox("📍 Select State", insurance['state'].unique())
    filtered_st = insurance[insurance['state'] == selected_st]

    fig_14 = px.line(
        filtered_st,
        x='year',
        y='transaction',
        markers=True
    )
    st.plotly_chart(fig_14, use_container_width=True)

    st.subheader("💰 Insurance Transaction Amount")
    fig_15 = px.bar(
        filtered_st,
        x='year',
        y='total_amount'
    )
    st.plotly_chart(fig_15, use_container_width=True)

# ==================== SCENARIO 4 ====================
elif Scenario == "scenario_4: 4️⃣ Transaction Analysis Across States & Districts":

    st.header("🌍 4️⃣ Transaction Analysis for Market Expansion")

    st.subheader("🏆 Top States by Transaction Value & Volume")
    q1 = '''
    select state,
        sum(amount) as total_transaction,
        sum(count) as total_count
    from agg_transaction
    group by state
    order by total_transaction desc
    limit 10;
    '''
    top_states = pd.read_sql(q1, eng)

    fig1 = px.bar(
        top_states,
        x='state',
        y='total_transaction',
        text='total_transaction',
        title='🏅 Top 10 States by Transaction Value'
    )
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("📊 Type-wise Transaction Distribution in Top States")
    top_state_list = top_states['state'].tolist()

    q2 = f'''
    select state, name,
        sum(amount) as total_transaction,
        sum(count) as total_count
    from agg_transaction
    where state in ({', '.join("'" + s + "'" for s in top_state_list)})
    group by state, name
    order by state, total_transaction desc;
    '''
    type_distribution = pd.read_sql(q2, eng)

    fig2 = px.bar(
        type_distribution,
        x='name',
        y='total_transaction',
        color='state',
        text='total_transaction',
        title='📌 Transaction Types Across Top States'
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("📈 Transaction Concentration Across States")
    q5 = '''
    select state,
        sum(amount) as total_transaction,
        sum(count) as total_count
    from agg_transaction
    group by state
    order by total_transaction desc
    limit 20;
    '''
    state_concentration = pd.read_sql(q5, eng)

    fig5 = px.bar(
        state_concentration,
        x='state',
        y='total_transaction',
        text='total_transaction',
        title='📍 Transaction Concentration by State'
    )
    st.plotly_chart(fig5, use_container_width=True)

    st.subheader("📅 Quarterly Transaction Trend – Tamil Nadu")
    q1 = '''
    select year, quarter,
        sum(amount) as total_transaction,
        sum(count) as total_count
    from agg_transaction
    where state = 'tamil-nadu'
    group by year, quarter
    order by year, quarter;
    '''
    quarterly_data = pd.read_sql(q1, eng)

    fig1 = px.line(
        quarterly_data,
        x='quarter',
        y='total_transaction',
        color='year',
        markers=True,
        title='📉 Quarterly Transaction Trend – Tamil Nadu'
    )
    st.plotly_chart(fig1, use_container_width=True)


elif Scenario == "scenario_5: 5️⃣ User Registration Analysis":

    st.header("👥 5️⃣ User Engagement & Growth Strategy")

    st.subheader("🌟 Top States by Registered Users")
    q1 = '''
    select state,
        sum(registeredUsers) as total_users
    from agg_user
    group by state
    order by total_users desc
    limit 10;
    '''
    top_users = pd.read_sql(q1, eng)

    fig1 = px.bar(
        top_users,
        x='state',
        y='total_users',
        text='total_users',
        title='🏆 Top 10 States by Registered Users'
    )
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("⚖️ State-wise Engagement Ratio")
    q2 = '''
    select state,
        sum(registeredUsers) as total_users,
        sum(appOpens) as total_app_opens,
        sum(appOpens)/sum(registeredUsers) as engagement_ratio
    from agg_user
    group by state
    order by engagement_ratio asc;
    '''
    engagement_state = pd.read_sql(q2, eng)

    fig2 = px.bar(
        engagement_state,
        x='state',
        y='engagement_ratio',
        title='📊 Engagement Ratio Across States (Low → High)'
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("📆 Year-wise Registered User Growth")
    q4 = '''
    select year,
        sum(registeredUsers) as total_users
    from agg_user
    group by year
    order by year;
    '''
    year_growth = pd.read_sql(q4, eng)

    fig4 = px.line(
        year_growth,
        x='year',
        y='total_users',
        markers=True,
        title='📈 Year-wise User Growth Trend'
    )
    st.plotly_chart(fig4, use_container_width=True)

    st.subheader("🎯 Top States for Re-engagement Campaigns")
    q5 = '''
    select state,
        sum(registeredUsers) as total_users,
        sum(appOpens) as total_app_opens,
        sum(appOpens)/sum(registeredUsers) as engagement_ratio
    from agg_user
    group by state
    order by engagement_ratio asc
    limit 10;
    '''
    reengage_targets = pd.read_sql(q5, eng)

    fig5 = px.bar(
        reengage_targets,
        x='state',
        y='engagement_ratio',
        text='engagement_ratio',
        title='🚀 States for Re-engagement Campaigns'
    )
    st.plotly_chart(fig5, use_container_width=True)


else:
    st.warning("⚠️ Please select a valid scenario")

st.markdown("---")
