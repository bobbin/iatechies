# Verificación de Instalación - Tests y Diagnóstico

## Script de Verificación Completo

Crea `verificar_instalacion.py` para diagnosticar tu instalación:

```python
#!/usr/bin/env python3
"""Script de verificación completa de instalación CrewAI"""

import sys
import os
import platform
from dotenv import load_dotenv

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def print_result(test_name, passed, message=""):
    symbol = "✅" if passed else "❌"
    print(f"{symbol} {test_name}")
    if message:
        print(f"   {message}")

def test_python_version():
    """Verificar versión de Python"""
    version = sys.version_info
    passed = version.major == 3 and version.minor >= 9
    print_result(
        "Python 3.9+",
        passed,
        f"Versión: {version.major}.{version.minor}.{version.micro}"
    )
    return passed

def test_system_info():
    """Mostrar información del sistema"""
    print(f"   SO: {platform.system()} {platform.release()}")
    print(f"   Arquitectura: {platform.machine()}")
    return True

def test_dependencies():
    """Verificar dependencias principales"""
    dependencies = {
        'crewai': 'CrewAI Framework',
        'crewai.tools': 'CrewAI Tools',
        'openai': 'OpenAI Client',
        'dotenv': 'Python-dotenv',
        'pydantic': 'Pydantic'
    }
    
    all_passed = True
    for module, name in dependencies.items():
        try:
            __import__(module.replace('.', '/'))
            print_result(name, True)
        except ImportError as e:
            print_result(name, False, str(e))
            all_passed = False
    
    return all_passed

def test_memory():
    """Verificar memoria disponible"""
    try:
        import psutil
        mem = psutil.virtual_memory()
        total_gb = mem.total / (1024**3)
        available_gb = mem.available / (1024**3)
        passed = available_gb >= 4
        
        print_result(
            "Memoria RAM",
            passed,
            f"Total: {total_gb:.1f}GB, Disponible: {available_gb:.1f}GB"
        )
        return passed
    except ImportError:
        print_result("Memoria RAM", False, "Instala psutil: pip install psutil")
        return False

def test_env_file():
    """Verificar archivo .env"""
    if not os.path.exists('.env'):
        print_result("Archivo .env", False, "No encontrado")
        return False
    
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        print_result("OPENAI_API_KEY", False, "No configurada en .env")
        return False
    
    if not api_key.startswith('sk-'):
        print_result("OPENAI_API_KEY", False, "Formato inválido (debe empezar con 'sk-')")
        return False
    
    print_result("OPENAI_API_KEY", True, "Configurada correctamente")
    return True

def test_openai_connection():
    """Verificar conexión con OpenAI"""
    try:
        import openai
        load_dotenv()
        
        client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        models = client.models.list()
        
        print_result("Conexión OpenAI", True, f"{len(list(models.data))} modelos disponibles")
        return True
    except openai.AuthenticationError:
        print_result("Conexión OpenAI", False, "API Key inválida")
        return False
    except Exception as e:
        print_result("Conexión OpenAI", False, str(e))
        return False

def test_basic_agent():
    """Test de agente básico"""
    try:
        from crewai import Agent, Task, Crew, Process
        load_dotenv()
        
        agent = Agent(
            role="Test",
            goal="Verificar funcionamiento",
            backstory="Agente de prueba",
            verbose=False
        )
        
        task = Task(
            description="Di 'OK' si funciona",
            agent=agent,
            expected_output="Confirmación"
        )
        
        crew = Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential,
            verbose=False
        )
        
        result = crew.kickoff()
        print_result("Test de Agente", True, "Ejecutado correctamente")
        return True
    except Exception as e:
        print_result("Test de Agente", False, str(e))
        return False

def main():
    print_header("VERIFICACIÓN DE INSTALACIÓN - CrewAI")
    
    tests = [
        ("Versión de Python", test_python_version),
        ("Información del Sistema", test_system_info),
        ("Dependencias", test_dependencies),
        ("Memoria", test_memory),
        ("Configuración", test_env_file),
        ("Conectividad", test_openai_connection),
        ("Funcionalidad", test_basic_agent)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        try:
            passed = test_func()
            results.append(passed)
        except Exception as e:
            print_result(test_name, False, f"Error inesperado: {e}")
            results.append(False)
    
    # Resumen
    print_header("RESUMEN")
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"✅ TODOS LOS TESTS PASADOS ({passed}/{total})")
        print("\n¡Tu instalación está lista para usar!")
        return 0
    else:
        print(f"⚠️  ALGUNOS TESTS FALLARON ({passed}/{total})")
        print("\nRevisa los errores arriba y consulta la documentación.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
```

## Ejecutar Verificación

```bash
python verificar_instalacion.py
```

## Troubleshooting Común

### Problema: Dependencia falta

**Solución**:
```bash
pip install --upgrade crewai crewai-tools openai python-dotenv
```

### Problema: API Key inválida

**Solución**:
1. Verifica `.env`: `OPENAI_API_KEY=sk-...`
2. Regenera key en https://platform.openai.com/api-keys
3. Sin espacios ni comillas extra

### Problema: Sin créditos OpenAI

**Solución**:
1. Ve a https://platform.openai.com/account/billing
2. Agrega créditos o tarjeta
3. Configura límites de gasto

## Checklist Final

- [ ] Python 3.9+ ✅
- [ ] Entorno virtual activo ✅
- [ ] CrewAI instalado ✅
- [ ] .env configurado ✅
- [ ] OpenAI conectado ✅
- [ ] Test de agente exitoso ✅

¡Listo para comenzar!

