#!/usr/bin/env python3
"""
Script de Transcrição de Áudio usando Whisper
Autor: Claude
Data: 2025-10-12
"""

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Optional

try:
    import whisper
    from whisper.utils import get_writer
except ImportError:
    print("❌ Erro: biblioteca 'openai-whisper' não encontrada!")
    print("📦 Instale com: pip install openai-whisper")
    sys.exit(1)


MODELOS_DISPONIVEIS = {
    'tiny': 'Mais rápido, menos preciso (~1GB RAM)',
    'base': 'Rápido, boa precisão (~1GB RAM)',
    'small': 'Balanceado (~2GB RAM)',
    'medium': 'Preciso, mais lento (~5GB RAM)',
    'large': 'Máxima precisão, muito lento (~10GB RAM)',
    'turbo': '8x mais rápido que large, qualidade ~large-v2 (~6GB RAM) ⚡',
    'large-v3-turbo': 'Mesmo que turbo (~6GB RAM)'
}


def formatar_tempo(segundos: float) -> str:
    """Formata segundos em HH:MM:SS"""
    horas = int(segundos // 3600)
    minutos = int((segundos % 3600) // 60)
    segs = int(segundos % 60)
    return f"{horas:02d}:{minutos:02d}:{segs:02d}"


def transcrever_audio(
    caminho_audio: Path,
    modelo: str = 'base',
    idioma: Optional[str] = None,
    verbose: bool = True,
    output_dir: Optional[Path] = None
) -> dict:
    """
    Transcreve arquivo de áudio usando Whisper
    
    Args:
        caminho_audio: Caminho do arquivo de áudio
        modelo: Modelo Whisper a usar (tiny, base, small, medium, large)
        idioma: Código do idioma (pt, en, es, etc.) ou None para autodetectar
        verbose: Mostrar progresso detalhado
        output_dir: Diretório para salvar resultados (padrão: mesmo do áudio)
    
    Returns:
        Dict com resultado da transcrição
    """
    if not caminho_audio.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho_audio}")
    
    if output_dir is None:
        output_dir = caminho_audio.parent
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"🎙️  Arquivo: {caminho_audio.name}")
    print(f"📊 Tamanho: {caminho_audio.stat().st_size / (1024*1024):.2f} MB")
    print(f"🤖 Modelo: {modelo} - {MODELOS_DISPONIVEIS.get(modelo, 'Desconhecido')}")
    
    # Carregar modelo
    print(f"\n⏳ Carregando modelo Whisper '{modelo}'...")
    inicio_modelo = time.time()
    model = whisper.load_model(modelo)
    tempo_modelo = time.time() - inicio_modelo
    print(f"✅ Modelo carregado em {tempo_modelo:.2f}s")
    
    # Transcrever
    print(f"\n🎯 Iniciando transcrição...")
    inicio_transcricao = time.time()
    
    opcoes = {
        'verbose': verbose,
        'fp16': False  # Compatibilidade com CPUs
    }
    
    if idioma:
        opcoes['language'] = idioma
        print(f"🌐 Idioma forçado: {idioma}")
    else:
        print(f"🌐 Detectando idioma automaticamente...")
    
    resultado = model.transcribe(str(caminho_audio), **opcoes)
    tempo_transcricao = time.time() - inicio_transcricao
    
    # Informações sobre o resultado
    idioma_detectado = resultado.get('language', 'desconhecido')
    texto_completo = resultado['text'].strip()
    num_segmentos = len(resultado.get('segments', []))
    
    print(f"\n✅ Transcrição concluída em {formatar_tempo(tempo_transcricao)}")
    print(f"🌍 Idioma detectado: {idioma_detectado.upper()}")
    print(f"📝 Segmentos: {num_segmentos}")
    print(f"📄 Caracteres: {len(texto_completo)}")
    print(f"📄 Palavras: {len(texto_completo.split())}")
    
    return resultado, output_dir


