import flet as ft
import json
import os
import random
from datetime import datetime

DB_FILE = "data.json"

# ==========================================
#   GESTIÓN DE BASE DE DATOS LOCAL (JSON)
# ==========================================
def inicializar_base_datos():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump({"estudiantes": [], "historial": []}, f, indent=4)

def obtener_estructura():
    inicializar_base_datos()
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            datos = json.load(f)
            if "estudiantes" not in datos:
                datos["estudiantes"] = []
            if "historial" not in datos:
                datos["historial"] = []
            return datos
    except:
        return {"estudiantes": [], "historial": []}

def guardar_o_actualizar_en_json(nombre, materia, notas, promedio):
    estructura = obtener_estructura()
    datos = estructura["estudiantes"]
    nom_buscar = nombre.strip().lower()
    mat_buscar = materia.strip().lower()
    
    fecha_str = datetime.now().strftime("%d/%m/%Y %I:%M %p")
    existe = False
    
    for item in datos:
        if item["estudiante"].strip().lower() == nom_buscar and item["materia"].strip().lower() == mat_buscar:
            item["notas"] = notas
            item["promedio"] = round(promedio, 2)
            existe = True
            estructura["historial"].insert(0, {
                "fecha": fecha_str,
                "accion": "MODIFICAR",
                "detalle": f"Notas actualizadas a {notas} para {nombre.strip()} en {materia.strip()}."
            })
            break
            
    if not existe:
        datos.append({
            "estudiante": nombre.strip(),
            "materia": materia.strip(),
            "notas": notas,
            "promedio": round(promedio, 2)
        })
        estructura["historial"].insert(0, {
            "fecha": fecha_str,
            "accion": "AGREGAR",
            "detalle": f"Creado registro de {nombre.strip()} en {materia.strip()} con notas {notas}."
        })
        
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(estructura, f, indent=4, ensure_ascii=False)

def eliminar_registro_json(nombre, materia):
    estructura = obtener_estructura()
    datos = estructura["estudiantes"]
    nom_buscar = nombre.strip().lower()
    mat_buscar = materia.strip().lower()
    
    nuevos_datos = [
        item for item in datos 
        if not (item["estudiante"].strip().lower() == nom_buscar and item["materia"].strip().lower() == mat_buscar)
    ]
    
    estructura["estudiantes"] = nuevos_datos
    fecha_str = datetime.now().strftime("%d/%m/%Y %I:%M %p")
    
    estructura["historial"].insert(0, {
        "fecha": fecha_str,
        "accion": "ELIMINAR",
        "detalle": f"Se borró la materia {materia.strip()} de {nombre.strip()}."
    })
    
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(estructura, f, indent=4, ensure_ascii=False)


