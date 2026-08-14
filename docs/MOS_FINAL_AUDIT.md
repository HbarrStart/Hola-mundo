# MOS — auditoría de depuración antes del montaje Alpha

Fecha: 2026-08-14
Rama: `mos-v0-emergencia`

## Correcciones obligatorias aplicadas

### 1. Identidad de eventos
El motor anterior podía devolver `SAME_EVENT_CANDIDATE` cuando solo dos de tres señales estaban disponibles. Eso era demasiado permisivo para un sistema de emergencia. Ahora la candidatura sísmica requiere que estén disponibles y sean compatibles las tres señales: tiempo, ubicación y magnitud. Una candidatura sigue sin ser confirmación.

### 2. Confirmación separada de identidad
`SAME_EVENT` se reserva al mismo identificador de evento dentro de la misma fuente. La correlación entre fuentes independientes nunca se convierte aquí en confirmación.

### 3. Estado temporal
La situación debe distinguir entre el tiempo del hecho (`observed_at`), el tiempo de recepción (`received_at`) y el tiempo de verificación/publicación. No se debe usar la hora de ingesta como si fuera la hora del evento.

### 4. Historial inmutable
Las actualizaciones no deben sobrescribir afirmaciones anteriores. Una nueva versión debe referenciar a la anterior y marcarla como `superseded`, `corrected` o `retracted` cuando corresponda.

### 5. Información desconocida
`unknowns` es parte del modelo de situación. Nunca se infiere que un elemento no mencionado sea inexistente.

### 6. Fuentes independientes
Medios independientes, periodistas, investigadores, autoridades electas y reportes ciudadanos pueden aportar evidencia. Ninguna categoría recibe una confianza automática; la evaluación depende de procedencia, evidencia, corroboración y contexto temporal.

## Elementos que NO se automatizan en Alpha

- confirmación de víctimas;
- instrucciones de evacuación;
- rutas seguras;
- seguridad estructural;
- diagnóstico médico;
- clasificación automática de un evento como réplica confirmada;
- resolución automática de cifras contradictorias.

## Criterio de salida

Si existe ambigüedad relevante, datos contradictorios, fuente ausente o evidencia insuficiente: `HOLD`.

El montaje Alpha solo puede consumir observaciones que conserven trazabilidad hasta su fuente original.
