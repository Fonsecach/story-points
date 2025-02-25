import streamlit as st
import pandas as pd

def calcular_story_points(complexidade, esforco, incerteza, fator=1.0):
    return round(((complexidade + esforco + incerteza) / 3) * fator, 1)

st.set_page_config(page_title="Estimativa de Story Points", layout="wide")

st.title("Estimativa de Story Points")
st.write("Insira as tarefas e ajuste os parâmetros para calcular os Story Points.")

# Criando abas
aba_estimar, aba_instrucoes = st.tabs(["Estimar Story Points", "Instruções"])

with aba_estimar:
    nome_pessoa = st.text_input("Nome da Pessoa")
    tarefa = st.text_input("Nome da Tarefa")
    tag = st.text_input("Tag da Tarefa")

    complexidade = st.slider("Complexidade", 1, 10, 5)
    esforco = st.slider("Esforço", 1, 10, 5)
    incerteza = st.slider("Incerteza", 1, 10, 5)

    fator = st.number_input("Fator de Ajuste", min_value=0.1, max_value=2.0, value=1.0, step=0.1)

    if "tasks" not in st.session_state:
        st.session_state.tasks = []

    if st.button("Calcular Estimativa"):
        story_points = calcular_story_points(complexidade, esforco, incerteza, fator)
        st.session_state.tasks.append({
            "Pessoa": nome_pessoa,
            "Tarefa": tarefa,
            "Tag": tag,
            "Complexidade": complexidade,
            "Esforço": esforco,
            "Incerteza": incerteza,
            "Story Points": story_points
        })
        st.success(f"Pessoa: {nome_pessoa} - Tarefa: {tarefa} (Tag: {tag}) - Estimativa em Story Points: {story_points}")

    if st.session_state.tasks:
        df = pd.DataFrame(st.session_state.tasks)
        st.write("### Tarefas Registradas")
        st.dataframe(df)
        
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Baixar CSV", csv, "estimativas.csv", "text/csv", key="download-csv")

with aba_instrucoes:
    st.write("## Como identificar os parâmetros")
    st.markdown("**Complexidade:** Avalie o nível de dificuldade técnica da tarefa. Se envolve múltiplas integrações ou lógica avançada, a complexidade será maior.")
    st.markdown("- **Exemplo 1:** Criar um simples formulário de login (Complexidade Baixa)")
    st.markdown("- **Exemplo 2:** Desenvolver um algoritmo de recomendação baseado em IA (Complexidade Alta)")
    
    st.markdown("**Esforço:** Quantidade de trabalho necessário para completar a tarefa. Pode ser baseado no tempo estimado ou no número de pessoas envolvidas.")
    st.markdown("- **Exemplo 1:** Ajustar um botão em uma página web (Esforço Baixo)")
    st.markdown("- **Exemplo 2:** Criar um novo módulo de faturamento para um sistema (Esforço Alto)")
    
    st.markdown("**Incerteza:** Grau de desconhecimento sobre a tarefa. Se há poucos detalhes ou riscos desconhecidos, a incerteza será maior.")
    st.markdown("- **Exemplo 1:** Implementar uma funcionalidade com documentação clara e requisitos bem definidos (Incerteza Baixa)")
    st.markdown("- **Exemplo 2:** Desenvolver uma integração com um sistema externo sem documentação (Incerteza Alta)")
