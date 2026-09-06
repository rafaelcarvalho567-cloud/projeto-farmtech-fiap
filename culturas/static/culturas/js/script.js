// FarmTech Solutions - interação da página de Clima
// 1) Geocodifica a cidade/CEP digitada em /api/geocode/ (lat/lon)
// 2) Consulta o clima nessas coordenadas em /api/clima/
// Tudo exibido dinamicamente, sem recarregar a página.

document.addEventListener('DOMContentLoaded', function () {
    var formClima = document.getElementById('form-clima');
    if (!formClima) return;

    var resultadoDiv = document.getElementById('resultado-clima');

    formClima.addEventListener('submit', function (evento) {
        evento.preventDefault();

        var consulta = document.getElementById('cidade_cep').value;
        resultadoDiv.innerHTML = '<div class="stat-card"><h3>Localizando...</h3></div>';

        fetch('/api/geocode/?q=' + encodeURIComponent(consulta))
            .then(function (resposta) { return resposta.json(); })
            .then(function (local) {
                if (!local.ok) {
                    resultadoDiv.innerHTML =
                        '<div class="stat-card"><h3>Erro</h3><p>' + local.erro + '</p></div>';
                    return null;
                }

                resultadoDiv.innerHTML = '<div class="stat-card"><h3>Consultando clima...</h3></div>';

                var nomeLocal = local.nome + (local.estado ? ' - ' + local.estado : '');
                var url = '/api/clima/?lat=' + local.latitude +
                          '&lon=' + local.longitude +
                          '&local=' + encodeURIComponent(nomeLocal);

                return fetch(url).then(function (resposta) { return resposta.json(); });
            })
            .then(function (dados) {
                if (!dados) return; // erro já tratado na etapa de geocodificação

                if (!dados.ok) {
                    resultadoDiv.innerHTML =
                        '<div class="stat-card"><h3>Erro</h3><p>' + dados.erro + '</p></div>';
                    return;
                }

                resultadoDiv.innerHTML =
                    '<div class="stat-card">' +
                        '<h3>' + dados.local + '</h3>' +
                        '<p><span class="stat-label">Temperatura</span>' +
                        '<span class="stat-value">' + dados.temperatura + ' °C</span></p>' +
                    '</div>' +
                    '<div class="stat-card">' +
                        '<h3>Umidade / Vento</h3>' +
                        '<p><span class="stat-label">Umidade relativa</span>' +
                        '<span class="stat-value">' + dados.umidade + ' %</span></p>' +
                        '<p><span class="stat-label">Vento</span>' +
                        '<span class="stat-value">' + dados.vento + ' km/h</span></p>' +
                    '</div>' +
                    '<div class="stat-card">' +
                        '<h3>Precipitação</h3>' +
                        '<p><span class="stat-label">Registrada</span>' +
                        '<span class="stat-value">' + dados.precipitacao + ' mm</span></p>' +
                        '<p><span class="stat-label">Horário da leitura</span>' +
                        '<span class="stat-value">' + dados.horario + '</span></p>' +
                    '</div>';
            })
            .catch(function (erro) {
                resultadoDiv.innerHTML =
                    '<div class="stat-card"><h3>Erro de conexão</h3><p>' + erro + '</p></div>';
            });
    });
});
