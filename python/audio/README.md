# Transcrição de Áudio com Whisper

Script Python profissional para transcrever áudio para texto usando o modelo Whisper da OpenAI.

## ⚠️ IMPORTANTE: Compatibilidade Python

**Python 3.13 NÃO É SUPORTADO!**

- ✅ **Recomendado:** Python 3.12 ou 3.11
- ✅ **Funciona:** Python 3.8 - 3.12
- ❌ **NÃO funciona:** Python 3.13+ (pkg_resources deprecated)

**Versão dos Pacotes:**

- `openai-whisper`: **v20250625** (mais recente - junho 2025)
- `torch`: >=2.0.0
- `torchaudio`: >=2.0.0

## ✅ Verificar Compatibilidade (RODE PRIMEIRO!)

```bash
# Verificação completa do sistema
python3 check_compatibility.py

# Ver árvore de dependências transitivas
python3 check_dependencies_tree.py
```

Estes scripts verificam:

- ✅ Versão do Python (3.8-3.12)
- ✅ Pacotes instalados e suas versões
- ✅ Dependências transitivas
- ✅ FFmpeg instalado
- ✅ Capacidade de importar módulos

## 🚀 Instalação Rápida

```bash
# 1. Verificar compatibilidade PRIMEIRO
python3 check_compatibility.py

# 2. Instalar dependências (se compatível)
pip install -r requirements.txt

# 3. Instalar FFmpeg (se necessário)
# macOS:
brew install ffmpeg

# Ubuntu/Debian:
# sudo apt update && sudo apt install ffmpeg

# Windows:
# choco install ffmpeg
```

### Ou use o script automático:

```bash
chmod +x install.sh
./install.sh
```

## 📖 Uso

### Transcrição Básica

```bash
python transcribe_audio.py data/sample_audio_file.m4a
```

### Executar com script pronto

```bash
chmod +x run_transcribe.sh
./run_transcribe.sh
```

### Escolher Modelo (trade-off velocidade vs precisão)

```bash
# Rápido (recomendado para testes)
python transcribe_audio.py data/sample_audio_file.m4a --modelo base

# Balanceado
python transcribe_audio.py data/sample_audio_file.m4a --modelo small

# Máxima precisão (mais lento)
python transcribe_audio.py data/sample_audio_file.m4a --modelo medium
```

### Forçar Idioma

```bash
# Português
python transcribe_audio.py data/sample_audio_file.m4a --idioma pt

# Inglês
python transcribe_audio.py data/sample_audio_file.m4a --idioma en
```

### Escolher Formatos de Saída

```bash
# Apenas texto simples
python transcribe_audio.py data/sample_audio_file.m4a --formatos txt

# Texto + Legendas SRT
python transcribe_audio.py data/sample_audio_file.m4a --formatos txt srt

# Todos os formatos
python transcribe_audio.py data/sample_audio_file.m4a --formatos txt srt vtt json
```

### Especificar Diretório de Saída

```bash
python transcribe_audio.py data/sample_audio_file.m4a --output ./resultados
```

## 🤖 Modelos Disponíveis

| Modelo   | Velocidade | Precisão   | RAM    | Uso Recomendado                   |
| -------- | ---------- | ---------- | ------ | --------------------------------- |
| `tiny`   | ⚡⚡⚡⚡⚡ | ⭐         | ~1 GB  | Testes rápidos, rascunhos         |
| `base`   | ⚡⚡⚡⚡   | ⭐⭐       | ~1 GB  | **Uso geral (recomendado)**       |
| `small`  | ⚡⚡⚡     | ⭐⭐⭐     | ~2 GB  | Boa precisão, tempo razoável      |
| `medium` | ⚡⚡       | ⭐⭐⭐⭐   | ~5 GB  | Alta precisão, áudio profissional |
| `large`  | ⚡         | ⭐⭐⭐⭐⭐ | ~10 GB | Máxima qualidade, sem pressa      |

## 📄 Formatos de Saída

- **TXT**: Texto puro da transcrição
- **SRT**: Legendas com timestamps (compatível com players de vídeo)
- **VTT**: Legendas para web (HTML5)
- **JSON**: Dados completos incluindo segmentos, timestamps e metadados

## 💡 Dicas

### Para seu arquivo de 78.5MB:

```bash
# Começe com base (rápido, ~2-5 minutos)
python transcribe_audio.py data/sample_audio_file.m4a --modelo base

# Se precisar de mais qualidade:
python transcribe_audio.py data/sample_audio_file.m4a --modelo medium
```

### Ver todos os comandos:

```bash
python transcribe_audio.py --help
```

### Listar modelos:

```bash
python transcribe_audio.py --listar-modelos
```

## 🐛 Solução de Problemas

### Erro: Python 3.13

```bash
# Python 3.13 NÃO é suportado! Use Python 3.12:
pyenv install 3.12.8
pyenv local 3.12.8

# Ou use conda:
conda create -n whisper python=3.12
conda activate whisper
```

### Erro: "openai-whisper não encontrado"

```bash
pip install openai-whisper>=20250625
```

### Erro: "ffmpeg não encontrado"

Instale o FFmpeg conforme instruções de instalação acima.

### Erro de memória (RAM insuficiente)

Use um modelo menor:

```bash
python transcribe_audio.py data/sample_audio_file.m4a --modelo tiny
```

### Transcrição em idioma errado

Force o idioma:

```bash
python transcribe_audio.py data/sample_audio_file.m4a --idioma pt
```

### Verificar se tudo está funcionando

```bash
# Diagnóstico completo
python3 check_compatibility.py

# Ver dependências transitivas
python3 check_dependencies_tree.py
```

## 📊 Performance Estimada

Para um arquivo de ~78 MB:

- **tiny/base**: 2-5 minutos
- **small**: 5-10 minutos
- **medium**: 10-20 minutos
- **large**: 20-40 minutos

_(Tempos variam conforme CPU/GPU disponível)_

## 🛠️ Scripts Disponíveis

- `transcribe_audio.py` - Script principal de transcrição
- `check_compatibility.py` - Verificador de compatibilidade do sistema
- `check_dependencies_tree.py` - Analisador de dependências transitivas
- `install.sh` - Instalação automática
- `run_transcribe.sh` - Execução rápida com configurações padrão

## 📚 Mais Informações

- [Documentação oficial do Whisper](https://github.com/openai/whisper)
- [PyPI - openai-whisper](https://pypi.org/project/openai-whisper/)
- [Paper original](https://arxiv.org/abs/2212.04356)
