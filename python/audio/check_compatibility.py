#!/usr/bin/env python3
"""
Script de Verificação de Compatibilidade Python
Verifica se todos os pacotes funcionam com a versão atual do Python
"""

import sys
import subprocess
import json
from pathlib import Path
from typing import Dict, List, Tuple


def get_python_version() -> Tuple[int, int, int]:
    """Retorna a versão do Python como tupla (major, minor, patch)"""
    return sys.version_info[:3]


def check_python_version_compatibility() -> Dict:
    """Verifica se a versão do Python é compatível com Whisper"""
    major, minor, patch = get_python_version()
    version_str = f"{major}.{minor}.{patch}"

    result = {
        "version": version_str,
        "major": major,
        "minor": minor,
        "patch": patch,
        "compatible": True,
        "warnings": [],
        "errors": [],
    }

    # Verificar compatibilidade conhecida
    if major < 3 or (major == 3 and minor < 8):
        result["compatible"] = False
        result["errors"].append(
            f"Python {version_str} é muito antigo. Whisper requer Python 3.8 ou superior."
        )
    elif major == 3 and minor > 12:
        result["compatible"] = False
        result["errors"].append(
            f"Python {version_str} não é suportado ainda. "
            "Whisper funciona com Python 3.8-3.12. "
            "Python 3.13+ tem problemas com pkg_resources (deprecado)."
        )
        result["errors"].append(
            "Recomendação: Use Python 3.12 ou 3.11 para melhor compatibilidade."
        )
    elif major == 3 and minor == 12:
        result["warnings"].append("Python 3.12 é compatível e recomendado!")

    return result


