import os
from datetime import datetime

def limpiar_consola():
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_menu(): 

    print("\nMENÚ DE OPCIONES:")
    print("1. Registrar equipo")
    print("2. Programar fecha")
    print("3. Registrar marcador de un partido")
    print("4. Ver equipo con más goles a favor")
    print("5. Ver equipo con más goles en contra")
    print("6. Registrar plantel de un equipo")
    print("7. Salir")

def inscribir_equipo(conjunto_equipos):

    while True:
        nombre_nuevo_equipo = input("Introduce el nombre del nuevo equipo: ").strip().lower()
        if not nombre_nuevo_equipo:
            print("Error: El nombre del equipo no puede estar vacío. Inténtalo de nuevo.")
        elif nombre_nuevo_equipo in conjunto_equipos:
            print("Error: El equipo ya está registrado. Inténtalo con otro nombre.")
        else:
            conjunto_equipos[nombre_nuevo_equipo] = {
                "pj": 0, "pg": 0, "pp": 0, "pe": 0, "gf": 0, "gc": 0, 
                "plantel": {"jugadores": [], "cuerpo_tecnico": []} 
            }
            print(f"¡Equipo '{nombre_nuevo_equipo}' registrado con éxito!")
            break

def definir_encuentro(conjunto_equipos, agenda_partidos):

    if len(conjunto_equipos) < 2:
        print("Necesitas al menos dos equipos registrados para programar una fecha.")
        return

    print("Equipos disponibles:", ", ".join(conjunto_equipos.keys()))

    while True:
        equipo_local = input("Introduce el nombre del equipo local: ").strip().lower()
        if not equipo_local:
            print("Error: El nombre del equipo local no puede estar vacío.")
        elif equipo_local not in conjunto_equipos:
            print("Error: El equipo local no está registrado. Por favor, regístralo primero.")
        else:
            break
    
    while True:
        equipo_visitante = input("Introduce el nombre del equipo visitante: ").strip().lower()
        if not equipo_visitante:
            print("Error: El nombre del equipo visitante no puede estar vacío.")
        elif equipo_visitante not in conjunto_equipos:
            print("Error: El equipo visitante no está registrado. Por favor, regístralo primero.")
        elif equipo_local == equipo_visitante:
            print("Error: Un equipo no puede jugar contra sí mismo. Elige otro equipo visitante.")
        else:
            break
    
    while True:
        fecha_str = input("Introduce la fecha del partido (DD-MM-AAAA): ").strip()
        if not fecha_str:
            print("Error: La fecha no puede estar vacía.")
            continue
        try:
            dia, mes, anno = map(int, fecha_str.split('-'))
            fecha_partido = datetime(anno, mes, dia)
            
            # Fechas en el pasado 
            if fecha_partido < datetime.now().replace(hour=0, minute=0, second=0, microsecond=0):
                print("Error: No puedes programar un partido en una fecha anterior a la actual.")
                continue

            #  Duplicidad de partidos 
            partido_ya_existe = False
            for partido_existente in agenda_partidos:
                if (partido_existente["local"] == equipo_local and 
                    partido_existente["visitante"] == equipo_visitante and 
                    partido_existente["fecha"] == fecha_partido.strftime("%d-%m-%Y")):
                    partido_ya_existe = True
                    break
            
            if partido_ya_existe:
                print(f"Error: Ya existe un partido programado entre '{equipo_local.capitalize()}' y '{equipo_visitante.capitalize()}' para la fecha {fecha_partido.strftime('%d-%m-%Y')}.")
                continue

            break
        except ValueError:
            print("Error: Formato de fecha incorrecto o fecha inválida. Usa DD-MM-AAAA.")

    partido_nuevo = {
        "local": equipo_local,
        "visitante": equipo_visitante,
        "marcador_local": None,
        "marcador_visitante": None,
        "fecha": fecha_partido.strftime("%d-%m-%Y") 
    }
    agenda_partidos.append(partido_nuevo)
    print(f"Partido '{equipo_local.capitalize()} vs {equipo_visitante.capitalize()}' programado para el {partido_nuevo['fecha']}.")

