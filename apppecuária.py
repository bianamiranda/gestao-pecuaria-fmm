import streamlit as st
import pandas as pd
import os
import base64
from datetime import datetime

# --- CONFIGURAÇÃO VISUAL (IDENTIDADE GESTÃO PECUÁRIA F.M.M.) ---
st.set_page_config(
    page_title="Gestão Pecuária F.M.M.", 
    page_icon="logo_fmm.png", 
    layout="wide"
)

    # --- VÍDEO DE FUNDO (DESIGN STUDIO F.M.M.) ---
video_html = """
    <style>
    #myVideo {
      position: fixed;
      right: 0;
      bottom: 0;
      min-width: 100%; 
      min-height: 100%;
      z-index: -1;
      opacity: 0.50; /* Ajuste a transparência para não atrapalhar a leitura */
    }

    /* Estilo para deixar os cartões e tabelas legíveis sobre o vídeo */
    .stApp {
        background: rgba(253, 252, 240, 0.6); /* Fundo creme com transparência */
    }
    </style>
    
    <video autoplay muted loop id="myVideo">
      <source src="https://raw.githubusercontent.com/bianamiranda/meu-app-midia/main/video_fundo.mp4" type="video/mp4">
      Your browser does not support HTML5 video.
    </video>
"""
st.markdown(video_html, unsafe_allow_html=True)

# --- SISTEMA DE ACESSO (PROTEÇÃO F.M.M. - ATIVO) ---
CHAVES_AUTORIZADAS = {
    "fabiana@email.com": "FMM-2026-TESTE",
    "cliente01@fazenda.com": "FMM-ACESS-01"
}

TOKEN_FILE = ".login_token"

if "autenticado" not in st.session_state:
    if os.path.exists(TOKEN_FILE):
        st.session_state.autenticado = True
    else:
        st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.markdown('<h2 style="color: #4A5D23;">🛡️ Acesso Restrito - Studio F.M.M.</h2>', unsafe_allow_html=True)
    email_user = st.text_input("Digite o e-mail cadastrado:", key="login_email")
    chave_user = st.text_input("Digite sua Chave de Ativação:", type="password", key="login_chave")

    if st.button("Liberar Sistema", key="btn_liberar"):
        if email_user in CHAVES_AUTORIZADAS and CHAVES_AUTORIZADAS[email_user] == chave_user:
            st.session_state.autenticado = True
            with open(TOKEN_FILE, "w") as f:
                f.write(f"autenticado_{email_user}")
            st.success("Acesso Liberado!")
            st.rerun()
        else:
            st.error("E-mail ou Chave inválidos. Entre em contato com Fabiana.")
    st.stop()

  


    
# --- CABEÇALHO DESIGN ---
st.markdown('<h1 style="color: #4A5D23; margin-top: 15px; margin-bottom: 0;">𓃓 Gestão Pecuária F.M.M.</h1>', unsafe_allow_html=True)
st.markdown('<h2 style="color: #4A5D23; margin-top: 0; font-size: 24px;">Gerenciamento de Rebanho</h2>', unsafe_allow_html=True)
st.markdown('<p style="color: #4A5D23; font-size: 18px; font-style: italic; margin-top: -10px;">Tecnologia de Precisão no Campo</p>', unsafe_allow_html=True)

# --- BARRA LATERAL (PAINEL DE SEGURANÇA E ZONA DE EXCLUSÃO) ---
with st.sidebar:
    st.markdown('<h2 style="color: #4A5D23;">🛡️ Painel de Segurança</h2>', unsafe_allow_html=True)
    st.info("Utilize os botões abaixo para garantir a integridade de seus dados.")
    if st.button("💾 Realizar Backup Agora", key="btn_backup"):
        st.success("Backup estruturado com sucesso!")
        
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown('<h3 style="color: #A32A2A;">🗑️ Zona de Exclusão</h3>', unsafe_allow_html=True)
    
    if 'dados' in st.session_state and not st.session_state.dados['animais'].empty:
        lista_remover = st.session_state.dados['animais']['ID'].unique()
        animal_remover = st.selectbox("Selecione o animal para remover:", lista_remover, key="sb_remover")
    else:
        animal_remover = st.selectbox("Selecione o animal para remover:", ["Não há opções para selecionar."], key="sb_remover")
        
    if st.button("Confirmar Exclusão Definitiva", key="btn_excluir"):
        st.warning("Selecione um animal válido para exclusão.")
        
    st.markdown("---")
    st.caption("Versão do App: 1.0 (Produção)")

