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
  }
}
```

