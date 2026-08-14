# MOS — Protocolo operativo de emergencia

## Regla 0: seguridad informativa
MOS no publica automáticamente una afirmación crítica solo porque una fuente haya sido encontrada por software o IA.

**FAIL CLOSED:** si una condición crítica no puede comprobarse, el sistema retiene la afirmación.

## Fuentes
MOS puede utilizar fuentes oficiales, territoriales, humanitarias, medios independientes, medios comunitarios, investigadores, funcionarios electos, reportes ciudadanos y señales de redes sociales.

La categoría de una fuente nunca convierte automáticamente sus afirmaciones en hechos. Cada afirmación conserva su evidencia, hora, ubicación y cadena de corroboración.

Las fuentes primarias tienen competencia directa sobre determinados hechos técnicos; las fuentes secundarias e independientes pueden aportar corroboración, contexto o descubrimientos. Una fuente independiente no se descarta por no ser institucional.

## Estados de afirmaciones

- `CONFIRMED_EVENT`: existencia de un evento establecida por una fuente primaria competente o por múltiples fuentes independientes trazables con evidencia suficiente.
- `CONFIRMED_FACT`: hecho específico respaldado por evidencia y por el estándar de verificación correspondiente.
- `CORROBORATED_FACT`: dos o más fuentes independientes coinciden, pero el estándar de confirmación primaria o específico aún no se ha alcanzado.
- `PENDING_VERIFICATION`: señal o afirmación que necesita comprobación adicional.
- `CONFLICTING_REPORTS`: fuentes trazables presentan datos incompatibles; no se consolida una conclusión.
- `REJECTED`: contradicho o desmentido mediante evidencia suficiente.
- `EXPIRED`: información temporal que ya no debe utilizarse para decisiones actuales.

**La confirmación no se propaga:** confirmar que ocurrió un desastre no confirma automáticamente víctimas, daños, vías, refugios, necesidades ni instrucciones operativas.

## Regla de cifras
Toda cifra de víctimas, desaparecidos, heridos, viviendas, rescates o suministros debe conservar:

- fuente exacta;
- enlace al material original;
- fecha/hora del corte de la fuente;
- fecha/hora de nuestra verificación;
- contexto sobre si es preliminar o consolidada;
- alcance geográfico.

Nunca mezclar cifras de cortes distintos para producir un total propio.

## Información operacional
Una afirmación que pueda inducir una acción física —por ejemplo, apertura de una vía, seguridad estructural, ruta de acceso, evacuación o instrucciones de rescate— requiere revisión humana explícita, incluso si existen fuentes corroborantes.

MOS informa; no sustituye a los organismos oficiales de emergencia ni imparte órdenes de rescate.

## Reportes ciudadanos
Un reporte ciudadano se almacena como señal con su evidencia original. No se convierte en una afirmación confirmada por sí solo.

## Frescura
Los hechos temporales tienen TTL. Al vencer, pasan a `EXPIRED` y no se presentan como información vigente. La existencia de un evento histórico no expira por TTL.

## Correcciones
Cuando un dato cambia, no se borra silenciosamente. Se conserva el registro histórico y se muestra la corrección con hora, fuente y motivo.

## Separación editorial
La cobertura humanitaria y los análisis políticos/geopolíticos permanecen separados. Una crítica política no puede alterar el estado factual de una alerta humanitaria.

## Objetivo
Reducir el daño causado por desinformación y convertir información verificable en información útil para rescate, atención, movilidad, alojamiento, agua, alimentos, salud y ayuda humanitaria.
