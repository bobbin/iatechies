"""
Ejemplo 14: Simulación NPC tipo "TownAI" (Lite)
===============================================

Complejidad: MEDIA-ALTA

Concepto:
---------
Simulación de comportamiento de NPCs (Non-Player Characters) con:
1.  **Memoria Persistente**: Guardan sus acciones y las de otros en un "Tablón de Anuncios" (cache/log).
2.  **Objetivos Diarios**: Cada agente tiene una meta para el día.
3.  **Ciclo de Día**: El script simula momentos del día (Mañana, Tarde, Noche).

Flujo:
------
1.  **Observar**: El NPC lee el estado del mundo y eventos recientes.
2.  **Decidir**: Basado en su personalidad y objetivo, decide qué hacer.
3.  **Actuar**: Ejecuta una acción que queda registrada en la memoria compartida.

Diferencia con otros ejemplos:
Aquí los agentes reaccionan dinámicamente a lo que hacen los otros agentes
en pasos anteriores, creando una narrativa emergente.
"""

import os
import json
import sys
import io
import time
from datetime import datetime
from typing import List, Dict
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai.tools import tool

# Configurar encoding UTF-8 para consola en Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

load_dotenv()

# ==============================================================================
# SISTEMA DE MEMORIA DEL MUNDO (Town Board)
# ==============================================================================

class WorldMemory:
    """
    Gestiona el estado del mundo y la memoria compartida de los NPCs.
    Actúa como una base de datos/cache simple en JSON.
    """
    def __init__(self, db_path="world_memory.json"):
        # Ruta dinámica para evitar errores de path
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.file_path = os.path.join(base_dir, db_path)
        
        self.reset_memory()

    def reset_memory(self):
        """Reinicia el mundo para una nueva simulación."""
        initial_state = {
            "events": [],
            "locations": {
                "Plaza": "Tranquila, algunos pájaros cantando.",
                "Taberna": "Cerrada por limpieza.",
                "Mercado": "Los puestos se están montando."
            },
            "day_time": "Mañana (08:00 AM)"
        }
        self._save(initial_state)

    def _load(self) -> Dict:
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def _save(self, data: Dict):
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def get_context(self) -> str:
        """Devuelve el contexto actual para que el NPC 'vea'."""
        data = self._load()
        
        # Obtener los últimos 5 eventos
        recent_events = data["events"][-5:] if data["events"] else ["Nada ha pasado aún."]
        recent_events_str = "\n".join([f"- [{e['time']}] {e['actor']}: {e['action']}" for e in recent_events])
        
        return f"""
        🕒 HORA ACTUAL: {data['day_time']}
        
        📍 ESTADO LUGARES:
        {json.dumps(data['locations'], indent=2, ensure_ascii=False)}
        
        📜 EVENTOS RECIENTES (Lo que ha pasado antes):
        {recent_events_str}
        """

    def record_action(self, actor: str, action: str, location: str):
        """Registra una acción en la memoria del mundo."""
        data = self._load()
        
        entry = {
            "time": data["day_time"],
            "actor": actor,
            "action": action,
            "location": location,
            "timestamp": datetime.now().isoformat()
        }
        
        data["events"].append(entry)
        
        # Actualizar estado del lugar (simulado simple)
        # Si la acción implica cambio, actualizamos la descripción del lugar
        if "abrir" in action.lower() or "entra" in action.lower():
            data["locations"][location] = f"Actividad presente. {actor} está aquí."
            
        self._save(data)
        return f"Acción registrada: {actor} hizo '{action}' en {location}"

    def set_time(self, time_str: str):
        data = self._load()
        data["day_time"] = time_str
        self._save(data)

# Instancia global para ser usada por las tools
world = WorldMemory()

# ==============================================================================
# TOOLS PARA LOS AGENTES
# ==============================================================================

@tool("Observar Entorno")
def observar_entorno(dummy: str = "") -> str:
    """
    Permite al NPC mirar a su alrededor, ver qué hora es y recordar qué ha pasado recientemente.
    Siempre usa esta herramienta ANTES de actuar.
    """
    return world.get_context()

@tool("Realizar Acción")
def realizar_accion(accion: str, lugar: str) -> str:
    """
    Registra una acción física en el mundo.
    Args:
        accion: Descripción de lo que haces (ej: "Abro la panadería y pongo el pan").
        lugar: Dónde estás (ej: "Mercado", "Plaza", "Taberna").
    """
    # En crewai, el nombre del agente no se pasa directo a la tool fácilmente sin contexto,
    # así que pedimos al modelo que incluya su nombre en la acción o lo inferimos.
    # Para este ejemplo, asumimos que el modelo narra en tercera persona o primera.
    return world.record_action("NPC", accion, lugar)

# ==============================================================================
# DEFINICIÓN DE AGENTES (NPCs)
# ==============================================================================

# 1. El Panadero (Ciudadano promedio)
panadero = Agent(
    role="Beto el Panadero",
    goal="Vender todo el pan posible y enterarse de los chismes",
    backstory="""Eres Beto, el panadero del pueblo. Te levantas temprano. 
    Eres amable pero muy curioso. Tu objetivo hoy es vender tus baguettes especiales 
    y averiguar por qué el Guardia está tan nervioso.""",
    verbose=True,
    allow_delegation=False,
    tools=[observar_entorno, realizar_accion]
)

