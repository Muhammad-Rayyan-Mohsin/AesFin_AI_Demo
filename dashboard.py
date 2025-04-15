import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import time
from datetime import datetime

# Import functions from the analysis script
from one import (
    preprocess_data, detect_anomalies, risk_scoring, 
    variance_analysis, generate_commentary, document_intelligence
)

# Set page configuration
st.set_page_config(
    page_title="Maple Leaf Financial Analytics",
    page_icon="🍃",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main {
        background-color: #FFFFFF;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        border-radius: 4px 4px 0px 0px;
        padding: 10px 20px;
        background-color: #E7F5E9;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #2E8B57 !important;
        color: white !important;
    }
    h1, h2, h3 {
        color: #2E8B57;
    }
    .metric-card {
        background-color: #E7F5E9;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stProgress > div > div {
        background-color: #2E8B57;
    }
    button {
        background-color: #2E8B57 !important;
        color: white !important;
    }
    .logo-container {
        display: flex;
        justify-content: center;
        margin-bottom: 20px;
    }
    .insight-card {
        background-color: #E7F5E9;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        border-left: 4px solid #2E8B57;
    }
</style>
""", unsafe_allow_html=True)

# Define consistent color scales
GREEN_SEQUENTIAL = ['#E7F5E9', '#C3E6CB', '#9FD8B4', '#78C27C', '#5AAD61', '#3C9748', '#2E8B57']
GREEN_DIVERGENT = ['#198754', '#63C392', '#C3E6CB', '#FFFFFF', '#C3E6CB', '#63C392', '#198754']

# Application header with logo
col1, col2 = st.columns([1, 5])

with col1:
    # Use st.image() instead of HTML to display the logo
    try:
        st.image("2.png", width=100)
    except:
        st.error("Logo not found. Please ensure '2.png' is in the same directory as this script.")

with col2:
    st.title("🍃 Maple Leaf Restaurant Financial Analytics")
    st.markdown("Interactive financial analysis dashboard with AI-powered insights.")

# Simplified sidebar for filters and controls
with st.sidebar:
    st.header("Dashboard Controls")
    
    # Set fixed date range without user control
    date_range = (datetime(2023, 1, 1), datetime(2023, 12, 31))
    
    # Add fixed description about the dashboard
    st.markdown("### About")
    st.info("This dashboard provides real-time financial analysis for Maple Leaf Restaurant operations.")

# Load and process data - hardcode the filename
@st.cache_data
def load_data():
    df = pd.read_csv('maple_leaf_restaurant_financial_data.csv')
    df = preprocess_data(df)
    return df

# Loading spinner
with st.spinner("Loading and analyzing data..."):
    df = load_data()
    
    # Run analyses with fixed anomaly threshold
    anomaly_threshold = 0.05  # Fixed value
    df, anomalies = detect_anomalies(df, contamination=anomaly_threshold)
    df = risk_scoring(df)
    monthly_data, variances = variance_analysis(df)
    commentary = generate_commentary(df, monthly_data, variances)
    df = document_intelligence(df)

# Dashboard main content
tabs = st.tabs([
    "📊 Overview", 
    "💡 Anomaly Detection", 
    "📈 Variance Analysis", 
    "🧠 AI Insights",
    "📑 Reports"
])

# 1. Overview Tab
with tabs[0]:
    st.header("Financial Overview")
    
    # KPI metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric(
            "Total Transactions", 
            f"{len(df):,}",
            delta=None
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric(
            "Total Amount", 
            f"${df['Amount'].sum():,.2f}",
            delta=f"{df['Amount'].sum() / len(df):.1f} avg"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        anomaly_pct = (len(anomalies) / len(df)) * 100
        st.metric(
            "Anomalies Detected", 
            f"{len(anomalies)} ({anomaly_pct:.1f}%)",
            delta=None
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        high_risk_count = len(df[df['Risk Level'] == 'High'])
        st.metric(
            "High Risk Transactions", 
            f"{high_risk_count} ({high_risk_count/len(df)*100:.1f}%)",
            delta=None,
            delta_color="inverse"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Transaction visualization
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Transactions by Category")
        category_amounts = df.groupby('Category')['Amount'].sum().sort_values(ascending=False)
        
        fig = px.bar(
            x=category_amounts.values, 
            y=category_amounts.index,
            orientation='h',
            color=category_amounts.values,
            color_continuous_scale=GREEN_SEQUENTIAL,
            labels={'x': 'Amount ($)', 'y': 'Category'},
            title=''
        )
        fig.update_layout(height=400, margin=dict(l=10, r=10, b=10, t=10))
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Monthly Transaction Volume")
        monthly_volume = df.groupby(df['Date'].dt.to_period('M'))['Amount'].sum()
        
        fig = px.line(
            x=monthly_volume.index.astype(str), 
            y=monthly_volume.values,
            markers=True,
            line_shape='spline',
            color_discrete_sequence=['#2E8B57'],
            labels={'x': 'Month', 'y': 'Amount ($)'},
            title=''
        )
        fig.update_layout(height=400, margin=dict(l=10, r=10, b=10, t=10))
        st.plotly_chart(fig, use_container_width=True)
    
    # Risk distribution
    st.subheader("Risk Score Distribution")
    fig = px.histogram(
        df, 
        x='Risk Score',
        color_discrete_sequence=['#78C27C'],
        opacity=0.8,
        nbins=20
    )
    fig.add_vline(x=30, line_dash="dash", line_color="#2E8B57", annotation_text="Low Risk Threshold")
    fig.add_vline(x=70, line_dash="dash", line_color="#2E8B57", annotation_text="High Risk Threshold")
    fig.update_layout(height=300, margin=dict(l=10, r=10, b=10, t=10))
    st.plotly_chart(fig, use_container_width=True)

# 2. Anomaly Detection Tab
with tabs[1]:
    st.header("Anomaly Detection")
    
    st.markdown("""
    Our AI-powered anomaly detection system identifies unusual patterns in your financial data.
    The algorithm examines transaction amounts, timing, and risk scores to flag potential issues.
    """)
    
    # Anomaly visualization
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Transaction Amount vs Risk Score")
        
        # Create a copy of the dataframe with absolute amounts for marker sizing
        plot_df = df.copy()
        plot_df['AbsAmount'] = plot_df['Amount'].abs()
        
        fig = px.scatter(
            plot_df, 
            x='Amount', 
            y='Risk Score',
            color='AI_Anomaly_Flag',
            color_discrete_map={0: '#78C27C', 1: '#2E8B57'},  
            hover_data=['Transaction ID', 'Category', 'Date'],
            size='AbsAmount',
            opacity=0.7,
            labels={'AI_Anomaly_Flag': 'Anomaly Status'},
            title=''
        )
        
        # Update marker properties to enhance visibility
        fig.update_traces(
            marker=dict(
                line=dict(width=1, color='#FFFFFF'),  # Add white border to make points more distinct
            ),
            selector=dict(mode='markers')
        )
        
        # Add custom legend to clarify anomaly status
        fig.update_layout(
            height=500, 
            margin=dict(l=10, r=10, b=10, t=10),
            legend=dict(
                title="Anomaly Status",
                itemsizing="constant",
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        # Rename legend items for clarity - with safer implementation
        newnames = {'0': 'Normal', '1': 'Anomaly'}
        
        # Updated trace naming logic to handle possible empty trace names
        def update_trace_name(trace):
            if trace.name in newnames:
                trace.update(name=newnames[trace.name])
        
        fig.for_each_trace(update_trace_name)
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Anomalies by Category")
        category_anomalies = df[df['AI_Anomaly_Flag'] == 1].groupby('Category').size().sort_values(ascending=False)
        
        fig = px.pie(
            values=category_anomalies.values,
            names=category_anomalies.index,
            color_discrete_sequence=GREEN_SEQUENTIAL,
            hole=0.4
        )
        fig.update_layout(height=500, margin=dict(l=10, r=10, b=10, t=10))
        st.plotly_chart(fig, use_container_width=True)
    
    # Anomaly data table
    st.subheader("Anomalous Transactions")
    if len(anomalies) > 0:
        # Get anomalies from the main dataframe after all processing is done
        # This ensures we have all columns including Risk Level
        anomaly_display = df[df['AI_Anomaly_Flag'] == 1]
        st.dataframe(
            anomaly_display[['Transaction ID', 'Date', 'Amount', 'Category', 'Vendor', 'Risk Score', 'Risk Level']],
            use_container_width=True
        )
    else:
        st.info("No anomalies detected with current settings.")

# 3. Variance Analysis Tab
with tabs[2]:
    st.header("Variance Analysis")
    
    st.markdown("""
    This analysis compares financial data across different time periods to identify trends and outliers.
    Significant variances can highlight areas requiring attention or potential growth opportunities.
    """)
    
    # Variance visualization
    st.subheader("Month-over-Month Category Variance (%)")
    
    # Convert the Period index to string for Plotly
    variance_df = variances.tail(3).reset_index()
    variance_df['Date'] = variance_df['Date'].astype(str)
    
    # Create a heatmap of the variances
    categories = variance_df.columns[1:]
    dates = variance_df['Date'].tolist()
    
    z_values = []
    for cat in categories:
        z_values.append(variance_df[cat].tolist())
    
    fig = go.Figure(data=go.Heatmap(
        z=z_values,
        x=dates,
        y=categories,
        colorscale=GREEN_SEQUENTIAL,
        colorbar=dict(title='Variance %'),
    ))
    
    fig.update_layout(
        height=500,
        margin=dict(l=10, r=10, b=10, t=10),
        xaxis_title="Month",
        yaxis_title="Category"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Category trends
    st.subheader("Category Trends Over Time")
    
    # Convert monthly data to a format suitable for plotting
    monthly_df = monthly_data.reset_index()
    monthly_df['Date'] = monthly_df['Date'].astype(str)
    
    # Create dropdown for category selection
    selected_categories = st.multiselect(
        "Select Categories to Display",
        options=monthly_data.columns.tolist(),
        default=monthly_data.columns[:3].tolist()
    )
    
    if selected_categories:
        fig = go.Figure()
        
        # Use different shades of green for each category
        green_colors = GREEN_SEQUENTIAL
        
        for i, category in enumerate(selected_categories):  # Fixed: added enumerate() function
            color_idx = i % len(green_colors)
            fig.add_trace(go.Scatter(
                x=monthly_df['Date'],
                y=monthly_df[category],
                mode='lines+markers',
                name=category,
                line=dict(color=green_colors[color_idx], width=3),
                marker=dict(color=green_colors[color_idx], size=8)
            ))
        
        fig.update_layout(
            height=400,
            margin=dict(l=10, r=10, b=10, t=10),
            xaxis_title="Month",
            yaxis_title="Amount ($)"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Please select at least one category to display.")

# 4. AI Insights Tab
with tabs[3]:
    st.header("AI-Generated Insights")
    
    st.markdown("""
    Our AI analyzes your financial data to provide relevant insights and recommendations.
    These automated interpretations help you quickly understand key trends and issues.
    """)
    
    # Display AI commentary with improved styling
    for i, insight in enumerate(commentary):
        st.markdown(f"""
        <div class="insight-card">
            <h3 style="color: #2E8B57; margin-top: 0;">Insight {i+1}</h3>
            <p style="font-size: 18px;">{insight}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Document intelligence insights
    st.subheader("Document Intelligence")
    
    notes_count = df['Notes'].notna().sum()
    if notes_count > 0:
        common_words = []
        for note in df['Notes'].dropna():
            words = note.lower().split()
            common_words.extend([w for w in words if len(w) > 3])
        
        from collections import Counter
        word_counts = Counter(common_words).most_common(10)
        
        # Create word cloud visualization
        words = [item[0] for item in word_counts]
        counts = [item[1] for item in word_counts]
        
        fig = px.bar(
            x=counts,
            y=words,
            orientation='h',
            color=counts,
            color_continuous_scale=GREEN_SEQUENTIAL,
            labels={'x': 'Frequency', 'y': 'Term'},
            title="Common Terms in Transaction Notes"
        )
        fig.update_layout(height=400, margin=dict(l=10, r=10, b=10, t=10))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No transaction notes available for analysis.")

# 5. Reports Tab
with tabs[4]:
    # Add logo in reports section
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        try:
            st.image("2.png", width=80)
        except:
            st.error("Logo not found. Please ensure '2.png' is in the same directory as this script.")
    
    st.header("Reports")
    
    st.markdown("""
    Generate and download comprehensive reports for your financial data.
    These reports are designed to provide detailed insights for stakeholders.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Standard Reports")
        
        if st.button("Generate Financial Summary", key="fin_summary"):
            with st.spinner("Generating financial summary..."):
                time.sleep(1)  # Simulate report generation
                
                report_content = f"""
                === Maple Leaf Restaurant Financial Analysis ===

                Report Date: {datetime.now().strftime('%Y-%m-%d')}
                Analysis Period: {df['Date'].min().strftime('%Y-%m-%d')} to {df['Date'].max().strftime('%Y-%m-%d')}

                == Key Metrics ==
                Total Transactions: {len(df)}
                Total Transaction Value: ${df['Amount'].sum():.2f}
                Average Transaction Amount: ${df['Amount'].mean():.2f}
                Anomalies Detected: {len(anomalies)} ({len(anomalies)/len(df)*100:.1f}%)

                == AI Commentary ==
                """
                
                for insight in commentary:
                    report_content += f"• {insight}\n"
                
                st.download_button(
                    "Download Financial Summary",
                    report_content,
                    file_name="financial_summary.txt",
                    mime="text/plain"
                )
        
        if st.button("Generate Anomaly Report", key="anomaly_report"):
            with st.spinner("Generating anomaly report..."):
                time.sleep(1)  # Simulate report generation
                
                if len(anomalies) > 0:
                    csv = anomalies.to_csv(index=False)
                    
                    st.download_button(
                        "Download Anomaly Report",
                        csv,
                        file_name="anomaly_transactions.csv",
                        mime="text/csv"
                    )
                else:
                    st.warning("No anomalies detected to include in report.")
    
    with col2:
        st.subheader("Custom Reports")
        
        report_type = st.selectbox(
            "Select Report Type",
            options=["Category Analysis", "Vendor Analysis", "Risk Assessment"]
        )
        
        include_charts = st.checkbox("Include visualizations", value=True)
        include_raw_data = st.checkbox("Include raw data", value=False)
        
        if st.button("Generate Custom Report", key="custom_report"):
            with st.spinner("Generating custom report..."):
                time.sleep(1.5)  # Simulate report generation
                
                st.success(f"{report_type} report generated successfully!")
                st.download_button(
                    "Download Custom Report",
                    f"This is a placeholder for the {report_type} report content.",
                    file_name=f"{report_type.lower().replace(' ', '_')}_report.txt",
                    mime="text/plain"
                )

# Footer with logo
st.markdown("---")
footer_col1, footer_col2, footer_col3 = st.columns([1, 3, 1])
with footer_col1:
    try:
        st.image("2.png", width=60)
    except:
        # Silently fail in footer to not show too many errors
        pass
    
with footer_col2:
    st.markdown(
        "<p style='text-align: center; color: gray;'>© 2023 Maple Leaf Restaurant | Powered by AI Financial Analytics</p>", 
        unsafe_allow_html=True
    )
