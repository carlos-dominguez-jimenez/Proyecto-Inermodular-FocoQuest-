from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone



# 1. PerfilUsuario

class PerfilUsuario(models.Model):
    OBJETIVOS = [
        ('Opositor', 'Opositor'),
        ('Universitario', 'Universitario'),
        ('Bachillerato/FP', 'Bachillerato/FP'),
    ]
    objetivo = models.CharField(max_length=20, choices=OBJETIVOS, default='Universitario')
    nivel = models.IntegerField(default=1)
    xp = models.IntegerField(default=0, help_text="Puntos de experiencia acumulados")
    racha_actual = models.IntegerField(default=0)
    racha_maxima = models.IntegerField(default=0)
    ultimo_dia_activo = models.DateField(null=True, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    biografia = models.TextField(blank=True)
    hora_recordatorio = models.TimeField(null=True, blank=True)
    notificaciones_push = models.BooleanField(default=False)
    acepta_tratamiento_salud = models.BooleanField(default=False)
    actualizado = models.DateTimeField(auto_now=True)

    # OneToOne: cada perfil pertenece a un único User y cada User tiene un único perfil
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    
    # ManyToMany con tabla intermedia (ObtencionLogro, con atributos extra)
    
    logros = models.ManyToManyField('Logro', through='ObtencionLogro', related_name='perfiles')
    
    # ManyToMany: un perfil puede tener varios psicólogos favoritos y un psicólogo ser favorito de varios perfiles
    
    psicologos_favoritos = models.ManyToManyField('Psicologo', blank=True, related_name='seguidores')

    def __str__(self):
        return f"Perfil de {self.user.username}"


# 2. Mascota

class Mascota(models.Model):
    ETAPAS = [
        ('Huevo', 'Huevo'),
        ('Larva', 'Larva'),
        ('Adulta', 'Adulta'),
        ('Resplandeciente', 'Resplandeciente'),
    ]
    etapa = models.CharField(max_length=20, choices=ETAPAS, default='Huevo')
    energia = models.IntegerField(default=100)
    color = models.CharField(max_length=7, default='#FFB547')
    fecha_adopcion = models.DateField(auto_now_add=True)
    activa = models.BooleanField(default=True)

    # OneToOne: cada perfil tiene una única mascota
    
    perfil = models.OneToOneField(PerfilUsuario, on_delete=models.CASCADE, related_name='mascota')

    def __str__(self):
        return f"Mascota ({self.etapa})"


# 3. Asignatura

class Asignatura(models.Model):
    nombre = models.CharField(max_length=80)
    descripcion = models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#3DBE9B')
    fecha_examen = models.DateField(null=True, blank=True)
    horas_objetivo = models.DecimalField(max_digits=6, decimal_places=1, default=0)
    activa = models.BooleanField(default=True)

    # ManyToOne: un perfil tiene muchas asignaturas
    
    perfil = models.ForeignKey(PerfilUsuario, on_delete=models.CASCADE, related_name='asignaturas')

    def __str__(self):
        return self.nombre


# 4. SesionEstudio (se abre con "Comenzar día" y se cierra con "Finalizar día")

class SesionEstudio(models.Model):
    inicio = models.DateTimeField(default=timezone.now)
    fin = models.DateTimeField(null=True, blank=True)
    minutos_estudiados = models.IntegerField(default=0)
    pomodoros_completados = models.IntegerField(default=0)
    xp_ganada = models.IntegerField(default=0)
    notas = models.TextField(blank=True)

    # ManyToOne: una asignatura tiene muchas sesiones de estudio
    
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE, related_name='sesiones')

    def __str__(self):
        return f"{self.asignatura} - {self.inicio:%d/%m/%Y}"


# 5. RegistroAnimo (cuestionario que salta al pulsar "Finalizar día")

class RegistroAnimo(models.Model):
    ESTADOS = [
        ('Tranquilo', 'Tranquilo'),
        ('Motivado', 'Motivado'),
        ('Agobiado', 'Agobiado'),
        ('Exhausto', 'Exhausto'),
    ]
    estado = models.CharField(max_length=20, choices=ESTADOS)
    nivel_estres = models.IntegerField(default=5, help_text="De 1 a 10")
    horas_sueno = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    comentario = models.TextField(blank=True)
    creado = models.DateTimeField(auto_now_add=True)

    # OneToOne: cada sesión tiene un único registro de ánimo
    
    sesion = models.OneToOneField(SesionEstudio, on_delete=models.CASCADE, related_name='registro_animo')

    def __str__(self):
        return self.estado


# 6. Tarjeta (flashcards con repetición espaciada)

class Tarjeta(models.Model):
    anverso = models.TextField(help_text="Pregunta o concepto")
    reverso = models.TextField(help_text="Respuesta o definición")
    caja = models.IntegerField(default=1)
    facilidad = models.FloatField(default=2.5)
    intervalo_dias = models.IntegerField(default=1)
    proximo_repaso = models.DateField(default=timezone.localdate)
    creada = models.DateTimeField(auto_now_add=True)

    # ManyToOne: una asignatura tiene muchas tarjetas
    
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE, related_name='tarjetas')

    def __str__(self):
        return self.anverso[:40]


# 7. Especialidad

class Especialidad(models.Model):
    nombre = models.CharField(max_length=60, unique=True)
    descripcion = models.TextField(blank=True)
    orden = models.IntegerField(default=0)
    activa = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


# 8. Psicologo (directorio de especialistas)

class Psicologo(models.Model):
    MODALIDADES = [
        ('Online', 'Online'),
        ('Presencial', 'Presencial'),
        ('Ambas', 'Ambas'),
    ]
    nombre_completo = models.CharField(max_length=120)
    numero_colegiado = models.CharField("nº de colegiado", max_length=20, unique=True)
    descripcion = models.TextField()
    email = models.EmailField(max_length=254, unique=True)
    telefono = models.CharField(max_length=16, blank=True)
    web = models.URLField(blank=True)
    modalidad = models.CharField(max_length=15, choices=MODALIDADES, default='Online')
    precio_sesion = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    fecha_alta = models.DateField(auto_now_add=True)

    # OneToOne: la cuenta de User con la que el psicólogo edita su ficha (opcional)
    
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='ficha_psicologo')
    
    # ManyToMany: un psicólogo tiene varias especialidades y una especialidad la tienen varios psicólogos
    
    especialidades = models.ManyToManyField(Especialidad, related_name='psicologos')

    def __str__(self):
        return self.nombre_completo


# 9. Logro

class Logro(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=80)
    descripcion = models.TextField()
    xp_recompensa = models.IntegerField(default=50)
    icono_url = models.URLField(blank=True)

    def __str__(self):
        return self.nombre


# 10. ObtencionLogro (tabla intermedia PerfilUsuario y Logro, con atributos extra)

class ObtencionLogro(models.Model):
    fecha_obtencion = models.DateTimeField(auto_now_add=True)
    progreso = models.IntegerField(default=0, help_text="Porcentaje de 0 a 100")
    destacado = models.BooleanField(default=False)
    notificado = models.BooleanField(default=False)

    # ManyToOne: un perfil puede obtener muchos logros
    
    perfil = models.ForeignKey(PerfilUsuario, on_delete=models.CASCADE, related_name='obtenciones')
    
    # ManyToOne: un logro puede ser obtenido por muchos perfiles
    
    logro = models.ForeignKey(Logro, on_delete=models.CASCADE, related_name='obtenciones')

    def __str__(self):
        return f"{self.perfil} - {self.logro}"