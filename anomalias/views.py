from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Anomalia
from .forms import AnomaliaForm, AnomaliaFilterForm


@login_required
def lista_anomalias(request):
    anomalias = Anomalia.objects.all().order_by('-data_registo')
    form = AnomaliaFilterForm(request.GET)

    if form.is_valid():
        if form.cleaned_data.get('sala'):
            anomalias = anomalias.filter(
                computador__sala=form.cleaned_data['sala'])
        if form.cleaned_data.get('estado'):
            anomalias = anomalias.filter(estado=form.cleaned_data['estado'])

    context = {
        'anomalias': anomalias,
        'form': form,
    }
    return render(request, 'anomalias/lista_anomalias.html', context)


@login_required
def registar_anomalia(request):
    if request.method == 'POST':
        form = AnomaliaForm(request.POST)
        if form.is_valid():
            anomalia = form.save(commit=False)
            anomalia.reportado_por = request.user
            anomalia.save()
            messages.success(request, 'Anomalia registada com sucesso!')
            return redirect('anomalias:lista_anomalias')
    else:
        computador_id = request.GET.get('computador')
        initial_data = {}
        if computador_id:
            initial_data['computador'] = computador_id
        form = AnomaliaForm(initial=initial_data)
    return render(request, 'anomalias/registar_anomalia.html', {'form': form})


@login_required
def atualizar_estado(request, pk):
    anomalia = get_object_or_404(Anomalia, pk=pk)
    if request.method == 'POST':
        novo_estado = request.POST.get('estado')
        if novo_estado in dict(Anomalia.ESTADO_CHOICES):
            anomalia.estado = novo_estado
            anomalia.save()
            messages.success(request, 'Estado atualizado com sucesso!')
    return redirect('anomalias:lista_anomalias')
