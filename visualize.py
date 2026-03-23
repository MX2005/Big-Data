import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv('data_preprocessed.csv')

plt.figure(figsize=(10, 6))
sns.histplot(data=df, x='Hour', bins=24, kde=True, color='skyblue')
plt.title('Distribution of Crimes by Hour')
plt.xlabel('Hour of the Day')
plt.ylabel('Frequency')
plt.grid(axis='y', alpha=0.3)
plt.show()

cols_to_plot = ['Hour', 'Month', 'District', 'Arrest']
sns.pairplot(df[cols_to_plot].sample(min(1000, len(df))), hue='Arrest', diag_kind='kde')
plt.suptitle('Pairplot of Crime Features', y=1.02)
plt.show()

plt.figure(figsize=(12, 8))
numeric_cols = ['Arrest', 'Domestic', 'District', 'Ward', 'Community Area', 'Month', 'DayOfWeek', 'Hour']
corr_matrix = df[numeric_cols].corr()

sns.heatmap(corr_matrix, annot=True, cmap='RdBu', fmt='.2f', center=0)
plt.title('Correlation Matrix of Crime Features')
plt.show()