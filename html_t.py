import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Genel stil ayarları
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("Set2")

# Veri doğrulama ve temizleme
def validate_data(df):
    if df.isnull().values.any():
        print("Uyarı: Veri setinde eksik değerler var! Eksik değerler dolduruluyor...")
        df = df.fillna(df.mean())
    return df

# Isı haritası
def create_heatmap(data, title):
    plt.figure(figsize=(10, 8))
    sns.heatmap(data.corr(), annot=True, cmap="coolwarm", fmt=".2f", cbar=True)
    plt.title(f"{title} - Correlation Heatmap", fontsize=16)
    plt.tight_layout()
    plt.close()

# Swarmplot
def create_swarmplot(data, title):
    plt.figure(figsize=(10, 8))
    sns.swarmplot(data=data, palette="husl", size=5)
    plt.title(f"{title} - Swarmplot", fontsize=16)
    plt.ylabel("Completion Time (ms)", fontsize=14)
    plt.tight_layout()
    plt.close()

# Çizgi grafiği
def create_lineplot(data, title):
    plt.figure(figsize=(10, 8))
    for col in data.columns:
        plt.plot(data.index, data[col], marker="o", label=col)
    plt.title(f"{title} - Line Plot", fontsize=16)
    plt.xlabel("Samples", fontsize=14)
    plt.ylabel("Completion Time (ms)", fontsize=14)
    plt.legend(loc="best", fontsize=12)
    plt.tight_layout()
    plt.close()

# En hızlı iki kütüphaneyi seçme
def select_top_two_libraries(data):
    mean_times = data.mean().sort_values()
    return mean_times.head(2).index.tolist()

# HTML Dosyasına görselleştirmeleri yerleştirme
def create_html_visualization(files):
    html_content = "<html><head><title>Visualizations</title></head><body>"
    html_content += "<h1>Visualizations</h1>"

    for file, title, _ in files:
        # Veriyi yükle ve doğrula
        df = pd.read_csv(file, sep='\t')
        data = df.iloc[:, 1:]
        data = validate_data(data)

        # Görselleştirmeleri oluştur (görselleri kaydetmeden doğrudan HTML içeriğiyle göstermek)
        html_content += f"<h2>{title} Visualizations</h2>"
        
        # Isı haritası
        html_content += f"<h3>Correlation Heatmap</h3>"
        html_content += f"<pre><code>{create_heatmap(data, title)}</code></pre>"

        # Swarmplot
        html_content += f"<h3>Swarmplot</h3>"
        html_content += f"<pre><code>{create_swarmplot(data, title)}</code></pre>"

        # Çizgi grafiği
        html_content += f"<h3>Line Plot</h3>"
        html_content += f"<pre><code>{create_lineplot(data, title)}</code></pre>"

        # En hızlı 2 kütüphane için bar plot
        top_two = select_top_two_libraries(data)
        filtered_data = data[top_two]
        
        html_content += f"<h3>Top 2 Bar Plot</h3>"
        html_content += f"<pre><code>{create_barplot(filtered_data, title)}</code></pre>"

    html_content += "</body></html>"

    # HTML dosyasını kaydet
    with open("visualizations.html", "w") as f:
        f.write(html_content)

    print("HTML dosyası başarıyla oluşturuldu!")

# Dosya bilgileri
files = [
    ('temp/setup_function_completion.tsv', 'Setup Function Completion', 'setup_performance'),
    ('temp/global_completion.tsv', 'Global Completion', 'global_performance'),
    ('temp/path_completion.tsv', 'Path Completion', 'path_performance')
]

# HTML dosyasını oluştur
create_html_visualization(files)