def salvar_resultados(
    resultado: dict,
    caminho_audio: Path,
    output_dir: Path,
    formatos: list = ['txt', 'srt', 'json']
):
    """Salva resultados em diferentes formatos"""
    base_name = caminho_audio.stem
    
    # Salvar texto simples
    if 'txt' in formatos:
        txt_path = output_dir / f"{base_name}_transcricao.txt"
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(resultado['text'].strip())
        print(f"💾 Texto salvo: {txt_path}")
    
    # Salvar SRT (legendas)
    if 'srt' in formatos:
        srt_writer = get_writer('srt', str(output_dir))
        srt_writer(resultado, str(caminho_audio), {'max_line_width': 50, 'max_line_count': 2})
        srt_path = output_dir / f"{base_name}.srt"
        print(f"💾 Legendas (SRT) salvas: {srt_path}")
    
    # Salvar VTT (legendas web)
    if 'vtt' in formatos:
        vtt_writer = get_writer('vtt', str(output_dir))
        vtt_writer(resultado, str(caminho_audio), {'max_line_width': 50})
        vtt_path = output_dir / f"{base_name}.vtt"
        print(f"💾 Legendas (VTT) salvas: {vtt_path}")
    
    # Salvar JSON completo
    if 'json' in formatos:
        json_path = output_dir / f"{base_name}_completo.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(resultado, f, ensure_ascii=False, indent=2)
        print(f"💾 JSON completo salvo: {json_path}")


def main():
    parser = argparse.ArgumentParser(
        description='Transcreve áudio para texto usando Whisper',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  # Transcrição básica (modelo base)
  python transcribe_audio.py audio.m4a
  
  # Usar modelo mais preciso
  python transcribe_audio.py audio.m4a --modelo medium
  
  # Forçar idioma português
  python transcribe_audio.py audio.m4a --idioma pt
  
  # Salvar apenas texto e legendas
  python transcribe_audio.py audio.m4a --formatos txt srt
  
  # Especificar diretório de saída
  python transcribe_audio.py audio.m4a --output ./transcricoes
        """
    )
    
    parser.add_argument(
        'arquivo',
        type=str,
        help='Caminho do arquivo de áudio'
    )
    
    parser.add_argument(
        '-m', '--modelo',
        type=str,
        choices=list(MODELOS_DISPONIVEIS.keys()),
        default='base',
        help=f'Modelo Whisper (padrão: base)'
    )
    
    parser.add_argument(
        '-i', '--idioma',
        type=str,
        help='Código do idioma (pt, en, es, etc.) - autodetectar se omitido'
    )
    
    parser.add_argument(
        '-f', '--formatos',
        nargs='+',
        choices=['txt', 'srt', 'vtt', 'json'],
        default=['txt', 'srt', 'json'],
        help='Formatos de saída (padrão: txt srt json)'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        help='Diretório de saída (padrão: mesmo do áudio)'
    )
    
    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='Modo silencioso (menos output)'
    )
    
    parser.add_argument(
        '--listar-modelos',
        action='store_true',
        help='Lista modelos disponíveis e sai'
    )
    
    args = parser.parse_args()
    
    # Listar modelos
    if args.listar_modelos:
        print("🤖 Modelos Whisper Disponíveis:\n")
        for modelo, desc in MODELOS_DISPONIVEIS.items():
            print(f"  • {modelo:8} - {desc}")
        return
    
    # Processar arquivo
    try:
        caminho_audio = Path(args.arquivo).resolve()
        output_dir = Path(args.output).resolve() if args.output else None
        
        print("=" * 70)
        print("🎙️  TRANSCRIÇÃO DE ÁUDIO COM WHISPER")
        print("=" * 70)
        
        resultado, output_dir = transcrever_audio(
            caminho_audio=caminho_audio,
            modelo=args.modelo,
            idioma=args.idioma,
            verbose=not args.quiet,
            output_dir=output_dir
        )
        
        print("\n" + "=" * 70)
        print("💾 SALVANDO RESULTADOS")
        print("=" * 70 + "\n")
        
        salvar_resultados(
            resultado=resultado,
            caminho_audio=caminho_audio,
            output_dir=output_dir,
            formatos=args.formatos
        )
        
        print("\n" + "=" * 70)
        print("✅ CONCLUÍDO COM SUCESSO!")
        print("=" * 70)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Operação cancelada pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
