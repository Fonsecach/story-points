import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def calcular_story_points(complexidade, esforco, fator=1.0):
    return round(((complexidade + esforco) / 2) * fator, 1)

st.set_page_config(page_title="Estimativa de Story Points", layout="wide")

st.title("Estimativa de Story Points")
st.write("Insira as tarefas e ajuste os parâmetros para calcular os Story Points.")

# Criando abas
aba_estimar, aba_instrucoes, aba_graficos = st.tabs(["Estimar Story Points", "Instruções", "Gráficos"])

with aba_estimar:
    nome_pessoa = st.text_input("Nome da Pessoa")
    projeto = st.text_input("Projeto")
    tarefa = st.text_input("Nome da Tarefa")
    tag = st.text_input("Tag da Tarefa")

    complexidade = st.slider("Complexidade", 1, 10, 5)
    esforco = st.slider("Esforço", 1, 10, 5)

    fator = st.number_input("Fator de Ajuste", min_value=0.1, max_value=2.0, value=1.0, step=0.1)

    if "tasks" not in st.session_state:
        st.session_state.tasks = []

    if st.button("Calcular Estimativa"):
        story_points = calcular_story_points(complexidade, esforco, fator)
        st.session_state.tasks.append({
            "Pessoa": nome_pessoa,
            "Projeto": projeto,
            "Tarefa": tarefa,
            "Tag": tag,
            "Complexidade": complexidade,
            "Esforço": esforco,
            "Story Points": story_points
        })
        st.success(f"Pessoa: {nome_pessoa} - Projeto: {projeto} - Tarefa: {tarefa} (Tag: {tag}) - Estimativa em Story Points: {story_points}")

    if st.session_state.tasks:
        df = pd.DataFrame(st.session_state.tasks)
        st.write("### Tarefas Registradas")
        st.dataframe(df)
        
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Baixar CSV", csv, "estimativas.csv", "text/csv", key="download-csv")

    st.write("### Upload de Arquivo CSV")
    uploaded_file = st.file_uploader("Carregar arquivo CSV", type=["csv"])
    if uploaded_file is not None:
        df_uploaded = pd.read_csv(uploaded_file)
        st.write("### Dados do Arquivo Carregado")
        st.dataframe(df_uploaded)

with aba_instrucoes:
    st.write("## Como identificar os parâmetros")
    st.markdown("**Complexidade:** Avalie o nível de dificuldade técnica da tarefa. Se envolve múltiplas integrações ou lógica avançada, a complexidade será maior.")
    st.markdown("- **Exemplo 1:** Criar um simples formulário de login (Complexidade Baixa)")
    st.markdown("- **Exemplo 2:** Desenvolver um algoritmo de recomendação baseado em IA (Complexidade Alta)")
    
    st.markdown("**Esforço:** Quantidade de trabalho necessário para completar a tarefa. Pode ser baseado no tempo estimado ou no número de pessoas envolvidas.")
    st.markdown("- **Exemplo 1:** Ajustar um botão em uma página web (Esforço Baixo)")
    st.markdown("- **Exemplo 2:** Criar um novo módulo de faturamento para um sistema (Esforço Alto)")
    
    st.markdown("**Fator de Ajuste:** Permite calibrar a estimativa conforme experiências anteriores ou particularidades do projeto. Pode ser usado para corrigir variações identificadas na prática.")
    st.markdown("- **Exemplo 1:** Um time experiente pode reduzir o fator para 0.9, refletindo maior eficiência.")
    st.markdown("- **Exemplo 2:** Um projeto incerto pode aumentar o fator para 1.5, considerando riscos adicionais.")

with aba_graficos:
    if st.session_state.tasks:
        df = pd.DataFrame(st.session_state.tasks)
        
        st.write("### Quantidade de Tarefas por Pessoa")
        fig, ax = plt.subplots()
        df["Pessoa"].value_counts().plot(kind="bar", ax=ax)
        ax.set_ylabel("Número de Tarefas")
        ax.set_xlabel("Pessoa")
        ax.set_title("Quantidade de Tarefas por Pessoa")
        st.pyplot(fig)
        
        st.write("### Distribuição de Story Points")
        fig, ax = plt.subplots()
        df.groupby("Pessoa")["Story Points"].sum().plot(kind="bar", ax=ax)
        ax.set_ylabel("Story Points")
        ax.set_xlabel("Pessoa")
        ax.set_title("Story Points por Pessoa")
        st.pyplot(fig)
        
        st.write("### Quantidade de Tarefas por Projeto")
        fig, ax = plt.subplots()
        df["Projeto"].value_counts().plot(kind="bar", ax=ax)
        ax.set_ylabel("Número de Tarefas")
        ax.set_xlabel("Projeto")
        ax.set_title("Quantidade de Tarefas por Projeto")
        st.pyplot(fig)
    else:
        st.write("Nenhuma tarefa registrada para exibição de gráficos.")
