# app.py — Analizador IA de Documentos de Licitación (versión corregida)
import streamlit as st
import os
import tempfile
import json
import re
from dotenv import load_dotenv

# LangChain / loaders / embeddings / LLM
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.docstore.document import Document

load_dotenv()  # carga OPENAI_API_KEY desde .env

# Rutas
VECTOR_DIR = "vector_store"
PROCESSED_DIR = "processed"
EXTRACTED_JSON = os.path.join(PROCESSED_DIR, "extracted_info.json")
DETECTED_ISSUES = os.path.join(PROCESSED_DIR, "detected_issues.json")
SUMMARY_COMPARISON = os.path.join(PROCESSED_DIR, "summary_comparison.json")

os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(VECTOR_DIR, exist_ok=True)

# ---------------------
# Util: limpiar respuesta LLM y extraer JSON
# ---------------------
def clean_and_extract_json(text: str) -> str:
    if not text:
        return ""
    s = text.strip()
    # quitar fences ```json``` y ```
    s = re.sub(r"```(?:json)?\s*", "", s)
    s = re.sub(r"\s*```$", "", s)
    # si hay texto adicional, extraer el primer bloque JSON {...}
    m = re.search(r"\{.*\}", s, re.DOTALL)
    if m:
        return m.group(0)
    # fallback: devolver texto limpio
    return s

# ---------------------
# Crear vector DB desde lista de textos (chunks)
# ---------------------
def crear_vector_db(textos, fuente):
    # embeddings
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    docs = []
    for i, txt in enumerate(textos):
        docs.append(Document(page_content=txt, metadata={"source": fuente, "chunk": i}))
    db = Chroma.from_documents(docs, embeddings, persist_directory=VECTOR_DIR)
    # Chroma moderna persiste automáticamente
    return db

# ---------------------
# Extraer info con LLM y limpiar JSON
# ---------------------
def extraer_info_from_db(db, query, secciones):
    # recomponer db (asegura embedding_function)
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    db = Chroma(persist_directory=VECTOR_DIR, embedding_function=embeddings)

    resultados = db.similarity_search(query, k=5)
    texto_combinado = "\n".join([r.page_content for r in resultados])

    prompt_template = """
Extrae la siguiente información del siguiente texto del contrato en formato JSON EXACTO (devuelve sólo JSON, sin explicaciones ni texto adicional):
{secciones}

TEXTO:
{texto}
"""
    prompt = PromptTemplate(input_variables=["texto", "secciones"], template=prompt_template)
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY"))
    chain = LLMChain(llm=llm, prompt=prompt)

    respuesta = chain.run(texto=texto_combinado, secciones=secciones)

    respuesta_limpia = clean_and_extract_json(respuesta)
    try:
        resultado_json = json.loads(respuesta_limpia)
    except json.JSONDecodeError:
        resultado_json = {
            "error": "No se pudo parsear la respuesta como JSON",
            "respuesta_original": respuesta,
            "respuesta_limpia": respuesta_limpia
        }
    return resultado_json

# ---------------------
# Detecta vacíos simples y opcional LLM para ambigüedades
# ---------------------
def detect_issues(extracted, use_llm=False):
    required = ["clausulas_legales", "requisitos_tecnicos", "condiciones_economicas"]
    vacios = {}
    for r in required:
        val = extracted.get(r, "")
        if not val or (isinstance(val, str) and val.strip() == ""):
            vacios[r] = "Falta o está vacío"
    issues = {"vacios": vacios}

    if use_llm:
        llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY"))
        prompt = f"""
Eres un auditor de contratos. Revisa este JSON y devuelve sólo un JSON con:
- ambiguedades: lista de frases ambiguas
- contradicciones: lista de contradicciones entre campos
JSON input: {json.dumps(extracted, ensure_ascii=False)}
"""
        resp = llm.invoke(prompt).content
        # limpiar y guardar texto LLM (intentar JSON)
        clean = clean_and_extract_json(resp)
        try:
            llm_json = json.loads(clean)
        except:
            llm_json = {"llm_raw": resp}
        issues["llm_checks"] = llm_json
    return issues

# ---------------------
# Streamlit UI
# ---------------------
st.title("Analizador IA de Documentos de Licitación")
st.markdown("Carga un PDF (pliego/contrato/oferta). Se generará extracción y checks automáticos.")

uploaded_file = st.file_uploader("Sube un documento PDF", type=["pdf"], help="Pliegos / ofertas / contratos")

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_file_path = tmp_file.name

    st.info(f"Procesando archivo: {uploaded_file.name}")

    # Cargar PDF y extraer páginas
    try:
        loader = PyPDFLoader(tmp_file_path)
        pages = loader.load_and_split()
        textos = [p.page_content for p in pages]
    except Exception as e:
        st.error(f"Error leyendo PDF: {e}")
        raise

    # Crear vector DB
    with st.spinner("Creando base vectorial..."):
        db = crear_vector_db(textos, uploaded_file.name)
    st.success("Base vectorial creada.")

    # Secciones a extraer 
    secciones_a_extraer = """
    {
      "clausulas_legales": "Obligaciones, responsabilidades y aceptación de las partes",
      "requisitos_tecnicos": "Plazos, entregables, especificaciones técnicas",
      "condiciones_economicas": "Multas, pagos, presupuestos y garantías"
    }
    """

    query = st.text_input("Consulta (ej: 'condiciones del contrato'):", "condiciones del contrato")
    usar_llm_checks = st.checkbox("Usar LLM para detectar ambigüedades/contradicciones (genera consumo de API)", value=False)

    if st.button("Extraer información"):
        with st.spinner("Ejecutando análisis con IA..."):
            info = extraer_info_from_db(db, query, secciones_a_extraer)
            st.subheader("🔎 Extracción (estructurada)")
            st.json(info)

            # Guardar extracción
            with open(EXTRACTED_JSON, "w", encoding="utf-8") as f:
                json.dump(info, f, ensure_ascii=False, indent=2)

            # Detectar issues
            issues = detect_issues(info, use_llm=usar_llm_checks)
            with open(DETECTED_ISSUES, "w", encoding="utf-8") as f:
                json.dump(issues, f, ensure_ascii=False, indent=2)

            st.subheader("⚠️ Issues detectados")
            st.json(issues)

            # Si existe summary_comparison.json mostrarlo
            if os.path.exists(SUMMARY_COMPARISON):
                st.subheader("📊 Resumen comparativo (summary_comparison.json)")
                with open(SUMMARY_COMPARISON, "r", encoding="utf-8") as f:
                    summary = json.load(f)
                st.json(summary)
            else:
                st.info("No se encontró summary_comparison.json (ejecute compare_proposals.py si tiene propuestas estructuradas).")

        st.success("Análisis completado. Archivos guardados en carpeta processed/")

st.markdown("---")
st.caption("Nota: NO subas claves ni archivos con información sensible al repositorio. Mantén OPENAI_API_KEY en tu .env local.")

