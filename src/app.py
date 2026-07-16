import asyncio
try:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

import os
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# --- Configuración inicial (se ejecuta una sola vez gracias al cache) ---
@st.cache_resource
def cargar_recursos():
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    vector_store = FAISS.load_local(
        os.path.join(BASE_DIR, "..", "data", "vector_store_muestra"),
        embeddings,
        allow_dangerous_deserialization=True
    )
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    return vector_store, llm

vector_store, llm = cargar_recursos()

# --- Interfaz de Streamlit ---
st.set_page_config(page_title="Asistente de Tickets de Soporte", page_icon="🎫")

st.title("🎫 Asistente de Tickets de Soporte")
st.caption("🤖 Estás hablando con un agente de IA, no con una persona. Las respuestas se basan en una muestra de 100 tickets.")

# Historial de conversación
if "historial" not in st.session_state:
    st.session_state.historial = []

# Mostrar historial previo
for mensaje in st.session_state.historial:
    with st.chat_message(mensaje["rol"]):
        st.write(mensaje["contenido"])
        if mensaje.get("fuentes"):
            st.caption(f"📎 Fuentes (Ticket IDs): {mensaje['fuentes']}")

# Input del usuario
pregunta = st.chat_input("Escribe tu pregunta sobre los tickets de soporte...")

if pregunta:
    st.session_state.historial.append({"rol": "user", "contenido": pregunta})
    with st.chat_message("user"):
        st.write(pregunta)

    with st.chat_message("assistant"):
        with st.spinner("Buscando en los tickets..."):
            resultado = responder_pregunta(pregunta)
        st.write(resultado["respuesta"])
        if resultado["fuentes"]:
            st.caption(f"📎 Fuentes (Ticket IDs): {resultado['fuentes']}")

        col1, col2 = st.columns([1, 10])
        with col1:
            st.button("👍", key=f"like_{len(st.session_state.historial)}")
        with col2:
            st.button("👎", key=f"dislike_{len(st.session_state.historial)}")

    st.session_state.historial.append({
        "rol": "assistant",
        "contenido": resultado["respuesta"],
        "fuentes": resultado["fuentes"]
    })