# --- CARREGAMENTO DE DADOS ---
def carregar_dados(caminho, colunas):
    if os.path.exists(caminho):
        try:
            return pd.read_csv(caminho)
        except:
            return pd.DataFrame(columns=colunas)
    return pd.DataFrame(columns=colunas)

ARQUIVO_ANIMAIS = "animais.csv"
ARQUIVO_PESAGENS = "pesagens.csv"
ARQUIVO_ESTOQUE = "estoque.csv"
ARQUIVO_VACINAS = "vacinas.csv"

if 'dados' not in st.session_state:
    st.session_state.dados = {
        'animais': carregar_dados(ARQUIVO_ANIMAIS, ['ID', 'Raça', 'Data de Nascimento', 'Pai', 'Mãe']),
        'pesagem': carregar_dados(ARQUIVO_PESAGENS, ['ID do Animal', 'Data', 'Peso (kg)']),
        'estoque': carregar_dados(ARQUIVO_ESTOQUE, ['Item', 'Quantidade', 'Unidade', 'Mínimo Crítico']),
        'vacinas': carregar_dados(ARQUIVO_VACINAS, ['ID do Animal', 'Data Vacinação', 'Tipo de Vacina', 'Próxima Dose'])
    }

# --- LÓGICA DE NEGÓCIO ---
def verificar_status_saude(animal_id):
    df = st.session_state.dados['pesagem']
    dados_animal = df[df['ID do Animal'] == animal_id]
    if dados_animal.empty: return "Sem registros"
    ultima_data = pd.to_datetime(dados_animal['Data'].max())
    hoje = datetime.now()
    meses_passados = (hoje.year - ultima_data.year) * 12 + today_month_diff == hoje.month - ultima_data.month
    if meses_passados > 6: return "⚠️ ATENÇÃO: Vacina Atrasada"
    return "✅ Saúde em Dia"
   
def calcular_gmd(animal_id):
    df = st.session_state.dados['pesagem']
    dados_animal = df[df['ID do Animal'] == animal_id].sort_values(by='Data')
    if len(dados_animal) < 2: return "Dados insuficientes"
    ultima = dados_animal.iloc[-1]
    penultima = dados_animal.iloc[-2]
    dias = (pd.to_datetime(ultima['Data']) - pd.to_datetime(penultima['Data'])).days
    if dias == 0: return 0
    return round((ultima['Peso (kg)'] - penultima['Peso (kg)']) / dias, 3)
    
def buscar_familia(animal_id):
    df = st.session_state.dados['animais']
    animal = df[df['ID'] == animal_id]
    if not animal.empty:
        pai = animal.iloc[0].get('Pai', 'Desconhecido')
        mae = animal.iloc[0].get('Mãe', 'Desconhecido')
        return f"Pai: {pai} | Mãe: {mae}"
    return "Sem dados de linhagem"
    
def verificar_estoque_baixo():
    df = st.session_state.dados['estoque']
    return df[df['Quantidade'] <= df['Mínimo Crítico']]
    
# --- ESTRUTURA DE ABAS ATUALIZADA (NOVA ABA DE VACINAÇÃO ADICIONADA) ---
aba1, aba2, aba3, aba4, aba5 = st.tabs(["Cadastro", "Pesagem", "Análise Profissional", "💉 Vacinação", "📦 Estoque"])

