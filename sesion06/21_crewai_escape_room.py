"""
Ejercicio 21 — Diseña un Escape Room IA Multiagente.

Un equipo de agentes que diseña, valida y prueba un Escape Room
interactivo que el usuario puede jugar por chat.
"""

from __future__ import annotations

import os
from pathlib import Path

from crewai import Agent, Task, Crew, Process
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv


# Tools opcionales para el crew
@tool
def get_random_word(categoria: str = "objeto") -> str:
    """
    Genera una palabra aleatoria de una categoría para inspirar elementos del puzzle.
    Úsalo cuando necesites ideas para objetos, lugares o conceptos.
    
    Args:
        categoria: Categoría de la palabra (ej: "objeto", "lugar", "concepto").
    """
    palabras = {
        "objeto": ["llave", "candado", "código", "mapa", "piedra", "espejo", "reloj"],
        "lugar": ["biblioteca", "laboratorio", "mazmorra", "torre", "cripta", "templo"],
        "concepto": ["tiempo", "reflexión", "orden", "secuencia", "patrón", "símbolo"],
    }
    import random
    opciones = palabras.get(categoria.lower(), palabras["objeto"])
    return random.choice(opciones)


@tool
def generate_cipher(tipo: str, texto: str, clave: str = "") -> str:
    """
    Genera un texto cifrado usando diferentes tipos de cifrado.
    Úsalo para crear puzzles de descifrado.
    
    Args:
        tipo: Tipo de cifrado ("cesar", "inverso", "numerico").
        texto: Texto a cifrar.
        clave: Clave para el cifrado (opcional).
    """
    if tipo.lower() == "cesar":
        # Cifrado César simple (desplazamiento de 3)
        desplazamiento = 3
        resultado = ""
        for char in texto.upper():
            if char.isalpha():
                resultado += chr((ord(char) - ord('A') + desplazamiento) % 26 + ord('A'))
            else:
                resultado += char
        return resultado
    elif tipo.lower() == "inverso":
        return texto[::-1]
    elif tipo.lower() == "numerico":
        return " ".join([str(ord(c)) for c in texto])
    return texto


def load_env() -> None:
    load_dotenv(Path(__file__).resolve().parent.parent / "sesion03" / ".env", override=False)


