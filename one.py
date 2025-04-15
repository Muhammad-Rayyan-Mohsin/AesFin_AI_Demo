# This is a renamed copy of the original 1.py file to make it importable

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import os
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

# Data preprocessing
def preprocess_data(df):
    # Convert Date to datetime
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Extract month and year for time-based analysis
    df['Month'] = df['Date'].dt.month
    df['Year'] = df['Date'].dt.year
    
    return df

# a. Anomaly Detection
def detect_anomalies(df, contamination=0.05):
    """
    Detect anomalies using Isolation Forest algorithm
    """
    print("\n1. 💡 Anomaly Detection")
    
    # Select numerical features for anomaly detection
    features = df[['Amount', 'Risk Score']].copy()
    
    # Scale the features
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)
    
    # Train Isolation Forest
    model = IsolationForest(contamination=contamination, random_state=42)
    df['AI_Anomaly_Score'] = model.fit_predict(features_scaled)
    
    # Convert prediction to binary flag (1 for normal, -1 for anomaly)
    df['AI_Anomaly_Flag'] = np.where(df['AI_Anomaly_Score'] == -1, 1, 0)
    
    # Compare with existing Anomaly Flag
    agreement = (df['AI_Anomaly_Flag'] == df['Anomaly Flag']).mean() * 100
    print(f"Agreement between AI and existing anomaly detection: {agreement:.2f}%")
    
    # Identify transactions flagged as anomalies
    anomalies = df[df['AI_Anomaly_Flag'] == 1]
    print(f"Detected {len(anomalies)} anomalous transactions")
    
    return df, anomalies

# b. Risk Scoring
def risk_scoring(df):
    """
    Assign risk levels based on Risk Score
    """
    print("\n2. 📊 Risk Scoring")
    
    # Define risk level categories
    df['Risk Level'] = pd.cut(
        df['Risk Score'],
        bins=[0, 30, 70, 100],
        labels=['Low', 'Medium', 'High']
    )
    
    # Count transactions by risk level
    risk_counts = df['Risk Level'].value_counts()
    print("Transactions by risk level:")
    print(risk_counts)
    
    return df

# c. Variance Analysis
def variance_analysis(df):
    """
    Analyze variances in transaction amounts over time
    """
    print("\n3. 📈 Variance Analysis")
    
    # Group by month and category
    monthly_category = df.groupby([df['Date'].dt.to_period('M'), 'Category'])['Amount'].sum().unstack()
    
    # Calculate month-over-month variance
    mom_variance = monthly_category.pct_change() * 100
    
    print("Month-over-month variance by category (%):")
    print(mom_variance.tail(3))
    
    return monthly_category, mom_variance

# d. AI-Generated Commentary
def generate_commentary(df, monthly_data, variances):
    """
    Generate insights based on financial data (placeholder for Qwen 0.5B)
    """
    print("\n4. 🧠 AI-Generated Commentary")
    
    # This would use Qwen 0.5B in a full implementation
    commentary = []
    
    # Overall financial health
    total_transactions = len(df)
    total_amount = df['Amount'].sum()
    avg_amount = df['Amount'].mean()
    
    commentary.append(f"Analysis of {total_transactions} transactions totaling ${total_amount:.2f}")
    commentary.append(f"Average transaction amount: ${avg_amount:.2f}")
    
    # Risk assessment
    high_risk = df[df['Risk Level'] == 'High']
    high_risk_amount = high_risk['Amount'].sum()
    high_risk_pct = (high_risk_amount / total_amount) * 100
    
    commentary.append(f"{len(high_risk)} high-risk transactions ({high_risk_pct:.1f}% of total value)")
    
    # Print the commentary
    print("AI-Generated Insights:")
    for insight in commentary:
        print(f" - {insight}")
    
    return commentary

