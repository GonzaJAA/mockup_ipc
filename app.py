import streamlit as st
import pandas as pd
import plotly.express as px

def main():
    st.set_page_config(page_title="Calculadora IPC - SDE", page_icon="📊", layout="wide")
    
    st.title("📊 Calculadora del Índice de Precios al Consumidor (IPC)")
    
    # Crear dos columnas principales
    col_left, col_right = st.columns([1, 1])
    
    with col_left:
        with st.container():
            # Crear columnas para la tabla de inputs
            col1, col2, col3 = st.columns([3, 2, 2])
            
            with col1:
                st.markdown("**Selección de aperturas del IPC**")
            with col2:
                st.markdown("**Gasto en pesos**")
            with col3:
                st.markdown("**Participación porcentual**")
            
            st.markdown("---")
            
            # Definir las categorías y sus items
            items = {
                "Alimentos y bebidas no alcohólicas": {
                    "icon": "ℹ️",
                    "subitems": [
                        "Carnes y derivados",
                        "Frutas", 
                        "Verduras, tubérculos y legumbres",
                        "Resto de alimentos y bebidas n/a"
                    ]
                },
                "Bebidas alcohólicas y tabaco": {
                    "icon": None,
                    "subitems": []
                },
                "Prendas de vestir y calzado": {
                    "icon": None,
                    "subitems": []
                },
                "Vivienda, agua, electricidad, gas y otros combustibles": {
                    "icon": "ℹ️",
                    "subitems": [
                        "Alquiler de la vivienda y gastos conexos",
                        "Electricidad, gas y otros combustibles"
                    ]
                },
                "Equipamiento y mantenimiento del hogar": {
                    "icon": "ℹ️",
                    "subitems": []
                },
                "Salud": {
                    "icon": "ℹ️",
                    "subitems": [
                        "Productos medicinales, artefactos y equipos para la salud",
                        "Gastos de prepagas"
                    ]
                },
                "Transporte": {
                    "icon": "ℹ️",
                    "subitems": [
                        "Combustibles y lubricantes para vehículos de uso del hogar",
                        "Transporte público"
                    ]
                },
                "Servicios de telefonía e internet": {
                    "icon": "ℹ️",
                    "subitems": []
                },
                "Recreación y cultura": {
                    "icon": "ℹ️",
                    "subitems": []
                },
                "Educación": {
                    "icon": "ℹ️",
                    "subitems": []
                },
                "Restaurantes y comidas fuera del hogar": {
                    "icon": "ℹ️",
                    "subitems": []
                },
                "Cuidado personal": {
                    "icon": "ℹ️",
                    "subitems": []
                },
            }
            
            # Diccionario para almacenar los inputs
            gastos = {}
            participaciones = {}
            
            # Crear inputs para cada categoria/item
            for categoria, info in items.items():
                col1, col2, col3 = st.columns([3, 2, 2])
                
                with col1:
                    if info["icon"]:
                        st.markdown(f"{info['icon']} **{categoria}**")
                    else:
                        st.markdown(f"**{categoria}**")
                
                # Si no tiene subitems, mostrar input directo
                if not info["subitems"]:
                    with col2:
                        gasto = st.number_input(
                            f"Gasto {categoria}",
                            min_value=0.0,
                            value=0.0,
                            step=100.0,
                            format="%.0f",
                            label_visibility="collapsed",
                            key=f"gasto_{categoria}"
                        )
                        gastos[categoria] = gasto
                    
                    with col3:
                        participacion = st.empty()
                        participaciones[categoria] = participacion
                
                # Si tiene subitems, mostrar cada uno
                else:
                    with col2:
                        st.write("")  # Espacio vacío
                    with col3:
                        st.write("")  # Espacio vacío
                    
                    for subitem in info["subitems"]:
                        col1, col2, col3 = st.columns([3, 2, 2])
                        
                        with col1:
                            st.markdown(f"　• {subitem}")
                        
                        with col2:
                            gasto = st.number_input(
                                f"Gasto {subitem}",
                                min_value=0.0,
                                value=0.0,
                                step=100.0,
                                format="%.0f",
                                label_visibility="collapsed",
                                key=f"gasto_{subitem}"
                            )
                            gastos[subitem] = gasto
                        
                        with col3:
                            participacion = st.empty()
                            participaciones[subitem] = participacion
                
                st.markdown("---")
            
            # Botón de calcular centrado
            col_center = st.columns([1, 1, 1])[1]
            with col_center:
                calcular = st.button("**Calcular**", use_container_width=True, type="primary")
            
            # Realizar cálculos cuando se presiona el botón
            if calcular:
                total_gasto = sum(gastos.values())
                
                if total_gasto > 0:
                    # Mostrar gasto total
                    st.metric("💰 Gasto Total", f"${total_gasto:,.0f}")
                    
                    # Calcular y mostrar participaciones
                    gastos_para_grafico = {}
                    for item, gasto in gastos.items():
                        if gasto > 0:
                            participacion_pct = (gasto / total_gasto) * 100
                            participaciones[item].markdown(f"**{participacion_pct:.2f}%**")
                            gastos_para_grafico[item] = gasto
                        else:
                            participaciones[item].markdown("0.00%")
                    
                    # Actualizar gráfico en la columna derecha
                    with col_right:
                        if gastos_para_grafico:
                            st.markdown("### 🍰 Distribución de Gastos")
                            
                            df_pie = pd.DataFrame({
                                'Categoría': list(gastos_para_grafico.keys()),
                                'Gasto': list(gastos_para_grafico.values())
                            })
                            
                            fig = px.pie(df_pie, 
                                        values='Gasto', 
                                        names='Categoría',
                                        hole=0.4,
                                        title="Distribución porcentual de gastos")
                            
                         #   fig.update_traces(textposition='inside', textinfo='percent+label')
                            fig.update_layout(
                                showlegend=True,
                                legend=dict(orientation="v", yanchor="middle", y=0.5)
                            )
                            
                            st.plotly_chart(fig, use_container_width=True)
                            
                            # Gráfico de evolución temporal (mockup)
                            st.markdown("### 📈 Evolución del IPC")
                            
                            # Datos mockup para el gráfico temporal
                            fechas = ['Jul-2024', 'Ago-2024', 'Sep-2024', 'Oct-2024', 'Nov-2024', 
                                     'Dic-2024', 'Ene-2025', 'Feb-2025', 'Mar-2025', 'Abr-2025', 
                                     'May-2025', 'Jun-2025', 'Jul-2025', 'Ago-2025']
                            
                            # Datos simulados para las tres líneas (mismo tamaño)
                            tu_ipc = [5.8, 6.2, 5.1, 3.9, 3.7, 2.8, 2.2, 2.1, 6.1, 2.8, 1.2, 2.1, 2.3, 2.3]
                            ipc_noa = [4.9, 4.4, 2.2, 2.4, 2.3, 2.9, 3.7, 1.8, 1.6, 2.2, 2.1, 1.9, 2.0, 2.2]
                            ipc_nacional = [4.2, 4.3, 2.7, 2.4, 2.4, 2.6, 2.5, 1.7, 1.9, 2.1, 1.8, 1.7, 1.9, 2.0]
                            
                            df_temporal = pd.DataFrame({
                                'Fecha': fechas,
                                'Tu IPC mensual': tu_ipc,
                                'IPC NOA': ipc_noa,
                                'IPC Nacional': ipc_nacional
                            })
                            
                            # Crear gráfico de líneas
                            fig_temporal = px.line(df_temporal, 
                                                 x='Fecha', 
                                                 y=['Tu IPC mensual', 'IPC NOA', 'IPC Nacional'],
                                                 title="Comparación de Evolución del IPC",
                                                 color_discrete_map={
                                                     'Tu IPC mensual': '#1f77b4',
                                                     'IPC NOA': '#aec7e8', 
                                                     'IPC Nacional': '#ff7f0e'
                                                 })
                            
                            fig_temporal.update_layout(
                                yaxis_title="Porcentaje (%)",
                                xaxis_title="",
                                legend=dict(
                                    orientation="h",
                                    yanchor="bottom",
                                    y=1.02,
                                    xanchor="center",
                                    x=0.5
                                ),
                                yaxis=dict(range=[0, 8]),
                                showlegend=True
                            )
                            
                            fig_temporal.update_traces(mode='lines+markers', line=dict(width=3))
                            
                            st.plotly_chart(fig_temporal, use_container_width=True)
                        else:
                            st.info("No hay gastos para mostrar en el gráfico")
                else:
                    st.warning("Ingresa al menos un gasto para calcular las participaciones")
    
    with col_right:
        # Espacio inicial para el gráfico (se llena cuando se presiona calcular)
        st.markdown("### 📊 Gráfico de Participación")
        st.info("💡 Presiona 'Calcular' para ver la distribución de gastos")

if __name__ == "__main__":
    main()