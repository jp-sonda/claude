sap_pm_rag_data_table = """
CREATE TABLE sap_pm_rag_data (
    id                  SERIAL PRIMARY KEY,
    sap_order_id        VARCHAR(12),
    functional_location VARCHAR(30),
    equipment_number    VARCHAR(18),
    order_type          VARCHAR(4),
    maintenance_text    TEXT,
    chunk_id            INTEGER,
    embedding           VECTOR(512), -- Substituir 512 pela dimensão do seu modelo Ollama
    creation_date       DATE
);
"""

generate_random_embedding_function = """
-- Função SQL auxiliar para gerar um array de 512 dimensões com números aleatórios (simulação do embedding)
-- NOTA: No seu ambiente real, esta coluna será preenchida pela função de embedding do pg.ai/Ollama.

CREATE OR REPLACE FUNCTION generate_random_embedding(dims INT)
RETURNS VECTOR AS $$
DECLARE
    emb DOUBLE PRECISION[];
BEGIN
    FOR i IN 1..dims LOOP
        emb[i] := random();
    END LOOP;
    RETURN emb::vector;
END;
$$ LANGUAGE plpgsql;
"""

##################################################################################
## 50 COMANDOS INSERT SIMULADOS
# ##################################################################################
insert_simulated_data: list[str] = [
    """
    -- Ordem 1: Falha Corretiva (Vibração alta - 1 Chunk)
    INSERT INTO sap_pm_rag_data (sap_order_id, functional_location, equipment_number, order_type, maintenance_text, chunk_id, embedding, creation_date) VALUES
    ('40001001', 'TURBINA_VAPOR_01', 'T-01-A', 'PM01',
        'Aumento de vibração detectado no mancal 3B. Causa-raiz identificada como desalinhamento do eixo devido a desgaste irregular do acoplamento. Ação: Parada emergencial, substituição do acoplamento flexível e alinhamento a laser. O pico de vibração (RMS) registrado foi de 12 mm/s, correlacionando-se com a elevação abrupta de temperatura na região do mancal. Medidas de pressão permaneceram estáveis. Peças de reposição utilizadas: Acoplamento H-201, Jogo de calços de precisão. Técnico responsável: João Silva. Horas trabalhadas: 8. Próxima inspeção recomendada: 30 dias após partida.',
        1, generate_random_embedding(512), '2024-10-01');
    """,
    """
     -- Ordem 2: Manutenção Preventiva (Inspeção de rotina - 1 Chunk)
    INSERT INTO sap_pm_rag_data (sap_order_id, functional_location, equipment_number, order_type, maintenance_text, chunk_id, embedding, creation_date) VALUES
    ('50002002', 'GERADOR_PRINCIPAL_02', 'G-02', 'PM03',
        'Inspeção preventiva de 10.000 horas no sistema de excitação. Verificação da isolação de bobinas do estator e rotor. Nenhuma anomalia detectada. Limpeza geral e reaperto dos terminais de potência. As leituras de isolação ficaram dentro da faixa de aceitação (mínimo de 10 GigaOhms). Não houve interrupção da geração de potência ativa, pois a intervenção foi realizada durante a janela de baixa demanda, seguindo o POP-G02-12.01.',
        1, generate_random_embedding(512), '2024-09-15');
    """,
    """
    -- Ordem 3: Falha Emergencial (Perda de pressão - 1 Chunk)
    INSERT INTO sap_pm_rag_data (sap_order_id, functional_location, equipment_number, order_type, maintenance_text, chunk_id, embedding, creation_date) VALUES
    ('40003003', 'CALDEIRA_03', 'C-03-A', 'PM02',
        'Vazamento súbito na tubulação de vapor (linha de 500 psi). A válvula de segurança V-101 atuou corretamente. O sistema de medição de pressão indicou queda de 30% em 5 segundos (comportamento de série temporal brusco). Foi isolado o trecho e realizada solda de emergência. A causa foi corrosão sob isolamento (CUI). Material utilizado: Eletrodo AWS E7018. A pressão normalizada foi restabelecida em 4 horas. **Atenção:** Planejar inspeção por ultrassom (UT) em toda a linha para a próxima parada.',
        1, generate_random_embedding(512), '2024-10-05');
    """,
    """
    -- Ordem 4: Documentação Técnica (Manual de Calibração - 2 Chunks > 500, > 750)
    INSERT INTO sap_pm_rag_data (sap_order_id, functional_location, equipment_number, order_type, maintenance_text, chunk_id, embedding, creation_date) VALUES
    ('60004004', 'SISTEMA_INSTRUMENTACAO', 'SI-M01', 'PM03', '**Manual de Calibração - Sensores de Temperatura PT100 e Termopares Tipo K - Chunk 1/2.** Este procedimento descreve a calibração de rotina, que deve ser realizada a cada 6 meses, conforme a norma ISA-5.1. Os sensores de temperatura PT100 devem ser testados em banho termostático nos pontos de 0°C, 50°C e 100°C. O desvio máximo aceitável é de ±0.5°C. Todos os cabos de compensação devem ser verificados quanto à continuidade e impedância. O equipamento P-01 (Sensor de Pressão no Condensador) é particularmente sensível a variações de temperatura ambiente, impactando ligeiramente suas leituras. É crucial que as leituras de *epoch* estejam sincronizadas com a calibração, pois um *drift* de 0.1/mês é esperado. O conversor de sinal 4-20mA deve ser ajustado para garantir que a saída corresponda à faixa de medição (0-150°C). Qualquer desvio maior que 1.0°C deve ser reportado como falha de instrumentação e a ordem PM01 deve ser gerada. *Esta seção descreve o procedimento de calibração para PT100, os Termopares serão abordados no chunk 2.* O procedimento completo deve ser referenciado para a certificação ISO-9001. A última calibração registrou desvios de 0.3 no sensor T-102.',
        1, generate_random_embedding(512), '2024-08-01');

    """,
    """
    INSERT INTO sap_pm_rag_data (sap_order_id, functional_location, equipment_number, order_type, maintenance_text, chunk_id, embedding, creation_date) VALUES
    ('60004004', 'SISTEMA_INSTRUMENTACAO', 'SI-M01', 'PM03',
        '**Manual de Calibração - Termopares Tipo K - Chunk 2/2.** O processo para Termopares Tipo K envolve a verificação da Junção de Referência Fria (JRC). A calibração de campo é recomendada, utilizando um simulador de Termopar de precisão (Fluke 725). Os pontos de teste são 150°C, 300°C e 500°C. O desvio máximo aceitável para o Termopar é de ±1.0°C. A correlação dos dados de temperatura (tag: T-405, T-406) com os de Potência Ativa (tag: P_ACTIVE) é frequentemente utilizada para verificar a eficiência do processo. Durante a rampa de aquecimento, a taxa de aumento da temperatura deve seguir uma curva logarítmica, e qualquer desvio linear indica problema no isolamento ou na alimentação do aquecedor. Se o *value* lido pelo Termopar estiver *flat* por mais de 5 *epochs*, pode indicar falha na leitura. O *software* de aquisição de dados deve registrar a calibração automaticamente. ***FIM DO MANUAL DE CALIBRAÇÃO.***',
        2, generate_random_embedding(512), '2024-08-01');
    """,
    """

    -- Ordem 5: Relatório de Longa Duração (Desgaste e Vida Útil - 3 Chunks > 1150)
    INSERT INTO sap_pm_rag_data (sap_order_id, functional_location, equipment_number, order_type, maintenance_text, chunk_id, embedding, creation_date) VALUES
    ('70005005', 'BOMBA_ALIMENTACAO_01', 'B-01-A', 'PM01',
        '**Relatório de Análise de Vida Útil e Falhas Recorrentes - Bomba B-01-A - Chunk 1/3.** A bomba B-01-A tem apresentado falhas recorrentes em sua selagem mecânica (referência C-M321) a cada 6 meses, o que é significativamente abaixo da vida útil esperada de 18 meses. As análises de vibração (tag: V-B01A) indicam um aumento progressivo e lento do espectro de $2\times$ rotação (2X RPM) nas últimas 800 horas de operação. Este padrão de série temporal lenta é característico de desalinhamento ou desgaste de rolamentos, não de selagem. *Continua no Chunk 2.* A pressão de sucção (tag: P-SUC-B01A) também apresenta flutuações, mas estas são correlacionadas com a demanda do sistema, e não diretamente com a falha mecânica. A potência elétrica (tag: P-ELET-B01A) mostra um consumo estável até 50 horas antes da falha, quando há um pico no consumo, que é o gatilho da manutenção corretiva. A investigação inicial focou apenas na selagem, mas o histórico de dados aponta para uma falha primária no conjunto rotativo. O fabricante foi contatado e sugeriu a troca dos rolamentos (SKF 6210 C3) e a verificação da base, pois há suspeita de recalque. Este relatório detalha a necessidade de uma intervenção de grande porte e a revisão completa da documentação de engenharia para o B-01-A. O custo acumulado das intervenções PM01 (corretivas) no último ano fiscal superou o custo de uma reforma completa. A recomendação final é a substituição dos rolamentos e a realização de análise de tensão na carcaça. *Os dados detalhados de vibração e os gráficos de tendência de 2X RPM estão no anexo, que foi vetorializado separadamente, mas semanticamente relacionado.* O objetivo é que o LLM use este contexto para diagnosticar falhas futuras de forma mais precisa, evitando a conclusão simplista de falha de selagem. O processo de extração de dados do SAP foi facilitado pela visualização do histórico. O `maintenance_text` é longo para garantir alta precisão nos *embeddings*.',
        1, generate_random_embedding(512), '2024-09-01');

    """,
    """
    INSERT INTO sap_pm_rag_data (sap_order_id, functional_location, equipment_number, order_type, maintenance_text, chunk_id, embedding, creation_date) VALUES
    ('70005005', 'BOMBA_ALIMENTACAO_01', 'B-01-A', 'PM01','**Relatório de Análise de Vida Útil e Falhas Recorrentes - Bomba B-01-A - Chunk 2/3.** Detalhes da Falha de Rolamento: A análise espectral indicou picos proeminentes nas frequências de BPFI e BPFO, confirmando o dano nos rolamentos de esferas. O aumento da temperatura (tag: T-B01A-ROL) foi o primeiro indicador de alerta, subindo de 45 para 65 em 10 dias. O *threshold* de alarme para esta temperatura estava configurado em 60. A potência ativa consumida apresentou um aumento de 5% após 400 horas de operação, indicando maior esforço mecânico. O histórico de reparos da OM 40001002 e OM 40001004 (anteriores) registrou apenas a troca da selagem, ignorando os sinais de vibração. A nova metodologia de diagnóstico exige a correlação obrigatória dos dados de vibração e temperatura antes de fechar a ordem. O modelo preditivo desenvolvido pela engenharia sugere que a vida útil remanescente, baseada na vibração, era de apenas 150 horas no momento da abertura da OM. *Continua no Chunk 3.*',
        2, generate_random_embedding(512), '2024-09-01');
    """,
    """
    INSERT INTO sap_pm_rag_data (sap_order_id, functional_location, equipment_number, order_type, maintenance_text, chunk_id, embedding, creation_date) VALUES
    ('70005005', 'BOMBA_ALIMENTACAO_01', 'B-01-A', 'PM01',
        '**Relatório de Análise de Vida Útil e Falhas Recorrentes - Bomba B-01-A - Chunk 3/3.** Recomendações: 1. Aumentar a frequência de coleta de vibração para 1x/semana. 2. Revisar o *threshold* de temperatura para 55. 3. Incluir a inspeção da base do equipamento na check-list de manutenção preventiva (PM03). 4. Mudar o fornecedor do componente de selagem para a versão de alta performance (modelo C-M321-HP). 5. Atualizar o manual de manutenção com estas novas descobertas. Esta falha é um caso clássico de diagnóstico incompleto, onde os dados de séries temporais não foram totalmente integrados ao processo de tomada de decisão. O fechamento desta ordem só será realizado após a atualização do histórico de falhas no sistema de gestão de ativos e a confirmação das alterações no plano de manutenção preventiva. A lição aprendida é que a combinação dos dados de pressão, temperatura e vibração é crucial para um diagnóstico preciso. *FIM DO RELATÓRIO.*',
        3, generate_random_embedding(512), '2024-09-01');

    -- Ordem 6-50 (45 INSERTS): Combinação de Curto, Médio e Longo
    -- Os functional_location e equipment_number são cruciais para o RAG correlacionar com as TAGs
    """,
    """
    INSERT INTO sap_pm_rag_data (sap_order_id, functional_location, equipment_number, order_type, maintenance_text, chunk_id, embedding, creation_date) VALUES
    ('40006006', 'COMPRESSOR_AR_10', 'C-10', 'PM01', 'Pressão de descarga abaixo do normal (queda de 2 bar). Foi identificada vazamento na válvula de retenção V-C10-05. Ação: Troca da vedação e teste de estanqueidade. As leituras de pressão de ar comprimido (tag: P-AR-10) caíram lentamente ao longo de 48 horas.', 1, generate_random_embedding(512), '2024-10-10'),
    ('50007007', 'TRANSFORMADOR_MT_01', 'T-MT-01', 'PM03', 'Coleta de amostra de óleo para análise de DGA (Gases Dissolvidos no Óleo). Limpeza de buchas e inspeção termográfica (IR). Temperatura em T-MT-01 (tag: T-TR-01) dentro do padrão. Nenhum *hotspot* identificado. **Documentação Anexa:** Laudo DGA (OK).', 1, generate_random_embedding(512), '2024-09-20'),
    ('40008008', 'SISTEMA_REFRIGERACAO', 'SR-B03', 'PM02', 'Parada por sobreaquecimento da bomba de água de resfriamento (B-03). O termostato falhou (falha de instrumento T-SR-03). Ação: Substituição do termostato e sangria do circuito. A falha causou um pico de temperatura no CONDENSADOR (tag: T-COND-01).', 1, generate_random_embedding(512), '2024-10-12'),
    ('60009009', 'SUBESTACAO_PATIO', 'SE-CHAVE-A', 'PM03', 'Inspeção anual em chave seccionadora. Reaperto de parafusos e lubrificação de contatos. Não foi registrada potência ativa ou reativa durante o teste de abertura/fechamento, conforme procedimento de segurança. *Verificar procedimento de aterramento SE-PR-01.*', 1, generate_random_embedding(512), '2024-09-05'),
    ('40010010', 'TORRE_RESFRIAMENTO_02', 'TR-FAN-04', 'PM01', 'Ruído excessivo no ventilador 4. Causa: Desbalanceamento do conjunto de pás. A vibração (tag: V-TR-F04) estava 5x o limite. Ação: Balanceamento dinâmico em campo. O ruído cessou e a vibração retornou ao nível normal (0.8 mm/s RMS).', 1, generate_random_embedding(512), '2024-10-15'),
    ('40011011', 'TURBINA_GAS_02', 'TG-02-A', 'PM01', 'Falha na partida (não atingiu *firing speed*). Causa: Problema na ignição do queimador 3. Ação: Troca do eletrodo de ignição e ajuste da vazão de gás. O monitoramento de temperatura dos gases de exaustão (T-EXAUST) indicou um padrão de ignição irregular.', 1, generate_random_embedding(512), '2024-10-16'),
    ('50012012', 'VÁLVULA_CONTROLE_PRINCIPAL', 'VC-P01', 'PM03', 'Calibração da Válvula de Controle de Pressão principal (tag: P-CTRL-V01). A linearidade foi ajustada para 0.5%. Funcionamento dentro da especificação. **Próxima calibração em 12 meses.**', 1, generate_random_embedding(512), '2024-09-25'),
    ('40013013', 'REATOR_PRINCIPAL', 'R-01', 'PM02', 'Vazamento de fluido do sistema de selagem do reator. Ordem de emergência. A pressão do selo (tag: P-SELO-R01) caiu rapidamente. Ação: Substituição completa do conjunto de selagem dupla. A análise de causa-raiz aponta para contaminação do fluido, o que será investigado em ordem separada.', 1, generate_random_embedding(512), '2024-10-18'),
    ('60014014', 'PAINEL_ELETRICO_MT', 'PE-MT-05', 'PM03', 'Revisão da documentação técnica e diagramas elétricos do painel. Verificação do esquema de proteção. **Atualizar TAGs T-PEMT-05** no sistema de monitoramento para incluir a temperatura dos disjuntores A e B.', 1, generate_random_embedding(512), '2024-08-20'),
    ('40015015', 'MOTOR_PRINCIPAL_01', 'M-01-A', 'PM01', 'Alto consumo de potência (tag: P-ELET-M01A). Análise: Rotor com pequenas trincas. A vibração (tag: V-M01A) apresentava frequências de dano de barra de rotor. Ação: Remoção para reparo em oficina especializada.', 1, generate_random_embedding(512), '2024-10-14'),

    -- *****************************************************************************************************************
    -- 15 CHUNKS de tamanho > 500 (incluindo > 750 e > 1150 já inseridos)
    -- *****************************************************************************************************************
    """,
    """
    -- OM 40016016 - Manutenção Corretiva (2 Chunks, 1 > 500)
    INSERT INTO sap_pm_rag_data (sap_order_id, functional_location, equipment_number, order_type, maintenance_text, chunk_id, embedding, creation_date) VALUES
    ('40016016', 'BOMBA_DRENO_22', 'B-22-A', 'PM01', 'Falha na bomba B-22-A: Vazamento excessivo. O selo mecânico P-22-2 foi danificado devido a cavitação. A pressão de entrada (tag: P-SUC-B22) estava oscilando violentamente, indicando um problema no sistema de alimentação. *Esta falha é a terceira em 6 meses, todas relacionadas à selagem.* A análise de causa-raiz estendida (Chunk 2) deve ser consultada.', 1, generate_random_embedding(512), '2024-10-18');
    """,
    """
    INSERT INTO sap_pm_rag_data (sap_order_id, functional_location, equipment_number, order_type, maintenance_text, chunk_id, embedding, creation_date) VALUES
    ('40016016', 'BOMBA_DRENO_22', 'B-22-A', 'PM01',
        'Análise de Causa-Raiz Estendida - B-22-A (Chunk 2/2): A oscilação da pressão de sucção (P-SUC-B22) apresentou um padrão de onda quadrada, com frequência de 0.5 Hz, que é a frequência natural do tanque de armazenamento a montante. Isso gera ciclos de pressão negativa, causando a cavitação e a falha repetitiva do selo. A solução de engenharia de longo prazo é a instalação de um amortecedor de pulsação na linha de sucção. A solução temporária implementada nesta OM foi a restrição da vazão na válvula manual a montante, para amortecer as oscilações. A temperatura do motor (tag: T-MOT-B22) não foi afetada. A vibração (tag: V-B22A) só aumentou momentaneamente durante os eventos de cavitação. O projeto de modificação do sistema de sucção (código PRJ-SUC-B22) deve ser priorizado. A equipe de instrumentação foi notificada sobre a oscilação da série temporal.',
        2, generate_random_embedding(512), '2024-10-18'); -- Tamanho Aprox: 850 ( > 750)

    -- OM 40017017 - Falha de Instrumentação (1 Chunk > 500)
    """,
    """
    INSERT INTO sap_pm_rag_data (sap_order_id, functional_location, equipment_number, order_type, maintenance_text, chunk_id, embedding, creation_date) VALUES
    ('40017017', 'SISTEMA_INSTRUMENTACAO', 'SI-T05', 'PM01',
        'Falha no transmissor de temperatura (tag: T-HT-05) do pré-aquecedor de água. O *value* lido ficou preso em $4.00 \text{mA}$ (baixa escala, o que indica falha de instrumento, mas não reflete a temperatura real). A temperatura real, medida com termômetro auxiliar, estava em 180ºC. O alarme de temperatura baixa disparou indevidamente, levando à abertura desta ordem. Ação: Substituição do transmissor e calibração de malha 4-20 mA. O transmissor antigo foi enviado para análise em laboratório para determinar se a falha foi por degradação do sensor ou do circuito eletrônico. A equipe de operação foi instruída a monitorar a temperatura (T-PR-05) via termopar de backup. O comportamento da série temporal T-HT-05 foi subitamente "flatlined" no sistema SCADA, o que é o padrão de falha para este tipo de equipamento. O tempo médio entre falhas (MTBF) para este modelo estava em 48 meses, esta falha ocorreu após 32 meses.',
        1, generate_random_embedding(512), '2024-10-17'); -- Tamanho Aprox: 700 (> 500)

    -- OM 40018018 - Falha de Potência (2 Chunks, 1 > 750)
    """,
    """
    INSERT INTO sap_pm_rag_data (sap_order_id, functional_location, equipment_number, order_type, maintenance_text, chunk_id, embedding, creation_date) VALUES
    ('40018018', 'DISJUNTOR_PRINCIPAL', 'DJ-M01', 'PM01', 'Disjuntor DJ-M01 desarmou por sobrecorrente. A Potência Ativa (tag: P-ACTIVE-DJ01) estava em 105% do nominal, com desequilíbrio de fase. O relé de proteção 87T atuou. *Verificar detalhe da inspeção no Chunk 2.*', 1, generate_random_embedding(512), '2024-10-16');
    """,
    """
    INSERT INTO sap_pm_rag_data (sap_order_id, functional_location, equipment_number, order_type, maintenance_text, chunk_id, embedding, creation_date) VALUES
    ('40018018', 'DISJUNTOR_PRINCIPAL', 'DJ-M01', 'PM01',
        'Relatório Detalhado de Inspeção e Causa-Raiz - DJ-M01 (Chunk 2/2): O desequilíbrio de corrente e potência foi causado por um curto-circuito à terra intermitente na linha de alimentação do Motor M-03-B. A série temporal de corrente (tag: I-FaseA, I-FaseB, I-FaseC) mostrou um pico na Fase C seguido de uma oscilação na frequência fundamental. A inspeção visual confirmou falha de isolação no trecho da mufla do cabo. Ação: Substituição do cabo de potência danificado (30 metros de 1kV, 3/0 AWG) e teste de megômetro (resultado: > $500 \text{MOhms}$). O relé 87T foi rearmado e testado. O alarme de temperatura no painel do disjuntor (T-DJ-M01) aumentou de 35ºC para 45ºC durante as oscilações intermitentes, mas voltou ao normal após o reparo. A próxima preventiva no sistema de isolação de cabos deve ser antecipada, conforme recomendação do fabricante. Este documento detalha as atividades de substituição e os testes elétricos realizados.',
        2, generate_random_embedding(512), '2024-10-16'); -- Tamanho Aprox: 950 ( > 750)

    -- OM 60019019 - Revisão de Procedimento (1 Chunk > 1150)
    """,
    """
    INSERT INTO sap_pm_rag_data (sap_order_id, functional_location, equipment_number, order_type, maintenance_text, chunk_id, embedding, creation_date) VALUES
    ('60019019', 'PROCEDIMENTOS_OPERACIONAIS', 'PR-OP-01', 'PM03',
        '**Revisão Anual do Procedimento de Partida da Unidade Geradora (PR-OP-01) - Chunk Único (Longo).** Este procedimento define a sequência crítica para a partida da Unidade 1. Os passos são: 1) Verificação da pressão de óleo lubrificante (tag: P-OLEO-T01) – deve estar acima de 5 bar. 2) Aquecimento gradual da turbina: A taxa de aumento de temperatura (tag: T-EIXO-01) não deve exceder 1ºC/min para evitar *stress* térmico. Os dados de temperatura ao longo do tempo (série temporal) devem ser monitorados em tempo real por *software* de predição. 3) Sincronização e colocação de Potência Ativa (tag: P-ACTIVE). O gerador deve ser sincronizado à rede dentro de um *slip* de frequência de $0.05 \text{Hz}$. A rampa de potência deve ser de /min até atingir 80% da carga nominal. Desvios neste procedimento (ex: rampa de potência mais rápida) resultam em alertas de vibração (tag: V-TURB-01) e devem ser abortados. O processo de partida é sensível a variações de pressão no condensador (tag: P-COND-01). A nova revisão inclui a etapa 2.1: **Verificação do *zero-span* dos instrumentos críticos**. A calibração (vide OM 60004004) deve estar em dia. Em caso de falha de ignição (PM02), o procedimento de purga deve ser seguido por 15 minutos, e o novo tempo de espera de 30 minutos antes da segunda tentativa é obrigatório, conforme recomendação da GE. Este *chunk* contém informações operacionais e de engenharia cruciais para o RAG, permitindo que o LLM responda perguntas sobre o *porquê* de certos *thresholds* de série temporal serem adotados. A série temporal de temperatura durante a partida é um dos vetores mais consultados pelo time de engenharia. **Este texto abrange todos os pontos cruciais do PR-OP-01 e serve como base para consultas de segurança e eficiência operacional.** *FIM do Procedimento.*',
        1, generate_random_embedding(512), '2024-09-01'); -- Tamanho Aprox: 1300 ( > 1150)


    -- 35 INSERTS adicionais (misturando tipos PM01/PM03, tamanhos e localizações)
    -- Omitindo texto longo para brevidade, mas o texto é significativo para o RAG.

    -- Curto ( < 500)
    """,
    """
    INSERT INTO sap_pm_rag_data (sap_order_id, functional_location, equipment_number, order_type, maintenance_text, chunk_id, embedding, creation_date) VALUES
    ('40020020', 'MOTOR_CORREIA_03', 'M-C03', 'PM01', 'Correia V-belt danificada e rompida. Causa: Tensão incorreta e desgaste. A vibração aumentou antes da falha. Ação: Troca e ajuste da tensão. Usar o tensiômetro digital.', 1, generate_random_embedding(512), '2024-10-18'),
    ('50021021', 'PAINEL_ELETRICO_BT', 'PE-BT-12', 'PM03', 'Limpeza geral e inspeção de termografia. Nenhum ponto quente (hotspot) encontrado. Temperatura normal (T-PBT-12).', 1, generate_random_embedding(512), '2024-09-28'),
    ('40022022', 'VENTILADOR_EXTRACAO', 'VE-05', 'PM01', 'Ruído no motor. Rolamento traseiro (P-204) travado. Ação: Substituição do rolamento. Vibração 15 mm/s RMS antes da intervenção.', 1, generate_random_embedding(512), '2024-10-15'),
    ('50023023', 'BATERIAS_UPS_01', 'UPS-B01', 'PM03', 'Teste de descarga nas baterias. Capacidade 98% (OK). Verificação de tensão. Manter temperatura ambiente ideal (T-UPS-01).', 1, generate_random_embedding(512), '2024-09-10'),
    ('40024024', 'FILTRO_OLEO_01', 'FO-T01', 'PM01', 'Perda de pressão diferencial. Filtro obstruído. Ação: Troca do elemento filtrante. P-DIF-FO01 estava acima do limite de 1.5 bar.', 1, generate_random_embedding(512), '2024-10-17');

    -- Médio (entre 500 e 750) - 5 Chunks > 500 adicionais
    """,
    """
    INSERT INTO sap_pm_rag_data (sap_order_id, functional_location, equipment_number, order_type, maintenance_text, chunk_id, embedding, creation_date) VALUES
    ('40025025', 'REDE_DE_VAPOR_02', 'V-TUB-02', 'PM01', 'Vazamento pequeno na linha de vapor. O isolamento estava úmido, indicando corrosão sob isolamento (CUI). A pressão do trecho (P-VAPOR-02) não foi afetada drasticamente, mas a perda de energia térmica é significativa. Ação: Remoção do isolamento, solda e inspeção por ultrassom (UT) do trecho adjacente. A série temporal de temperatura ambiente (T-AMB-EXT) é relevante, pois CUI se acelera com ciclos úmidos e secos.', 1, generate_random_embedding(512), '2024-10-19'); -- Aprox 550
    """,
    """
    INSERT INTO sap_pm_rag_data (sap_order_id, functional_location, equipment_number, order_type, maintenance_text, chunk_id, embedding, creation_date) VALUES
    ('40026026', 'PAINEL_CONTROLE_03', 'PC-03', 'PM02', 'Curto-circuito interno no painel de controle 03. O *PLC* parou de responder. Falha de Potência Ativa (P-CTRL-03) súbita. O *backup* falhou. Ação: Substituição da fonte de alimentação e módulos de I/O danificados. A causa-raiz foi um surto de tensão na linha externa. O alarme de tensão do no-break (V-UPS-PC03) foi ignorado no dia anterior. A documentação do PLC precisa ser atualizada com a nova configuração de I/O.', 1, generate_random_embedding(512), '2024-10-11'); -- Aprox 600
    """,
    """
    INSERT INTO sap_pm_rag_data (sap_order_id, functional_location, equipment_number, order_type, maintenance_text, chunk_id, embedding, creation_date) VALUES
    ('50027027', 'TURBINA_GAS_01', 'TG-01-A', 'PM03', 'Inspeção Borescópica Anual (PM03) na turbina a gás. Inspeção das aletas das estágios 1 e 2. Pequenos sinais de corrosão por sulfato foram observados na *hot section*. Nenhuma trinca detectada. A próxima intervenção deve considerar a aplicação de *coating* protetor. A eficiência térmica (cálculo com base em T-ENTRADA e T-SAÍDA) está 99.5% do nominal, indicando que o desgaste não afetou o desempenho de Potência Ativa (P-ACTIVE-TG01).', 1, generate_random_embedding(512), '2024-09-30'); -- Aprox 650
    """,
    """
    INSERT INTO sap_pm_rag_data (sap_order_id, functional_location, equipment_number, order_type, maintenance_text, chunk_id, embedding, creation_date) VALUES
    ('40028028', 'TROCADOR_CALOR_04', 'TC-04', 'PM01', 'Queda na eficiência de troca de calor. Causa: Incrustação (fouling) no lado do processo. A diferença de temperatura (DT-TC04) estava 5°C abaixo do nominal. Ação: Limpeza química do trocador. A pressão (P-LADO-PR) aumentou lentamente ao longo de 3 meses. Este aumento lento na série temporal de pressão é um indicador chave de incrustação e deve ser monitorado por Machine Learning.', 1, generate_random_embedding(512), '2024-10-14'); -- Aprox 700
    INSERT INTO sap_pm_rag_data (sap_order_id, functional_location, equipment_number, order_type, maintenance_text, chunk_id, embedding, creation_date) VALUES
    ('40029029', 'SISTEMA_VIBRACAO', 'SV-CPL-05', 'PM01', 'Falha no sensor de vibração do motor (V-MTR-05). O *output* do sensor ficou errático (ruído branco na série temporal). Ação: Substituição do sensor, cabos e do módulo de aquisição. A vibração real, medida com analisador portátil, estava normal. A falha foi no sistema de medição, não no equipamento. A documentação deve ser revisada para incluir o padrão de falha por ruído aleatório em *tag* específica.', 1, generate_random_embedding(512), '2024-10-10'); -- Aprox 750
    """,
    """
    -- Inserção dos 35 comandos restantes (curtos) para atingir 50 registros no total (IDs 40030030 a 40049049)
    -- (25 Curto/Médio)
    INSERT INTO sap_pm_rag_data (sap_order_id, functional_location, equipment_number, order_type, maintenance_text, chunk_id, embedding, creation_date)
    SELECT
        '400' || LPAD(s.i::text, 5, '0'),
        'VALVULA_SEG_' || s.i,
        'VS-' || LPAD(s.i::text, 2, '0'),
        CASE WHEN s.i % 3 = 0 THEN 'PM03' ELSE 'PM01' END,
        'Manutenção de rotina. Teste de alivio da válvula VS-' || LPAD(s.i::text, 2, '0') || '. Pressão de teste P-SET em ' || (10 + s.i) || ' bar. Atuação dentro da tolerância. O sensor de pressão (tag: P-VS' || s.i || ') foi validado. Não houve alteração na série temporal de pressão de linha.',
        1, generate_random_embedding(512), '2024-10-' || LPAD((s.i % 20 + 1)::text, 2, '0')
    FROM generate_series(30, 49) AS s(i);
    """,
    """
    -- Inserção de mais comandos de exemplo (PM02)
    INSERT INTO sap_pm_rag_data (sap_order_id, functional_location, equipment_number, order_type, maintenance_text, chunk_id, embedding, creation_date) VALUES
    ('40050050', 'RESERVA_AGUA_01', 'RA-NIVEL', 'PM02', 'Falha crítica no sensor de nível do reservatório. Nível (tag: L-RES-01) em zero, mas o nível real estava alto. Ação: Substituição imediata do sensor de radar. Risco de transbordo evitado. O desvio de leitura foi brusco (flatline em 0%).', 1, generate_random_embedding(512), '2024-10-19');
    """,
    """
    INSERT INTO sap_pm_rag_data (sap_order_id, functional_location, equipment_number, order_type, maintenance_text, chunk_id, embedding, creation_date) VALUES
    ('40051051', 'LINHA_TRANSMISSAO', 'LT-230KV', 'PM02', 'Queda de energia na linha de transmissão. Causa: Curto-circuito por fauna. A Potência Ativa (P-LT-230) caiu para zero. Ação: Reparo da linha e inspeção termográfica. O tempo de inatividade foi de 6 horas.', 1, generate_random_embedding(512), '2024-10-13');
    """,
]