# ==========================================
#   APLICACIÓN VISUAL PRINCIPAL
# ==========================================
def main(page: ft.Page):
    page.title = "Nota Calk"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#080B10"  
    page.window_width = 450
    page.window_height = 750
    page.padding = 0  
    page.scroll = "auto"

    # Pool de anuncios simulados para @EscapeTecnico
    anuncios_pool = [
        "🔥 ¿Quieres automatizar tus tareas? Aprende Python hoy en @EscapeTecnico",
        "💻 Sube de nivel tu Setup. Los mejores tips de hardware en @EscapeTecnico",
        "⚡ Nota Calk Pro: Elimina los anuncios por solo $1.99 al mes.",
        "🚀 Invierte en tu futuro. Domina bases de datos y desarrollo de software."
    ]
    
    txt_anuncio = ft.Text(random.choice(anuncios_pool), size=11, color="#A0AEC0", text_align="center", weight="w500", expand=True)
    
    # Banner de Publicidad Fijo sin ft.padding ni ft.BorderSide problemáticos
    banner_publicidad = ft.Container(
        content=ft.Row(
            controls=[
                ft.Container(content=ft.Text("AD", size=9, weight="bold", color="#111622"), bgcolor="#FBBF24", padding=3, border_radius=4),
                ft.VerticalDivider(width=10, color="#1E293B"),
                txt_anuncio  
            ],
            alignment="center"
        ),
        bgcolor="#111622",
        height=50,
        padding=16, # Pasamos el entero directo, Flet lo toma como padding uniforme sin colapsar
    )

    def rotar_anuncio(e):
        txt_anuncio.value = random.choice(anuncios_pool)
        page.update()

    def wrapper_vista(contenido_vista):
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(content=contenido_vista, expand=True),
                    banner_publicidad
                ],
                spacing=0
            ),
            expand=True,
            padding=0
        )

    def boton_volver():
        return ft.IconButton(
            icon=ft.Icons.ARROW_BACK_ROUNDED, 
            icon_color="#708599", 
            on_click=lambda _: mostrar_menu_principal()
        )

    def mostrar_tutorial(e):
        dialogo_tutorial = ft.AlertDialog(
            title=ft.Text("¿Cómo usar Nota Calk?", color="#E2F1FF", weight="bold"),
            content=ft.Column(
                controls=[
                    ft.Text("1. Agregar Notas:", weight="bold", color="#34D399"),
                    ft.Text("Ingresa el alumno, materia y notas separadas por un espacio (Ej: 19 18 20).", color="#FFFFFF", size=13),
                    ft.Container(height=5),
                    ft.Text("2. Actualizar Datos:", weight="bold", color="#FBBF24"),
                    ft.Text("Si repites Alumno y Materia, el sistema actualizará sus notas automáticamente.", color="#FFFFFF", size=13),
                    ft.Container(height=5),
                    ft.Text("3. Editar o Eliminar:", weight="bold", color="#F87171"),
                    ft.Text("Ve a 'Promedios individuales', toca al alumno y gestiona la materia.", color="#FFFFFF", size=13),
                ],
                tight=True, spacing=5
            ),
            bgcolor="#111622",
            actions=[ft.TextButton("Entendido", on_click=lambda x: [setattr(dialogo_tutorial, "open", False), page.update()])]
        )
        page.show_dialog(dialogo_tutorial)

    # ==========================================
    #   VISTA 1: MENÚ PRINCIPAL
    # ==========================================
    def mostrar_menu_principal():
        page.controls.clear()

        header_row = ft.Row(
            controls=[
                ft.Column([
                    ft.Text("Nota Calk", size=36, weight=ft.FontWeight.BOLD, color="#E2F1FF"),
                    ft.Text("Organiza todo desde aquí", size=16, color="#708599")
                ]),
                ft.IconButton(
                    icon=ft.Icons.HELP_OUTLINE_ROUNDED, icon_color="#34D399", icon_size=28,
                    on_click=mostrar_tutorial
                )
            ],
            alignment="space-between"
        )

        def crear_tarjeta_modulo(titulo, icono_nativo, color_neon, on_click_func):
            return ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Icon(icono_nativo, color=color_neon, size=36),
                        ft.Text(titulo, size=12, weight=ft.FontWeight.BOLD, color="#FFFFFF", text_align="center")
                    ],
                    alignment="center", horizontal_alignment="center", spacing=8
                ),
                bgcolor="#111622", width=165, height=140,  
                border_radius=20, padding=12, on_click=on_click_func
                # Eliminados los bordes problemáticos por completo para máxima compatibilidad
            )

        fila_superior = ft.Row(
            controls=[
                crear_tarjeta_modulo("Agregar estudiante y notas", ft.Icons.EDIT_NOTE, "#34D399", ir_a_agregar),
                crear_tarjeta_modulo("Promedios individuales", ft.Icons.PERSON, "#FBBF24", ir_a_individuales),
            ],
            alignment="center", spacing=16
        )

        fila_inferior = ft.Row(
            controls=[
                crear_tarjeta_modulo("Promedios generales", ft.Icons.BAR_CHART, "#F87171", ir_a_generales),
                crear_tarjeta_modulo("Historial de registro", ft.Icons.HISTORY, "#60A5FA", ir_a_historial),
            ],
            alignment="center", spacing=16
        )

        bloque_principal_centrado = ft.Row(
            controls=[ft.Column(controls=[fila_superior, fila_inferior], spacing=16)],
            alignment="center"
        )

        contenido = ft.Container(
            content=ft.Column(
                controls=[ft.Container(height=10), header_row, ft.Divider(height=40, color="#1E293B"), bloque_principal_centrado]
            ),
            padding=24
        )
        
        rotar_anuncio(None)
        page.add(wrapper_vista(contenido))
        page.update()

    # ==========================================
    #   VISTA 2: AGREGAR / EDITAR ESTUDIANTE
    # ==========================================
    def ir_a_agregar(e, nombre_previo="", materia_previas="", notas_previas=""):
        page.controls.clear()

        txt_estudiante = ft.TextField(label="Nombre del Estudiante", border_color="#34D399", value=nombre_previo)
        txt_materia = ft.TextField(label="Materia", border_color="#34D399", value=materia_previas)
        txt_notas = ft.TextField(label="Notas", hint_text="Ej: 19 18 20", border_color="#34D399", value=notas_previas)

        if nombre_previo and materia_previas:
            txt_estudiante.disabled = True
            txt_materia.disabled = True

        def guardar_registro(e):
            if not txt_estudiante.value or not txt_materia.value or not txt_notas.value:
                return
            lista_de_notas = [int(n) for n in txt_notas.value.split() if n.isdigit()]
            if len(lista_de_notas) == 0:
                return
            promedio = sum(lista_de_notas) / len(lista_de_notas)
            
            guardar_o_actualizar_en_json(txt_estudiante.value, txt_materia.value, lista_de_notas, promedio)
            mostrar_menu_principal()

        btn_guardar = ft.ElevatedButton(
            "Guardar Datos", on_click=guardar_registro,
            style=ft.ButtonStyle(bgcolor="#10B981", color="#FFFFFF")
        )

        contenido = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row([boton_volver(), ft.Text("Estudiantes y notas", size=24, weight=ft.FontWeight.BOLD, color="#E2F1FF")]),
                    ft.Divider(height=20, color="#1E293B"),
                    txt_estudiante, txt_materia, txt_notas,
                    ft.Container(height=20),
                    ft.Row([btn_guardar], alignment="center")
                ]
            ),
            padding=24
        )
        page.add(wrapper_vista(contenido))
        page.update()

    # ==========================================
    #   VISTA 3: PROMEDIOS INDIVIDUALES
    # ==========================================
    def ir_a_individuales(e):
        page.controls.clear()
        estructura = obtener_estructura()
        datos = estructura["estudiantes"]
        
        lista_estudiantes = ft.Column(spacing=12)
        
        if not datos:
            lista_estudiantes.controls.append(ft.Text("No hay estudiantes registrados.", color="#708599"))
        else:
            alumnos = {}
            for item in datos:
                nom = item["estudiante"].strip()
                if nom not in alumnos:
                    alumnos[nom] = []
                alumnos[nom].append(item)

            for nombre_alumno, registros in alumnos.items():
                promedio_total_alumno = sum(r["promedio"] for r in registros) / len(registros)
                
                txt_materias_list = []
                for r in registros:
                    txt_materias_list.append(
                        ft.Text(f"• {r['materia']}: {r['notas']} (Prom: {r['promedio']})", color="#708599", size=13)
                    )

                def crear_panel_opciones(regs=registros, nombre=nombre_alumno):
                    dialogo = ft.AlertDialog(
                        title=ft.Text("Opciones de Registro", color="#E2F1FF"),
                        content=ft.Text(f"Selecciona una materia de {nombre} para gestionar:", color="#FFFFFF"),
                        bgcolor="#111622"
                    )
                    
                    botones_materias = []
                    for rm in regs:
                        def m_click(e, r_materia=rm):
                            dialogo.open = False
                            page.update()
                            
                            sub_dialogo = ft.AlertDialog(
                                title=ft.Text(f"{r_materia['estudiante']} - {r_materia['materia']}", color="#E2F1FF"),
                                bgcolor="#111622",
                                actions=[
                                    ft.TextButton("Editar Notas", on_click=lambda _: [
                                        setattr(sub_dialogo, "open", False), page.update(),
                                        ir_a_agregar(None, r_materia["estudiante"], r_materia["materia"], " ".join(map(str, r_materia["notas"])))
                                    ]),
                                    ft.TextButton("Eliminar", style=ft.ButtonStyle(color="#F87171"), on_click=lambda _: [
                                        setattr(sub_dialogo, "open", False), page.update(),
                                        eliminar_registro_json(r_materia["estudiante"], r_materia["materia"]),
                                        ir_a_individuales(None)
                                    ])
                                ]
                            )
                            page.show_dialog(sub_dialogo)

                        botones_materias.append(ft.ElevatedButton(rm["materia"], on_click=m_click, style=ft.ButtonStyle(bgcolor="#1E293B", color="#E2F1FF")))
                    
                    dialogo.actions = botones_materias
                    return lambda _: page.show_dialog(dialogo)

                lista_estudiantes.controls.append(
                    ft.Container(
                        content=ft.ListTile(
                            title=ft.Text(nombre_alumno, weight="bold", color="#FFFFFF", size=16),
                            subtitle=ft.Column(controls=txt_materias_list, spacing=4),
                            trailing=ft.Column(
                                controls=[
                                    ft.Text("Total", size=10, color="#708599", weight="bold"),
                                    ft.Text(f"{round(promedio_total_alumno, 2)}", size=18, weight="bold", color="#FBBF24")
                                ],
                                alignment="center", horizontal_alignment="center"
                            ),
                            leading=ft.Icon(ft.Icons.PERSON, color="#FBBF24"),
                            on_click=crear_panel_opciones()
                        ),
                        bgcolor="#111622", padding=6, border_radius=15
                    )
                )

        contenido = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row([boton_volver(), ft.Text("Promedios Individuales", size=24, weight=ft.FontWeight.BOLD, color="#E2F1FF")]),
                    ft.Divider(height=20, color="#1E293B"),
                    lista_estudiantes
                ]
            ),
            padding=24
        )
        page.add(wrapper_vista(contenido))
        page.update()

    # ==========================================
    #   VISTA 4: PROMEDIOS GENERALES
    # ==========================================
    def ir_a_generales(e):
        page.controls.clear()
        estructura = obtener_estructura()
        datos = estructura["estudiantes"]
        
        total_registros = len(datos)
        promedio_general_seccion = 0.0
        lista_materias_ui = []
        
        if total_registros > 0:
            promedio_general_seccion = sum(item["promedio"] for item in datos) / total_registros
            
            materias_map = {}
            for item in datos:
                mat = item["materia"].strip()
                if mat not in materias_map:
                    materias_map[mat] = []
                materias_map[mat].append(item["promedio"])
            
            for mat_nombre, promedios in materias_map.items():
                prom_mat = sum(promedios) / len(promedios)
                lista_materias_ui.append(
                    ft.Row(
                        controls=[
                            ft.Text(f"• {mat_nombre}:", color="#FFFFFF", size=14),
                            ft.Text(f"{round(prom_mat, 2)}", color="#60A5FA", weight="bold", size=14)
                        ],
                        alignment="space-between"
                    )
                )
        else:
            lista_materias_ui.append(ft.Text("No hay materias registradas.", color="#708599"))

        tarjeta_info = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Promedio por Asignatura", size=18, weight="bold", color="#708599"),
                    ft.Divider(color="#1E293B"),
                    ft.Column(controls=lista_materias_ui, spacing=6),
                    ft.Divider(color="#1E293B"),
                    ft.Row(
                        controls=[
                            ft.Text("PROMEDIO SECCIÓN TOTAL:", size=15, weight="bold", color="#FFFFFF"),
                            ft.Text(f"{round(promedio_general_seccion, 2)}", size=22, weight="bold", color="#F87171")
                        ],
                        alignment="space-between"
                    )
                ],
                spacing=10
            ),
            bgcolor="#111622", padding=20, border_radius=15
            # Quitamos los borders conflictivos aquí también
        )

        contenido = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row([boton_volver(), ft.Text("Promedios Generales", size=24, weight=ft.FontWeight.BOLD, color="#E2F1FF")]),
                    ft.Divider(height=20, color="#1E293B"),
                    tarjeta_info
                ]
            ),
            padding=24
        )
        page.add(wrapper_vista(contenido))
        page.update()

    # ==========================================
    #   VISTA 5: HISTORIAL DE REGISTRO
    # ==========================================
    def ir_a_historial(e):
        page.controls.clear()
        estructura = obtener_estructura()
        historial = estructura["historial"]
        
        tabla_historial = ft.Column(spacing=8)
        
        if not historial:
            tabla_historial.controls.append(ft.Text("Historial de acciones vacío.", color="#708599"))
        else:
            for item in historial:
                color_accion = "#34D399" if item["accion"] == "AGREGAR" else "#FBBF24" if item["accion"] == "MODIFICAR" else "#F87171"
                
                tabla_historial.controls.append(
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Text(item["accion"], color=color_accion, weight="bold", size=12),
                                        ft.Text(item["fecha"], color="#708599", size=11)
                                    ],
                                    alignment="space-between"
                                ),
                                ft.Text(item["detalle"], color="#FFFFFF", size=13)
                            ],
                            spacing=4
                        ),
                        bgcolor="#111622", padding=12, border_radius=10
                    )
                )

        contenido = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row([boton_volver(), ft.Text("Historial de Acciones", size=22, weight=ft.FontWeight.BOLD, color="#E2F1FF")]),
                    ft.Divider(height=20, color="#1E293B"),
                    tabla_historial
                ]
            ),
            padding=24
        )
        page.add(wrapper_vista(contenido))
        page.update()

    inicializar_base_datos()
    mostrar_menu_principal()

if __name__ == "__main__":
    ft.app(main)