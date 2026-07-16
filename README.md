# 🎫 Data Analysis Agent - Asistente de Tickets de Soporte

Agente de tipo RAG (Retrieval-Augmented Generation) que responde preguntas sobre tickets de soporte técnico, citando siempre la fuente (Ticket ID) y evitando alucinaciones cuando no encuentra información relevante.

🔗 **App en vivo:** [data-analysis-agent-jw8uj9hakjkhjxnejdrwet.streamlit.app](https://data-analysis-agent-jw8uj9hakjkhjxnejdrwet.streamlit.app/)

## 📋 Descripción del proyecto

Este proyecto fue desarrollado como capstone del curso de AI Builder de Alura. Utiliza un dataset público de tickets de soporte técnico (Kaggle) para construir un agente que permite consultar, en lenguaje natural, información sobre problemas reportados, resoluciones y patrones de soporte.

## 🏗️ Arquitectura

Usuario → Streamlit (interfaz de chat)
↓
Pregunta en lenguaje natural
↓
Embeddings (Gemini) → Búsqueda semántica en FAISS
↓
Top 3 tickets más relevantes (con umbral de relevancia)
↓
LLM (Gemini 2.5 Flash) genera respuesta usando SOLO ese contexto
↓
Respuesta + Ticket IDs citados + botones de feedback

**Componentes:**
- **Dataset:** [Customer Support Ticket Dataset](https://www.kaggle.com/datasets/muqaddasejaz/customer-support-ticket-dataset) (Kaggle), 8,469 tickets, muestra de 100 usada para el vector store.
- **Embeddings:** `gemini-embedding-001` (Google)
- **Vector Store:** FAISS (búsqueda por similitud semántica)
- **LLM:** `gemini-2.5-flash`, temperatura 0 (respuestas conservadoras, menor riesgo de alucinación)
- **Framework RAG:** LangChain
- **Interfaz:** Streamlit
- **Deploy:** Streamlit Community Cloud

## 🛡️ Control de alucinación

- El LLM recibe instrucción explícita de responder **únicamente** con base en el contexto recuperado.
- Se aplica un umbral de relevancia (0.7) en la búsqueda semántica: si ningún ticket es suficientemente relevante, el agente no genera respuesta e indica que no encontró información.
- Cada respuesta cita el/los Ticket ID(s) de origen para que sea verificable.

## 💬 Ejemplos de preguntas y respuestas

**Pregunta:** ¿Qué problemas ha tenido la gente con GoPro Hero?

**Respuesta:**
> La gente ha tenido los siguientes problemas con GoPro Hero:
> - Un error de software en la aplicación GoPro Hero que causa pérdida de datos y errores inesperados (Ticket ID: 3004).
> - Preocupación por la seguridad de su GoPro Hero y la seguridad de sus datos (Ticket ID: 3004).
> - Un problema con la GoPro Hero que no se resolvió con un restablecimiento de fábrica (Ticket ID: 5889).

**Pregunta:** ¿Cuál es la capital de Francia?

**Respuesta:**
> No encontré información relevante en los tickets disponibles para responder esta pregunta.

*(Este segundo ejemplo demuestra el fallback: el agente no inventa una respuesta fuera del alcance de la base de conocimiento.)*

## 🚀 Cómo ejecutar el proyecto localmente

### 1. Clona el repositorio
```bash
git clone https://github.com/anaalexrmo/Data-Analysis-Agent.git
cd Data-Analysis-Agent
```

### 2. Crea y activa un entorno virtual
```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instala las dependencias
```bash
pip install -r requirements.txt
```

### 4. Configura tu API key de Gemini
Crea un archivo `.env` en la raíz del proyecto con:
GOOGLE_API_KEY=tu_api_key_aqui

(genera tu clave gratis en [aistudio.google.com/apikey](https://aistudio.google.com/apikey))

### 5. Ejecuta la app
```bash
cd src
streamlit run app.py
```

La app se abrirá en `http://localhost:8501`

## 📁 Estructura del proyecto

Data-Analysis-Agent/
├── data/
│   ├── customer_support_tickets.csv
│   └── vector_store_muestra/       # Vector store FAISS pre-generado
├── notebooks/
│   └── 01_exploracion.ipynb         # Exploración, limpieza y desarrollo del RAG
├── src/
│   └── app.py                       # Interfaz de Streamlit
├── requirements.txt
├── .gitignore
└── README.md

## 🔧 Mantenimiento continuo (propuesta)

Para un entorno de producción real, este proyecto contemplaría:

- **Actualización de datos:** pipeline que detecte nuevos tickets y reprocese el índice vectorial de forma periódica (diaria/semanal).
- **Curaduría:** revisión periódica de que los tickets indexados sigan siendo representativos.
- **Monitoreo de calidad:** seguimiento de tasa de preguntas sin respuesta y feedback negativo (ya capturado vía botones 👍/👎 en la interfaz) para identificar vacíos de información.
- **Ciclo de mejora:** preguntas recurrentes sin buena respuesta señalan necesidad de ampliar la muestra de tickets indexados (actualmente limitada a 100 por límites de cuota gratuita de la API).
- **Actualización de modelo:** evaluación periódica de nuevas versiones de Gemini antes de sustituir el modelo en producción.

## ⚠️ Limitaciones conocidas

- El dataset es sintético (generado para práctica), por lo que algunas descripciones de tickets contienen frases genéricas no completamente naturales.
- La muestra indexada es de 100 tickets (de 8,469 totales) debido a límites de cuota gratuita de la API de Gemini.

## 🧑‍💻 Autora

Ana Alejandra Rocha Montes de Oca — [GitHub](https://github.com/anaalexrmo)