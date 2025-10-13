#!/bin/bash
# Script para verificar compatibilidade antes da instalação

echo "🔍 VERIFICAÇÃO DE COMPATIBILIDADE"
echo "=================================="
echo ""

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado!"
    echo "   Instale Python 3.12 antes de continuar."
    exit 1
fi

# Executar verificação Python
echo "📊 Verificando versão do Python..."
python3 check_python.py
python_exit=$?

echo ""
echo "=================================="

if [ $python_exit -ne 0 ]; then
    echo ""
    echo "⚠️  AVISO: Problemas de compatibilidade detectados!"
    echo ""
    echo "💡 Recomendações:"
    echo "   1. Instale Python 3.12:"
    echo "      • macOS: brew install python@3.12"
    echo "      • Ubuntu: sudo apt install python3.12"
    echo "   2. Crie um ambiente virtual:"
    echo "      python3.12 -m venv venv"
    echo "      source venv/bin/activate"
    echo ""
    read -p "Deseja continuar mesmo assim? (s/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Ss]$ ]]; then
        echo "Instalação cancelada."
        exit 1
    fi
fi

echo ""
echo "✅ Verificação concluída!"
echo ""