def get_package_info(package_name: str) -> Dict:
    """Obtém informações sobre um pacote via pip"""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "show", package_name],
            capture_output=True,
            text=True,
            timeout=10,
        )

        if result.returncode != 0:
            return {"installed": False, "error": "Pacote não instalado"}

        info = {}
        for line in result.stdout.split("\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                info[key.strip().lower()] = value.strip()

        return {"installed": True, "info": info}
    except Exception as e:
        return {"installed": False, "error": str(e)}


def check_package_compatibility(
    package_name: str, required_version: str = None
) -> Dict:
    """Verifica compatibilidade de um pacote específico"""
    print(f"  🔍 Verificando {package_name}...", end=" ")

    result = {
        "package": package_name,
        "required": required_version,
        "installed": False,
        "version": None,
        "compatible": False,
        "messages": [],
    }

    pkg_info = get_package_info(package_name)

    if not pkg_info.get("installed"):
        result["messages"].append(
            f"❌ Não instalado: {pkg_info.get('error', 'Desconhecido')}"
        )
        print("❌ Não instalado")
        return result

    result["installed"] = True
    result["version"] = pkg_info["info"].get("version", "Desconhecida")
    result["compatible"] = True
    result["messages"].append(f"✅ Instalado: v{result['version']}")

    print(f"✅ v{result['version']}")
    return result


def test_import_package(package_name: str, import_name: str = None) -> Dict:
    """Testa se um pacote pode ser importado"""
    if import_name is None:
        import_name = package_name

    print(f"  🧪 Testando importação de {import_name}...", end=" ")

    result = {
        "package": package_name,
        "import_name": import_name,
        "can_import": False,
        "error": None,
    }

    try:
        __import__(import_name)
        result["can_import"] = True
        print("✅ OK")
    except ImportError as e:
        result["error"] = str(e)
        print(f"❌ Erro: {e}")
    except Exception as e:
        result["error"] = str(e)
        print(f"⚠️  Aviso: {e}")

    return result


def check_all_dependencies() -> Dict:
    """Verifica todas as dependências do projeto"""

    dependencies = {
        "openai-whisper": {
            "package": "openai-whisper",
            "import": "whisper",
            "required": ">=20250625",
        },
        "torch": {"package": "torch", "import": "torch", "required": ">=2.0.0"},
        "torchaudio": {
            "package": "torchaudio",
            "import": "torchaudio",
            "required": ">=2.0.0",
        },
    }

    results = {"packages": {}, "imports": {}, "all_compatible": True}

    print("\n📦 Verificando pacotes instalados:")
    print("=" * 60)

    for key, dep in dependencies.items():
        pkg_result = check_package_compatibility(dep["package"], dep["required"])
        results["packages"][key] = pkg_result

        if not pkg_result["installed"] or not pkg_result["compatible"]:
            results["all_compatible"] = False

    print("\n🧪 Testando importações:")
    print("=" * 60)

    for key, dep in dependencies.items():
        if results["packages"][key]["installed"]:
            import_result = test_import_package(dep["package"], dep["import"])
            results["imports"][key] = import_result

            if not import_result["can_import"]:
                results["all_compatible"] = False

    return results


def check_system_requirements() -> Dict:
    """Verifica requisitos do sistema (FFmpeg, etc)"""
    print("\n🖥️  Verificando requisitos do sistema:")
    print("=" * 60)

    results = {"ffmpeg": {"installed": False}}

    # Verificar FFmpeg
    print("  🔍 Verificando FFmpeg...", end=" ")
    try:
        result = subprocess.run(
            ["ffmpeg", "-version"], capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            version_line = result.stdout.split("\n")[0]
            results["ffmpeg"]["installed"] = True
            results["ffmpeg"]["version"] = version_line
            print(f"✅ Instalado")
            print(f"     {version_line}")
        else:
            print("❌ Não encontrado")
    except FileNotFoundError:
        print("❌ Não encontrado")
        results["ffmpeg"]["install_hint"] = {
            "macOS": "brew install ffmpeg",
            "Linux": "sudo apt update && sudo apt install ffmpeg",
            "Windows": "choco install ffmpeg",
        }
    except Exception as e:
        print(f"⚠️  Erro: {e}")
        results["ffmpeg"]["error"] = str(e)

    return results


def generate_report(python_check: Dict, deps_check: Dict, system_check: Dict):
    """Gera relatório completo"""
    print("\n" + "=" * 70)
    print("📊 RELATÓRIO DE COMPATIBILIDADE")
    print("=" * 70)

    # Python
    print(f"\n🐍 Python: {python_check['version']}")
    if python_check["compatible"]:
        print("   Status: ✅ COMPATÍVEL")
    else:
        print("   Status: ❌ INCOMPATÍVEL")

    for warning in python_check.get("warnings", []):
        print(f"   ⚠️  {warning}")

    for error in python_check.get("errors", []):
        print(f"   ❌ {error}")

    # Pacotes
    print("\n📦 Pacotes Python:")
    all_installed = True
    for pkg_name, pkg_info in deps_check["packages"].items():
        status = "✅" if pkg_info["installed"] else "❌"
        version = f"v{pkg_info['version']}" if pkg_info["version"] else "N/A"
        print(f"   {status} {pkg_info['package']}: {version}")
        if not pkg_info["installed"]:
            all_installed = False

    # Importações
    print("\n🧪 Importações:")
    all_imports_ok = True
    for pkg_name, import_info in deps_check["imports"].items():
        status = "✅" if import_info["can_import"] else "❌"
        print(f"   {status} {import_info['import_name']}")
        if not import_info["can_import"]:
            all_imports_ok = False
            if import_info["error"]:
                print(f"      Erro: {import_info['error']}")

    # Sistema
    print("\n🖥️  Sistema:")
    ffmpeg_status = "✅" if system_check["ffmpeg"]["installed"] else "❌"
    print(f"   {ffmpeg_status} FFmpeg")

    if (
        not system_check["ffmpeg"]["installed"]
        and "install_hint" in system_check["ffmpeg"]
    ):
        print(f"\n   💡 Como instalar FFmpeg:")
        for os_name, cmd in system_check["ffmpeg"]["install_hint"].items():
            print(f"      {os_name}: {cmd}")

    # Conclusão
    print("\n" + "=" * 70)
    if (
        python_check["compatible"]
        and deps_check["all_compatible"]
        and system_check["ffmpeg"]["installed"]
    ):
        print("✅ SISTEMA PRONTO PARA USO!")
        print("\nVocê pode executar:")
        print("  python3 transcribe_audio.py data/sample_audio_file.m4a")
    else:
        print("⚠️  CONFIGURAÇÃO INCOMPLETA")
        print("\nAções necessárias:")

        if not python_check["compatible"]:
            print("  1. Instalar Python 3.8-3.12 (recomendado: 3.12)")

        if not all_installed:
            print("  2. Instalar dependências:")
            print("     pip3 install -r requirements.txt")

        if not system_check["ffmpeg"]["installed"]:
            print("  3. Instalar FFmpeg (veja instruções acima)")

    print("=" * 70 + "\n")


def main():
    print("=" * 70)
    print("🔬 VERIFICADOR DE COMPATIBILIDADE - Whisper Transcription")
    print("=" * 70)

    # Verificar Python
    print("\n🐍 Verificando versão do Python:")
    print("=" * 60)
    python_check = check_python_version_compatibility()
    print(f"  Python detectado: {python_check['version']}")

    # Verificar dependências
    deps_check = check_all_dependencies()

    # Verificar sistema
    system_check = check_system_requirements()

    # Gerar relatório
    generate_report(python_check, deps_check, system_check)

    # Código de saída
    if (
        python_check["compatible"]
        and deps_check["all_compatible"]
        and system_check["ffmpeg"]["installed"]
    ):
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
