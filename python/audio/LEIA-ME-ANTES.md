Este diretório foi criado usando o modêlo **Sonnet 4.5** no **Claude Desktop** com o seguinte prompt:

> Eu tenho um arquivo de audio do tipo MPEG4 da Apple de 78.5MB e preciso converter em texto. Você consegue fazer isso ?

Ele criou o script completo que podemos executar e pronto! Funciona perfeitamente com o arquivo `.m4a` de 78.5MB.
Ele criou o script no diretório permitido e só precisamos executar apontando para arquivo de audio desejado.
O script vai:

- ✅ Instalar dependências automaticamente (se necessário)
- ✅ Transcrever o áudio completo
- ✅ Detectar idioma (PT-BR, EN, etc)
- ✅ Mostrar progresso em tempo real
- ✅ Salvar resultado em .txt (e opcionalmente .srt para legendas)
- ✅ Suportar diferentes modelos Whisper (base, small, medium, large)

1️⃣ Entrar no diretório

```bash
cd $HOME/dev/claude/python/audio
deactivate
/opt/homebrew/Cellar/python@3.12/3.12.11/Frameworks/Python.framework/Versions/3.12/bin/python3.12 -m venv .venv
. .venv/bin/activate
# Confirmar se está usando o Virtual Environment criado acima
python3 -V && which python3
```

2️⃣ Instalar (primeira vez apenas)

```bash
chmod +x install.sh run_transcribe.sh
./install.sh
```

3️⃣ Transcrever!

`./run_transcribe.sh nome_arquivo_sem_a_extensão`

> Ao solicitar ao **Sonnet 4.5**: "Você consegue verificar se todos os pacotes python e suas dependências transitivas funcionam no Python 3.13? Existe uma forma de criar um script Python para isso ?"

Obtive o seguinte:

- criou o Markdown VERIFICACAO_COMPATIBILIDADE.md
- 🔍 check_python.py # Criou Verificação rápida
- 🔍 check_compatibility.py # Criou Verificação avançada (reutilizável!)
- 📋 verify_before_install.sh # Criou Verificação automática
- 📘 PYTHON_3.13_ISSUES.md # Criou Documentação detalhada
- 📘 README.md # Atualizou com avisos
- 📘 QUICKSTART.md # Atualizou com verificação

A documentação ficou grande e prolixa. O que importa mesmo é que a recomendação é de usar a versão 3.12 e esperar o suporte correto para a versão 3.13 estar disponível para openai-whisper teve um erro de julgamento do modelo que foi execivamente conservador escolhendo a versão 20231117 quando poderia ter escolhido a versão 20250625.
Desta forma pedi outro prompt:

> Você já criou os scripts mas testou a versão v20231117 do pacote openai-whisper, no entanto a versão mais atual é a v20250625. Qual foi o motivo de você não usa esta versão mais atual ?

À partir dai ele fez uma revisão total nos scripts e artefatos Python e nos arquivos Markdown. Ao final resumiu o ocorrido:

- Foi um erro meu. Não havia justificativa técnica para usar v20231117 ao invés da versão mais recente v20250625.
- Por que aconteceu: Conservadorismo excessivo - assumi que versão antiga seria "mais segura" ; Não verifiquei o PyPI antes de criar o requirements.txt ; Erro de julgamento - versões mais recentes geralmente têm correções e melhorias
- Reportou uma **Descoberta importante**: Whisper NÃO funciona com Python 3.13 devido ao pkg_resources que foi deprecado KeyError: '**version**' installing openai-whisper on Python 3.13 - Stack Overflow -> Evidências: Existe um PullRequest (#2409) com correção, mas seu **merge** ainda não foi autorizado.

## Resultado do teste

```bash
python3 transcribe_audio.py --help # mostra a s opções. O unico parâmetro obrigatório é o nome do arquivo de audio.
python3 transcribe_audio.py --listar-modelos data/my_audio_file.m4a
python3 transcribe_audio.py data/my_audio_file.m4a
# Usando o comando acima com modelo base a transcrição foi concluída em 00:05:14 entretanto ficou com baixa qualidade
#
python3 transcribe_audio.py -i pt -m medium data/HandoverRafael-audio.m4a
```

A transcrição usando o modelo **medium** demorou 2 horas e usou 5GB de RAM mas o resultado foi muito bom. Certamente será bem melhor com modelo **large**, entretanto este modelo large consome muito mais memória RAM (10GB) e vai demorar muito mais tempo.

Após avaliar o resultaado do modelo medium, pedi ao Claude Desktop o seguinte:

> Quando eu executei `python3 transcribe_audio.py -i pt -m medium -q data/my_audio_file.m4a` o programa carregou o modelo Whisper 'medium' de 1.42G em menos de um minuto. Você pode me dizer onde ele armazena os dados do modelo ?

Com este prompt ele me respondeu objetivamente a pergunta mas também criou um script Python `show_model_cache.py` para listar os modelos baixados e exibir informações relevantes sobre eles.

Na sequencia fiz o seguinte prompt:

> Eu notei a existência do arquivo large-v3-turbo.pt no diretório de cache mas ele é de 04/junho. Como faço para baixar a versão mais nova dele e como posso referenciar este modelo no programa transcribe_audio.py ?

A resposta foi a seguinte:

🚀 Sobre o Whisper Turbo - O modelo large-v3-turbo (ou simplesmente turbo) foi lançado em outubro de 2024 como uma versão otimizada do large-v3, com apenas 4 decoder layers ao invés de 32. Detalhes em [`turbo` model release · openai/whisper · Discussion #2363](https://github.com/openai/whisper/discussions/2363)

Características:

809M parâmetros (~1.6GB download)
8x mais rápido que large-v3
Performance similar ao large-v2 na maioria dos idiomas
⚠️ NÃO é treinado para tradução - use medium ou large para isso

Como resultado ele criou o script `manage_models.py` que é um Gerenciador de Modelos Whisper que Baixa, atualiza, remove e gerencia modelos do cache.