def cargar_marcador(conjunto_equipos, agenda_partidos):

    encuentros_por_resolver = [p for p in agenda_partidos if p["marcador_local"] is None]
    
    if not encuentros_por_resolver:
        print("No hay partidos pendientes de registrar marcador.")
        return

    print("\nPartidos pendientes:")
    for i, encuentro in enumerate(encuentros_por_resolver):
        if encuentro['local'] in conjunto_equipos and encuentro['visitante'] in conjunto_equipos:
            print(f"{i + 1}. {encuentro['local'].capitalize()} vs {encuentro['visitante'].capitalize()} (Fecha: {encuentro.get('fecha', 'No especificada')})")
        else:
            print(f"{i + 1}. (Partido con equipo(s) no registrado(s)) {encuentro['local'].capitalize()} vs {encuentro['visitante'].capitalize()} (Fecha: {encuentro.get('fecha', 'No especificada')}) - No se puede registrar marcador.")
            # Si un equipo no existe, este partido no debería ser seleccionable para cargar marcador

    while True:
        try:
            seleccion = input("Selecciona el número del partido para registrar el marcador: ").strip()
            if not seleccion:
                print("Error: La selección no puede estar vacía.")
                continue
            seleccion = int(seleccion) - 1
            if 0 <= seleccion < len(encuentros_por_resolver):
                partido_seleccionado = encuentros_por_resolver[seleccion]
                
                if partido_seleccionado['local'] not in conjunto_equipos or partido_seleccionado['visitante'] not in conjunto_equipos:
                    print("Error: Uno o ambos equipos de este partido ya no están registrados. No se puede registrar el marcador.")
                    return # Se sale de la función si los equipos no existen

                while True:
                    try:
                        goles_local_str = input(f"Goles de {partido_seleccionado['local'].capitalize()}: ").strip()
                        if not goles_local_str:
                            print("Error: Los goles del equipo local no pueden estar vacíos.")
                            continue
                        goles_local = int(goles_local_str)
                        if goles_local < 0:
                            print("Error: Los goles no pueden ser números negativos.")
                            continue
                        break
                    except ValueError:
                        print("Error: Debes introducir un número entero para los goles.")

                while True:
                    try:
                        goles_visitante_str = input(f"Goles de {partido_seleccionado['visitante'].capitalize()}: ").strip()
                        if not goles_visitante_str:
                            print("Error: Los goles del equipo visitante no pueden estar vacíos.")
                            continue
                        goles_visitante = int(goles_visitante_str)
                        if goles_visitante < 0:
                            print("Error: Los goles no pueden ser números negativos.")
                            continue
                        break
                    except ValueError:
                        print("Error: Debes introducir un número entero para los goles.")

                partido_seleccionado["marcador_local"] = goles_local
                partido_seleccionado["marcador_visitante"] = goles_visitante

                equipo_local_actual = partido_seleccionado["local"]
                equipo_visitante_actual = partido_seleccionado["visitante"]

                conjunto_equipos[equipo_local_actual]["pj"] += 1
                conjunto_equipos[equipo_visitante_actual]["pj"] += 1
                conjunto_equipos[equipo_local_actual]["gf"] += goles_local
                conjunto_equipos[equipo_visitante_actual]["gf"] += goles_visitante
                conjunto_equipos[equipo_local_actual]["gc"] += goles_visitante
                conjunto_equipos[equipo_visitante_actual]["gc"] += goles_local

                if goles_local > goles_visitante:
                    conjunto_equipos[equipo_local_actual]["pg"] += 1
                    conjunto_equipos[equipo_visitante_actual]["pp"] += 1
                elif goles_visitante > goles_local:
                    conjunto_equipos[equipo_visitante_actual]["pg"] += 1
                    conjunto_equipos[equipo_local_actual]["pp"] += 1
                else:
                    conjunto_equipos[equipo_local_actual]["pe"] += 1
                    conjunto_equipos[equipo_visitante_actual]["pe"] += 1
                
                print("Marcador registrado y estadísticas actualizadas.")
                break 
            else:
                print("Opción no válida. Por favor, selecciona un número de la lista.")
        except ValueError:
            print("Error: Debes introducir un número válido.")

