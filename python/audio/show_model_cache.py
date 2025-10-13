#!/usr/bin/env python3
"""
Script para localizar e listar modelos Whisper armazenados
"""

import os
import sys
from pathlib import Path


def get_whisper_cache_dir() -> Path:
    """Retorna o diretório de cache do Whisper"""
    # Whisper usa a variável de ambiente ou o padrão
    cache_dir = os.getenv("XDG_CACHE_HOME", os.path.expanduser("~/.cache"))
    return Path(cache_dir) / "whisper"


def get_human_readable_size(size_bytes: int) -> str:
    """Converte bytes para formato legível"""
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"


def list_whisper_models():
    """Lista todos os modelos Whisper baixados"""
    cache_dir = get_whisper_cache_dir()

    print("=" * 70)
    print("📦 MODELOS WHISPER ARMAZENADOS")
    print("=" * 70)
    print(f"\n📂 Diretório de cache: {cache_dir}")

    if not cache_dir.exists():
        print("\n⚠️  Diretório de cache não existe ainda!")
        print("   Os modelos serão baixados aqui quando você executar o Whisper")
        return

    print(f"   Status: {'✅ Existe' if cache_dir.is_dir() else '❌ Não é diretório'}")

    # Listar arquivos no diretório
    try:
        files = list(cache_dir.glob("*.pt"))

        if not files:
            print("\n⚠️  Nenhum modelo encontrado no cache")
            print("   Os modelos serão baixados na primeira execução")
            return

        print(f"\n🎯 Modelos encontrados: {len(files)}")
        print("-" * 70)

        total_size = 0

        for model_file in sorted(files):
            size = model_file.stat().st_size
            total_size += size

            # Tentar identificar o modelo pelo nome
            model_name = model_file.stem

            print(f"\n📄 {model_name}")
            print(f"   Tamanho: {get_human_readable_size(size)}")
            print(f"   Caminho completo: {model_file}")
            print(f"   Última modificação: {model_file.stat().st_mtime}")

        print("\n" + "=" * 70)
        print(f"💾 Espaço total usado: {get_human_readable_size(total_size)}")
        print("=" * 70)

    except Exception as e:
        print(f"\n❌ Erro ao listar modelos: {e}")


def show_model_info():
    """Mostra informações sobre os modelos Whisper"""
    print("\n" + "=" * 70)
    print("📚 INFORMAÇÕES SOBRE MODELOS WHISPER")
    print("=" * 70)

    models_info = {
        "tiny.pt": "75 MB",
        "tiny.en.pt": "75 MB",
        "base.pt": "142 MB",
        "base.en.pt": "142 MB",
        "small.pt": "466 MB",
        "small.en.pt": "466 MB",
        "medium.pt": "1.5 GB",
        "medium.en.pt": "1.5 GB",
        "large-v1.pt": "2.9 GB",
        "large-v2.pt": "2.9 GB",
        "large-v3.pt": "2.9 GB",
        "large.pt": "2.9 GB",
    }

    print("\n🤖 Tamanhos esperados dos modelos:")
    print("-" * 70)

    for model, size in models_info.items():
        print(f"   • {model:20} → {size}")

    print("\n💡 Nota:")
    print("   • Modelos '.en' são otimizados apenas para inglês")
    print("   • Modelos sem '.en' são multilíngues (incluem PT-BR)")
    print("   • O modelo é baixado apenas uma vez e reutilizado")


def check_disk_space():
    """Verifica espaço disponível em disco"""
    cache_dir = get_whisper_cache_dir()

    try:
        import shutil

        total, used, free = shutil.disk_usage(cache_dir.parent)

        print("\n" + "=" * 70)
        print("💽 ESPAÇO EM DISCO")
        print("=" * 70)
        print(f"\n   Total: {get_human_readable_size(total)}")
        print(f"   Usado: {get_human_readable_size(used)}")
        print(f"   Livre: {get_human_readable_size(free)}")

        # Avisar se pouco espaço
        if free < 5 * 1024 * 1024 * 1024:  # Menos de 5GB
            print("\n   ⚠️  Pouco espaço livre!")
            print("      Certifique-se de ter pelo menos 5GB para modelos grandes")
    except Exception as e:
        print(f"\n   ⚠️  Não foi possível verificar espaço: {e}")


def show_env_vars():
    """Mostra variáveis de ambiente relacionadas"""
    print("\n" + "=" * 70)
    print("🔧 VARIÁVEIS DE AMBIENTE")
    print("=" * 70)

    env_vars = {
        "XDG_CACHE_HOME": "Diretório de cache customizado",
        "WHISPER_CACHE_DIR": "Diretório específico do Whisper (se configurado)",
    }

    for var, description in env_vars.items():
        value = os.getenv(var)
        status = f"✅ {value}" if value else "❌ Não configurado (usa padrão)"
        print(f"\n   {var}:")
        print(f"      {description}")
        print(f"      {status}")


def main():
    print("\n")
    list_whisper_models()
    show_model_info()
    check_disk_space()
    show_env_vars()

    print("\n" + "=" * 70)
    print("💡 DICAS")
    print("=" * 70)
    print("""
   1. Para mudar o diretório de cache, defina:
      export XDG_CACHE_HOME=/seu/diretorio/cache

   2. Para limpar modelos antigos:
      rm -rf ~/.cache/whisper/*.pt

   3. Para ver quanto espaço os modelos ocupam:
      du -sh ~/.cache/whisper/

   4. Os modelos são compartilhados entre todas as aplicações
      que usam Whisper no seu sistema
""")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
