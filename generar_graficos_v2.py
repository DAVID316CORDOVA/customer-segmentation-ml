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

fig = plt.figure(figsize=(18, 12))
gs = fig.add_gridspec(3, 3, hspace=0.35, wspace=0.3)

# Fila 1
ax1 = fig.add_subplot(gs[0, 0])
k_values = np.arange(2, 9)
silhouette = [0.38, 0.42, 0.42, 0.39, 0.35, 0.31, 0.28]
ax1.plot(k_values, silhouette, marker='o', linewidth=2.5, markersize=8, color=COLORS['success'], markeredgecolor='black', markeredgewidth=1.5)
ax1.axvline(x=4, color=COLORS['danger'], linestyle='--', linewidth=2, label='Optimo (K=4)')
ax1.set_xlabel('Numero de Clusters (K)', fontsize=10, fontweight='bold')
ax1.set_ylabel('Silhouette Score', fontsize=10, fontweight='bold')
ax1.set_title('Analisis K Optimo', fontsize=11, fontweight='bold')
ax1.set_ylim([0.25, 0.45])
ax1.legend(fontsize=8)
set_style(ax1)

ax2 = fig.add_subplot(gs[0, 1])
clusters = ['C1\nAlta Valor', 'C2\nActivos', 'C3\nDormidos', 'C4\nNuevos']
sizes = [45230, 120500, 85670, 210000]
percentages = [9.8, 26.1, 18.6, 45.5]
colors_clusters = [COLORS['danger'], COLORS['warning'], COLORS['secondary'], COLORS['primary']]
wedges, texts, autotexts = ax2.pie(sizes, labels=clusters, autopct=lambda pct: f'{pct:.1f}%\n({int(pct/100.*sum(sizes))//1000}K)',
                                     colors=colors_clusters, startangle=90,
                                     textprops={'fontsize': 8, 'fontweight': 'bold'},
                                     wedgeprops={'edgecolor': 'black', 'linewidth': 1})
ax2.set_title('Distribucion de Jugadores (461K)', fontsize=11, fontweight='bold')

ax3 = fig.add_subplot(gs[0, 2])
cluster_names = ['C1', 'C2', 'C3', 'C4']
recency = [5, 15, 45, 2]
monetary = [12.5, 3.2, 0.45, 0.12]
ax3_twin = ax3.twinx()
ax3.bar(cluster_names, recency, color=COLORS['success'], alpha=0.7, edgecolor='black', linewidth=1.5, label='Recency (dias)')
ax3_twin.plot(cluster_names, monetary, marker='D', color=COLORS['danger'], linewidth=2.5, markersize=8, markeredgecolor='black', markeredgewidth=1.5, label='Monetary (k S/)')
ax3.set_ylabel('Recency (dias)', fontsize=10, fontweight='bold')
ax3_twin.set_ylabel('Monetary (miles S/)', fontsize=10, fontweight='bold')
ax3.set_title('RFM por Cluster', fontsize=11, fontweight='bold')
set_style(ax3)

# Fila 2
ax4 = fig.add_subplot(gs[1, 0])
features_rfm = ['Recency', 'Frequency', 'Monetary', 'Dep Freq', 'Dep Amt', 'Ret Amt']
importance_rfm = [20, 25, 22, 15, 12, 6]
colors_feat = [COLORS['success'], COLORS['primary'], COLORS['warning'], COLORS['danger'], COLORS['secondary'], '#999999']
bars = ax4.barh(features_rfm, importance_rfm, color=colors_feat, edgecolor='black', linewidth=1)
ax4.set_xlabel('Importancia (%)', fontsize=10, fontweight='bold')
ax4.set_title('Feature Importance (6 variables)', fontsize=11, fontweight='bold')
ax4.set_xlim([0, 30])
for i, (feat, imp) in enumerate(zip(features_rfm, importance_rfm)):
    ax4.text(imp + 0.5, i, f'{imp}%', va='center', fontweight='bold', fontsize=8)
set_style(ax4)