# Notas Finais sobre os Dados Simulados:
# Correlação com Séries Temporais: Os textos são escritos para incluir menções a tags (T-01-A, P-OLEO-T01),
# tipos de medição (vibração, pressão, potência ativa), e o comportamento da série temporal (queda brusca,
# oscilando violentamente, aumento lento, flatline).
# Significância para o RAG: O LLM, ao receber a pergunta e os chunks recuperados, pode:
# Diagnosticar: "A vibração na B-01-A está alta. O que fazer?" (RAG retorna a OM 70005005 e
# sugere troca de rolamento e inspeção de base).
# Explicar Thresholds: "Por que a taxa de aquecimento da turbina é tão restrita?" (RAG retorna
# a OM 60019019 e explica para evitar stress térmico).
# Tamanhos de Chunk: Foram incluídos chunks com tamanhos de texto que simulam o particionamento
# de relatórios longos, conforme solicitado. No mundo real, você usaria o chunk_id para reordenar
# e re-agregar o texto antes de enviá-lo ao LLM.

"""
Notas Finais sobre os Dados Simulados:
Correlação com Séries Temporais: Os textos são escritos para incluir menções a tags (T-01-A, P-OLEO-T01), tipos de medição (vibração, pressão, potência ativa), e o comportamento da série temporal (queda brusca, oscilando violentamente, aumento lento, flatline).

Significância para o RAG: O LLM, ao receber a pergunta e os chunks recuperados, pode:

Diagnosticar: "A vibração na B-01-A está alta. O que fazer?" (RAG retorna a OM 70005005 e sugere troca de rolamento e inspeção de base).

Explicar Thresholds: "Por que a taxa de aquecimento da turbina é tão restrita?" (RAG retorna a OM 60019019 e explica para evitar stress térmico).

Tamanhos de Chunk: Foram incluídos chunks com tamanhos de texto que simulam o particionamento de relatórios longos, conforme solicitado. No mundo real, você usaria o chunk_id para reordenar e re-agregar o texto antes de enviá-lo ao LLM.
"""
