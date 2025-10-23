# Guia de prompting do Claude

## Dicas gerais para prompting eficaz

### 1. Seja claro e específico
   - Declare claramente sua tarefa ou pergunta no início da sua mensagem.
   - Forneça contexto e detalhes para ajudar o Claude a entender suas necessidades.
   - Divida tarefas complexas em etapas menores e gerenciáveis.

   Prompt ruim:
   <prompt>
   "Me ajude com uma apresentação."
   </prompt>

   Prompt bom:
   <prompt>
   "Preciso de ajuda para criar uma apresentação de 10 slides para nossa reunião trimestral de vendas. A apresentação deve cobrir nosso desempenho de vendas do Q2, produtos mais vendidos e metas de vendas para o Q3. Por favor, forneça um esboço com os pontos-chave para cada slide."
   </prompt>

   Por que é melhor: O prompt bom fornece detalhes específicos sobre a tarefa, incluindo o número de slides, o propósito da apresentação e os tópicos-chave a serem abordados.

### 2. Use exemplos
   - Forneça exemplos do tipo de resultado que você está procurando.
   - Se você quer um formato ou estilo específico, mostre ao Claude um exemplo.

   Prompt ruim:
   <prompt>
   "Escreva um e-mail profissional."
   </prompt>

   Prompt bom:
   <prompt>
   "Preciso escrever um e-mail profissional para um cliente sobre um atraso no projeto. Aqui está um e-mail similar que enviei antes:

   'Prezado(a) [Cliente],
   Espero que este e-mail o(a) encontre bem. Gostaria de atualizá-lo(a) sobre o progresso do [Nome do Projeto]. Infelizmente, encontramos um problema inesperado que atrasará nossa data de conclusão em aproximadamente duas semanas. Estamos trabalhando diligentemente para resolver isso e manteremos você atualizado sobre nosso progresso.
   Por favor, me avise se tiver alguma dúvida ou preocupação.
   Atenciosamente,
   [Seu Nome]'

   Me ajude a redigir um novo e-mail seguindo um tom e estrutura similares, mas para nossa situação atual onde estamos atrasados em um mês devido a problemas na cadeia de suprimentos."
   </prompt>

   Por que é melhor: O prompt bom fornece um exemplo concreto do estilo e tom desejados, dando ao Claude um ponto de referência claro para o novo e-mail.

### 3. Incentive o raciocínio
   - Para tarefas complexas, peça ao Claude para "pensar passo a passo" ou "explicar seu raciocínio."
   - Isso pode levar a respostas mais precisas e detalhadas.

   Prompt ruim:
   <prompt>
   "Como posso melhorar a produtividade da equipe?"
   </prompt>

   Prompt bom:
   <prompt>
   "Estou buscando melhorar a produtividade da minha equipe. Pense nisso passo a passo, considerando os seguintes fatores:
   1. Bloqueios de produtividade atuais (ex: muitas reuniões, prioridades pouco claras)
   2. Soluções potenciais (ex: técnicas de gestão de tempo, ferramentas de gestão de projetos)
   3. Desafios de implementação
   4. Métodos para medir a melhoria

   Para cada etapa, por favor forneça uma breve explicação do seu raciocínio. Depois resuma suas ideias no final."
   </prompt>

   Por que é melhor: O prompt bom pede ao Claude para pensar no problema sistematicamente, fornecendo uma estrutura guiada para a resposta e pedindo explicações do processo de raciocínio. Também solicita ao Claude criar um resumo no final para facilitar a leitura.

### 4. Refinamento iterativo
   - Se a primeira resposta do Claude não estiver exatamente certa, peça esclarecimentos ou modificações.
   - Você sempre pode dizer "Está próximo, mas você pode ajustar X para ser mais como Y?"

   Prompt ruim:
   <prompt>
   "Melhore isso."
   </prompt>

   Prompt bom:
   <prompt>
   "Esse é um bom começo, mas por favor refine ainda mais. Faça os seguintes ajustes:
   1. Torne o tom mais casual e amigável
   2. Adicione um exemplo específico de como nosso produto ajudou um cliente
   3. Encurte o segundo parágrafo para focar mais nos benefícios em vez das características"
   </prompt>

   Por que é melhor: O prompt bom fornece feedback específico e instruções claras para melhorias, permitindo ao Claude fazer ajustes direcionados em vez de apenas confiar no senso inato do Claude do que "melhor" poderia ser — que provavelmente é diferente da definição do usuário!

