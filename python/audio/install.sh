#!/bin/bash
# Script de instalação com verificação de compatibilidade

echo "🚀 Instalando dependências para Transcrição de Áudio com Whisper..."
echo ""

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado!"
    exit 1
fi

echo "✅ Python encontrado: $(python3 --version)"
echo ""

# Verificar versão do Python
PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "🔍 Verificando compatibilidade do Python $PYTHON_VERSION..."

# Extrair major e minor version
MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$MAJOR" -eq 3 ] && [ "$MINOR" -ge 13 ]; then
    echo ""
    echo "❌❌❌ ERRO CRÍTICO ❌❌❌"
    echo "Python 3.13+ NÃO É SUPORTADO pelo openai-whisper!"
    echo ""
    echo "Problema: pkg_resources foi deprecado no Python 3.13"
    echo ""
    echo "📥 SOLUÇÃO: Use Python 3.12 ou 3.11"
    echo ""
    echo "   # Com pyenv:"
    echo "   pyenv install 3.12.8"
    echo "   pyenv local 3.12.8"
    echo ""
    echo "   # Com conda:"
    echo "   conda create -n whisper python=3.12"
    echo "   conda activate whisper"
    echo ""
    exit 1
elif [ "$MAJOR" -eq 3 ] && [ "$MINOR" -ge 8 ] && [ "$MINOR" -le 12 ]; then
    echo "✅ Python $PYTHON_VERSION é compatível!"
else
    echo "⚠️  Python $PYTHON_VERSION pode não ser suportado"
    echo "   Recomendado: Python 3.8-3.12"
    echo ""
    read -p "Deseja continuar mesmo assim? (s/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Ss]$ ]]; then
        exit 1
    fi
fi

echo ""

# Verificar FFmpeg
echo "🔍 Verificando FFmpeg..."
if ! command -v ffmpeg &> /dev/null; then
    echo "⚠️  FFmpeg não encontrado!"
    echo ""
    echo "📦 Instale FFmpeg:"
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "   brew install ffmpeg"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "   sudo apt update && sudo apt install ffmpeg"
    fi
    echo ""
    read -p "Deseja continuar mesmo assim? (s/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Ss]$ ]]; then
        exit 1
    fi
else
    echo "✅ FFmpeg encontrado"
fi

echo ""
echo "📦 Instalando bibliotecas Python..."
echo "   (openai-whisper v20250625 + torch + torchaudio)"
echo ""

pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo ""
    echo "=" * 70
    echo "✅ Instalação concluída com sucesso!"
    echo "=" * 70
    echo ""
    echo "🔍 Executando verificação de compatibilidade..."
    echo ""
    python3 check_compatibility.py

    if [ $? -eq 0 ]; then
        echo ""
        echo "🎯 Tudo pronto! Execute agora:"
        echo "   ./run_transcribe.sh"
        echo ""
        echo "   Ou:"
        echo "   python3 transcribe_audio.py data/sample_audio_file.m4a"
        echo ""
    else
        echo ""
        echo "⚠️  Alguns problemas foram detectados."
        echo "   Revise a saída acima e corrija antes de continuar."
        echo ""
    fi
else
    echo ""
    echo "❌ Erro na instalação!"
    echo "   Verifique os erros acima e tente novamente."
    exit 1
fi
