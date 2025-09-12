# ===================================================================
# ATIVIDADE AVALIATIVA - FARMTECH SOLUTIONS
# SCRIPT DE ANÁLISE EM R (VERSÃO FINAL COMPLETA)
# ===================================================================

# --- 1. INSTALAÇÃO DE PACOTES ---
# Se já instalou, pode deixar estas linhas comentadas.
# install.packages("dplyr")
# install.packages("ggplot2")
# install.packages("httr")
# install.packages("jsonlite")


# --- 2. CARREGAMENTO DOS PACOTES ---
library(dplyr)
library(ggplot2)
library(httr)
library(jsonlite)


# ===================================================================
# PARTE 1: ANÁLISE DOS DADOS DE CULTURAS (DO ARQUIVO CSV)
# ===================================================================
cat("===== ANÁLISE DOS DADOS DE CULTURAS =====\n")

tryCatch({
  dados <- read.csv("dados_culturas.csv", sep = ",", header = TRUE, encoding = "UTF-8")
  
  print("=== Dados Carregados do CSV ===")
  print(dados)
  
  cat("\n=== Estatísticas Gerais ===\n")
  cat("Média da área:", mean(dados$Area_m2), "m²\n")
  cat("Desvio padrão da área:", sd(dados$Area_m2), "\n")
  
  cat("\n=== Estatísticas por Cultura ===\n")
  estatisticas <- dados %>%
    group_by(Cultura) %>%
    summarise(media_area = mean(Area_m2), desvio_area = sd(Area_m2), .groups = 'drop')
  print(estatisticas)
  
  # --- GERAÇÃO E SALVAMENTO DOS GRÁFICOS ---
  
  # 1. Gráfico de Barras (Área)
  grafico_area <- ggplot(dados, aes(x = Cultura, y = Area_m2, fill = Cultura)) +
    geom_bar(stat = "identity") +
    labs(title = "Área de Plantio por Cultura", x = "Cultura", y = "Área (m²)")
  
  # Salva o primeiro gráfico
  ggsave("grafico_area_por_cultura.png", plot = grafico_area, width = 8, height = 6)
  
  # 2. Gráfico de Pizza (Insumos)
  grafico_insumos <- ggplot(dados, aes(x = "", y = Quantidade, fill = Cultura)) +
    geom_bar(stat = "identity", width = 1) +
    coord_polar("y", start = 0) +
    labs(title = "Distribuição de Insumos por Cultura")
  
  # Salva o segundo gráfico (ESTA É A LINHA QUE FALTAVA)
  ggsave("grafico_distribuicao_insumos.png", plot = grafico_insumos, width = 8, height = 6)
  
  cat("\nGráficos salvos com sucesso na pasta do projeto!\n")
  
}, error = function(e) {
  cat("\nERRO: Não foi possível ler o arquivo 'dados_culturas.csv'.\n")
})


# ===================================================================
# PARTE 2: IR ALÉM (CONEXÃO COM API DE METEOROLOGIA)
# ===================================================================
cat("\n\n===== CONSULTA DE PREVISÃO DO TEMPO =====\n")

url_api <- "https://api.open-meteo.com/v1/forecast?latitude=-2.51&longitude=-42.13&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&timezone=America/Sao_Paulo"

tryCatch({
  resposta <- GET(url_api )
  
  if (status_code(resposta) == 200) {
    dados_clima <- fromJSON(content(resposta, "text"))
    cat("Previsão do tempo para os próximos dias em Água Doce do Maranhão, MA:\n")
    for (i in 1:length(dados_clima$daily$time)) {
      dia <- dados_clima$daily$time[i]
      temp_max <- dados_clima$daily$temperature_2m_max[i]
      temp_min <- dados_clima$daily$temperature_2m_min[i]
      chuva <- dados_clima$daily$precipitation_sum[i]
      cat(paste0("----------------------------------------\n", "Data: ", dia, "\n", "  - Temperatura Máxima: ", temp_max, " °C\n", "  - Temperatura Mínima: ", temp_min, " °C\n", "  - Precipitação Prevista: ", chuva, " mm\n"))
    }
  } else {
    cat("Falha ao conectar com a API. Código de status:", status_code(resposta), "\n")
  }
}, error = function(e) {
  cat("Ocorreu um erro de conexão com a API. Verifique sua internet.\n")
})