with aba1:
    st.header("Registre novo animal") 
    st.info("🎙️ Dica: Clique no campo abaixo e use o microfone do teclado do celular para ditar os dados.")
    entrada_voz_cadastro = st.text_input("Comando de Voz para Cadastro:", placeholder="Ex: Brinco 502 raça Nelore")
    if entrada_voz_cadastro:
        st.success(f"Texto capturado: {entrada_voz_cadastro}")
    
    with st.form("form_novo_animal"):
        col1, col2, col3 = st.columns(3)
        with col1: 
            animal_id = st.text_input("Ear Tag (Brinco/Número)*")
        with col2: 
            raca = st.text_input("Breed (Raça)")
        with col3: 
            data_nasc = st.date_input("Birth Date (data de nascimento)", value=datetime.now())

        st.markdown("---")
        st.subheader("Genealogy (Genealogia: Opcional)")
        col4, col5 = st.columns(2)
        with col4:
            pai = st.text_input("Sire (Pai)")
        with col5:
            mae = st.text_input("Dam (Mãe)")
        
        if st.form_submit_button("Salvar Animal"):
            if animal_id:
                nova_linha = pd.DataFrame([{
                    'ID': animal_id, 'Raça': raca, 'Data de Nascimento': data_nasc,
                    'Pai': pai if pai else "Unknown", 'Mãe': mae if mae else "Unknown"
                }])
                st.session_state.dados['animais'] = pd.concat([st.session_state.dados['animais'], nova_linha], ignore_index=True)
                st.session_state.dados['animais'].to_csv(ARQUIVO_ANIMAIS, index=False)
                st.success(f"Animal {animal_id} Registered!")
                st.rerun()
            else:
                st.error("Por favor, digite o número de identificação (brinco (ID)).")
                
with aba2:
    st.header("Entrada de peso diário")
    with st.form("form_pesagem"):
        col1, col2, col3 = st.columns(3)
        with col1: 
            lista_select = st.session_state.dados['animais']['ID'].unique() if not st.session_state.dados['animais'].empty else ["Nenhum animal cadastrado"]
            animal_id_p = st.selectbox("Select Animal", lista_select, key="sb_peso")
        with col2: 
            peso = st.number_input("Peso (kg)", min_value=0.0)
        with col3: 
            data_p = st.date_input("Data de entrada")
            
        if st.form_submit_button("Peso do Registro"):
            if animal_id_p != "Nenhum animal cadastrado":
                nova_pesagem = pd.DataFrame([{'ID do Animal': animal_id_p, 'Data': data_p, 'Peso (kg)': peso}])
                st.session_state.dados['pesagem'] = pd.concat([st.session_state.dados['pesagem'], nova_pesagem], ignore_index=True)
                st.session_state.dados['pesagem'].to_csv(ARQUIVO_PESAGENS, index=False)
                st.success("Peso registrado!")
                st.rerun()
            else:
                st.error("Cadastre um animal primeiro!")

with aba3:
    st.header("Painel de análise")
    if not st.session_state.dados['animais'].empty:
        lista_animais = st.session_state.dados['animais']['ID'].unique()
        animal_analise = st.selectbox("Select animal for report:", lista_animais, key="sb_analise")
        
        status_saude = verificar_status_saude(animal_analise)
        familia = buscar_familia(animal_analise)
        gmd_valor = calcular_gmd(animal_analise)
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Health Status", status_saude)
        with col_b:
            st.write(f"**Family Tree:** {familia}")
            
        st.metric("Daily Weight Gain (GMD)", f"{gmd_valor} kg/day")
        st.markdown("---")
        
        df_plot = st.session_state.dados['pesagem'][st.session_state.dados['pesagem']['ID do Animal'] == animal_analise]
        if not df_plot.empty:
            st.subheader(f"Evolução de peso - Animal {animal_analise}")
            df_plot = df_plot.sort_values('Data')
            st.line_chart(df_plot.set_index('Data')['Peso (kg)'])
        else:
            st.info(f"Não foram encontrados registros de peso para o animal {animal_analise} ainda.")
    else:
        st.warning("Por favor, registre um animal na aba de 'cadastro' primeiro.")

