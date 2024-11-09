import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("Set2")

def validate_data(df):
   if df.isnull().values.any():
       print("Uyarı: Veri setinde eksik değerler var! Eksik değerler dolduruluyor...")
       df = df.fillna(df.mean())
   return df

def create_performance_visualization(file, title):
   # Performance verilerini yükle
   performance_df = pd.read_csv(file, sep='\t', names=['Library', 'Duration'])
   performance_df.set_index('Library', inplace=True)
   
   # Ana görselleştirme
   fig, axes = plt.subplots(2, 2, figsize=(14, 12))
   fig.suptitle(f"{title} - Performance Visualizations", fontsize=16, fontweight='bold')

   # Bar plot
   performance_df.plot(kind='bar', ax=axes[0, 0], legend=False)
   axes[0, 0].set_title('Library Performance Comparison')
   axes[0, 0].set_xlabel('Libraries')
   axes[0, 0].set_ylabel('Duration (seconds)')
   plt.setp(axes[0, 0].get_xticklabels(), rotation=45, ha='right')

   # Pie chart
   axes[0, 1].pie(performance_df['Duration'], labels=performance_df.index, autopct='%1.1f%%')
   axes[0, 1].set_title('Performance Distribution')

   # Box plot
   sns.boxplot(x=performance_df.index, y=performance_df['Duration'], ax=axes[1, 0])
   axes[1, 0].set_title('Performance Box Plot')
   plt.setp(axes[1, 0].get_xticklabels(), rotation=45, ha='right')

   # Horizontal bar plot
   performance_df.sort_values('Duration').plot(kind='barh', ax=axes[1, 1], legend=False)
   axes[1, 1].set_title('Sorted Library Performance')
   axes[1, 1].set_xlabel('Duration (seconds)')

   plt.tight_layout(rect=[0, 0.03, 1, 0.95])
   plt.savefig(f"temp/{title}_performance_analysis.png", dpi=300, bbox_inches="tight")
   plt.close()

   # En hızlı iki kütüphaneyi seç
   top_two = performance_df['Duration'].nsmallest(2).index.tolist()
   print(f"{title} için en hızlı 2 kütüphane: {top_two}")

# Dosya bilgileri
files = [
   ('temp/performance_results.tsv', 'Performance Results'),
   ('temp/setup_function_completion.tsv', 'Setup Function Completion'),
   ('temp/global_completion.tsv', 'Global Completion'),
   ('temp/path_completion.tsv', 'Path Completion')
]

# Tümleşik görselleştirmeyi çalıştır
for file, title in files:
   try:
       create_performance_visualization(file, title)
   except Exception as e:
       print(f"{file} için hata: {e}")

print("Tüm görselleştirmeler tamamlandı!")