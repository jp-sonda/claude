#!/usr/bin/env python3
"""
Script simples para mostrar onde estão os modelos Whisper
"""

import os
from pathlib import Path

# Diretório padrão do Whisper
cache_home = os.getenv('XDG_CACHE_HOME', os.path.expanduser('~/.cache'))
whisper_cache = Path(cache_home) / 'whisper'

print("=" * 70)
print("📍 LOCALIZAÇÃO DOS MODELOS WHISPER")
print("=" * 70)
print(f"\n📂 Diretório: {whisper_cache}")
print(f"   Existe? {whisper_cache.exists()}")

if whisper_cache.exists():
    print("\n💾 Modelos baixados:")
    print("-" * 70)
    
    for model in sorted(whisper_cache.glob('*.pt')):
        size_mb = model.stat().st_size / (1024 * 1024)
        print(f"   ✅ {model.name:20} → {size_mb:.2f} MB")
    
    print("\n💡 Para ver todos os arquivos:")
    print(f"   ls -lh {whisper_cache}")
    print("\n💡 Para ver espaço usado:")
    print(f"   du -sh {whisper_cache}")
else:
    print("\n⚠️  Diretório ainda não existe")
    print("   Será criado no primeiro uso do Whisper")

print("\n" + "=" * 70)