def equipo_mas_goles_favor(conjunto_equipos):

    if not conjunto_equipos:
        print("No hay equipos registrados para calcular.")
        return
    
    equipos_con_goles = {equipo: data for equipo, data in conjunto_equipos.items() if data['gf'] > 0}
    
    if not equipos_con_goles:
        print("Ningún equipo ha anotado goles aún.")
        return

    equipo_max_gf = max(equipos_con_goles, key=lambda e: equipos_con_goles[e]['gf'])
    print(f"El equipo con más goles a favor es: {equipo_max_gf.capitalize()} ({conjunto_equipos[equipo_max_gf]['gf']} goles).")

def equipo_mas_goles_contra(conjunto_equipos):

    if not conjunto_equipos:
        print("No hay equipos registrados para calcular.")
        return
    
    equipos_con_goles_en_contra = {equipo: data for equipo, data in conjunto_equipos.items() if data['gc'] > 0}

    if not equipos_con_goles_en_contra:
        print("Ningún equipo ha recibido goles aún.")
        return
    
    equipo_max_gc = max(equipos_con_goles_en_contra, key=lambda e: equipos_con_goles_en_contra[e]['gc'])
    print(f"El equipo con más goles en contra es: {equipo_max_gc.capitalize()} ({conjunto_equipos[equipo_max_gc]['gc']} goles).")

#  Función para agregar jugador 
def agregar_jugador(conjunto_equipos, nombre_equipo):

    while True:
        nombre = input("Nombre del jugador: ").strip().capitalize()
        if not nombre:
            print("Error: El nombre del jugador no puede estar vacío.")
            input("Presiona ENTER para volver a intentarlo...")
            print("\033[F\033[K" * 3, end='') 
            continue
        
        # Validar duplicidad de jugador por nombre y dorsal dentro del equipo
        existe_jugador = False
        for jugador_existente in conjunto_equipos[nombre_equipo]["plantel"]["jugadores"]:
            if jugador_existente["nombre"].lower() == nombre.lower():
                print(f"Error: El jugador '{nombre}' ya existe en el plantel de '{nombre_equipo.capitalize()}'.")
                existe_jugador = True
                break
        if existe_jugador:
            continue

        while True:
            try:
                dorsal_str = input("Dorsal del jugador: ").strip()
                if not dorsal_str:
                    print("Error: El dorsal no puede estar vacío.")
                    input("Presiona ENTER para volver a intentarlo...")
                    print("\033[F\033[K" * 2, end='') 
                    continue

                dorsal = int(dorsal_str)
                if not (1 <= dorsal <= 99):
                    print("Error: El dorsal debe ser un número entre 1 y 99.")
                    input("Presiona ENTER para volver a intentarlo...")
                    print("\033[F\033[K" * 3, end='')
                    continue

                # Validar que el dorsal no esté duplicado para el mismo equipo
                existe_dorsal = False
                for jugador_existente in conjunto_equipos[nombre_equipo]["plantel"]["jugadores"]:
                    if jugador_existente["dorsal"] == dorsal:
                        print(f"Error: El dorsal '{dorsal}' ya está ocupado por otro jugador en '{nombre_equipo.capitalize()}'.")
                        existe_dorsal = True
                        break
                if existe_dorsal:
                    continue
                break
            except ValueError:
                print("Error: El dorsal debe ser un número entero.")

        posicion = input("Posición del jugador: ").strip().capitalize()
        if not posicion:
            print("Error: La posición no puede estar vacía.")
            input("Presiona ENTER para volver a intentarlo...")
            print("\033[F\033[K" * 3, end='')
            continue

        while True:
            try:
                edad_str = input("Edad del jugador: ").strip()
                if not edad_str:
                    print("Error: La edad no puede estar vacía.")
                    continue
                edad = int(edad_str)
                if not (16 <= edad <= 99): 
                    print("Error: La edad debe ser un número entre 5 y 99.")
                    continue
                break
            except ValueError:
                print("Error: La edad debe ser un número entero.")

        jugador = {"nombre": nombre, "dorsal": dorsal, "posicion": posicion, "edad": edad}
        conjunto_equipos[nombre_equipo]["plantel"]["jugadores"].append(jugador)
        print(f"Jugador '{nombre}' añadido al plantel de '{nombre_equipo.capitalize()}'.")
        break