### 5. Aproveite o conhecimento do Claude
   - O Claude tem amplo conhecimento em muitos campos. Não hesite em pedir explicações ou informações de contexto
   - Certifique-se de incluir contexto e detalhes relevantes para que a resposta do Claude seja maximamente direcionada para ser útil

   Prompt ruim:
   <prompt>
   "O que é marketing? Como faço isso?"
   </prompt>

   Prompt bom:
   <prompt>
   "Estou desenvolvendo uma estratégia de marketing para uma nova linha de produtos de limpeza ecológicos. Você pode fornecer uma visão geral das tendências atuais em marketing verde? Por favor inclua:
   1. Principais estratégias de mensagem que ressoam com consumidores ambientalmente conscientes
   2. Canais eficazes para alcançar esse público
   3. Exemplos de campanhas de marketing verde bem-sucedidas do último ano
   4. Potenciais armadilhas a evitar (ex: acusações de greenwashing)

   Esta informação me ajudará a moldar nossa abordagem de marketing."
   </prompt>

   Por que é melhor: O prompt bom pede informações específicas e contextualmente relevantes que aproveitam a ampla base de conhecimento do Claude. Ele fornece contexto sobre como a informação será usada, o que ajuda o Claude a enquadrar sua resposta da maneira mais relevante.

### 6. Use interpretação de papéis
   - Peça ao Claude para adotar um papel ou perspectiva específica ao responder.

   Prompt ruim:
   <prompt>
   "Me ajude a me preparar para uma negociação."
   </prompt>

   Prompt bom:
   <prompt>
   "Você é um fornecedor de tecidos para minha empresa de fabricação de mochilas. Estou me preparando para uma negociação com este fornecedor para reduzir os preços em 10%. Como o fornecedor, por favor forneça:
   1. Três objeções potenciais ao nosso pedido de redução de preço
   2. Para cada objeção, sugira um contra-argumento da minha perspectiva
   3. Duas propostas alternativas que o fornecedor poderia oferecer em vez de um corte direto de preço

   Então, mude de papel e forneça conselhos sobre como eu, como comprador, posso melhor abordar esta negociação para alcançar nosso objetivo."
   </prompt>

   Por que é melhor: Este prompt usa interpretação de papéis para explorar múltiplas perspectivas da negociação, fornecendo uma preparação mais abrangente. A interpretação de papéis também encoraja o Claude a adotar mais prontamente as nuances de perspectivas específicas, aumentando a inteligência e o desempenho da resposta do Claude.


## Dicas e exemplos específicos por tarefa

### Criação de Conteúdo

1. **Especifique seu público**
   - Diga ao Claude para quem o conteúdo é destinado.

   Prompt ruim:
   <prompt>
   "Escreva algo sobre cibersegurança."
   </prompt>

   Prompt bom:
   <prompt>
   "Preciso escrever um post de blog sobre melhores práticas de cibersegurança para proprietários de pequenas empresas. O público não é muito experiente em tecnologia, então o conteúdo deve ser:
   1. Fácil de entender, evitando jargão técnico quando possível
   2. Prático, com dicas acionáveis que eles possam implementar rapidamente
   3. Envolvente e levemente bem-humorado para manter o interesse deles

   Por favor, forneça um esboço para um post de blog de 1000 palavras que cubra as 5 principais práticas de cibersegurança que esses empresários devem adotar."
   </prompt>

   Por que é melhor: O prompt bom especifica o público, tom desejado e características-chave do conteúdo, dando ao Claude diretrizes claras para criar um resultado apropriado e eficaz.