# e. Document Intelligence (NLP)
def document_intelligence(df):
    """
    NLP-based document analysis focusing on Notes field
    """
    print("\n5. 📁 Document Intelligence (NLP)")
    
    # Analyze the Notes field where available
    notes_count = df['Notes'].notna().sum()
    print(f"Found {notes_count} transactions with notes")
    
    # Example of simple NLP analysis on notes
    if notes_count > 0:
        # Extract common keywords or themes
        common_words = []
        for note in df['Notes'].dropna():
            words = note.lower().split()
            common_words.extend([w for w in words if len(w) > 3])
        
        # Count word frequencies
        word_counts = Counter(common_words).most_common(5)
        
        print("Most common terms in notes:")
        for word, count in word_counts:
            print(f" - {word}: {count} occurrences")
    
    return df

# f. Real-Time Dashboards
def create_visualizations(df, monthly_data):
    """
    Create visualizations for dashboard
    """
    print("\n6. 📊 Real-Time Dashboards")
    print("Generating visualizations for dashboard...")
    
    # Create a directory for saving visualizations
    if not os.path.exists('visualizations'):
        os.makedirs('visualizations')
    
    # Transactions by category
    category_amounts = df.groupby('Category')['Amount'].sum().sort_values(ascending=False)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=category_amounts.values, y=category_amounts.index)
    plt.title('Transaction Amount by Category')
    plt.tight_layout()
    plt.savefig('visualizations/category_amounts.png')
    
    # Risk score distribution
    plt.figure(figsize=(10, 6))
    sns.histplot(df['Risk Score'], bins=20, kde=True)
    plt.title('Distribution of Risk Scores')
    plt.savefig('visualizations/risk_distribution.png')
    
    print("Saved visualizations to the 'visualizations' directory")
    
    return True

# g. Reporting
def generate_reports(df, anomalies, commentary, monthly_data, variances):
    """
    Generate financial reports
    """
    print("\n7. 📤 Reporting")
    
    # Create a directory for reports
    if not os.path.exists('reports'):
        os.makedirs('reports')
    
    # Summary Report
    with open('reports/financial_summary.txt', 'w') as f:
        f.write("=== Maple Leaf Restaurant Financial Analysis ===\n\n")
        f.write(f"Report Date: {datetime.now().strftime('%Y-%m-%d')}\n")
        f.write(f"Analysis Period: {df['Date'].min().strftime('%Y-%m-%d')} to {df['Date'].max().strftime('%Y-%m-%d')}\n\n")
        
        f.write("== Key Metrics ==\n")
        f.write(f"Total Transactions: {len(df)}\n")
        f.write(f"Total Transaction Value: ${df['Amount'].sum():.2f}\n")
        f.write(f"Average Transaction Amount: ${df['Amount'].mean():.2f}\n")
        f.write(f"Anomalies Detected: {len(anomalies)} ({len(anomalies)/len(df)*100:.1f}%)\n\n")
        
        f.write("== AI Commentary ==\n")
        for insight in commentary:
            f.write(f"• {insight}\n")
    
    # Anomaly Report
    if len(anomalies) > 0:
        anomalies.to_csv('reports/anomaly_transactions.csv', index=False)
    
    print(f"Generated reports in the 'reports' directory")
    
    return True

# Main execution
def main():
    print("=== Maple Leaf Restaurant Financial Analysis System ===")
    
    # Read the data
    df = pd.read_csv('maple_leaf_restaurant_financial_data.csv')
    print("Data Overview:")
    df.info()
    
    # Preprocess the data
    df = preprocess_data(df)
    
    # Execute analysis pipeline
    df, anomalies = detect_anomalies(df)
    df = risk_scoring(df)
    monthly_data, variances = variance_analysis(df)
    commentary = generate_commentary(df, monthly_data, variances)
    df = document_intelligence(df)
    create_visualizations(df, monthly_data)
    generate_reports(df, anomalies, commentary, monthly_data, variances)
    
    print("\nAnalysis completed successfully!")

if __name__ == "__main__":
    main()