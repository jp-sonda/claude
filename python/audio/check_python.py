#!/usr/bin/env python3
"""
Verificação Rápida de Compatibilidade Python
Verifica se a versão atual do Python é adequada para o projeto
"""

import sys
from pathlib import Path


def check_python_version():
    """Verifica versão do Python e dá recomendações"""

    version_info = sys.version_info
    version_str = f"{version_info.major}.{version_info.minor}.{version_info.micro}"
    major_minor = f"{version_info.major}.{version_info.minor}"

    print("=" * 70)
    print("🐍 VERIFICAÇÃO DE COMPATIBILIDADE DO PYTHON")
    print("=" * 70)
    print(f"\n📊 Versão atual: Python {version_str}")
    print(f"📍 Executável: {sys.executable}\n")

    # Verificar compatibilidade específica do projeto
    print("🔍 Verificando compatibilidade com openai-whisper...")
    print("-" * 70)

    if version_info.major < 3:
        print("\n❌ INCOMPATÍVEL")
        print("   Python 2 não é suportado.")
        print("   Instale Python 3.8 ou superior.")
        return False

    if version_info.minor < 8:
        print("\n❌ INCOMPATÍVEL")
        print(f"   Python {major_minor} é muito antigo.")
        print("   Versão mínima: Python 3.8")
        print("\n💡 Recomendação: Instale Python 3.12")
        return False

    if version_info.minor == 13:
        print("\n⚠️  PARCIALMENTE COMPATÍVEL (COM PROBLEMAS CONHECIDOS)")
        print("   Python 3.13 tem problemas conhecidos com openai-whisper:")
        print("   • Erro com pkg_resources (depreciado no Python 3.13)")
        print("   • Algumas dependências ainda não suportam Python 3.13")
        print("   • Há um PR pendente com correções no GitHub")
        print("\n❗ STATUS: Funciona com workarounds, mas não recomendado")
        print("\n💡 Recomendações:")
        print("   1. Use Python 3.12 para melhor compatibilidade (RECOMENDADO)")
        print("   2. Ou use Python 3.11 (também funciona bem)")
        print("   3. Se quiser continuar com 3.13:")
        print("      pip install git+https://github.com/openai/whisper.git")
        print("      (instala do repo, pode ter menos issues)")
        return False

    if version_info.minor >= 8 and version_info.minor <= 12:
        print("\n✅ TOTALMENTE COMPATÍVEL")
        print(f"   Python {major_minor} funciona perfeitamente com openai-whisper")

        if version_info.minor == 12:
            print("   ⭐ Python 3.12 é a versão recomendada atualmente!")
        elif version_info.minor in [10, 11]:
            print(f"   ✅ Python {major_minor} é uma ótima escolha!")
        else:  # 3.8 ou 3.9
            print(
                f"   ✅ Python {major_minor} funciona, mas considere atualizar para 3.12"
            )

        return True

    # Versões futuras (> 3.13)
    print("\n⚠️  VERSÃO MUITO NOVA")
    print(f"   Python {major_minor} pode ter problemas de compatibilidade.")
    print("   Recomendação: Use Python 3.12 para melhor estabilidade")
    return False


def check_dependencies():
    """Verifica se dependências estão instaladas"""
    print("\n" + "=" * 70)
    print("📦 VERIFICANDO DEPENDÊNCIAS")
    print("=" * 70 + "\n")

    dependencies = {
        "whisper": "openai-whisper",
        "torch": "torch (PyTorch)",
    }

    installed = []
    missing = []

    for module, package in dependencies.items():
        try:
            __import__(module)
            installed.append(package)
            print(f"✅ {package}")
        except ImportError:
            missing.append(package)
            print(f"❌ {package}")

    if missing:
        print(f"\n⚠️  {len(missing)} dependência(s) faltando!")
        print("   Execute: ./install.sh ou pip install -r requirements.txt")
        return False
    else:
        print(f"\n✅ Todas as {len(installed)} dependências instaladas!")
        return True


def main():
    """Função principal"""
    try:
        is_compatible = check_python_version()
        has_deps = check_dependencies()

        print("\n" + "=" * 70)
        print("📋 RESUMO")
        print("=" * 70)

        if is_compatible and has_deps:
            print("\n✅ TUDO OK! Você pode executar o script de transcrição.")
            print("\n🚀 Execute:")
            print("   python3 transcribe_audio.py data/sample_audio_file.m4a")
        elif is_compatible and not has_deps:
            print("\n⚠️  Python compatível, mas dependências faltando.")
            print("\n🔧 Execute:")
            print("   ./install.sh")
        else:
            print("\n❌ Python incompatível ou com problemas.")
            print("\n💡 Recomendação: Use Python 3.12")
            print("   • macOS: brew install python@3.12")
            print("   • Ubuntu: sudo apt install python3.12")
            print("   • Ou use pyenv: pyenv install 3.12.0")

        print("\n" + "=" * 70 + "\n")

        sys.exit(0 if (is_compatible and has_deps) else 1)

    except KeyboardInterrupt:
        print("\n\n⚠️  Verificação cancelada")
        sys.exit(1)


if __name__ == "__main__":
    main()
