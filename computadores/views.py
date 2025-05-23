from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Computador
from .forms import ComputadorForm


@login_required
def lista_computadores(request):
    computadores = Computador.objects.all().order_by(
        'sala__numero', 'numero_identificacao')
    return render(request, 'computadores/lista_computadores.html', {'computadores': computadores})


@login_required
def registar_computador(request):
    if request.method == 'POST':
        form = ComputadorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Computador registado com sucesso!')
            return redirect('computadores:lista_computadores')
    else:
        sala_id = request.GET.get('sala')
        initial_data = {}
        if sala_id:
            initial_data['sala'] = sala_id
        form = ComputadorForm(initial=initial_data)
    return render(request, 'computadores/registar_computador.html', {'form': form})


@login_required
def detalhe_computador(request, pk):
    computador = get_object_or_404(Computador, pk=pk)
    anomalias = computador.anomalias.all()
    return render(request, 'computadores/detalhe_computador.html', {
        'computador': computador,
        'anomalias': anomalias
    })
