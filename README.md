# API Tokusatsu

Sistema web Back End desarrollado con Django y Django REST Framework para gestionar una base de datos de franquicias y series del género Tokusatsu (Kamen Rider, Super Sentai, etc.).

La aplicación expone endpoints para administrar la información de las series, manejar relaciones de spin-offs (relaciones recursivas), y protege la creación de registros mediante autenticación de Tokens JWT.

## Descripción del proyecto

API Tokusatsu es una solución RESTful orientada a facilitar la consulta y gestión del catálogo de producciones Tokusatsu. 
El sistema integra modelos relacionales en una base de datos SQLite y una API segura. Además, incorpora un script de automatización en Python capaz de consumir la API, autenticarse y poblar la base de datos de forma inteligente, evitando duplicidad de registros.

## Objetivo

Desarrollar una solución Back End utilizando Django que permita:
* Administrar Franquicias (Kamen Rider, Super Sentai, etc.).
* Administrar Series y sus atributos (plataforma, año, temática).
* Gestionar relaciones 1 a N (Franquicia -> Series) y relaciones recursivas (Serie base -> Spin-off).
* Exponer la información mediante una API REST en formato JSON.
* Proteger los endpoints de escritura utilizando seguridad mediante JSON Web Tokens (JWT).
* Desarrollar un script externo de automatización (`poblar_api.py`) para interactuar con la API.

## Tecnologías utilizadas

* Python
* Django
* Django REST Framework (DRF)
* djangorestframework-simplejwt (JWT)
* SQLite
* Requests (Librería Python para el script)
* Git y GitHub

## Funcionalidades principales

### Gestión de Franquicias
Permite almacenar las franquicias principales. Atributos:
* ID
* Nombre (ej. Kamen Rider)
* Productora (ej. Toei Company)
* Año de creación

### Gestión de Series
Permite administrar las series pertenecientes a cada franquicia. Atributos:
* ID
* Franquicia (Llave foránea)
* Título
* Plataforma de emisión (TV, WEB, PRIME, OTHER)
* Año de lanzamiento
* Cantidad de episodios
* Temática
* Estado de emisión (is_airing)
* Serie Base (Llave foránea recursiva a `self` para determinar si es un spin-off).

### Poblado Automatizado
Un script (`poblar_api.py`) que:
* Solicita un token JWT al servidor enviando credenciales de administrador.
* Navega la paginación de la API leyendo la llave `"results"`.
* Verifica mediante peticiones `GET` si el registro ya existe antes de inyectarlo mediante un `POST` para evitar redundancia de datos.

## API REST

El proyecto incorpora una API REST utilizando Django REST Framework.

### Endpoints disponibles

```text
/api/v1/franchises/
/api/v1/series/
/api/token/          (Para solicitar el JWT)
/api/token/refresh/  (Para renovar el JWT)
```

Los recursos utilizan ViewSets y están registrados mediante `DefaultRouter`.

### Operaciones HTTP

Los ViewSets permiten trabajar con operaciones HTTP estándar (GET, POST, PUT, PATCH, DELETE).
Durante la validación, la API devolvió correctamente los siguientes códigos de estado:

```text
GET     → 200 OK (Lectura de Franquicias y Series)
POST    → 200 OK (Generación de Token JWT exitosa)
POST    → 201 Created (Inyección de datos mediante script)
POST    → 400 Bad Request (Intento de duplicación de Franquicia mitigado)
POST    → 401 Unauthorized (Intento de acceso sin enviar el Bearer Token)
GET     → 404 Not Found (Rutas no existentes)
```

## Arquitectura del proyecto

La aplicación utiliza la arquitectura de Django y DRF.

### Models
Define las estructuras de datos y relaciones entre `Franchise` y `Series`.

### Views
Gestiona los ViewSets utilizados por la API REST para exponer los datos y resolver los verbos HTTP.

### Serializers
Transforman los modelos Django en representaciones JSON. Se agregaron campos `read_only` (ej. `franchise_name`) para enviar respuestas más legibles al cliente.

## Base de datos

El proyecto utiliza **SQLite** (por defecto en Django), el cual es idóneo para entornos de desarrollo y pruebas locales.
Durante el desarrollo se aplicaron migraciones iterativas para asegurar la consistencia del esquema (como la adición de la columna `platform` a la tabla de series).

## Validación y pruebas

El proyecto fue validado mediante pruebas locales y de consola.
Se utilizó:
```bash
python manage.py check
```
Resultado final:
```text
System check identified no issues (0 silenced).
```

### Prueba de integración del Script
Se comprobó el flujo completo mediante el script `poblar_api.py`:
1. Autenticación exitosa (Recepción del token).
2. Verificación GET (Detectar Franquicia existente).
3. Inyección POST (Crear nueva franquicia y series).
4. Relación recursiva (Creación de Spin-off apuntando a serie principal).

