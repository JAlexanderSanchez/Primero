import os

from langchain.llms import OpenAI
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA

from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Annoy

import streamlit as st

os.environ['OPENAI_API_KEY'] = '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'
doc_name = 'doc.pdf'

#crear una funcion para el parametro path si es local o no
def process_doc(
        path: str = 'https://proceedings.neurips.cc/paper_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf',
        is_local: bool = False,
        question: str = 'Cuáles son los autores del pdf?'
):
       #curl peticiones http
       #-o especifica el archivo de salida donde guarda el contenido descargado
       #f se utiliza para crear una cadena formateada para string
    _, loader = os.system(f'curl -o {doc_name} {path}'), PyPDFLoader(f"./{doc_name}") if not is_local \
        else PyPDFLoader(path)

    doc = loader.load_and_split()

    print(doc[-1])

    #db = Chroma.from_documents(doc, embedding=OpenAIEmbeddings())
    db = Annoy.from_documents(doc, embedding=HuggingFaceEmbeddings())

    qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type='map_rerank', retriever=db.as_retriever())

    st.write(qa.run(question))
    # print(qa.run(question))


def client():
    st.title('Gestionar LLM con LangChain')
    uploader = st.file_uploader('Upload PDF', type='pdf')

    if uploader:
        #wb escritura binaria, se carga el archivo, nombre default_doc_ en forma de escrituria binaria
        #
        with open(f'./{doc_name}', 'wb') as f:
            #Escribir los datos de los vectores cargador en forma de un buffer de memoria
            f.write(uploader.getbuffer())
        st.success('PDF saved!!')

    question = st.text_input('Generar un resumen de 20 palabras sobre el pdf',
                             placeholder='Da respuesta sobre tu PDF', disabled=not uploader)

    if st.button('Send Question'):
        if uploader:
            process_doc(
                path=doc_name,
                is_local=True,
                question=question
            )
        else:
            st.info('Cargando PDF')
            process_doc()

    if st.button('Mensaje'):
        st.info('Presiono el boton mensaje')

if __name__ == '__main__':
    client()
    # process_doc()

#pip install langchain
#pip install Annoy
#pip install sentences_transformers
#pip install openai
#pip install pypdf
#pip install chromadb
#pip install tiktoken
#pip install streamlit
#streamlit run nombre_del_proyecto.py --server.port 0000
#