def main() -> None:
    print("🟦 EJERCICIO 21: DISEÑA UN ESCAPE ROOM IA MULTIAGENTE\n")
    
    load_env()
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: Configura OPENAI_API_KEY en el archivo .env")
        return
    
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
    
    # ============================================================
    # 1. DEFINICIÓN DE AGENTES ESPECIALIZADOS
    # ============================================================
    
    story_weaver = Agent(
        role="Story Weaver (Narrative Agent)",
        goal="Crear una narrativa coherente y envolvente para el Escape Room",
        backstory=(
            "Eres un escritor experto en narrativas interactivas. Tu trabajo es crear "
            "historias que sumerjan al jugador en un mundo coherente. Te aseguras de que "
            "la ambientación, los personajes y el tono sean consistentes. Si una puerta "
            "estaba cerrada, sigue cerrada. Si un objeto no existía antes, no puede aparecer "
            "mágicamente sin explicación. Puedes usar herramientas como get_random_word "
            "para inspirarte en elementos del puzzle."
        ),
        verbose=True,
        allow_delegation=False,
        # Tools opcionales - comentadas para evitar problemas de compatibilidad
        # tools=[get_random_word],
        llm=llm,
    )
    
    puzzle_architect = Agent(
        role="Puzzle Architect",
        goal="Diseñar acertijos lógicos, resolubles y equilibrados",
        backstory=(
            "Eres un diseñador de puzzles con años de experiencia. Creas acertijos que son "
            "desafiantes pero justos. Te aseguras de que cada puzzle sea resoluble usando "
            "solo texto y lógica, sin requerir conocimientos externos específicos. "
            "Defines mecánicas claras, reglas consistentes y niveles de dificultad apropiados. "
            "Puedes usar herramientas como generate_cipher para crear puzzles de descifrado "
            "o get_random_word para inspirarte."
        ),
        verbose=True,
        allow_delegation=False,
        # Tools opcionales - comentadas para evitar problemas de compatibilidad
        # tools=[generate_cipher, get_random_word],
        llm=llm,
    )
    
    clue_designer = Agent(
        role="Clue Designer",
        goal="Generar pistas progresivas, coherentes y útiles",
        backstory=(
            "Eres un maestro de las pistas. Sabes cómo dar información suficiente sin "
            "revelar la solución directamente. Tus pistas son progresivas: empiezan sutiles "
            "y se vuelven más claras si el jugador se bloquea. Siempre mantienes coherencia "
            "con la narrativa: las pistas tienen sentido en el contexto de la historia."
        ),
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )
    
    logic_guardian = Agent(
        role="Logic Guardian (Consistency & Logic)",
        goal="Asegurar coherencia lógica y detectar contradicciones",
        backstory=(
            "Eres el guardián de la lógica. Tu trabajo es revisar que todo tenga sentido: "
            "que los puzzles sean coherentes, que las pistas realmente lleven a la solución, "
            "que no haya contradicciones en la narrativa. Si encuentras problemas, los "
            "señalas claramente y puedes pedir correcciones a otros agentes."
        ),
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )
    
    puzzle_tester = Agent(
        role="Puzzle Tester (QA Agent)",
        goal="Probar el Escape Room y evaluar su equilibrio",
        backstory=(
            "Eres un tester experto. 'Juegas' el Escape Room de forma abreviada para "
            "verificar que es resoluble, que el nivel de dificultad es apropiado, y que "
            "las pistas funcionan correctamente. Simulas errores comunes de usuarios y "
            "verificas que las reacciones del sistema sean adecuadas."
        ),
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )
    
    document_compiler = Agent(
        role="Document Compiler",
        goal="Compilar todo el Escape Room en un documento markdown completo y guardarlo",
        backstory=(
            "Eres un editor experto que compila documentos técnicos. Tu trabajo es tomar "
            "todos los elementos del Escape Room (narrativa, puzzle, pistas, validación, test) "
            "y crear un documento markdown completo, bien estructurado y listo para usar. "
            "El documento debe ser claro, completo y fácil de seguir para implementar el Escape Room."
        ),
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )
    
    # ============================================================
    # 2. DEFINICIÓN DE TAREAS
    # ============================================================
    
    tarea_narrativa = Task(
        description=(
            "Crea la narrativa base del Escape Room. Define:\n"
            "1. Escenario y ambientación (ej: biblioteca antigua, laboratorio secreto, templo perdido)\n"
            "2. Historia de fondo (¿por qué está el jugador ahí? ¿cuál es el objetivo?)\n"
            "3. Reglas del mundo (no magia a menos que sea parte de la historia, objetos limitados)\n"
            "4. Tono y estilo narrativo\n"
            "\n"
            "La narrativa debe ser coherente y permitir que los puzzles encajen naturalmente."
        ),
        expected_output="Narrativa completa con escenario, historia, reglas y tono",
        agent=story_weaver,
    )
    
    tarea_puzzle = Task(
        description=(
            "Diseña un puzzle principal para el Escape Room basado en la narrativa creada. "
            "El puzzle debe:\n"
            "1. Ser resoluble usando solo texto y lógica\n"
            "2. Tener una solución clara y definida\n"
            "3. Tener pasos intermedios identificables\n"
            "4. Ser de dificultad media (ni demasiado fácil ni imposible)\n"
            "5. Encajar con la narrativa del Story Weaver\n"
            "\n"
            "Si necesitas crear puzzles de descifrado, puedes mencionar el uso de cifrados "
            "como César, inverso o numérico."
        ),
        expected_output="Puzzle completo con mecánica, solución y pasos necesarios",
        agent=puzzle_architect,
        context=[tarea_narrativa],
    )
    
    tarea_pistas = Task(
        description=(
            "Genera 3-4 pistas progresivas para el puzzle diseñado. Las pistas deben:\n"
            "1. Ser coherentes con la narrativa\n"
            "2. Ser progresivas (empezar sutiles, volverse más claras)\n"
            "3. No revelar la solución directamente\n"
            "4. Tener sentido en el contexto de la historia\n"
            "5. Proporcionar feedback útil si el jugador se bloquea\n"
            "\n"
            "Incluye también cómo y cuándo se revelarían estas pistas al jugador."
        ),
        expected_output="Lista de 3-4 pistas progresivas con contexto de cuándo revelarlas",
        agent=clue_designer,
        context=[tarea_narrativa, tarea_puzzle],
    )
    
    tarea_validacion = Task(
        description=(
            "Valida la coherencia total del Escape Room. Revisa:\n"
            "1. ¿La narrativa y el puzzle encajan?\n"
            "2. ¿Las pistas realmente llevan a la solución?\n"
            "3. ¿Hay contradicciones lógicas?\n"
            "4. ¿Los objetos y elementos mencionados son consistentes?\n"
            "5. ¿El flujo narrativo tiene sentido?\n"
            "\n"
            "Si encuentras problemas, identifícalos claramente. Si todo está bien, aprueba el diseño."
        ),
        expected_output="Reporte de validación con problemas encontrados (si los hay) o aprobación",
        agent=logic_guardian,
        context=[tarea_narrativa, tarea_puzzle, tarea_pistas],
    )
    
    tarea_test = Task(
        description=(
            "Prueba el Escape Room completo. Simula jugarlo y verifica:\n"
            "1. ¿Es resoluble siguiendo las pistas?\n"
            "2. ¿El nivel de dificultad es apropiado?\n"
            "3. ¿Las pistas funcionan correctamente?\n"
            "4. ¿Hay puntos donde el jugador podría bloquearse sin solución?\n"
            "\n"
            "Proporciona un informe con recomendaciones de mejora si es necesario."
        ),
        expected_output="Informe de testing con evaluación del equilibrio y recomendaciones",
        agent=puzzle_tester,
        context=[tarea_narrativa, tarea_puzzle, tarea_pistas, tarea_validacion],
    )
    
    tarea_compilacion = Task(
        description=(
            "Compila todo el Escape Room en un documento markdown completo y bien estructurado. "
            "El documento debe incluir:\n"
            "1. Título y descripción del Escape Room\n"
            "2. Narrativa completa (escenario, historia, reglas del mundo)\n"
            "3. Puzzle principal (mecánica, solución, pasos)\n"
            "4. Pistas progresivas (con indicación de cuándo revelarlas)\n"
            "5. Resumen de validación (si hubo problemas o está aprobado)\n"
            "6. Resultado del testing (evaluación y recomendaciones)\n"
            "7. Instrucciones para implementar el Escape Room en un chat\n"
            "\n"
            "El documento debe estar en formato markdown, bien formateado, y listo para guardar. "
            "Usa encabezados, listas, bloques de código si es necesario, y asegúrate de que sea "
            "fácil de leer y seguir."
        ),
        expected_output="Documento markdown completo con todo el Escape Room estructurado",
        agent=document_compiler,
        context=[tarea_narrativa, tarea_puzzle, tarea_pistas, tarea_validacion, tarea_test],
    )
    
    # ============================================================
    # 3. CREACIÓN DEL CREW
    # ============================================================
    
    crew = Crew(
        agents=[
            story_weaver,
            puzzle_architect,
            clue_designer,
            logic_guardian,
            puzzle_tester,
            document_compiler,
        ],
        tasks=[
            tarea_narrativa,
            tarea_puzzle,
            tarea_pistas,
            tarea_validacion,
            tarea_test,
            tarea_compilacion,
        ],
        verbose=True,
        process=Process.sequential,  # Flujo secuencial: cada tarea depende de la anterior
    )
    
    # ============================================================
    # 4. EJECUCIÓN
    # ============================================================
    
    print("=" * 60)
    print("EQUIPO MULTIAGENTE PARA DISEÑAR ESCAPE ROOM")
    print("=" * 60)
    print("\n👥 Agentes del equipo:")
    print("   1. 🧩 Puzzle Architect - Diseña los acertijos")
    print("   2. 🔎 Clue Designer - Genera pistas progresivas")
    print("   3. 📜 Story Weaver - Crea la narrativa")
    print("   4. ✔️  Logic Guardian - Valida coherencia")
    print("   5. 🧪 Puzzle Tester - Prueba el Escape Room")
    print("   6. 📄 Document Compiler - Compila todo en markdown")
    
    print("\n📋 Flujo de trabajo:")
    print("   Story Weaver → Puzzle Architect → Clue Designer → Logic Guardian → Puzzle Tester → Document Compiler")
    print("\n   Cada agente trabaja en su especialidad y pasa el resultado al siguiente.")
    
    print("\n💡 Nota sobre Tools:")
    print("   Las tools (get_random_word, generate_cipher) están disponibles como funciones")
    print("   que los agentes pueden usar conceptualmente. En producción, podrías")
    print("   integrarlas usando el formato correcto de CrewAI.")
    
    print("\n🚀 Iniciando diseño del Escape Room...\n")
    
    try:
        resultado = crew.kickoff()
        
        print("\n" + "=" * 60)
        print("ESCAPE ROOM DISEÑADO")
        print("=" * 60)
        print(resultado)
        
        # Extraer el documento markdown del resultado
        documento_markdown = str(resultado)
        
        # Guardar en archivo
        output_dir = Path("data")
        output_dir.mkdir(exist_ok=True)
        output_file = output_dir / "escape_room_disenado.md"
        
        # Mejorar el formato del markdown si es necesario
        contenido_markdown = f"""# Escape Room Diseñado por Equipo Multiagente

*Generado automáticamente por el equipo de agentes especializados*

---

{documento_markdown}

---

*Documento generado por: Story Weaver, Puzzle Architect, Clue Designer, Logic Guardian, Puzzle Tester, Document Compiler*
"""
        
        output_file.write_text(contenido_markdown, encoding="utf-8")
        
        print("\n" + "=" * 60)
        print("📄 DOCUMENTO GUARDADO")
        print("=" * 60)
        print(f"   ✅ Escape Room guardado en: {output_file}")
        print(f"   📊 Tamaño: {len(contenido_markdown)} caracteres")
        print(f"   📝 Puedes abrirlo para ver el diseño completo")
        
        print("\n" + "=" * 60)
        print("💡 PRÓXIMOS PASOS")
        print("=" * 60)
        print("""
   Con este diseño, podrías:
   1. Revisar el documento markdown guardado
   2. Implementar el Escape Room en un chat interactivo
   3. Usar el resultado como base para un juego real
   4. Iterar sobre el diseño basándote en el feedback del tester
   5. Agregar más puzzles siguiendo el mismo proceso
   
   El equipo multiagente asegura que el Escape Room sea:
   ✅ Narrativamente coherente
   ✅ Lógicamente consistente
   ✅ Con puzzles bien diseñados
   ✅ Con pistas útiles y progresivas
   ✅ Probado y equilibrado
   ✅ Documentado completamente
        """)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("=" * 60)
    print("💡 OBSERVACIONES SOBRE EL DISEÑO")
    print("=" * 60)
    print("""
   Este ejercicio demuestra:
   - Cómo diferentes especialistas colaboran en un proyecto complejo
   - La importancia de la validación y testing
   - Cómo las tools pueden enriquecer el proceso creativo
   - La coordinación entre agentes con diferentes responsabilidades
   
   Flujo elegido: Secuencial
   - Cada tarea depende de la anterior
   - Permite que cada agente vea el trabajo previo
   - Asegura coherencia en cada paso
   - El Logic Guardian valida antes del test final
   - El Document Compiler crea el documento final completo
        """)
    print("=" * 60)


if __name__ == "__main__":
    main()

