# Python 3.13 - Problemas de Compatibilidade

## ❌ Resumo

**Python 3.13 NÃO é recomendado para este projeto.**

Embora o PyPI liste Python 3.13 como suportado no pacote `openai-whisper`, existem **problemas práticos conhecidos** que podem causar falhas na instalação e execução.

## 🐛 Problemas Conhecidos

### 1. Erro com `pkg_resources`
```
DeprecationWarning: pkg_resources is deprecated as an API
```

O Python 3.13 deprecou `pkg_resources` em favor de `importlib.resources` e `importlib.metadata`. O openai-whisper ainda usa `pkg_resources`, causando erros na instalação.

### 2. Problemas na Build do Wheel
```
error: subprocess-exited-with-error
× Getting requirements to build wheel did not run successfully.
```

A instalação via pip pode falhar completamente ao tentar construir o wheel do pacote.

### 3. Dependências Transitivas Incompatíveis

Várias dependências do whisper ainda não suportam Python 3.13:
- `ctranslate2` (usado por faster-whisper)
- Algumas versões do PyTorch
- Outras bibliotecas de build

## ✅ Soluções

### Solução 1: Usar Python 3.12 (RECOMENDADO)

```bash
# macOS (usando Homebrew)
brew install python@3.12

# Ubuntu/Debian
sudo apt update
sudo apt install python3.12 python3.12-venv

# Usando pyenv (recomendado para gerenciar múltiplas versões)
pyenv install 3.12.0
pyenv local 3.12.0
```

### Solução 2: Usar Python 3.11 ou 3.10

Também funcionam perfeitamente:

```bash
# macOS
brew install python@3.11

# Ubuntu/Debian
sudo apt install python3.11

# pyenv
pyenv install 3.11.0
```

### Solução 3: Workaround para Python 3.13 (não recomendado)

Se você REALMENTE precisa usar Python 3.13, tente instalar diretamente do repositório:

```bash
# Instalar do GitHub (versão de desenvolvimento)
pip install git+https://github.com/openai/whisper.git

# Ou especificar uma versão mais recente quando disponível
pip install --upgrade --no-deps --force-reinstall git+https://github.com/openai/whisper.git
```

**Aviso:** Mesmo com o workaround, podem ocorrer problemas inesperados.

## 🔍 Como Verificar Sua Versão

```bash
# Ver versão do Python
python3 --version

# Verificar compatibilidade completa
python3 check_python.py

# Verificar pacotes específicos
python3 check_compatibility.py requirements.txt --python 3.13
```

## 📊 Matriz de Compatibilidade

| Versão Python | Status           | Observações                                    |
|---------------|------------------|------------------------------------------------|
| < 3.8         | ❌ Não suportado | Muito antigo                                   |
| 3.8           | ⚠️ Funciona     | Considere atualizar para 3.12                  |
| 3.9           | ✅ Funciona bem | Versão usada originalmente para treinar Whisper |
| 3.10          | ✅ Funciona bem | Estável e confiável                            |
| 3.11          | ✅ Funciona bem | Estável e confiável                            |
| 3.12          | ⭐ Recomendado  | **Melhor escolha atualmente**                  |
| 3.13          | ❌ Problemático | Problemas conhecidos, não recomendado          |
| > 3.13        | ❓ Desconhecido | Provavelmente terá problemas similares         |

## 🔗 Referências

- [Stack Overflow: KeyError installing openai-whisper on Python 3.13](https://stackoverflow.com/questions/79175945/)
- [GitHub Issue: Python 3.13 compatibility](https://github.com/openai/whisper/discussions/2410)
- [GitHub PR: Fix for Python 3.13](https://github.com/openai/whisper/pull/2409)
- [PyPI: openai-whisper](https://pypi.org/project/openai-whisper/)

## 📅 Status (Outubro 2025)

- ❌ Python 3.13 ainda tem problemas não resolvidos
- ✅ Python 3.12 é a versão recomendada
- 🔄 Há um PR pendente com correções, mas ainda não foi mergeado
- 📦 A versão do PyPI ainda não foi atualizada com as correções

## 💡 Recomendação Final

**Use Python 3.12.** É a versão mais estável, moderna e compatível para este projeto.

Se você está usando Python 3.13 e encontrar problemas:
1. Instale Python 3.12
2. Crie um ambiente virtual com Python 3.12
3. Reinstale as dependências

```bash
# Exemplo usando pyenv e venv
pyenv install 3.12.0
pyenv local 3.12.0
python3 -m venv venv
source venv/activate
pip install -r requirements.txt
```