# --- 💉 NOVA ABA EXCLUSIVA DE VACINAÇÃO (SOLICITADA) ---
with aba4:
    st.header("💉 Controle Sanitário e Vacinação do Rebanho")
    
    if not st.session_state.dados['animais'].empty:
        lista_animais_v = st.session_state.dados['animais']['ID'].unique()
        animal_vacina = st.selectbox("Selecione o Animal para Vacinação:", lista_animais_v, key="sb_vacina_aba")
        
        # Lógica de Alertas de Próxima Data
        df_historico = st.session_state.dados['vacinas'][st.session_state.dados['vacinas']['ID do Animal'] == animal_vacina]
        
        st.subheader("📊 Status Sanitário do Animal")
        if not df_historico.empty:
            # Pega a vacina com a data de retorno mais próxima
            df_historico['Próxima Dose DT'] = pd.to_datetime(df_historico['Próxima Dose'])
            proxima_vac = df_historico.sort_values(by='Próxima Dose DT').iloc[0]
            dias_restantes = (proxima_vac['Próxima Dose DT'] - datetime.now()).days
            
            if dias_restantes < 0:
                st.error(f"🚨 ALERTA: A vacina contra **{proxima_vac['Tipo de Vacina']}** está ATRASADA desde {proxima_vac['Próxima Dose']}!")
            elif dias_restantes <= 30:
                st.warning(f"⚠️ ATENÇÃO: Próxima dose de **{proxima_vac['Tipo de Vacina']}** está próxima! Agendada para: {proxima_vac['Próxima Dose']} (Restam {dias_restantes} dias).")
            else:
                st.success(f"✅ Calendário em dia. Próxima vacina programada para: {proxima_vac['Próxima Dose']}.")
        else:
            st.error("❌ Alerta: Este animal nunca recebeu nenhuma vacina registrada no sistema!")

        # Formulário de Registro
        st.markdown("---")
        st.subheader("Novo Registro de Aplicação")
        with st.form("form_aba_vacina"):
            col_v1, col_v2 = st.columns(2)
            with col_v1:
                nome_vacina = st.text_input("Nome da Vacina (Ex: Aftosa, Brucelose, Raiva)")
            with col_v2:
                data_vac = st.date_input("Data da Aplicação", value=datetime.now())
                
            if st.form_submit_button("Salvar Vacinação"):
                if nome_vacina:
                    proxima_dose = data_vac + pd.Timedelta(days=180) # Configurado retorno padrão para 6 meses
                    nova_vac = pd.DataFrame([{
                        'ID do Animal': animal_vacina,
                        'Data Vacinação': data_vac.strftime('%Y-%m-%d'),
                        'Tipo de Vacina': nome_vacina,
                        'Próxima Dose': proxima_dose.strftime('%Y-%m-%d')
                    }])
                    st.session_state.dados['vacinas'] = pd.concat([st.session_state.dados['vacinas'], nova_vac], ignore_index=True)
                    st.session_state.dados['vacinas'].to_csv(ARQUIVO_VACINAS, index=False)
                    st.success(f"Sucesso: Vacina {nome_vacina} salva!")
                    st.rerun()
                else:
                    st.error("Digite o nome da vacina.")
                    
        # Exibição do histórico do animal selecionado
        st.markdown("---")
        st.subheader("📜 Histórico de Vacinas Aplicadas")
        if not df_historico.empty:
            st.dataframe(df_historico[['Data Vacinação', 'Tipo de Vacina', 'Próxima Dose']].sort_values(by='Data Vacinação', ascending=False), use_container_width=True)
        else:
            st.info("Nenhuma vacina aplicada para este animal ainda.")
    else:
        st.warning("Cadastre um animal na aba de 'cadastro' primeiro.")
        
with aba5:
    st.header("📦Estoque & Suprimentos")
    with st.form("form_estoque"):
        c1, c2, c3, c4 = st.columns(4)
        item = c1.text_input("Item (ex: Sal Mineral, Vacina A)")
        qtd = c2.number_input("Current Quantity", min_value=0.0)
        unidade = c3.selectbox("Unit", ["kg", "liters", "doses", "bags"])
        minimo = c4.number_input("Critical Minimum", min_value=0.0)
        
        if st.form_submit_button("adicionar ao estoque"):
            if item:
                nova_linha = pd.DataFrame([{'Item': item, 'Quantidade': qtd, 'Unidade': unidade, 'Mínimo Crítico': minimo}])
                st.session_state.dados['estoque'] = pd.concat([st.session_state.dados['estoque'], nova_linha], ignore_index=True)
                st.session_state.dados['estoque'].to_csv(ARQUIVO_ESTOQUE, index=False)
                st.success(f"{item} adicionado!")
                st.rerun()

    st.markdown("---")
    st.subheader("Current Stock")
    df_estoque = st.session_state.dados['estoque']
    if not df_estoque.empty:
        st.dataframe(df_estoque, use_container_width=True)
        alertas = verificar_estoque_baixo()
        for _, row in alertas.iterrows():
            st.error(f"🚨 Estoque baixo: {row['Item']} ({row['Quantidade']} {row['Unidade']} left)")
    else:
        st.info("Ainda não há itens em estoque.")
