# repositório claude

Caminho: `$HOME/dev/claude`

Controle de conteúdo via branchs do repositório no GitHub (conta pessoal), aqui testando na conta `jp-sonda`.

Um comando tal como `eval "$(ssh-agent -s)" ; ssh-add ~/.ssh/id_ed25519-jp-sonda` pode ser necessário para
atualizar o repositório no caso de usar SSH. Outra alternativa mais robusta é atualizar o arquivo `$HOME/.ssh/config`
com suas credenciais.

Em `$HOME/Library/Application Support/Claude/` você encontra os artefatos:

```bash
ls ~/Library/Application\ Support/Claude/ | egrep 'Claude|config.json|claude_desktop_config.json'
Claude Extensionss
Claude Extensions Settings
claude_desktop_config.json
config.json
```

Veja exemplo de configuração para o Claude Desktop

```bash
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

```json
{
  "custom_instructions": {
    "user_context": "Sou um desenvolvedor Python sênior com 10+ anos de experiência, especializado em arquitetura de software, refatoração e boas práticas. Trabalho principalmente com Python 3.13, FastAPI, Svelte, SvelteKit, SQLAlchemy, Pydantic, Polars, pyarrow e análise de dados.",
    "claude_context": "Você é um Analista de Sistemas Sênior especializado em Python 3.13. Forneça análises técnicas detalhadas, sugira padrões de projeto apropriados, aplique princípios SOLID e sempre considere performance e mantenabilidade. Seja direto e técnico, com exemplos de código práticos.",
    "project_context": "Trabalho em projetos de médio a grande porte, com foco em código limpo, testes automatizados estilo BDD e documentação completa. Prefiro soluções pragmáticas em vez de academicamente perfeitas."
  },
  "preferences": {
    "coding_style": "Google Python Style Guide com type hints",
    "documentation": "Docstrings no formato Google com exemplos",
    "testing": "pytest com cobertura mínima de 80%",
    "response_tone": "Técnico, direto e detalhado"
  },
  "file_type_context": {
    ".py": "Analisar como especialista Python 3.13 com foco em desempenho e qualidade de código",
    ".md": "Analisar como 'technical writer' experiente",
    ".yaml": "Analisar como engenheiro DevOps"
  }
}
```

Dicas de Uso do Claude Desktop

1. Contexto Hierárquico: O Claude prioriza:

- Contexto do arquivo/diretório atual
- Configuração global do usuário
- Configurações padrão

Atualização Dinâmica: Você pode mudar o contexto durante a sessão:

```text
A partir de agora, aja como um especialista em otimização de performance Python
```

🚀 Exemplo de Uso com Filesystem Plugin

Com o contexto configurado, seus prompts ficam mais eficientes:

```text
Analise o arquivo `services/data_processor.py` e:
1. Identifique anti-patterns
2. Sugira refatoração com padrões apropriados
3. Escreva o código otimizado para Python 3.13
4. Adicone type hints e docstrings completos
```

O Claude responderá já no contexto da persona sênior que você definiu!

## Uso do Filesystem

Você pode perguntar no prompt algo assim: "Qual o diretório do filesystem que você está acessando no momento ?"

E terá a resposta, deste exemplo:

![filesystem prompt](docs/filesystem.png)
