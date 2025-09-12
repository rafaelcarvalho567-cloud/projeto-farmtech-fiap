# ===================================================================
# ATIVIDADE AVALIATIVA - FARMTECH SOLUTIONS
# SCRIPT DE ANÁLISE EM R (VERSÃO FINAL COMPLETA)
# ===================================================================

# --- 1. INSTALAÇÃO DE PACOTES ---
# Esta seção garante que todos os pacotes necessários estejam instalados.
# Execute estas linhas UMA ÚNICA VEZ. Depois, pode comentá-las.
install.packages("dplyr")
install.packages("ggplot2")
install.packages("httr")
install.packages("jsonlite")


# --- 2. CARREGAMENTO DOS PACOTES ---
# Carrega todos os pacotes necessários para a sessão atual do R.
library(dplyr)
library(ggplot2)
library(httr)
library(jsonlite)


# ===================================================================
# PARTE 1: ANÁLISE DOS DADOS DE CULTURAS (DO ARQUIVO CSV)
# ===================================================================
cat("===== ANÁLISE DOS DADOS DE CULTURAS =====\n")

# O bloco tryCatch lida com erros de forma elegante.
# Se o arquivo CSV não for encontrado, ele mostrará uma mensagem útil.
tryCatch({
  # Lê o arquivo CSV gerado pelo Python.
  dados <- read.csv("dados_culturas.csv", sep = ",", header = TRUE, encoding = "UTF-8")
  
  # Mostra os dados que foram carregados.
  print("=== Dados Carregados do CSV ===")
  print(dados)
  
  # Calcula e exibe estatísticas gerais.
  cat("\n=== Estatísticas Gerais ===\n")
  cat("Média da área:", mean(dados$Area_m2), "m²\n")
  cat("Desvio padrão da área:", sd(dados$Area_m2), "\n")
  
  # Calcula e exibe estatísticas por tipo de cultura.
  cat("\n=== Estatísticas por Cultura ===\n")
  estatisticas <- dados %>%
    group_by(Cultura) %>%
    summarise(
      media_area = mean(Area_m2),
      desvio_area = sd(Area_m2),
      .groups = 'drop'
    )
  print(estatisticas)
  
  # Salva os gráficos em arquivos PNG.
  ggsave("grafico_area_por_cultura.png", plot = ggplot(dados, aes(x = Cultura, y = Area_m2, fill = Cultura)) + geom_bar(stat = "identity"))
  cat("\nGráficos salvos com sucesso na pasta do projeto!\n")
  
}, error = function(e) {
  # Mensagem de erro se o arquivo 'dados_culturas.csv' não for encontrado.
  cat("\nERRO: Não foi possível ler o arquivo 'dados_culturas.csv'.\n")
  cat("Verifique se o arquivo CSV está na mesma pasta que este script R.\n")
  cat("Dica: Use o menu 'Session' -> 'Set Working Directory' para definir a pasta correta.\n")
})


# ===================================================================
# PARTE 2: IR ALÉM (CONEXÃO COM API DE METEOROLOGIA)
# ===================================================================
cat("\n\n===== CONSULTA DE PREVISÃO DO TEMPO =====\n")

# URL da API para Água Doce do Maranhão, MA (Latitude: -2.51, Longitude: -42.13)
url_api <- "https://api.open-meteo.com/v1/forecast?latitude=-2.51&longitude=-42.13&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&timezone=America/Sao_Paulo"

tryCatch({
  # Faz a requisição GET para a API.
  resposta <- GET(url_api )
  
  # Verifica se a conexão foi bem-sucedida.
  if (status_code(resposta) == 200) {
    # Converte a resposta da API para um formato que o R entende.
    dados_clima <- fromJSON(content(resposta, "text"))
    
    cat("Previsão do tempo para os próximos dias em Água Doce do Maranhão, MA:\n")
    
    # Loop para exibir a previsão de cada dia.
    for (i in 1:length(dados_clima$daily$time)) {
      dia <- dados_clima$daily$time[i]
      temp_max <- dados_clima$daily$temperature_2m_max[i]
      temp_min <- dados_clima$daily$temperature_2m_min[i]
      chuva <- dados_clima$daily$precipitation_sum[i]
      
      cat(paste0(
        "----------------------------------------\n",
        "Data: ", dia, "\n",
        "  - Temperatura Máxima: ", temp_max, " °C\n",
        "  - Temperatura Mínima: ", temp_min, " °C\n",
        "  - Precipitação Prevista: ", chuva, " mm\n"
      ))
    }
  } else {
    # Mensagem de erro se a API não responder corretamente.
    cat("Falha ao conectar com a API de meteorologia. Código de status:", status_code(resposta), "\n")
  }
}, error = function(e) {
  # Mensagem de erro se houver um problema de conexão com a internet.
  cat("Ocorreu um erro de conexão com a API. Verifique sua conexão com a internet.\n")
})
