# 🏆 Reto 1 Hackython 

Este proyecto implementa un sistema de procesamiento y análisis de documentos de contratación pública usando técnicas de NLP y bases de datos vectoriales. Incluye extracción de texto, procesamiento y creación de un sistema de consulta inteligente.

---

## 📂 Estructura del proyecto

```
📁 reto1/
├── 📄 README.md                         → Este archivo
├── 📄 Informe.pdf                       → Informe técnico del proyecto
└── 📁 Reto-1Hackython/
    ├── 📄 01_extract_text.ipynb         → Extracción de texto de documentos
    ├── 📄 02_process_text.ipynb         → Procesamiento y limpieza de texto
    ├── 📄 04_query_vector_db.ipynb      → Consultas en base de datos vectorial
    ├── 📄 05_generate_report.ipynb      → Generación de reportes automáticos
    ├── 📄 06_detect_issues.ipynb        → Detección de inconsistencias y problemas
    ├── 📄 app.py                        → Aplicación web principal (Streamlit/Flask)
    ├── 📄 app_rol1.ipynb               → Sistema de consulta inteligente (Notebook)
    ├── 📄 compare_pliego_vs_propuestas.ipynb → Comparación pliego vs propuestas
    ├── 📄 compare_proposals.ipynb       → Comparación entre propuestas
    ├── 📄 validators.ipynb              → Validadores y reglas de negocio
    ├── 📁 data/                         → Documentos fuente
    │   ├── 📁 contratos/                → Documentos de contratos
    │   ├── 📁 ofertas/                  → Documentos de ofertas
    │   └── 📁 pliegos/                  → Documentos de pliegos
    ├── 📁 processed/                    → Datos procesados
    │   ├── 📁 chunks/                   → Fragmentos de texto procesados
    │   ├── 📄 condiciones_particulares_del_contrato.txt
    │   ├── 📄 condiciones_particulares_del_pliego.txt
    │   └── 📄 formulario_unico_de_la_oferta.txt
    └── 📁 vector_store/                 → Base de datos vectorial generada
```

---

## ⚙️ Instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/usuario/reto1-hackython.git
   cd reto1/Reto-1Hackython
   ```

2. **Crear un entorno virtual (recomendado)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**
   * Copia el archivo `.env.example` a `.env`
   * Edita `.env` con tus claves de API reales:
   ```
   OPENAI_API_KEY=tu_openai_key_aqui
   HUGGINGFACE_TOKEN=tu_huggingface_token_aqui
   ```

---

## ▶️ Ejecución

### Flujo completo del proyecto:

1. **Abrir en Visual Studio Code**
   * Instala la extensión **Jupyter** en VS Code
   * Abre la carpeta `Reto-1Hackython`

2. **Ejecutar notebooks en orden:**

   **Paso 1: Extracción de texto**
   ```bash
   # Abrir y ejecutar: 01_extract_text.ipynb
   ```
   - Extrae texto de documentos PDF/Word en `/data/`
   - Genera archivos de texto plano en `/processed/`

   **Paso 2: Procesamiento de texto**
   ```bash
   # Abrir y ejecutar: 02_process_text.ipynb
   ```
   - Limpia y segmenta el texto extraído
   - Crea chunks optimizados en `/processed/chunks/`

   **Paso 3: Consultas vectoriales**
   ```bash
   # Abrir y ejecutar: 04_query_vector_db.ipynb
   ```
   - Ejecuta consultas sobre la base de datos vectorial
   - Sistema de búsqueda semántica avanzada

   **Paso 4: Generación de reportes**
   ```bash
   # Abrir y ejecutar: 05_generate_report.ipynb
   ```
   - Genera reportes automáticos de análisis
   - Extrae métricas y estadísticas clave

   **Paso 5: Detección de problemas**
   ```bash
   # Abrir y ejecutar: 06_detect_issues.ipynb
   ```
   - Identifica inconsistencias en documentos
   - Detecta problemas potenciales en contratos

3. **Herramientas de análisis avanzado:**

   **Comparación de documentos**
   ```bash
   # compare_pliego_vs_propuestas.ipynb - Compara pliegos con propuestas
   # compare_proposals.ipynb - Compara múltiples propuestas entre sí
   ```

   **Validación y reglas**
   ```bash
   # validators.ipynb - Ejecuta validadores y reglas de negocio
   ```

   **Aplicaciones principales**
   ```bash
   # app_rol1.ipynb - Sistema de consulta inteligente (Notebook)
   # app.py - Aplicación web interactiva
   ```

4. **Ejecutar aplicación web**
   ```bash
   python app.py
   ```

5. **Seleccionar kernel**
   * Escoge el kernel de Python correspondiente a tu entorno virtual

---

## 📦 Dependencias principales

Las librerías utilizadas incluyen:
* **pandas** - Manipulación de datos
* **numpy** - Computación numérica
* **PyPDF2 / pdfplumber** - Extracción de texto de PDFs
* **python-docx** - Procesamiento de documentos Word
* **transformers** - Modelos de NLP
* **sentence-transformers** - Embeddings semánticos
* **chromadb / faiss** - Base de datos vectorial
* **openai** - API de OpenAI (si se usa)
* **streamlit / flask** - Frameworks para aplicación web
* **python-dotenv** - Manejo de variables de entorno
* **scikit-learn** - Algoritmos de machine learning
* **matplotlib / seaborn** - Visualización de datos

---

## 🔒 Seguridad y Configuración

* **Nunca** subas tu archivo `.env` a GitHub
* `.env` ya está agregado a `.gitignore`
* Configuración segura de claves:

```python
from dotenv import load_dotenv
import os

