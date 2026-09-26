# 这段代码会生成一个完整的 Streamlit Web 应用

import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# Matplotlib 中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']
# Windows 请用 SimHei
plt.rcParams['axes.unicode_minus'] = False # 正常显示负号

# 1. 设置网页的标题和图标
st.set_page_config(page_title="EcoTrek 销售分析", page_icon="📈", layout="wide")

# 2. 添加网页主标题和副标题
st.title("EcoTrek Solutions - 销售与温度趋势分析")
st.markdown("本看板展示了每日销售量与温度之间的关系，帮助制定营销和生产策略。")

# 3. 使用缓存加载数据，避免每次刷新网页都要重新读取，提高性能
@st.cache_data
def load_data():
    df = pd.read_csv('Week_3_Temperature_DailySale.csv')
    # 确保日期格式正确
    df['Date'] = pd.to_datetime(df['Date'])
    return df

df = load_data()
#加载评论数据
@st.cache_data
def load_reviews_data():
    reviews_df = pd.read_csv('Chyi_Joelle_sentiment.csv')
    return reviews_df

reviews_df = load_reviews_data()

reviews_df = load_reviews_data()

# 4. 在网页侧边栏添加交互组件：日期范围选择器
st.sidebar.header("筛选条件")
start_date = st.sidebar.date_input("开始日期", df['Date'].min())
end_date = st.sidebar.date_input("结束日期", df['Date'].max())

# 根据选择的日期过滤数据
filtered_df = df[(df['Date'] >= pd.to_datetime(start_date)) & (df['Date'] <= pd.to_datetime(end_date))]

# 5. 展示关键业务指标 (KPI)
col1, col2, col3 = st.columns(3)
col1.metric("总销售量", f"{filtered_df['Daily Units Sold'].sum()} 件")
col2.metric("平均每日销量", f"{filtered_df['Daily Units Sold'].mean():.1f} 件")
col3.metric("平均温度", f"{filtered_df['Daily Temperature (C)'].mean():.1f} °C")

st.divider()

# 6. 绘制可视化图表
# 图表1：每日销量随时间变化的折线图
st.subheader("📅 每日销量趋势")
fig_line = px.line(filtered_df, x='Date', y='Daily Units Sold', 
                   title='每日销量趋势', markers=True)
st.plotly_chart(fig_line, use_container_width=True)

# 图表2：温度与销量的散点图（分析相关性）
st.subheader("🌡️ 温度与销量的关系")
fig_scatter = px.scatter(filtered_df, x='Daily Temperature (C)', y='Daily Units Sold',
                         trendline="ols", # 添加趋势线
                         title='温度 vs 销量', 
                         labels={'Daily Temperature (C)': '温度 (°C)', 'Daily Units Sold': '销量'})
st.plotly_chart(fig_scatter, use_container_width=True)

st.divider()
# ==========================【顾客评价情绪图】==============================================
st.subheader("顾客评价情绪分析")

# 使用两列布局让图表并排显示
col_pie, col_bar = st.columns(2)

with col_pie:
    # 第6：制作情绪百分比饼图
    sentiment_pct = reviews_df['sentiment'].value_counts(normalize=True) * 100
    
    # 创建 Matplotlib 图形对象 (不使用 plt.show())
    fig_pie, ax_pie = plt.subplots(figsize=(6, 5))
    # 颜色设置：绿、黄、红
    colors = ['#4CAF50', '#FFC107', '#F44336']
    
    ax_pie.pie(sentiment_pct, labels=sentiment_pct.index, autopct='%1.1f%%', 
               startangle=140, colors=colors)
    ax_pie.set_title('顾客评价情绪百分比分布')
    ax_pie.axis('equal') # 保证饼图是正圆
    
    # 在 Streamlit 中渲染 Matplotlib 图表
    st.pyplot(fig_pie)
  
with col_bar:
       # 第4：制作情绪极性数量柱状图
       fig_bar , ax_bar = plt.subplots(figsize=(8,5))

       # 使用 Seaborn 画柱状图，指定 ax=ax_bar
       sns.countplot(x='sentiment',
data=reviews_df,ax=ax_bar,
palette=colcrs)

       ax_bar.set_title('顾客评价情绪性数量分布',fontsize=14) 
       ax_bar.set_xlabel('情绪类别',fontsize=12)
       ax_bar.set_ylabel('数量',fontsize=12)

       # 在Streamlit 中渲染
       st.pyplot(fig_bar)

#
# ===================================================================

# 7. 添加页面底部说明
st.caption("EcoTrek Solutions - 商业数据分析报告")
# 8. 添加商业洞察与建议
st.divider()
st.subheader("商业洞察与建议")
st.markdown("""通过散点图及趋势线可以看出，温度与销量呈**明显的正相关**(温度越高，销量越大)。
              因此，建议公司在气温较高的月份（如夏季）**可提前增加产量，并加大营销投放力度**；在温度较低的月份则应**控制库存，避免积压**。""")