2. **Defina o tom e o estilo**
   - Descreva o tom desejado.
   - Se você tem um guia de estilo, mencione os pontos-chave dele.

   Prompt ruim:
   <prompt>
   "Escreva uma descrição de produto."
   </prompt>

   Prompt bom:
   <prompt>
   "Por favor me ajude a escrever uma descrição de produto para nossa nova cadeira de escritório ergonômica. Use um tom profissional mas envolvente. A voz da nossa marca é amigável, inovadora e consciente da saúde. A descrição deve:
   1. Destacar as principais características ergonômicas da cadeira
   2. Explicar como essas características beneficiam a saúde e produtividade do usuário
   3. Incluir uma breve menção aos materiais sustentáveis utilizados
   4. Terminar com uma chamada para ação encorajando os leitores a experimentar a cadeira

   Busque cerca de 200 palavras."
   </prompt>

   Por que é melhor: Este prompt fornece orientação clara sobre o tom, estilo e elementos específicos a incluir na descrição do produto.

3. **Defina a estrutura de saída**
   - Forneça um esboço básico ou lista de pontos que você quer cobrir.

   Prompt ruim:
   <prompt>
   "Crie uma apresentação sobre os resultados da nossa empresa."
   </prompt>

   Prompt bom:
   <prompt>
   "Preciso criar uma apresentação sobre nossos resultados do Q2. Estruture isso com as seguintes seções:
   1. Visão Geral
   2. Desempenho de Vendas
   3. Aquisição de Clientes
   4. Desafios
   5. Perspectivas para Q3

   Para cada seção, sugira 3-4 pontos-chave a cobrir, baseado em apresentações empresariais típicas. Além disso, recomende um tipo de visualização de dados (ex: gráfico, tabela) que seria eficaz para cada seção."
   </prompt>

   Por que é melhor: Este prompt fornece uma estrutura clara e pede elementos específicos (pontos-chave e visualizações de dados) para cada seção.

### Resumo de documentos e perguntas e respostas

1. **Seja específico sobre o que você quer**
   - Peça um resumo de aspectos ou seções específicas do documento.
   - Formule suas perguntas de forma clara e direta.
   - Certifique-se de especificar que tipo de resumo (estrutura de saída, tipo de conteúdo) você quer

2. **Use os nomes dos documentos**
   - Refira-se aos documentos anexados pelo nome.

3. **Peça citações**
   - Solicite que o Claude cite partes específicas do documento em suas respostas.

Aqui está um exemplo que combina todas as três técnicas acima:

   Prompt ruim:
   <prompt>
   "Resume este relatório para mim."
   </prompt>

   Prompt bom:
   <prompt>
   "Anexei um relatório de pesquisa de mercado de 50 páginas chamado 'Tendências da Indústria de Tecnologia 2023'. Você pode fornecer um resumo de 2 parágrafos focando em tendências de IA e aprendizado de máquina? Depois, por favor responda estas perguntas:
   1. Quais são as 3 principais aplicações de IA em negócios para este ano?
   2. Como o aprendizado de máquina está impactando as funções de trabalho na indústria de tecnologia?
   3. Quais riscos ou desafios potenciais o relatório menciona sobre a adoção de IA?

   Por favor cite seções específicas ou números de páginas ao responder essas perguntas."
   </prompt>

   Por que é melhor: Este prompt especifica o foco exato do resumo, fornece perguntas específicas e pede citações, garantindo uma resposta mais direcionada e útil. Também indica a estrutura de saída de resumo ideal, como limitar a resposta a 2 parágrafos.

### Análise e visualização de dados

1. **Especifique o formato desejado**
   - Descreva claramente o formato em que você quer os dados.

   Prompt ruim:
   <prompt>
   "Analise nossos dados de vendas."
   </prompt>

   Prompt bom:
   <prompt>
   "Anexei uma planilha chamada 'Dados de Vendas 2023'. Você pode analisar esses dados e apresentar as principais descobertas no seguinte formato:

   1. Resumo Executivo (2-3 frases)

   2. Métricas-Chave:
      - Vendas totais para cada trimestre
      - Categoria de produto com melhor desempenho
      - Região com maior crescimento

   3. Tendências:
      - Liste 3 tendências notáveis, cada uma com uma breve explicação

   4. Recomendações:
      - Forneça 3 recomendações baseadas em dados, cada uma com uma breve justificativa

   Após a análise, sugira três tipos de visualizações de dados que comunicariam efetivamente essas descobertas."
   </prompt>

   Por que é melhor: Este prompt fornece uma estrutura clara para a análise, especifica métricas-chave nas quais focar e pede recomendações e sugestões de visualização para formatação adicional.

