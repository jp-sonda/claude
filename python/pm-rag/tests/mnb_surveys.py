import marimo

__generated_with = "0.17.2"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Veja [Marimo](https://realpython.com/marimo-notebook/)""")
    return


@app.cell(hide_code=True)
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ---

    ---

    ## 📌 **Recomendações para Leitura**

    **Início**: Survey ACM 2024 (Zamanzadeh et al.)
    **Fundamentos**: TS2Vec (AAAI 2022)
    **Transformers**: Anomaly Transformer (ICLR 2022)
    **Industrial**: Embedding Models for Industry 5.0 (2025)
    **Prática**: GitHub benchmark repository

    Essas referências fornecem uma base sólida sobre o estado da arte em detecção de anomalias em séries temporais usando embeddings! 🎯

    Veja Detalhes abaixo:

    ---

    ## 📚 Referências de Trabalhos Científicos Recentes

    Aqui estão as principais referências sobre detecção de anomalias em séries temporais usando embeddings e deep learning, com alta relevância e citações:

    ---

    ### 🔥 **Surveys e Reviews Altamente Citados (2023-2025)**

    #### 1. **Deep Learning for Time Series Anomaly Detection: A Survey**
    - **Autores**: Zamanzadeh Darban, Z., Webb, G. I., Pan, S., Aggarwal, C. C., & Salehi, M.
    - **Publicação**: ACM Computing Surveys, 2024
    - **DOI**: 10.1145/3691338
    - **Link**: https://dl.acm.org/doi/10.1145/3691338
    - **Citações**: Survey mais completo e recente (2024)
    - **Relevância**: Revisão abrangente do estado da arte até 2024, incluindo TimesNet, Anomaly Transformer, e métodos baseados em embeddings

    #### 2. **A Survey of Deep Anomaly Detection in Multivariate Time Series**
    - **Autores**: Multiple authors
    - **Publicação**: Sensors (MDPI), Janeiro 2025
    - **Link**: https://www.mdpi.com/1424-8220/25/1/190
    - **Relevância**: Foco em séries temporais multivariadas (MTSAD) com aplicações em monitoramento financeiro e detecção de falhas em equipamentos industriais

    ---

    ### 🎯 **Modelos Fundamentais de Embeddings**

    #### 3. **TS2Vec: Towards Universal Representation of Time Series**
    - **Autores**: Yue, Z., Wang, Y., Duan, J., Yang, T., Huang, C., Tong, Y., & Xu, B.
    - **Publicação**: AAAI Conference on Artificial Intelligence, 2022
    - **DOI**: 10.1609/aaai.v36i8.20881
    - **Link**: https://ojs.aaai.org/index.php/AAAI/article/view/20881
    - **GitHub**: https://github.com/zhihanyue/ts2vec
    - **Citações**: 500+ citações
    - **Relevância**: Framework universal para aprendizado de representações em nível arbitrário de granularidade, com aplicação em detecção de anomalias não supervisionada estabelecendo SOTA

    #### 4. **TimesNet: Temporal 2D-Variation Modeling**
    - **Autores**: Wu, H., Hu, T., Liu, Y., Zhou, H., Wang, J., & Long, M.
    - **Publicação**: ICLR 2023
    - **Relevância**: Modelo versátil que transforma séries temporais 1D em tensores 2D para capturar padrões temporais complexos, excelente em forecasting, classificação e detecção de anomalias

    ---

    ### 🤖 **Transformers para Detecção de Anomalias**

    #### 5. **Anomaly Transformer: Time Series Anomaly Detection with Association Discrepancy**
    - **Autores**: Xu, J., et al.
    - **Publicação**: ICLR 2022 (Oral)
    - **arXiv**: 2110.02642
    - **Link**: https://arxiv.org/abs/2110.02642
    - **Citações**: 300+ citações
    - **Relevância**: Introduz mecanismo de Anomaly-Attention baseado em discrepância de associação, explorando que anomalias concentram associações em pontos adjacentes

    #### 6. **AnomalyBERT: Self-Supervised Transformer for Time Series Anomaly Detection**
    - **Autores**: Jeong, Y., et al.
    - **Publicação**: arXiv 2023
    - **arXiv**: 2305.04468
    - **Link**: https://arxiv.org/abs/2305.04468
    - **Relevância**: Abordagem auto-supervisionada com esquema de degradação de dados, define 4 tipos de outliers sintéticos e usa Transformer para reconhecer contexto temporal

    ---

    ### 🔬 **Métodos Contrastivos e Autoencoders**

    #### 7. **DCAD: Unsupervised Anomaly Detection by Densely Contrastive Learning**
    - **Publicação**: Neural Networks, 2023
    - **Link**: https://pmc.ncbi.nlm.nih.gov/articles/PMC11164417/
    - **Relevância**: Método de aprendizado contrastivo denso que contrasta séries temporais completas com suas sub-sequências em espaço latente, usando CNN com position embedding

    #### 8. **TFMAE: Temporal-Frequency Masked Autoencoders**
    - **Publicação**: ICDE 2024
    - **Relevância**: Autoencoder mascarado dual com estratégias de mascaramento temporal (window-based) e frequencial (amplitude-based), mitiga impacto de distribution shifts

    ---

    ### 🏭 **Aplicações Industriais e IoT**

    #### 9. **Embedding Models for Multivariate Time Series Anomaly Detection in Industry 5.0**
    - **Publicação**: Data Science and Engineering, 2025
    - **Link**: https://link.springer.com/article/10.1007/s41019-025-00295-w
    - **Relevância**: Introduz embeddings baseados em Time2Vec e Discrete Wavelet Transforms para Industry 5.0, representando séries multivariadas como vetores

    #### 10. **LTG: Long Short-Term Memory, Temporal Convolution and Graph Convolution**
    - **Publicação**: Journal of King Saud University, 2025
    - **Link**: https://link.springer.com/article/10.1007/s44443-025-00024-3
    - **Relevância**: Abordagem baseada em spatial-temporal graph learning para detecção de anomalias em sistemas Cyber-Physical

    ---

    ### 📊 **Benchmarks e Datasets**

    #### 11. **Time-Series Anomaly Detection Comprehensive Benchmark**
    - **Autores**: Zamanzadeh et al.
    - **GitHub**: https://github.com/zamanzadeh/ts-anomaly-benchmark
    - **Relevância**: Lista abrangente de métodos clássicos e estado-da-arte, datasets categorizados por domínio com hyperlinks para acesso fácil

    ---

    ### 🔄 **Métodos Híbridos e GNN**

    #### 12. **Deep Learning for Anomaly Detection in Multivariate Time Series**
    - **Autores**: Multiple authors
    - **Publicação**: Information Fusion, 2022
    - **Link**: https://www.sciencedirect.com/science/article/abs/pii/S1566253522001774
    - **Relevância**: Graph Neural Networks (GNNs) identificam anomalias capturando conexões temporais e interdependências, leveraging estrutura de grafo subjacente

    #### 13. **OmniAnomaly**
    - **Relevância**: Primeiro algoritmo MTSAD capaz de lidar com dependências temporais explícitas entre variáveis aleatórias, usando redes neurais recorrentes estocásticas

    ---

    ### 📖 **Livros e Capítulos**

    #### 14. **Anomaly Detection in Time Series: Current Focus and Future Challenges**
    - **Publicação**: IntechOpen, 2023
    - **Link**: https://www.intechopen.com/chapters/87583
    - **Relevância**: Visão geral de modelos de ponta, vantagens e desvantagens, focos atuais de pesquisa em dados de alta dimensionalidade e streams em tempo real

    ---

    ## 🎯 **Papers Específicos para RAG com Séries Temporais**

    Embora não exista um termo exato "Query Embedding de Série Temporal Anormal" na literatura, os conceitos estão distribuídos em:

    1. **Time Series Representation Learning** (TS2Vec, Time2Vec)
    2. **Contrastive Learning for Anomaly Detection** (DCAD, CARLA)
    3. **Embedding-based Similarity Search** (dynamic graph embeddings)
    4. **Reconstruction vs Forecasting-based Detection**

    ---

    ## 💡 **Tendências Atuais (2024-2025)**

    1. **Transformers** continuam dominantes mas com críticas sobre eficiência
    2. **Embedding methods** (TS2Vec style) estão crescendo
    3. **Hybrid approaches** (Transformer + GNN) ganham destaque
    4. **Self-supervised learning** é o paradigma predominante
    5. **Industry 5.0 applications** aumentando rapidamente
    """
    )
    return


if __name__ == "__main__":
    app.run()
