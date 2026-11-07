# RFM-L-DE — Segmentación Predictiva de Jugadores por Ciclo de Vida

Modelo K-Means que segmenta 461,400 jugadores activos en 4 clusters RFM sobre variables de 12 semanas. Complementado con LightGBM que predice quintiles de valor esperado dentro de cada cluster para priorización comercial.

**Estado:** En producción | **Schedule:** Lunes 08:00 UTC (03:00 Lima) | **Silhouette:** 0.42

---

## Resumen Ejecutivo

Segmentación que agrupa 461K jugadores en 4 clusters que representan etapas del ciclo de vida:

- **Cluster 1 - Alta Valor (45K, 9.8%):** Máximo gasto, frecuencia elevada, activos
- **Cluster 2 - Activos (120K, 26.1%):** Actividad regular, valor moderado
- **Cluster 3 - Dormidos (85K, 18.6%):** Inactivos, requieren reactivación
- **Cluster 4 - Nuevos (210K, 45.5%):** Muy recientes, bajo volumen

**Silhouette Score:** 0.42 (clusters bien separados). Dentro de cada cluster, LightGBM predice quintiles de valor esperado con **Spearman 0.41**, permitiendo priorizar acciones comerciales.

---

## Análisis Exploratorio de Datos (EDA)

### Distribución de Jugadores

| Cluster | Tamaño | Recency | Frequency | Monetary | Depositó | Retiró | Perfil |
|---------|--------|---------|-----------|----------|----------|--------|---------|
| **1 Alta Valor** | 45,230 (9.8%) | 5 días | 85 | S/ 12.5K | S/ 8.2K | S/ 7.1K | Máximo gasto, frecuencia alta, activos |
| **2 Activos** | 120,500 (26.1%) | 15 días | 45 | S/ 3.2K | S/ 2.1K | S/ 1.8K | Regulares, valor moderado |
| **3 Dormidos** | 85,670 (18.6%) | 45 días | 8 | S/ 450 | S/ 280 | S/ 200 | Inactivos, bajo valor |
| **4 Nuevos** | 210,000 (45.5%) | 2 días | 3 | S/ 120 | S/ 85 | S/ 30 | Recientes, onboarding |

**Insight:**
- Cluster 1: 5.4% de jugadores generan ~30% del volumen
- Cluster 4: Mitad de la base, pero value negligible inicialmente
- Oportunidad: Mover C2→C1 o C3→C2

### Análisis de Número Óptimo de Clusters

| K | Silhouette | Interpretabilidad | Nota |
|---|-----------|-------------------|------|
| K=2 | 0.38 | Muy alta | Demasiado genérico |
| K=3 | 0.42 | Alta | Competidor fuerte |
| **K=4** | **0.42** | **Excelente** | **ELEGIDO** - Máxima interpretabilidad |
| K=5 | 0.39 | Media | Empieza a degradar |
| K=6 | 0.35 | Baja | Clusters pequeños, ruido |

**Decisión:** K=4 mantiene Silhouette (0.42) igual a K=3 pero con interpretabilidad mucho mejor para acciones comerciales.

### Distribución de Valor Esperado (LightGBM Quintiles)

| Cluster | Q1 (Bajo) | Q2 | Q3 | Q4 | Q5 (Alto) | Focus |
|---------|-----------|-----|-----|-----|-----------|-------|
| Alta Valor | 12% | 28% | 35% | 18% | 7% | Retención VIP |
| Activos | 35% | 25% | 20% | 15% | 5% | Cross-sell |
| Dormidos | 60% | 25% | 10% | 4% | 1% | Reactivación |
| Nuevos | 70% | 20% | 8% | 1% | 1% | Onboarding |

**Insight:** Cluster 1 domina Q4-Q5 (alta renta). Cluster 4 concentrado en Q1 (bajo retorno inicial).

### Silhouette Score por K

![Análisis Clustering](./graficos_clustering_rfm.png)

Máximo en K=4, indicando:
- Clusters bien separados
- Solapamiento moderado (realista)
- Equilibrio interpretabilidad/cohesión

---

## Solución Implementada

### Variables RFM (6 totales) - Últimas 12 Semanas

| Variable | Rango | Interpretación |
|----------|-------|-----------------|
| Recency | 2-45 días | Cuánto falta para churn |
| Frequency | 3-85 apuestas | Compromiso/engagement |
| Monetary | S/ 120-12.5K | Volumen total |
| Deposit Frequency | 1-25 | Número de depósitos |
| Deposit Amount | S/ 85-8.2K | Inversión |
| Withdrawal Amount | S/ 30-7.1K | Retiros |

