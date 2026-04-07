from django.shortcuts import render, redirect, get_object_or_404
from django import forms
from .models import Contenido
from datetime import datetime
import re
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group

# -------- Formulario personalizado con select para el año --------
class ContenidoForm(forms.ModelForm):
    # Generar lista de años desde 1888 hasta año actual + 1 (para incluir el siguiente año)
    AÑOS = [(a, a) for a in range(1888, datetime.now().year + 2)]

    anio = forms.ChoiceField(
        choices=AÑOS,
        label="Año",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Contenido
        fields = ['titulo', 'descripcion', 'anio', 'genero', 'imagen_url', 'video_url']
        labels = {
            'titulo': 'Título',
            'descripcion': 'Descripción',
            'anio': 'Año',
            'genero': 'Género',
            'imagen_url': 'URL del póster',
            'video_url': 'URL del tráiler',
        }
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4}),
        }

# ---------- FUNCIÓN PARA VERIFICAR SI ES ADMIN ----------
def es_admin(user):
    return user.is_authenticated and (user.is_superuser or user.groups.filter(name='Administradores').exists())

# ---------- READ con filtro por género ----------
def lista_contenido(request):
    genero_filtro = request.GET.get('genero', None)
    contenidos = Contenido.objects.all().order_by('-anio')
    
    if genero_filtro and genero_filtro != 'todos':
        contenidos = contenidos.filter(genero__iexact=genero_filtro)
    
    generos = Contenido.objects.exclude(genero__isnull=True).exclude(genero__exact='').values_list('genero', flat=True).distinct().order_by('genero')
    
    context = {
        'contenidos': contenidos,
        'generos': generos,
        'genero_seleccionado': genero_filtro,
        'es_admin': es_admin(request.user),  # ← pasamos variable al template
    }
    return render(request, 'catalogos/lista.html', context)

# ---------- CREATE (solo admin) ----------
@user_passes_test(es_admin)
def crear_contenido(request):
    if request.method == 'POST':
        form = ContenidoForm(request.POST)
        if form.is_valid():
            form.instance.anio = int(form.cleaned_data['anio'])
            form.save()
            return redirect('lista_contenido')
    else:
        form = ContenidoForm()
    return render(request, 'catalogos/formulario.html', {'form': form, 'accion': 'Crear'})

# ---------- UPDATE (solo admin) ----------
@user_passes_test(es_admin)
def editar_contenido(request, pk):
    contenido = get_object_or_404(Contenido, pk=pk)
    if request.method == 'POST':
        form = ContenidoForm(request.POST, instance=contenido)
        if form.is_valid():
            form.instance.anio = int(form.cleaned_data['anio'])
            form.save()
            return redirect('lista_contenido')
    else:
        initial_data = {'anio': contenido.anio}
        form = ContenidoForm(instance=contenido, initial=initial_data)
    return render(request, 'catalogos/formulario.html', {'form': form, 'accion': 'Editar'})

# ---------- DELETE (solo admin) ----------
@user_passes_test(es_admin)
def eliminar_contenido(request, pk):
    contenido = get_object_or_404(Contenido, pk=pk)
    if request.method == 'POST':
        contenido.delete()
        return redirect('lista_contenido')
    return render(request, 'catalogos/confirmar_eliminar.html', {'contenido': contenido})

# ---------- DETALLE CON VIDEO (público) ----------

@login_required
def detalle_contenido(request, pk):
    contenido = get_object_or_404(Contenido, pk=pk)
    youtube_id = None
    if contenido.video_url:
        embed_match = re.search(r'youtube\.com/embed/([a-zA-Z0-9_-]+)', contenido.video_url)
        watch_match = re.search(r'youtube\.com/watch\?v=([a-zA-Z0-9_-]+)', contenido.video_url)
        short_match = re.search(r'youtu\.be/([a-zA-Z0-9_-]+)', contenido.video_url)
        if embed_match:
            youtube_id = embed_match.group(1)
        elif watch_match:
            youtube_id = watch_match.group(1)
        elif short_match:
            youtube_id = short_match.group(1)
    return render(request, 'catalogos/detalle.html', {
        'contenido': contenido,
        'youtube_id': youtube_id,
        'es_admin': es_admin(request.user),  # para mostrar botones de edición si es admin
    })

# ---------- AUTENTICACIÓN ----------
def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            grupo_usuarios, _ = Group.objects.get_or_create(name='Usuarios')
            user.groups.add(grupo_usuarios)
            login(request, user)
            return redirect('lista_contenido')
    else:
        form = UserCreationForm()
    return render(request, 'catalogos/registro.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('lista_contenido')
    else:
        form = AuthenticationForm()
    return render(request, 'catalogos/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
    return redirect('lista_contenido')
