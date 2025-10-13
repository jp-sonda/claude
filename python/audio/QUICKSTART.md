# 🚀 INÍCIO RÁPIDO - 4 Passos

## ⚠️ PASSO 0: Verificar Compatibilidade (IMPORTANTE!)

```bash
cd $HOME/dev/claude/python/audio

# Verificar se seu Python é compatível (3.8-3.12, NÃO 3.13!)
python3 check_compatibility.py
```

**Se aparecer Python 3.13:** você PRECISA usar Python 3.12 ou 3.11!

```bash
# Instalar Python 3.12 com pyenv
pyenv install 3.12.8
pyenv local 3.12.8

# Verificar novamente
python3 check_compatibility.py
```

---

## Passo 1: Instalar Dependências

```bash
# Dar permissão de execução aos scripts
chmod +x install.sh run_transcribe.sh check_compatibility.py

# Instalar tudo automaticamente
./install.sh
```

## Passo 2: Transcrever o Áudio

```bash
# Opção A: Usar script automático (RECOMENDADO)
./run_transcribe.sh

# Opção B: Comando direto (personalizável)
python3 transcribe_audio.py data/sample_audio_file.m4a
```

## Passo 3: Ver Resultados

Os arquivos serão salvos em `data/`:

- `sample_audio_file_transcricao.txt` - Texto completo
- `sample_audio_file.srt` - Legendas (importar em editor de vídeo)
- `sample_audio_file_completo.json` - Dados completos com timestamps

---

## ⚡ Comandos Úteis

### Diagnosticar problemas

```bash
# Verificação completa do sistema
python3 check_compatibility.py

# Ver todas as dependências transitivas
python3 check_dependencies_tree.py
```

### Ver ajuda completa

```bash
python3 transcribe_audio.py --help
```

### Usar modelo mais rápido (para testar)

```bash
python3 transcribe_audio.py data/sample_audio_file.m4a --modelo tiny
```

### Usar modelo mais preciso (melhor qualidade)

```bash
python3 transcribe_audio.py data/sample_audio_file.m4a --modelo medium
```

### Forçar português brasileiro

```bash
python3 transcribe_audio.py data/sample_audio_file.m4a --idioma pt
```

---

## 🐛 Problemas Comuns

### ❌ Python 3.13 detectado

```bash
# Whisper NÃO funciona com Python 3.13!
# Use Python 3.12:

pyenv install 3.12.8
pyenv local 3.12.8

# Ou com conda:
conda create -n whisper python=3.12
conda activate whisper
```

### "openai-whisper não encontrado"

```bash
pip3 install openai-whisper>=20250625
```

### "ffmpeg: command not found"

```bash
# macOS
brew install ffmpeg

# Linux
sudo apt update && sudo apt install ffmpeg

# Windows
choco install ffmpeg
```

### Ficou lento ou travou

- Use modelo menor: `--modelo tiny` ou `--modelo base`
- O primeiro uso baixa o modelo (~1-5GB), próximas vezes são mais rápidas
- Verifique RAM disponível: modelos maiores precisam de mais memória

---

## 📊 Tempo Estimado

Para seu arquivo de 78.5 MB:

- **tiny**: ~2 min (teste rápido)
- **base**: ~3-5 min ⭐ (RECOMENDADO)
- **small**: ~7-10 min (melhor qualidade)
- **medium**: ~15-20 min (profissional)

---

## 📦 Versões Usadas

- **openai-whisper**: v20250625 (mais recente)
- **Python**: 3.8-3.12 (recomendado: 3.12)
- **torch**: >=2.0.0

---

## 💡 Dica Final

1. **SEMPRE** rode `python3 check_compatibility.py` primeiro
2. Se tiver Python 3.13, downgrade para 3.12
3. Comece com modelo **base** (padrão)
4. Se qualidade não for suficiente, rode novamente com **medium**