**Período:** Últimas 12 semanas. Solo jugadores con ≥1 apuesta (461K de 850K totales).

### K-Means K=4

```python
from sklearn.cluster import KMeans

kmeans = KMeans(
    n_clusters=4,
    random_state=42,
    n_init=10,
    init='k-means++',
    n_jobs=-1
)

labels = kmeans.fit_predict(X_scaled)  # StandardScaler
```

**Reentrenamiento:** Cada lunes, histórico de 52 semanas para tracking de movimiento.

### LightGBM Quintiles

```python
for cluster in [1, 2, 3, 4]:
    X_cluster = X[labels == cluster]
    y_cluster = quintiles[labels == cluster]
    
    model = LGBMClassifier(
        num_leaves=31,
        n_estimators=100,
        class_weight="balanced"
    )
    model.fit(X_cluster, y_cluster)
    predicciones[cluster] = model.predict(X_cluster)
```

**Métrica:** Spearman 0.41 (cluster agrega poder predictivo vs 0.21 sin cluster)

---

## Resultados

### Performance de Clustering

| Métrica | Valor | Interpretación |
|---------|-------|-----------------|
| Jugadores analizados | 461,400 | 100% base activa |
| Número de clusters | 4 | Óptimo por Silhouette |
| Silhouette Score | 0.42 | Buena separabilidad |
| Separabilidad | Buena | Clusters interpretables |
| Estabilidad | Alta | K=4 es robusto |

### Power Predictivo del Cluster

| Métrica | Sin Cluster | Con Cluster | Ganancia |
|---------|-------------|------------|----------|
| Spearman (quintil predicho) | 0.21 | 0.41 | +0.20 (+95%) |
| Precisión top 20% | 32% | 51% | +19 pp |

**Conclusión:** Cluster agrega 95% de poder predictivo.

---

## Aplicaciones Comerciales

### 1. Comunicaciones Segmentadas

- **C1:** VIP rewards, eventos exclusivos, límites altos
- **C2:** Bonos de frecuencia, referrals, cross-sell
- **C3:** Reactivación, bonos atractivos, reinicio
- **C4:** Onboarding, bonus bienvenida, tutoriales

### 2. Prioridades de Retención

- Focus preventivo en C1 (máximo impacto económico)
- Movimiento C2→C1 como métrica de crecimiento
- Reactivación C3→C2 como métrica de eficiencia

### 3. Alertas de Abandono

| Cluster | Umbral de Alerta | Acción |
|---------|-----------------|--------|
| C1 | Sin actividad 7 días | Contacto VIP prioritario |
| C2 | Sin actividad 14 días | Oferta de reactivación |
| C3 | Sin actividad 60 días | Esperado (dormidos) |
| C4 | Sin actividad 3 días | Onboarding intensivo |

---

## Limitaciones

1. **Período corto:** 12 semanas puede no capturar ciclos muy largos
2. **K fijo:** K=4 óptimo estadísticamente, no necesariamente óptimo comercialmente
3. **Poder predictivo moderado:** Spearman 0.41 (no perfecto)
4. **Autoexcluidos:** No excluye jugadores voluntariamente
5. **Actualización semanal:** Cambios lentos, asignación se recalcula solo lunes

---

## Cómo Ejecutarlo

### En Airflow

```bash
airflow dags trigger dag_rfm_semanal_v3
```

Cada lunes 08:00 UTC (03:00 Lima)

### Consultar Resultados

```sql
SELECT cluster, COUNT(*) as n, ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER(), 1) as pct
FROM ml_score_risk.rfm_lde_quintiles_semanal
WHERE run_date = CURRENT_DATE
GROUP BY cluster
ORDER BY cluster;
```

---

## Tablas Generadas

### `ml_score_risk.rfm_lde_quintiles_semanal`

Actualizada cada lunes. Usable directamente en campaigns:
```
player | cluster | recency | frequency | monetary | quintil | run_date
```

### `ml_score_risk.rfm_lde_historico`

Retiene 52 snapshots (1 año) para análisis de movimiento entre clusters.

---

## Próximos Pasos

- Validación comercial de representatividad
- A/B testing: campaigns por cluster vs genéricas
- KPI: movimiento entre clusters
- Incorporar datos Redshift (últimas 24h) para update más frecuente
