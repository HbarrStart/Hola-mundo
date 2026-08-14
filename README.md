# MOS — Monitoreo Operativo Solidario

Prototipo de respuesta informativa para emergencias en Colombia.

## Principio
MOS no compite con organismos de socorro ni reemplaza fuentes oficiales. Su función es **agregar, verificar, fechar y traducir** información pública a formatos útiles para ciudadanía y voluntariado.

## Fuentes prioritarias
1. Servicio Geológico Colombiano (SGC)
2. UNGRD y autoridades territoriales
3. Cruz Roja Colombiana
4. Defensa Civil Colombiana
5. IDEAM
6. Otras fuentes institucionales o comunitarias, siempre etiquetadas y corroboradas

No se utilizarán medios comerciales como fuente primaria de hechos críticos. Pueden servir para detectar señales que luego deben verificarse en una fuente primaria.

## Estados editoriales
- CONFIRMADO: evidencia suficiente y fuente trazable.
- EN VERIFICACIÓN: señal recibida, todavía no publicable como hecho.
- DESCARTADO: información falsa, antigua, fuera de contexto o contradicha.

## Seguridad
No almacenar ni publicar cédulas, direcciones exactas, teléfonos personales, datos médicos privados o ubicación sensible de menores. Las solicitudes de ayuda deben minimizar exposición de personas vulnerables.

## Roadmap inmediato
- [x] Landing mínima
- [x] Registro de fuentes
- [x] Enlaces directos a fuentes primarias
- [x] Protocolo editorial visible
- [ ] Ingesta automática de fuentes oficiales
- [ ] Historial de cambios y sello de hora
- [ ] Base de datos de reportes territoriales
- [ ] Mapa de afectación
- [ ] Cola de verificación humana
- [ ] API pública de datos verificados
- [ ] Alertas por canales disponibles
- [ ] PWA offline

## Regla crítica
**Automatizar la recolección; no automatizar ciegamente la publicación.** Todo dato que pueda cambiar decisiones de vida o seguridad debe pasar por una regla de validación y, para los casos críticos, revisión humana.
