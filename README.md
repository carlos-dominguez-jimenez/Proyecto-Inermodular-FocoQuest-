# Proyecto-Intermodular-FocoQuest-
Glosario de Parámetros Django

    max_length: Límite de caracteres.

    choices: Opciones predefinidas en una lista.

    default: Valor inicial por defecto.

    null=True / blank=True: Permite campos vacíos en BBDD y formularios, respectivamente.

    auto_now_add / auto_now: Guarda la fecha de creación / modificación automáticamente.

    on_delete=models.CASCADE / SET_NULL: Si se borra el padre, borra los hijos (CASCADE) o deja el campo vacío (SET_NULL).

    related_name: Nombre para buscar relaciones en sentido inverso.

    unique=True: Evita valores duplicados en la base de datos.

    max_digits / decimal_places: Total de dígitos y cuántos son decimales.

Modelos y Atributos

1. PerfilUsuario: Datos extra del estudiante y gamificación.

    Atributos: objetivo (tipo de estudiante), nivel y xp (progreso), racha_actual/maxima (constancia), ultimo_dia_activo, fecha_nacimiento, biografia, hora_recordatorio, notificaciones_push, acepta_tratamiento_salud, actualizado.

    Relaciones: user (User 1:1), psicologos(N:M).

2. Mascota: Avatar virtual asociado al usuario.

    Atributos: etapa (evolución), energia (salud), color, fecha_adopcion, activa.

    Relaciones: perfil (1:1).

3. Asignatura: Materias a estudiar.

    Atributos: nombre, descripcion, color, fecha_examen, horas_objetivo, activa.

    Relaciones: perfil (N:1, pertenece a un usuario).

4. SesionEstudio: Bloques de tiempo dedicados.

    Atributos: inicio, fin, minutos_estudiados, pomodoros_completados, xp_ganada, notas.

    Relaciones: asignatura (N:1).

5. RegistroAnimo: Cuestionario de salud mental post-estudio.

    Atributos: estado (emoción), nivel_estres (1-10), horas_sueno, comentario, creado.

    Relaciones: SesionEstudio (1:1, un registro por sesión).

6. Tarjeta: Flashcards para repetición espaciada.

    Atributos: anverso (pregunta), reverso (respuesta), caja, facilidad, intervalo_dias, proximo_repaso (algoritmo de repaso), creada.

    Relaciones: asignatura (N:1).

7. Especialidad: Ramas clínicas (ansiedad, TDAH...).

    Atributos: nombre, descripcion, orden (para UI), activa.

8. Psicologo: Directorio de profesionales.

    Atributos: nombre_completo, numero_colegiado, descripcion, email, telefono, web, modalidad (online/presencial), precio_sesion, fecha_alta.

    Relaciones: user (1:1, cuenta opcional de gestión), especialidades (N:M).

9. Logro: Catálogo de medallas o metas.

    Atributos: codigo (interno), nombre, descripcion, xp_recompensa, icono_url.

10. ObtencionLogro: Progreso de un usuario hacia un logro (Tabla intermedia).

    Atributos: fecha_obtencion, progreso (0-100%), destacado, notificado.

    Relaciones: perfil (N:1), logro (N:1).



