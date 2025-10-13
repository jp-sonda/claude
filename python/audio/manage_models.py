#!/usr/bin/env python3
"""
Gerenciador de Modelos Whisper
Baixa, atualiza, remove e gerencia modelos do cache
"""

import os
import sys
import shutil
from pathlib import Path
from typing import List, Dict, Optional
import argparse


def get_cache_dir() -> Path:
    """Retorna o diretório de cache do Whisper"""
    cache_home = os.getenv('XDG_CACHE_HOME', os.path.expanduser('~/.cache'))
    return Path(cache_home) / 'whisper'


def get_human_readable_size(size_bytes: int) -> str:
    """Converte bytes para formato legível"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"


def list_cached_models() -> List[Dict]:
    """Lista todos os modelos no cache"""
    cache_dir = get_cache_dir()
    
    if not cache_dir.exists():
        return []
    
    models = []
    for model_file in cache_dir.glob('*.pt'):
        stat = model_file.stat()
        models.append({
            'name': model_file.stem,
            'path': model_file,
            'size': stat.st_size,
            'modified': stat.st_mtime
        })
    
    return sorted(models, key=lambda x: x['modified'], reverse=True)


def print_models_table(models: List[Dict]):
    """Imprime tabela de modelos"""
    if not models:
        print("⚠️  Nenhum modelo encontrado no cache")
        return
    
    print("\n📦 Modelos no cache:")
    print("=" * 80)
    print(f"{'Modelo':<25} {'Tamanho':>12} {'Última Modificação':>30}")
    print("-" * 80)
    
    from datetime import datetime
    for model in models:
        mod_time = datetime.fromtimestamp(model['modified']).strftime('%Y-%m-%d %H:%M:%S')
        print(f"{model['name']:<25} {get_human_readable_size(model['size']):>12} {mod_time:>30}")
    
    total_size = sum(m['size'] for m in models)
    print("-" * 80)
    print(f"{'Total':<25} {get_human_readable_size(total_size):>12}")
    print("=" * 80)


def delete_model(model_name: str) -> bool:
    """Remove um modelo do cache"""
    cache_dir = get_cache_dir()
    model_path = cache_dir / f"{model_name}.pt"
    
    if not model_path.exists():
        print(f"❌ Modelo '{model_name}' não encontrado no cache")
        return False
    
    size = model_path.stat().st_size
    model_path.unlink()
    print(f"✅ Modelo '{model_name}' removido ({get_human_readable_size(size)} liberados)")
    return True


def force_redownload(model_name: str) -> bool:
    """Remove modelo e força re-download"""
    print(f"\n🔄 Forçando re-download do modelo '{model_name}'...")
    
    # Primeiro, remover o modelo antigo
    if not delete_model(model_name):
        print(f"⚠️  Modelo '{model_name}' não estava no cache, será baixado na próxima execução")
    
    print(f"\n💡 Para baixar agora, execute:")
    print(f"   python3 -c \"import whisper; whisper.load_model('{model_name}')\"")
    print(f"\nOu use o transcribe_audio.py:")
    print(f"   python3 transcribe_audio.py --modelo {model_name} data/HandoverRafael-audio.m4a")
    
    return True


def download_model_now(model_name: str):
    """Baixa um modelo imediatamente"""
    print(f"\n📥 Baixando modelo '{model_name}'...")
    print("   (Isso pode levar alguns minutos dependendo do tamanho)")
    
    try:
        import whisper
        print(f"\n⏳ Carregando modelo '{model_name}'...")
        model = whisper.load_model(model_name)
        print(f"✅ Modelo '{model_name}' baixado e carregado com sucesso!")
        
        # Mostrar informações
        cache_dir = get_cache_dir()
        model_path = cache_dir / f"{model_name}.pt"
        if model_path.exists():
            size = model_path.stat().st_size
            print(f"   Tamanho: {get_human_readable_size(size)}")
            print(f"   Local: {model_path}")
    except Exception as e:
        print(f"❌ Erro ao baixar modelo: {e}")
        return False
    
    return True


def update_model(model_name: str):
    """Atualiza um modelo (remove e re-baixa)"""
    print(f"\n🔄 Atualizando modelo '{model_name}'...")
    
    cache_dir = get_cache_dir()
    model_path = cache_dir / f"{model_name}.pt"
    
    if model_path.exists():
        from datetime import datetime
        mod_time = datetime.fromtimestamp(model_path.stat().st_mtime)
        print(f"   Versão atual: {mod_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Remover
        delete_model(model_name)
    
    # Re-baixar
    download_model_now(model_name)


def clean_all():
    """Remove todos os modelos do cache"""
    models = list_cached_models()
    
    if not models:
        print("⚠️  Nenhum modelo para limpar")
        return
    
    total_size = sum(m['size'] for m in models)
    print(f"\n⚠️  Isso irá remover {len(models)} modelo(s) e liberar {get_human_readable_size(total_size)}")
    
    response = input("Confirma? (s/N): ")
    if response.lower() != 's':
        print("❌ Operação cancelada")
        return
    
    cache_dir = get_cache_dir()
    try:
        shutil.rmtree(cache_dir)
        print(f"✅ Cache limpo: {get_human_readable_size(total_size)} liberados")
    except Exception as e:
        print(f"❌ Erro ao limpar cache: {e}")


def show_available_models():
    """Mostra modelos disponíveis para download"""
    print("\n🤖 Modelos Whisper Disponíveis:")
    print("=" * 80)
    
    models_info = {
        'tiny': {'size': '~75 MB', 'speed': '⚡⚡⚡⚡⚡', 'quality': '⭐'},
        'tiny.en': {'size': '~75 MB', 'speed': '⚡⚡⚡⚡⚡', 'quality': '⭐', 'note': 'Inglês only'},
        'base': {'size': '~142 MB', 'speed': '⚡⚡⚡⚡', 'quality': '⭐⭐'},
        'base.en': {'size': '~142 MB', 'speed': '⚡⚡⚡⚡', 'quality': '⭐⭐', 'note': 'Inglês only'},
        'small': {'size': '~466 MB', 'speed': '⚡⚡⚡', 'quality': '⭐⭐⭐'},
        'small.en': {'size': '~466 MB', 'speed': '⚡⚡⚡', 'quality': '⭐⭐⭐', 'note': 'Inglês only'},
        'medium': {'size': '~1.5 GB', 'speed': '⚡⚡', 'quality': '⭐⭐⭐⭐'},
        'medium.en': {'size': '~1.5 GB', 'speed': '⚡⚡', 'quality': '⭐⭐⭐⭐', 'note': 'Inglês only'},
        'large': {'size': '~2.9 GB', 'speed': '⚡', 'quality': '⭐⭐⭐⭐⭐'},
        'large-v2': {'size': '~2.9 GB', 'speed': '⚡', 'quality': '⭐⭐⭐⭐⭐'},
        'large-v3': {'size': '~2.9 GB', 'speed': '⚡', 'quality': '⭐⭐⭐⭐⭐'},
        'turbo': {'size': '~1.6 GB', 'speed': '⚡⚡⚡⚡', 'quality': '⭐⭐⭐⭐', 'note': '8x mais rápido! ✨'},
        'large-v3-turbo': {'size': '~1.6 GB', 'speed': '⚡⚡⚡⚡', 'quality': '⭐⭐⭐⭐', 'note': 'Mesmo que turbo'},
    }
    
    for model, info in models_info.items():
        note = f"  ({info.get('note', '')})" if 'note' in info else ""
        print(f"  • {model:<18} {info['size']:>10} | Velocidade: {info['speed']} | Qualidade: {info['quality']}{note}")
    
    print("\n💡 Recomendação:")
    print("   • Para transcrição rápida: turbo ou base")
    print("   • Para melhor qualidade: medium ou large-v3")
    print("   • Para tradução: medium ou large (NÃO use turbo)")
    print("=" * 80)


def main():
    parser = argparse.ArgumentParser(
        description='Gerenciador de Modelos Whisper',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  # Listar modelos no cache
  python3 manage_models.py --list
  
  # Atualizar modelo turbo
  python3 manage_models.py --update turbo
  
  # Remover modelo antigo
  python3 manage_models.py --delete large-v3-turbo
  
  # Baixar novo modelo
  python3 manage_models.py --download turbo
  
  # Ver modelos disponíveis
  python3 manage_models.py --available
  
  # Limpar todo o cache
  python3 manage_models.py --clean-all
        """
    )
    
    parser.add_argument('--list', '-l', action='store_true',
                        help='Listar modelos no cache')
    parser.add_argument('--update', '-u', type=str, metavar='MODEL',
                        help='Atualizar modelo (remove e re-baixa)')
    parser.add_argument('--delete', '-d', type=str, metavar='MODEL',
                        help='Remover modelo do cache')
    parser.add_argument('--download', type=str, metavar='MODEL',
                        help='Baixar modelo agora')
    parser.add_argument('--available', '-a', action='store_true',
                        help='Mostrar modelos disponíveis')
    parser.add_argument('--clean-all', action='store_true',
                        help='Limpar todo o cache (CUIDADO!)')
    
    args = parser.parse_args()
    
    # Se nenhum argumento, mostrar help
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)
    
    cache_dir = get_cache_dir()
    print(f"\n📂 Diretório de cache: {cache_dir}")
    
    if args.list:
        models = list_cached_models()
        print_models_table(models)
    
    if args.available:
        show_available_models()
    
    if args.update:
        update_model(args.update)
    
    if args.delete:
        delete_model(args.delete)
    
    if args.download:
        download_model_now(args.download)
    
    if args.clean_all:
        clean_all()


if __name__ == '__main__':
    main()