load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")
hf_token = os.getenv("HUGGINGFACE_TOKEN")
```

---

## 💡 Funcionalidades

### ✅ **Procesamiento de Documentos**
- **Extracción automática** de texto de documentos de contratación
- **Procesamiento inteligente** con técnicas de NLP avanzadas
- **Base de datos vectorial** para búsqueda semántica

### ✅ **Sistema de Consultas**
- **Consultas naturales** sobre documentos usando IA
- **Búsqueda semántica** avanzada en base vectorial
- **Interfaz web interactiva** (`app.py`) y notebook (`app_rol1.ipynb`)

### ✅ **Análisis y Comparación**
- **Comparación pliego vs propuestas** automatizada
- **Comparación entre múltiples propuestas**
- **Detección de inconsistencias** y problemas potenciales

### ✅ **Reportes y Validación**
- **Generación automática de reportes** de análisis
- **Sistema de validadores** y reglas de negocio
- **Métricas y estadísticas** clave del proceso

### ✅ **Gestión Integral**
- **Análisis unificado** de contratos, ofertas y pliegos
- **Detección proactiva** de issues y problemas
- **Flujo completo** desde extracción hasta reporte final

---

## 📋 Uso del Sistema

### 🔧 **Configuración inicial**
1. Coloca tus documentos en las carpetas correspondientes:
   - `data/contratos/` - Documentos de contratos
   - `data/ofertas/` - Documentos de ofertas  
   - `data/pliegos/` - Documentos de pliegos

2. Ejecuta los notebooks de procesamiento en orden secuencial (01, 02, 04)

### 🔍 **Consultas y análisis**
3. Usa las herramientas de consulta:
   - **Aplicación web:** `python app.py`
   - **Notebook interactivo:** `app_rol1.ipynb`

### 📊 **Generación de reportes**
4. Ejecuta los notebooks de análisis:
   - `05_generate_report.ipynb` - Reportes automáticos
   - `06_detect_issues.ipynb` - Detección de problemas

### ⚖️ **Comparación y validación**
5. Usa las herramientas especializadas:
   - `compare_pliego_vs_propuestas.ipynb` - Análisis de cumplimiento
   - `compare_proposals.ipynb` - Ranking de propuestas
   - `validators.ipynb` - Validación de reglas de negocio

### 💬 **Ejemplos de consultas**
- "¿Cuáles son las condiciones particulares del contrato?"
- "¿Qué documentos debe presentar el oferente?"
- "¿Cuál es el plazo de ejecución?"
- "Compara las propuestas técnicas presentadas"
- "¿Hay inconsistencias entre el pliego y las ofertas?"

---

## 🤝 Contribución

Para contribuir al proyecto:
1. Fork del repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit de tus cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crea un Pull Request

---

✍️ **Equipo:** Reto 1 Hackython  
📅 **Fecha:** 2025  
🏆 **Evento:** Hackython - Análisis de Contratación Pública
