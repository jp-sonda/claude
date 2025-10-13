#!/usr/bin/env python3
"""
Verificador Avançado de Dependências Transitivas
Analisa toda a árvore de dependências e testa compatibilidade
"""

import sys
import subprocess
import json
from typing import Dict, List, Set


def get_installed_packages() -> Dict[str, str]:
    """Lista todos os pacotes instalados com versões"""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "list", "--format=json"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            packages = json.loads(result.stdout)
            return {pkg["name"]: pkg["version"] for pkg in packages}
        return {}
    except Exception as e:
        print(f"❌ Erro ao listar pacotes: {e}")
        return {}


def get_package_dependencies(package_name: str) -> Dict:
    """Obtém dependências de um pacote (transitivas)"""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "show", package_name],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode != 0:
            return {"error": "Pacote não encontrado"}
        
        info = {"name": package_name, "requires": [], "required_by": []}
        
        for line in result.stdout.split('\n'):
            if line.startswith('Requires:'):
                deps = line.split(':', 1)[1].strip()
                if deps:
                    info["requires"] = [d.strip() for d in deps.split(',')]
            elif line.startswith('Required-by:'):
                deps = line.split(':', 1)[1].strip()
                if deps:
                    info["required_by"] = [d.strip() for d in deps.split(',')]
            elif line.startswith('Version:'):
                info["version"] = line.split(':', 1)[1].strip()
        
        return info
    except Exception as e:
        return {"error": str(e)}


def build_dependency_tree(package_name: str, visited: Set[str] = None, level: int = 0) -> Dict:
    """Constrói árvore de dependências recursivamente"""
    if visited is None:
        visited = set()
    
    if package_name in visited or level > 5:  # Evitar loops infinitos
        return None
    
    visited.add(package_name)
    
    info = get_package_dependencies(package_name)
    if "error" in info:
        return None
    
    tree = {
        "name": package_name,
        "version": info.get("version", "unknown"),
        "level": level,
        "dependencies": []
    }
    
    for dep in info.get("requires", []):
        dep_tree = build_dependency_tree(dep, visited.copy(), level + 1)
        if dep_tree:
            tree["dependencies"].append(dep_tree)
    
    return tree


def print_tree(tree: Dict, indent: str = "", is_last: bool = True):
    """Imprime árvore de dependências de forma visual"""
    if not tree:
        return
    
    connector = "└── " if is_last else "├── "
    print(f"{indent}{connector}{tree['name']} (v{tree['version']})")
    
    new_indent = indent + ("    " if is_last else "│   ")
    
    deps = tree.get("dependencies", [])
    for i, dep in enumerate(deps):
        is_last_dep = (i == len(deps) - 1)
        print_tree(dep, new_indent, is_last_dep)


def check_python_313_problematic_packages() -> List[Dict]:
    """Lista pacotes conhecidos por terem problemas com Python 3.13"""
    problematic = []
    
    installed = get_installed_packages()
    
    # Pacotes conhecidos com problemas no Python 3.13
    known_issues = {
        "setuptools": {
            "issue": "pkg_resources deprecated",
            "solution": "Usar importlib.metadata"
        },
        "pkg-resources": {
            "issue": "Deprecated no Python 3.13",
            "solution": "Remover ou atualizar pacotes que dependem dele"
        }
    }
    
    for pkg_name, issue_info in known_issues.items():
        if pkg_name in installed:
            problematic.append({
                "package": pkg_name,
                "version": installed[pkg_name],
                "issue": issue_info["issue"],
                "solution": issue_info["solution"]
            })
    
    return problematic


def analyze_whisper_dependencies():
    """Análise completa das dependências do Whisper"""
    print("=" * 70)
    print("🔬 ANÁLISE DE DEPENDÊNCIAS TRANSITIVAS - OpenAI Whisper")
    print("=" * 70)
    
    major, minor, patch = sys.version_info[:3]
    python_version = f"{major}.{minor}.{patch}"
    
    print(f"\n🐍 Python: {python_version}")
    
    if major == 3 and minor >= 13:
        print("   ⚠️  ATENÇÃO: Python 3.13+ pode ter problemas de compatibilidade!")
    elif major == 3 and 8 <= minor <= 12:
        print("   ✅ Versão compatível!")
    else:
        print("   ❌ Versão não suportada!")
    
    # Verificar se openai-whisper está instalado
    installed = get_installed_packages()
    
    if "openai-whisper" not in installed:
        print("\n⚠️  openai-whisper não está instalado!")
        print("   Execute: pip3 install -r requirements.txt")
        return
    
    print(f"\n📦 openai-whisper v{installed['openai-whisper']} está instalado")
    
    # Construir árvore de dependências
    print("\n🌳 Árvore de Dependências:")
    print("-" * 70)
    tree = build_dependency_tree("openai-whisper")
    if tree:
        print_tree(tree, "", True)
    else:
        print("❌ Não foi possível construir a árvore de dependências")
    
    # Verificar problemas conhecidos com Python 3.13
    if major == 3 and minor >= 13:
        print("\n⚠️  Verificando problemas conhecidos com Python 3.13:")
        print("-" * 70)
        problematic = check_python_313_problematic_packages()
        
        if problematic:
            for pkg in problematic:
                print(f"\n❌ {pkg['package']} v{pkg['version']}")
                print(f"   Problema: {pkg['issue']}")
                print(f"   Solução: {pkg['solution']}")
        else:
            print("✅ Nenhum problema conhecido detectado nos pacotes instalados")
    
    # Estatísticas
    print("\n📊 Estatísticas:")
    print("-" * 70)
    
    def count_deps(tree: Dict) -> int:
        if not tree:
            return 0
        return 1 + sum(count_deps(dep) for dep in tree.get("dependencies", []))
    
    total_deps = count_deps(tree) - 1  # -1 para não contar o próprio whisper
    print(f"   Total de dependências (transitivas): {total_deps}")
    print(f"   Total de pacotes instalados: {len(installed)}")
    
    # Recomendações
    print("\n💡 Recomendações:")
    print("-" * 70)
    
    if major == 3 and minor >= 13:
        print("   ⚠️  USE PYTHON 3.12 ou 3.11 para melhor compatibilidade")
        print("   📥 Downgrade: pyenv install 3.12.8 && pyenv local 3.12.8")
    elif major == 3 and minor == 12:
        print("   ✅ Você está usando a versão recomendada!")
    else:
        print("   ✅ Sua versão é compatível, mas considere atualizar para 3.12")
    
    print("\n" + "=" * 70 + "\n")


def main():
    analyze_whisper_dependencies()


if __name__ == '__main__':
    main()