## Uso de Inteligencia Artificial (IA)

Durante el desarrollo del proyecto se utilizó Inteligencia Artificial como herramienta de asistencia, análisis forense de errores y documentación. 

La IA actuó como copiloto técnico y revisor de código, pero las decisiones de *lore* y validación técnica final fueron ejecutadas por el desarrollador.

### Acciones realizadas con apoyo de IA

* Analizar y descifrar reportes de error largos de la terminal (`Tracebacks`).
* Identificar y corregir errores tipográficos en variables críticas.
* Estructurar el script de poblado en Python para incluir manejo de Tokens y paginación.
* Solucionar problemas de desincronización entre el código y la base de datos (Migraciones).

### Auditoría, validación y evidencias del uso de IA

Las propuestas generadas por la IA no fueron copiadas a ciegas; fueron auditadas, contrastadas con los requerimientos y ejecutadas en un entorno de pruebas.

**Evidencias (Problemas solucionados mediante prompts compartidos con la IA):**

1. **Error de Tipografía en Serializers:**
   * *Problema:* El servidor caía con error 500. La IA analizó el Traceback y detectó un `AttributeError`.
   * *Solución:* Se corrigió el uso de `CharFild` por `CharField`, y `filds` por `fields` en `FranchiseSerializer` según la sintaxis correcta de DRF.
2. **Error de Paginación en Script Python:**
   * *Problema:* El prompt arrojaba `TypeError: string indices must be integers`.
   * *Diagnóstico IA:* La API devolvía un diccionario paginado (`count`, `next`, `results`), pero el script intentaba iterarlo como una lista.
   * *Solución Aplicada:* Refactorización del código para usar `data.get('results', data)` al procesar la respuesta JSON.
3. **Desincronización de Base de Datos:**
   * *Problema:* `sqlite3.OperationalError: table series_series has no column named platform`.
   * *Solución:* Mediante la guía de la IA, se detuvo el servidor y se ejecutaron los comandos `makemigrations` y `migrate` para crear la columna faltante en SQLite.
4. **Validación Crítica Humana sobre la IA:**
   * *Evidencia de uso responsable:* La IA sugirió clasificar el spin-off "Project Thouser" con la plataforma `"TTFC"`.
   * *Corrección humana:* Se contrastó la información con la Wiki oficial de Kamen Rider, detectando que era un lanzamiento exclusivo en Blu-Ray. El desarrollador intervino para modificar la propuesta de la IA y cambiar la plataforma a `"OTHER"` y ajustar la temática de la trama a "Creación de Thouser", demostrando dominio sobre el diseño de la API y rechazo de alucinaciones.

## Control de versiones

El proyecto utiliza Git para el control de versiones y GitHub como repositorio remoto.

Repositorio:
`[INGRESA_TU_LINK_DE_GITHUB_AQUI]`

## Instalación

### Clonar el repositorio
```bash
git clone [INGRESA_TU_LINK_DE_GITHUB_AQUI]
```

### Ingresar al proyecto
```bash
cd Eva_3
```

### Crear el entorno virtual e instalar dependencias
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Ejecutar las migraciones
```bash
python manage.py migrate
```

### Crear una cuenta de Superusuario
Para interactuar con la API y generar los tokens de seguridad JWT, debes crear una cuenta con privilegios de administrador. Ejecuta el siguiente comando y sigue las instrucciones para asignar tu usuario y contraseña:
```bash
python manage.py createsuperuser
```

### Ejecutar el servidor
```bash
python manage.py runserver
```

### 6. Poblar la base de datos (Script de pruebas)
Para demostrar el funcionamiento del sistema de seguridad y las relaciones de la base de datos, se incluye un script que consume la API automáticamente.

1. Abre el archivo **`poblar_api.py`** en tu editor de código.

2. Modifica las variables de la cabecera reemplazándolas con el usuario y la contraseña que creaste en el **Paso 4**:

   ```
   USERNAME = "tu_usuario_aqui"
   PASSWORD = "tu_contraseña_aqui"
   
   ```

3. Guarda el archivo. Abre una **segunda terminal** (manteniendo el servidor corriendo en la primera), activa tu entorno virtual y ejecuta:

   ```
   python poblar_api.py
   
   ```

El script te informará en consola la autenticación exitosa, la revisión de existencias y la creación de los recursos.

## Estado del proyecto

Proyecto completamente funcional y validado localmente.
Se verificó exitosamente:
* Funcionamiento de Django y DRF.
* Rutas y ViewSets.
* Validaciones JWT (Token access y refresh).
* Integridad de la base de datos (Llaves foráneas simples y recursivas).
* Script de consumo externo.