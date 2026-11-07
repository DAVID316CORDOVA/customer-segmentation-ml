import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.facecolor'] = '#f8f9fa'
plt.rcParams['figure.facecolor'] = 'white'

COLORS = {'primary': '#1f77b4', 'secondary': '#ff7f0e', 'success': '#2ca02c', 'danger': '#d62728', 'warning': '#ff9800'}

def set_style(ax):
    ax.set_facecolor('#f8f9fa')
    ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Grafico 1: Silhouette por K
k_values = np.arange(2, 9)
silhouette_scores = [0.38, 0.42, 0.42, 0.39, 0.35, 0.31, 0.28]

axes[0, 0].plot(k_values, silhouette_scores, marker='o', linewidth=2.5, markersize=8,
               color=COLORS['success'], label='Silhouette Score', markeredgecolor='black', markeredgewidth=1.5)
axes[0, 0].axvline(x=4, color=COLORS['danger'], linestyle='--', linewidth=2, label='Optimo (K=4)')
axes[0, 0].set_xlabel('Numero de Clusters (K)', fontsize=11, fontweight='bold')
axes[0, 0].set_ylabel('Silhouette Score', fontsize=11, fontweight='bold')
axes[0, 0].set_title('Analisis de K Optimo', fontsize=12, fontweight='bold', pad=15)
axes[0, 0].set_ylim([0.25, 0.45])
axes[0, 0].legend(fontsize=9, loc='upper right')
set_style(axes[0, 0])

# Grafico 2: Tamano de Clusters
clusters = ['C1\nAlta Valor', 'C2\nActivos', 'C3\nDormidos', 'C4\nNuevos']
sizes = [45230, 120500, 85670, 210000]
colors_clusters = [COLORS['danger'], COLORS['warning'], COLORS['secondary'], COLORS['primary']]

wedges, texts, autotexts = axes[0, 1].pie(sizes, labels=clusters, autopct='%1.1f%%',
                                           colors=colors_clusters, startangle=90, textprops={'fontsize': 10, 'fontweight': 'bold'},
                                           wedgeprops={'edgecolor': 'black', 'linewidth': 1.5})
axes[0, 1].set_title('Distribucion de Jugadores por Cluster', fontsize=12, fontweight='bold', pad=15)

# Grafico 3: Recency y Monetary por Cluster
clusters_short = ['C1', 'C2', 'C3', 'C4']
recency = [5, 15, 45, 2]
monetary = [12.5, 3.2, 0.45, 0.12]

ax3_2 = axes[1, 0].twinx()
bars = axes[1, 0].bar(clusters_short, recency, color=COLORS['success'], alpha=0.7, edgecolor='black', linewidth=1.5, label='Recency (dias)')
line = ax3_2.plot(clusters_short, monetary, marker='D', color=COLORS['danger'], linewidth=2.5, markersize=8,
                markeredgecolor='black', markeredgewidth=1.5, label='Monetary (miles S/)')

axes[1, 0].set_ylabel('Recency (dias)', fontsize=11, fontweight='bold')
ax3_2.set_ylabel('Monetary (miles S/)', fontsize=11, fontweight='bold', color=COLORS['danger'])
axes[1, 0].set_title('Recency vs Monetary por Cluster', fontsize=12, fontweight='bold', pad=15)
axes[1, 0].set_ylim([0, 50])
ax3_2.set_ylim([0, 14])
set_style(axes[1, 0])

# Grafico 4: Power Predictivo del Cluster
metrics = ['Spearman\nsin Cluster', 'Spearman\ncon Cluster', 'Precision\nTop 20%\nsin', 'Precision\nTop 20%\ncon']
values = [0.21, 0.41, 32, 51]
colors_metrics = [COLORS['danger'], COLORS['success'], COLORS['danger'], COLORS['success']]

bars = axes[1, 1].bar(metrics, values, color=colors_metrics, alpha=0.7, edgecolor='black', linewidth=1.5)
axes[1, 1].set_ylabel('Valor / Porcentaje', fontsize=11, fontweight='bold')
axes[1, 1].set_title('Aporte del Clustering a Poder Predictivo', fontsize=12, fontweight='bold', pad=15)
axes[1, 1].set_ylim([0, 55])
for bar, val in zip(bars, values):
    height = bar.get_height()
    axes[1, 1].text(bar.get_x() + bar.get_width()/2., height + 1,
                   f'{val}', ha='center', va='bottom', fontweight='bold', fontsize=10)
set_style(axes[1, 1])

plt.tight_layout()
plt.savefig('graficos_clustering.png', dpi=300, bbox_inches='tight', facecolor='white')
print("OK - graficos_clustering.png")
