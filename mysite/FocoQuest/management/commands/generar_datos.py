import random
from datetime import timedelta
from decimal import Decimal
from itertools import product
 
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
 
from FocoQuest.models import (
    Especialidad, Logro, PerfilUsuario, Psicologo, Mascota,
    Asignatura, SesionEstudio, RegistroAnimo, Tarjeta, ObtencionLogro,
)
 
 
class Command(BaseCommand):
    help = 'Generando datos usando Faker'
 
    def handle(self, *args, **kwargs):
        fake = Faker('es_ES')
        tz = timezone.get_current_timezone()
 
        # 1. Especialidades
        especialidades = []
        for _ in range(10):
            especialidades.append(Especialidad.objects.create(
                nombre=fake.unique.word().capitalize(),
                descripcion=fake.text(max_nb_chars=120),
                orden=fake.random_int(0, 10),
                activa=fake.boolean(),
            ))
 
        # 2. Logros
        logros = []
        for _ in range(10):
            logros.append(Logro.objects.create(
                codigo=f"LOGRO_{fake.unique.random_int(1000, 9999)}",
                nombre=fake.sentence(nb_words=3).rstrip('.'),
                descripcion=fake.text(max_nb_chars=120),
                xp_recompensa=fake.random_int(10, 500),
                icono_url=fake.image_url(),
            ))
 
        # 3. Usuarios + perfiles (OneToOne con User)
        perfiles = []
        for _ in range(10):
            user = User.objects.create_user(
                username=fake.unique.user_name(),
                email=fake.email(),
                password='1234',
            )
            racha_actual = fake.random_int(0, 30)
            perfiles.append(PerfilUsuario.objects.create(
                user=user,
                objetivo=fake.random_element([o[0] for o in PerfilUsuario.OBJETIVOS]),
                nivel=fake.random_int(1, 20),
                xp=fake.random_int(0, 5000),
                racha_actual=racha_actual,
                racha_maxima=racha_actual + fake.random_int(0, 20),
                ultimo_dia_activo=fake.date_between(start_date='-30d', end_date='today'),
                fecha_nacimiento=fake.date_of_birth(minimum_age=16, maximum_age=40),
                biografia=fake.text(max_nb_chars=150),
                hora_recordatorio=fake.time_object(),
                notificaciones_push=fake.boolean(),
                acepta_tratamiento_salud=fake.boolean(),
            ))
 
        # 4. Psicólogos (ManyToMany con Especialidad)
        psicologos = []
        for _ in range(10):
            psicologo = Psicologo.objects.create(
                nombre_completo=fake.name(),
                numero_colegiado=f"M-{fake.unique.random_int(10000, 99999)}",
                descripcion=fake.text(max_nb_chars=200),
                email=fake.unique.email(),
                telefono=fake.phone_number()[:16],
                web=fake.url(),
                modalidad=fake.random_element([m[0] for m in Psicologo.MODALIDADES]),
                precio_sesion=Decimal(f"{random.uniform(30, 90):.2f}"),
            )
            psicologo.especialidades.set(
                random.sample(especialidades, k=random.randint(1, 3))
            )
            psicologos.append(psicologo)
 
        # 5. Psicólogos favoritos de cada perfil (ManyToMany)
        for perfil in perfiles:
            perfil.psicologos_favoritos.set(
                random.sample(psicologos, k=random.randint(0, 3))
            )
 
        # 6. Mascotas (una por perfil)
        for perfil in perfiles:
            Mascota.objects.create(
                perfil=perfil,
                etapa=fake.random_element([e[0] for e in Mascota.ETAPAS]),
                energia=fake.random_int(0, 100),
                color=fake.hex_color(),
                activa=fake.boolean(),
            )
 
        # 7. Asignaturas
        asignaturas = []
        for _ in range(10):
            asignaturas.append(Asignatura.objects.create(
                perfil=random.choice(perfiles),
                nombre=fake.word().capitalize(),
                descripcion=fake.text(max_nb_chars=100),
                color=fake.hex_color(),
                fecha_examen=fake.date_between(start_date='today', end_date='+90d'),
                horas_objetivo=Decimal(f"{random.uniform(10, 200):.1f}"),
                activa=fake.boolean(),
            ))
 
        # 8. Sesiones de estudio
        sesiones = []
        for _ in range(10):
            inicio = fake.date_time_between(start_date='-30d', end_date='now', tzinfo=tz)
            minutos = fake.random_int(20, 240)
            sesiones.append(SesionEstudio.objects.create(
                asignatura=random.choice(asignaturas),
                inicio=inicio,
                fin=inicio + timedelta(minutes=minutos),
                minutos_estudiados=minutos,
                pomodoros_completados=minutos // 25,
                xp_ganada=minutos * 2,
                notas=fake.sentence(),
            ))
 
        # 9. Registros de ánimo (uno por sesión)
        for sesion in sesiones:
            RegistroAnimo.objects.create(
                sesion=sesion,
                estado=fake.random_element([e[0] for e in RegistroAnimo.ESTADOS]),
                nivel_estres=fake.random_int(1, 10),
                horas_sueno=Decimal(f"{random.uniform(4, 9):.1f}"),
                comentario=fake.sentence(),
            )
 
        # 10. Tarjetas
        for _ in range(10):
            Tarjeta.objects.create(
                asignatura=random.choice(asignaturas),
                anverso=fake.sentence().rstrip('.') + '?',
                reverso=fake.text(max_nb_chars=100),
                caja=fake.random_int(1, 5),
                facilidad=round(random.uniform(1.3, 3.0), 2),
                intervalo_dias=fake.random_int(1, 30),
                proximo_repaso=fake.date_between(start_date='today', end_date='+30d'),
            )
 
        # 11. Logros obtenidos (parejas perfil-logro sin repetir)
        for perfil, logro in random.sample(list(product(perfiles, logros)), 10):
            ObtencionLogro.objects.create(
                perfil=perfil,
                logro=logro,
                progreso=fake.random_int(0, 100),
                destacado=fake.boolean(),
                notificado=fake.boolean(),
            )
 
        self.stdout.write(self.style.SUCCESS('Datos generados correctamente'))
