# Integrantes

Juan Pablo Ante - 2140132
Nicolás Garcés Larrahondo - 2180066
Natalia Andrea Marín - 2041622
Juan Camilo Valencia - 2259459


# Proyecto ADA II

A continuación, se explica cómo instalar las dependencias necesarias y configurar el entorno para ejecutar el proyecto correctamente.

## Requisitos

- Python 3.x
- MiniZinc (normalmente se instala en `C:\Program Files\MiniZinc`)

## Instalación

1. Clona el repositorio en tu máquina local.

    ```bash
    git clone https://github.com/tu_usuario/tu_repositorio.git
    ```

2. Navega a la carpeta del proyecto:

    ```bash
    cd tu_repositorio
    ```

3. Crea un entorno virtual y actívalo:

    ```bash
    python -m venv venv
    .\venv\Scripts\Activate
    ```

4. Instala las dependencias del proyecto:

    ```bash
    pip install -r requirements.txt
    ```

## Configuración de la Variable de Entorno en Windows

Para que MiniZinc funcione correctamente desde cualquier ubicación en la línea de comandos, debes configurar la variable de entorno `Path` de Windows para que incluya la ruta de instalación de MiniZinc.

1. Abre el Panel de Control de Windows y ve a **Sistema** > **Configuración avanzada del sistema**.
2. En la ventana de Propiedades del sistema, haz clic en el botón **Variables de entorno...**.
3. En la sección **Variables del sistema**, busca la variable `Path` y selecciona **Editar**.
4. Agrega la siguiente ruta a la lista de valores (asegúrate de ajustar la ruta si instalaste MiniZinc en otro lugar):

    ```
    C:\Program Files\MiniZinc
    ```

5. Guarda los cambios y cierra las ventanas.

Ahora, puedes ejecutar comandos de MiniZinc desde cualquier ubicación en la línea de comandos de Windows.

## Ejecución

Para ejecutar el proyecto, asegúrate de tener el entorno activado y ejecuta el script principal:

```bash
python main.py