### Brainstorming
 1. Use o Claude para gerar ideias pedindo uma lista de possibilidades ou alternativas.
     - Seja específico sobre quais tópicos você quer que o Claude cubra em seu brainstorming

   Prompt ruim:
   <prompt>
   "Me dê algumas ideias de team-building."
   </prompt>

   Prompt bom:
   <prompt>
   "Precisamos criar atividades de team-building para nossa equipe remota de 20 pessoas. Você pode me ajudar a fazer um brainstorming:
   1. Sugerindo 10 atividades virtuais de team-building que promovam colaboração
   2. Para cada atividade, explique brevemente como ela promove o trabalho em equipe
   3. Indique quais atividades são melhores para:
      a) Quebra-gelos
      b) Melhorar a comunicação
      c) Habilidades de resolução de problemas
   4. Sugira uma opção de baixo custo e uma opção premium."
   </prompt>

   Por que é melhor: Este prompt fornece parâmetros específicos para a sessão de brainstorming, incluindo o número de ideias, tipo de atividades e categorização adicional, resultando em uma saída mais estruturada e útil.

2. Solicite respostas em formatos específicos como marcadores, listas numeradas ou tabelas para facilitar a leitura.

   Prompt Ruim:
   <prompt>
   "Compare opções de software de gestão de projetos."
   </prompt>

   Prompt Bom:
   <prompt>
   "Estamos considerando três opções diferentes de software de gestão de projetos: Asana, Trello e Microsoft Project. Você pode compará-los em formato de tabela usando os seguintes critérios:
   1. Principais Características
   2. Facilidade de Uso
   3. Escalabilidade
   4. Preços (inclua planos específicos se possível)
   5. Capacidades de integração
   6. Mais adequado para (ex: pequenas equipes, empresas, indústrias específicas)"
   </prompt>

   Por que é melhor: Este prompt solicita uma estrutura específica (tabela) para a comparação, fornece critérios claros, tornando a informação fácil de entender e aplicar.

## Solução de problemas, minimizando alucinações e maximizando o desempenho

1. **Permita que o Claude reconheça incerteza**
   - Diga ao Claude que ele deve dizer que não sabe se não souber. Ex. "Se você não tiver certeza sobre algo, tudo bem admitir. Apenas diga que não sabe."

2. **Divida tarefas complexas**
   - Se uma tarefa parece muito grande e o Claude está perdendo etapas ou não executando certas etapas bem, divida-a em etapas menores e trabalhe nelas com o Claude uma mensagem de cada vez.

3. **Inclua todas as informações contextuais para novas solicitações**
   - O Claude não retém informações de conversas anteriores, então inclua todo o contexto necessário em cada nova conversa.

## Exemplos de prompts bons vs. ruins

Estes são mais exemplos que combinam múltiplas técnicas de prompting para mostrar a diferença marcante entre prompts ineficazes e altamente eficazes.

### Exemplo 1: Desenvolvimento de estratégia de marketing

Prompt ruim:
<prompt>
"Me ajude a criar uma estratégia de marketing."
</prompt>

Prompt bom:
<prompt>
"Como um consultor sênior de marketing, preciso de sua ajuda para desenvolver uma estratégia de marketing abrangente para nossa nova linha de acessórios de smartphone ecológicos. Nosso público-alvo são millennials e consumidores da Geração Z ambientalmente conscientes. Por favor, forneça uma estratégia detalhada que inclua:

1. Análise de Mercado:
   - Tendências atuais em acessórios de tecnologia ecológicos
   - 2-3 principais concorrentes e suas estratégias
   - Tamanho potencial do mercado e projeções de crescimento

2. Persona do Público-Alvo:
   - Descrição detalhada do nosso cliente ideal
   - Seus pontos de dor e como nossos produtos os resolvem

