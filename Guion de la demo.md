# Guion de la demo: CI con GitHub Actions

Funciones de una mesa de servicio (prioridad y SLA), pruebas con pytest y un pipeline en GitHub Actions que bloquea el merge cuando una prueba falla.

Los tiempos de SLA del código (P1 = 4 h, P2 = 8 h, P3 = 24 h, P4 = 72 h) y la matriz de prioridad son valores de ejemplo para la demo.

## Archivos

| Archivo | Contenido |
|---|---|
| `sla.py` | `prioridad`, `cumple_sla`, `tiempo_restante_sla` |
| `test_sla.py` | 10 pruebas: happy path y casos borde por función |
| `ci.yml` | Workflow que corre `pytest -v` en cada Pull Request y push a main. Se mueve a `.github/workflows/` en el paso 5 |
| `requirements.txt` | pytest |
| `.gitignore` | Cachés de Python |

El archivo `ci.yml` viene en la raíz de la carpeta porque la ruta `.github` no se puede escribir desde la herramienta. Moverlo a `.github/workflows/` es parte de la demo (paso 5) y sirve para mostrar dónde busca GitHub los workflows.

## Antes de clase (2 minutos)

En la máquina de presentación, desde la terminal:

```bash
python3 --version              # Python 3.x
pip3 install pytest
git config --global user.name  # debe mostrar tu nombre
git config --global user.email # debe mostrar tu correo
gh auth status                 # o un git push de prueba, para que no pida credenciales en clase
```

Copiar la carpeta a una ubicación de trabajo fuera de ITSM (por ejemplo, el escritorio), para que el `git init` no quede dentro de la carpeta sincronizada.

## Paso 1. El código (editor)

Abrir la carpeta en VS Code. Mostrar `sla.py` y `test_sla.py` lado a lado.

- La matriz `MATRIZ` es la de impacto × urgencia vista en la sesión de incidentes.
- Una prueba es una función que llama a otra y compara el resultado con `assert`.
- Los nombres de las pruebas se leen como requisitos: `test_impacto_alto_urgencia_alta_es_P1`.

## Paso 2. Usar las funciones (terminal)

```bash
python3 -i sla.py
>>> prioridad(1, 1)
'P1'
>>> cumple_sla("P1", 180)
True
>>> tiempo_restante_sla("P2", 300)
180
>>> prioridad(5, 1)
ValueError: Impacto y urgencia deben ser 1, 2 o 3
>>> exit()
```

## Paso 3. Correr las pruebas (terminal)

```bash
pytest -v
```

Resultado esperado: `10 passed`, cada prueba en verde con su nombre.

## Paso 4. Romper una prueba a propósito (terminal)

En `sla.py`, cambiar la primera celda de la matriz:

```python
1: {1: "P2", 2: "P2", 3: "P3"},   # antes: {1: "P1", ...}
```

```bash
pytest -v
```

Resultado esperado: `1 failed, 9 passed`. Falla `test_impacto_alto_urgencia_alta_es_P1` con `AssertionError: assert 'P2' == 'P1'`.

Pregunta para la clase: ¿qué pasa en una mesa de servicio si un incidente crítico entra como P2?

Revertir el cambio (`Ctrl+Z`) y volver a correr `pytest -v` para dejarlo en verde.

## Paso 5. Subir el proyecto a GitHub

Ubicar el workflow donde GitHub lo busca:

```bash
mkdir -p .github/workflows
mv ci.yml .github/workflows/ci.yml
```

Mostrar `ci.yml` en el editor: `on` (cuándo corre), `jobs.pruebas` (qué corre) y los cuatro pasos.

Crear en GitHub un repositorio **público** vacío, sin README, llamado `demo-ci-sla`.

```bash
git init
git add .
git commit -m "Funciones de prioridad y SLA con pruebas"
git branch -M main
git remote add origin https://github.com/<usuario>/demo-ci-sla.git
git push -u origin main
```

En GitHub, pestaña **Actions**: el workflow `CI` corre por el push a main y termina en verde. Abrir el job `pruebas` y mostrar el paso "Ejecutar pruebas" con las 10 pruebas.

## Paso 6. Proteger la rama main (GitHub)

**Settings → Branches → Add classic branch protection rule**

- Branch name pattern: `main`
- Marcar **Require a pull request before merging** (desmarcar "Require approvals" para la demo)
- Marcar **Require status checks to pass before merging**
- En el buscador de checks, escribir y seleccionar `pruebas`
- **Create**

El check `pruebas` solo aparece en el buscador después de que el workflow corrió al menos una vez (paso 5). La interfaz de GitHub puede ofrecer "rulesets" en lugar de la regla clásica; la configuración equivalente es "Require status checks to pass" con el check `pruebas`.

## Paso 7. Un cambio que rompe el pipeline

```bash
git checkout -b cambio-matriz
```

Repetir el cambio del paso 4 (`{1: "P2", ...}`).

```bash
git commit -am "Ajuste a la matriz de prioridad"
git push -u origin cambio-matriz
```

En GitHub: **Compare & pull request → Create pull request**.

Resultado esperado: el check `CI / pruebas` en rojo y el botón de merge bloqueado ("Required statuses must pass before merging"). Abrir el detalle del check y mostrar la prueba que falló.

## Paso 8. Corregir y habilitar el merge

Revertir la celda a `"P1"`.

```bash
git commit -am "Corrige prioridad de impacto alto y urgencia alta"
git push
```

El mismo Pull Request vuelve a correr el check. Resultado esperado: verde y el botón **Merge pull request** habilitado. Hacer el merge.

## Cierre

La secuencia que se mostró es la misma que la P07 pide presentar el lunes 19 de octubre: prueba que falla, merge bloqueado, corrección, merge habilitado. La P07 usa otras funciones (opciones A, B o C), así que esta muestra no resuelve el laboratorio.

## Si algo falla en vivo

| Síntoma | Causa probable |
|---|---|
| `pytest: command not found` | Usar `python3 -m pytest -v` |
| `ModuleNotFoundError: sla` | La terminal no está en la carpeta del proyecto |
| `git push` pide usuario y contraseña | Falta autenticación; usar `gh auth login` |
| No aparece la pestaña Actions o no corre | El archivo no está en `.github/workflows/` o el repositorio no tiene el push a main |
| El check `pruebas` no aparece al proteger la rama | El workflow todavía no ha corrido una vez |
| El merge no se bloquea | La regla no tiene marcado "Require status checks" o el repositorio es privado en una cuenta gratuita |
