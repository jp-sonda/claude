#!/bin/bash
# Script de execução rápida para transcrever o HandoverRafael

filename="sample_audio_file" # TODO: Modifique o nome do arquivo adequadamente.

echo "🎙️  Transcrevendo data/${filename}.m4a"
echo "================================================"
echo ""

# Modelo recomendado: base (bom equilíbrio)
python3 transcribe_audio.py data/${filename}.m4a \
    --modelo base \
    --formatos txt srt json

echo ""
echo "================================================"
echo "✅ Transcrição concluída!"
echo ""
echo "📁 Arquivos gerados em: data/"
echo "   • ${filename}_transcricao.txt"
echo "   • ${filename}.srt"
echo "   • ${filename}_completo.json"
echo ""
