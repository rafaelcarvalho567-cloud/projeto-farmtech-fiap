import re
import statistics

import requests
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import Cultura


def home(request):
    """Saida de Dados: lista todas as culturas cadastradas."""
    culturas = Cultura.objects.all()
    return render(request, 'culturas/home.html', {'culturas': culturas})


def nova_cultura(request):
    """Entrada de Dados: cadastra uma nova cultura."""
    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()
        largura = float(request.POST.get('largura'))
        comprimento = float(request.POST.get('comprimento'))
        ruas = int(request.POST.get('ruas'))
        Cultura.objects.create(
            nome=nome, largura=largura, comprimento=comprimento, ruas=ruas
        )
        messages.success(request, f'Cultura "{nome}" cadastrada com sucesso!')
        return redirect('home')
    return render(request, 'culturas/form.html', {'titulo': 'Nova Cultura', 'cultura': None})


def editar_cultura(request, pk):
    """Atualização de Dados de uma cultura existente."""
    cultura = get_object_or_404(Cultura, pk=pk)
    if request.method == 'POST':
        cultura.nome = request.POST.get('nome', '').strip()
        cultura.largura = float(request.POST.get('largura'))
        cultura.comprimento = float(request.POST.get('comprimento'))
        cultura.ruas = int(request.POST.get('ruas'))
        cultura.save()
        messages.success(request, f'Cultura "{cultura.nome}" atualizada com sucesso!')
        return redirect('home')
    return render(request, 'culturas/form.html', {'titulo': 'Editar Cultura', 'cultura': cultura})


def deletar_cultura(request, pk):
    """Deleção de Dados de uma cultura."""
    cultura = get_object_or_404(Cultura, pk=pk)
    if request.method == 'POST':
        nome = cultura.nome
        cultura.delete()
        messages.success(request, f'Cultura "{nome}" deletada com sucesso!')
        return redirect('home')
    return render(request, 'culturas/confirma_exclusao.html', {'cultura': cultura})


def estatisticas(request):
    """Equivalente ao Estatistica_Farm_Tech.R: media e desvio padrao de area e ruas."""
    culturas = Cultura.objects.all()
    contexto = {'tem_dados': culturas.exists(), 'culturas': culturas}

    if contexto['tem_dados']:
        areas = [c.area for c in culturas]
        ruas = [c.ruas for c in culturas]
        contexto.update({
            'media_area': round(statistics.mean(areas), 2),
            'desvio_area': round(statistics.stdev(areas), 2) if len(areas) > 1 else 0,
            'media_ruas': round(statistics.mean(ruas), 2),
            'desvio_ruas': round(statistics.stdev(ruas), 2) if len(ruas) > 1 else 0,
        })

    return render(request, 'culturas/estatisticas.html', contexto)


def clima(request):
    """Pagina que consome a API de clima (equivalente ao Clima_API.R)."""
    return render(request, 'culturas/clima.html')


def geocode(request):
    """
    Recebe uma cidade (ex: 'Ribeirão Preto, SP') ou um CEP e devolve
    latitude/longitude. Se for CEP, primeiro resolve a cidade via ViaCEP;
    depois usa a API de geocodificação do Open-Meteo para achar as coordenadas.
    """
    query = request.GET.get('q', '').strip()
    if not query:
        return JsonResponse({'ok': False, 'erro': 'Informe uma cidade ou CEP.'}, status=400)

    nome_busca = query
    cep_limpo = re.sub(r'\D', '', query)

    if len(cep_limpo) == 8:
        try:
            resp_cep = requests.get(f'https://viacep.com.br/ws/{cep_limpo}/json/', timeout=10)
            resp_cep.raise_for_status()
            dados_cep = resp_cep.json()
        except requests.RequestException as exc:
            return JsonResponse({'ok': False, 'erro': f'Erro ao consultar o CEP: {exc}'}, status=502)

        if dados_cep.get('erro'):
            return JsonResponse({'ok': False, 'erro': 'CEP não encontrado.'}, status=404)

        nome_busca = f"{dados_cep['localidade']}, {dados_cep['uf']}"

    try:
        resp_geo = requests.get(
            'https://geocoding-api.open-meteo.com/v1/search',
            params={
                'name': nome_busca.split(',')[0].strip(),
                'count': 1,
                'language': 'pt',
                'country_code': 'BR',
            },
            timeout=10,
        )
        resp_geo.raise_for_status()
        resultados = resp_geo.json().get('results') or []
    except requests.RequestException as exc:
        return JsonResponse({'ok': False, 'erro': f'Erro ao buscar coordenadas: {exc}'}, status=502)

    if not resultados:
        return JsonResponse({'ok': False, 'erro': f'Local "{nome_busca}" não encontrado.'}, status=404)

    melhor = resultados[0]
    return JsonResponse({
        'ok': True,
        'nome': melhor['name'],
        'estado': melhor.get('admin1', ''),
        'latitude': melhor['latitude'],
        'longitude': melhor['longitude'],
    })


def clima_api(request):
    """Endpoint consumido via JS: consulta a API publica Open-Meteo."""
    latitude = request.GET.get('lat', '-21.1775')
    longitude = request.GET.get('lon', '-47.8103')
    local = request.GET.get('local', 'Fazenda - Ribeirão Preto/SP')

    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}&longitude={longitude}"
        "&current=temperature_2m,relative_humidity_2m,wind_speed_10m,precipitation"
    )

    try:
        resposta = requests.get(url, timeout=10)
        resposta.raise_for_status()
        atual = resposta.json().get('current', {})
        return JsonResponse({
            'ok': True,
            'local': local,
            'temperatura': atual.get('temperature_2m'),
            'umidade': atual.get('relative_humidity_2m'),
            'vento': atual.get('wind_speed_10m'),
            'precipitacao': atual.get('precipitation'),
            'horario': atual.get('time'),
        })
    except requests.RequestException as exc:
        return JsonResponse({'ok': False, 'erro': str(exc)}, status=502)
