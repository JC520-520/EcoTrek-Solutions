# 这段代码会生成一个完整的 Streamlit Web 应用

import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 设置网页的标题和图标
st.set_page_config(page_title="EcoTrek 销售分析", page_icon="📈", layout="wide")

# 2. 添加网页主标题和副标题
st.title(" EcoTrek Solutions - 销售与温度趋势分析")
st.markdown("本看板展示了每日销售量与温度之间的关系，帮助制定营销和生产策略。")

# 3. 使用缓存加载数据，避免每次刷新网页都要重新读取，提高性能
@st.cache_data
def load_data():
    df = pd.read_csv('Week_3_Temperature_DailySale.csv')
    # 确保日期格式正确
    df['Date'] = pd.to_datetime(df['Date'])
    return df

df = load_data()

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

# 7. 添加页面底部说明
st.caption("EcoTrek Solutions - 商业数据分析报告")
# 8. 添加商业洞察与建议
st.divider()
st.subheader("商业洞察与建议")
st.markdown("""通过散点图及趋势线可以看出，温度与销量呈**明显的正相关**(温度越高，销量越大)。
              因此，建议公司在气温较高的月份（如夏季）**可提前增加产量，并加大营销投放力度**；在温度较低的月份则应**控制库存，避免积压**。""")