def agregar_cuerpo_tecnico(conjunto_equipos, nombre_equipo):

    while True:
        nombre = input("Nombre del personal técnico: ").strip().capitalize()
        if not nombre:
            print("Error: El nombre del personal técnico no puede estar vacío.")
            continue
        
        # Validar duplicidad de personal técnico por nombre y cargo dentro del equipo
        existe_personal = False
        for personal_existente in conjunto_equipos[nombre_equipo]["plantel"]["cuerpo_tecnico"]:
            if personal_existente["nombre"].lower() == nombre.lower():
                print(f"Error: '{nombre}' ya existe en el cuerpo técnico de '{nombre_equipo.capitalize()}'.")
                existe_personal = True
                break
        if existe_personal:
            continue

        cargo = input("Cargo (Ej: Entrenador, Fisioterapeuta): ").strip().capitalize()
        if not cargo:
            print("Error: El cargo no puede estar vacío.")
            continue
        
        # Validar duplicidad de personal técnico por nombre y cargo dentro del equipo
        existe_personal_cargo = False
        for personal_existente in conjunto_equipos[nombre_equipo]["plantel"]["cuerpo_tecnico"]:
            if personal_existente["nombre"].lower() == nombre.lower() and personal_existente["cargo"].lower() == cargo.lower():
                print(f"Error: '{nombre}' con el cargo '{cargo}' ya existe en el cuerpo técnico de '{nombre_equipo.capitalize()}'.")
                existe_personal_cargo = True
                break
        if existe_personal_cargo:
            continue

        personal = {"nombre": nombre, "cargo": cargo}
        conjunto_equipos[nombre_equipo]["plantel"]["cuerpo_tecnico"].append(personal)
        print(f"Personal '{nombre}' ({cargo}) añadido al cuerpo técnico de '{nombre_equipo.capitalize()}'.")
        break

def registrar_plantel(conjunto_equipos):

    if not conjunto_equipos:
        print("No hay equipos registrados para añadir jugadores o cuerpo técnico.")
        return

    print("Equipos disponibles:", ", ".join(conjunto_equipos.keys()))
    while True:
        nombre_equipo = input("Introduce el nombre del equipo para registrar su plantel: ").strip().lower()
        if not nombre_equipo:
            print("Error: El nombre del equipo no puede estar vacío.")
        elif nombre_equipo not in conjunto_equipos:
            print("Error: El equipo no está registrado. Inténtalo de nuevo.")
        else:
            break
    
    #  Submenú para el registro de plantel 
    while True:
        limpiar_consola()
        print(f"\n--- MENÚ DE REGISTRO DE PLANTEL para {nombre_equipo.capitalize()} ---")
        print("1. Agregar jugador")
        print("2. Agregar personal del cuerpo técnico")
        print("3. Volver al menú principal")

        opcion_plantel = input("Elige una opción: ").strip()

        if opcion_plantel == '1':
            agregar_jugador(conjunto_equipos, nombre_equipo)
            input("\nPresiona Enter para volver al menú de registro de plantel...")
        elif opcion_plantel == '2':
            agregar_cuerpo_tecnico(conjunto_equipos, nombre_equipo)
            input("\nPresiona Enter para volver al menú de registro de plantel...")
        elif opcion_plantel == '3':
            print("Volviendo al menú principal.")
            break
        else:
            print("Opción no válida. Por favor, introduce 1, 2 o 3.")
        

def mainMenu():

    equipos = {}
    calendario = []

    while True:
        limpiar_consola()
        mostrar_menu()
        opcion = input("Elige una opción: ").strip() 

        if opcion == '1':
            inscribir_equipo(equipos)
        elif opcion == '2':
            definir_encuentro(equipos, calendario)
        elif opcion == '3':
            cargar_marcador(equipos, calendario)
        elif opcion == '4':
            equipo_mas_goles_favor(equipos)
        elif opcion == '5':
            equipo_mas_goles_contra(equipos)
        elif opcion == '6':
            registrar_plantel(equipos)
        elif opcion == '7':
            print("Saliendo del programa. ¡Hasta pronto!")
            break
        else:
            print("Opción no válida. Por favor, introduce un número del 1 al 7.")
        
        input("\nPresiona Enter para continuar...")

if __name__ == "__main__":
    mainMenu()