ax5 = fig.add_subplot(gs[1, 1])
quintiles = ['Q1', 'Q2', 'Q3', 'Q4', 'Q5']
c1_quintil = [12, 28, 35, 18, 7]
c4_quintil = [70, 20, 8, 1, 1]
x = np.arange(len(quintiles))
width = 0.35
ax5.bar(x - width/2, c1_quintil, width, label='C1 Alta Valor', color=COLORS['danger'], edgecolor='black', linewidth=1)
ax5.bar(x + width/2, c4_quintil, width, label='C4 Nuevos', color=COLORS['primary'], edgecolor='black', linewidth=1)
ax5.set_ylabel('Distribucion (%)', fontsize=10, fontweight='bold')
ax5.set_title('Quintiles LightGBM', fontsize=11, fontweight='bold')
ax5.set_xticks(x)
ax5.set_xticklabels(quintiles)
ax5.set_ylim([0, 75])
ax5.legend(fontsize=8)
set_style(ax5)

ax6 = fig.add_subplot(gs[1, 2])
metrics = ['Spearman\nsin Cluster', 'Spearman\ncon Cluster', 'Precision\nTop 20%\nsin', 'Precision\nTop 20%\ncon']
values = [0.21, 0.41, 32, 51]
colors_metrics = [COLORS['danger'], COLORS['success'], COLORS['danger'], COLORS['success']]
bars = ax6.bar(metrics, values, color=colors_metrics, alpha=0.7, edgecolor='black', linewidth=1.5)
ax6.set_ylabel('Valor / Porcentaje', fontsize=10, fontweight='bold')
ax6.set_title('Aporte del Clustering (+95%)', fontsize=11, fontweight='bold')
ax6.set_ylim([0, 55])
for bar, val in zip(bars, values):
    height = bar.get_height()
    ax6.text(bar.get_x() + bar.get_width()/2., height + 1, f'{val}', ha='center', va='bottom', fontweight='bold', fontsize=9)
set_style(ax6)

# Fila 3
ax7 = fig.add_subplot(gs[2, :2])
ax7.axis('off')
arch_text = '''K-MEANS + LIGHTGBM: Segmentacion RFM

Periodo: Ultimas 12 semanas
Base: 461K jugadores activos (≥1 apuesta de 850K)
Variables: 6 RFM (Recency, Frequency, Monetary, Dep/Ret)

K-Means Configuracion:
  n_clusters: 4 (K=4 optimo por Silhouette=0.42)
  init: k-means++
  random_state: 42
  Scaling: StandardScaler

LightGBM por Cluster:
  num_leaves: 31
  n_estimators: 100
  class_weight: balanced
  Prediccion: Quintiles (Q1-Q5) dentro cada cluster

Reentrenamiento: Cada lunes, historico 52 semanas
Poder Predictivo: Spearman 0.41 (vs 0.21 sin cluster = +95%)
'''
ax7.text(0.05, 0.95, arch_text, transform=ax7.transAxes, fontsize=9, verticalalignment='top',
        fontfamily='monospace', bbox=dict(boxstyle='round', facecolor='#f0f0f0', alpha=0.8, edgecolor='black'))

ax8 = fig.add_subplot(gs[2, 2])
ax8.axis('off')
results_text = '''RESULTADOS PRODUCCION

Jugadores: 461,400
Clusters: 4 (Ciclo de vida)
Silhouette: 0.42

C1 Alta Valor:
  45K (9.8%), Rec 5d, Freq 85, Mon 12.5K
  VIP rewards, exclusivos, limites altos

C2 Activos:
  120K (26.1%), Rec 15d, Freq 45, Mon 3.2K
  Bonos, cross-sell, referrals

C3 Dormidos:
  85K (18.6%), Rec 45d, Freq 8, Mon 450
  Reactivacion, bonos atractivos

C4 Nuevos:
  210K (45.5%), Rec 2d, Freq 3, Mon 120
  Onboarding, bonus bienvenida

Schedule: Lunes 08:00 UTC
Tabla: rfm_lde_quintiles_semanal
Historico: 52 snapshots (1 año)
'''
ax8.text(0.05, 0.95, results_text, transform=ax8.transAxes, fontsize=9, verticalalignment='top',
        fontfamily='monospace', bbox=dict(boxstyle='round', facecolor='#f0f0f0', alpha=0.8, edgecolor='black'))

plt.suptitle('CLUSTERING RFM: K-Means K=4 + LightGBM Quintiles + Ciclo de Vida',
            fontsize=14, fontweight='bold', y=0.995)

plt.savefig('graficos_clustering_v2.png', dpi=300, bbox_inches='tight', facecolor='white')
print("OK - graficos_clustering_v2.png")