3. Mix de Marketing:
   - Produto: Características-chave a destacar
   - Preço: Estratégia de preços sugerida com justificativa
   - Praça: Canais de distribuição recomendados
   - Promoção: 
     a) 5 canais de marketing nos quais focar, com prós e contras para cada
     b) 3 ideias criativas de campanha para o lançamento

4. Estratégia de Conteúdo:
   - 5 temas de conteúdo que ressoariam com nosso público
   - Tipos de conteúdo sugeridos (ex: posts de blog, vídeos, infográficos)

5. KPIs e Medição:
   - 5 métricas-chave para rastrear
   - Ferramentas sugeridas para medir essas métricas

Por favor, apresente esta informação em um formato estruturado com cabeçalhos e marcadores. Onde relevante, explique seu raciocínio ou forneça exemplos breves.

Após delinear a estratégia, por favor identifique quaisquer desafios ou riscos potenciais dos quais devemos estar cientes e sugira estratégias de mitigação para cada um."
</prompt>

Por que é melhor: Este prompt combina múltiplas técnicas incluindo atribuição de papel, divisão específica de tarefas, solicitação de saída estruturada, brainstorming (para ideias de campanha e temas de conteúdo) e pedindo explicações. Ele fornece diretrizes claras enquanto permite espaço para a análise e criatividade do Claude.

### Exemplo 2: Análise de relatório financeiro

Prompt ruim:
<prompt>
"Analise este relatório financeiro."
</prompt>

Prompt bom:
<prompt>
"Anexei o relatório financeiro do Q2 da nossa empresa intitulado 'Relatório_Financeiro_Q2_2023.pdf'. Atue como um CFO experiente e analise este relatório e prepare um briefing para nosso conselho de administração. Por favor estruture sua análise da seguinte forma:

1. Resumo Executivo (3-4 frases destacando pontos-chave)

2. Visão Geral do Desempenho Financeiro:
   a) Receita: Compare com o trimestre anterior e mesmo trimestre do ano passado
   b) Margens de lucro: Bruta e Líquida, com explicações para quaisquer mudanças significativas
   c) Fluxo de caixa: Destaque quaisquer preocupações ou desenvolvimentos positivos

3. Indicadores-Chave de Desempenho:
   - Liste nossos 5 principais KPIs e seu status atual (Use formato de tabela)
   - Para cada KPI, forneça uma breve explicação de sua importância e quaisquer tendências notáveis

4. Análise por Segmento:
   - Detalhe o desempenho pelos nossos três principais segmentos de negócio
   - Identifique os segmentos de melhor e pior desempenho, com razões potenciais para seu desempenho

5. Revisão do Balanço Patrimonial:
   - Destaque quaisquer mudanças significativas em ativos, passivos ou patrimônio
   - Calcule e interprete índices-chave (ex: índice de liquidez corrente, dívida sobre patrimônio)

6. Declarações Prospectivas:
   - Baseado nestes dados, forneça 3 previsões-chave para o Q3
   - Sugira 2-3 movimentos estratégicos que devemos considerar para melhorar nossa posição financeira

7. Avaliação de Riscos:
   - Identifique 3 riscos financeiros potenciais baseados neste relatório
   - Proponha estratégias de mitigação para cada risco

8. Comparação com Concorrentes:
   - Compare nosso desempenho com 2-3 principais concorrentes (use dados publicamente disponíveis)
   - Destaque áreas onde estamos superando e áreas para melhoria

Por favor use gráficos ou tabelas quando apropriado para visualizar dados. Para quaisquer suposições ou interpretações que você fizer, por favor declare-as claramente e forneça seu raciocínio.

Após completar a análise, por favor gere 5 perguntas potenciais que membros do conselho poderiam fazer sobre este relatório, juntamente com respostas sugeridas.

Finalmente, resuma toda esta análise em um único parágrafo que eu possa usar como declaração de abertura na reunião do conselho."
</prompt>

Por que é melhor: Este prompt combina interpretação de papéis (como CFO), saída estruturada, solicitações específicas de análise de dados, análise preditiva, avaliação de riscos, análise comparativa e até antecipa perguntas de acompanhamento. Ele fornece uma estrutura clara enquanto encoraja análise profunda e pensamento estratégico.