# 2. El Guardia (Autoridad)
guardia = Agent(
    role="Sargento Clave",
    goal="Mantener el orden y encontrar al ladrón que robó el escudo del alcalde",
    backstory="""Eres el Sargento Clave. Estás estresado. Ayer robaron el escudo 
    ceremonial del alcalde y si no lo encuentras hoy, estás despedido. 
    Sospechas de todos, especialmente de 'Sombra'.""",
    verbose=True,
    allow_delegation=False,
    tools=[observar_entorno, realizar_accion]
)

# 3. El Pícaro (Elemento de caos)
picaro = Agent(
    role="Sombra (El Pícaro)",
    goal="Robar algo de valor sin ser detectado y burlarse del guardia",
    backstory="""Nadie sabe tu nombre real, te dicen Sombra. 
    Tu objetivo es causar confusión y robar comida o monedas. 
    Te encanta molestar al Sargento Clave pero sin que te atrape.""",
    verbose=True,
    allow_delegation=False,
    tools=[observar_entorno, realizar_accion]
)

# ==============================================================================
# BUCLE DE SIMULACIÓN
# ==============================================================================

def ejecutar_turno(momento_dia: str, descripcion_escenario: str):
    """Ejecuta un turno (mañana, tarde, noche) para todos los agentes."""
    
    # 1. Actualizar reloj del mundo
    world.set_time(momento_dia)
    
    print(f"\n🌞 --- INICIO DE TURNO: {momento_dia} ---")
    print(f"Escenario: {descripcion_escenario}\n")

    # Definimos tareas dinámicas para este turno
    
    # Tarea Beto
    tarea_beto = Task(
        description=f"""
        Es {momento_dia}.
        1. USA la herramienta 'Observar Entorno' para ver qué está pasando y qué han hecho los otros.
        2. Basado en tu memoria y objetivo (Vender pan/Chismear), decide tu próxima acción.
        3. USA 'Realizar Acción' para ejecutarla.
        
        Importante: Reacciona a lo que haya hecho el Guardia o Sombra si lo ves en el registro.
        """,
        agent=panadero,
        expected_output="Acción registrada en el mundo."
    )

    # Tarea Guardia
    tarea_guardia = Task(
        description=f"""
        Es {momento_dia}.
        1. USA 'Observar Entorno'. Busca pistas sobre el robo o comportamientos sospechosos en el registro.
        2. Si ves a Sombra o algo raro, actúa. Si no, patrulla.
        3. USA 'Realizar Acción'.
        """,
        agent=guardia,
        expected_output="Acción registrada en el mundo."
    )

    # Tarea Pícaro
    tarea_picaro = Task(
        description=f"""
        Es {momento_dia}.
        1. USA 'Observar Entorno'. Mira dónde está el Guardia.
        2. Si el Guardia está distraído, intenta robar o hacer una broma.
        3. USA 'Realizar Acción'.
        """,
        agent=picaro,
        expected_output="Acción registrada en el mundo."
    )

    # Creamos el equipo para este turno
    # Nota: Process.sequential significa que actúan en orden (Beto -> Guardia -> Pícaro)
    # Esto simula iniciativa. Podríamos rotar el orden en otros turnos.
    crew_turno = Crew(
        agents=[panadero, guardia, picaro],
        tasks=[tarea_beto, tarea_guardia, tarea_picaro],
        process=Process.sequential,
        verbose=False # Menos ruido en consola, veremos el log del mundo
    )

    crew_turno.kickoff()

def mostrar_resumen_final():
    """Muestra la historia completa generada."""
    data = world._load()
    print("\n" + "="*80)
    print("📜 CRÓNICA DEL DÍA EN VILLA CODE")
    print("="*80)
    
    for evento in data["events"]:
        print(f"⏰ {evento['time']}")
        print(f"👤 {evento['actor']} en {evento['location']}")
        print(f"action: {evento['action']}")
        print("-" * 40)

if __name__ == "__main__":
    # Limpiar memoria anterior
    world.reset_memory()
    
    print("🏘️ INICIANDO SIMULACIÓN DE VILLA CODE")
    print("Objetivo: Simular interacciones emergentes con memoria compartida.\n")

    # --- TURNO 1: MAÑANA ---
    ejecutar_turno(
        "Mañana (08:00 AM)", 
        "El sol sale. El mercado abre. Beto prepara el pan. El Guardia inicia ronda."
    )

    # --- TURNO 2: MEDIODÍA ---
    ejecutar_turno(
        "Mediodía (12:00 PM)", 
        "El sol está alto. Hay mucha gente en la plaza. Hora de comer."
    )

    # --- TURNO 3: TARDE/NOCHE ---
    ejecutar_turno(
        "Tarde (06:00 PM)", 
        "Empieza a oscurecer. La taberna abre sus puertas. El cansancio se nota."
    )

    # Resultado Final
    mostrar_resumen_final()

