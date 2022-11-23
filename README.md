# API

## Models

### Estudiantes

- id_estudiante (int PK)
- nombre (string)
- apellidos (string)
- n_control (string)
- rfid
- carrera (string)
- campus (string)
- ultimo_log (datetime)
- telefono (string)
- curp (string)
- t_sangre (string)
- alergias (string)
- remark (string)
- foto (blob)

### Logs

- id_log (int PK)
- id_estudiante (int FK)
- tipo (string)
- fecha (date)
- hora (time)
- fecha_hora (datetime)
- dia_semana (string)
- remark (string)
