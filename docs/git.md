# Git — Convenciones de Commits

Usamos **Conventional Commits** para mantener los commits claros, consistentes y fáciles de entender.

---

## Formato

```text
<tipo>(<alcance>): <descripción>
```

**Ejemplo:**
```bash
git commit -m "feat(auth): agregar login de usuarios"
```

---

## Tipos de Commit

| Tipo | Uso |
| :--- | :--- |
| **feat** | Nueva funcionalidad |
| **fix** | Corrección de un error |
| **docs** | Cambios en documentación |
| **style** | Cambios de formato, sin modificar lógica |
| **refactor** | Refactorización del código |
| **test** | Agregar o modificar tests |
| **chore** | Tareas de mantenimiento |
| **perf** | Mejora de rendimiento |
| **build** | Cambios en compilación o dependencias |
| **ci** | Cambios en CI/CD |

---

## Ejemplos

```bash
git commit -m "feat(users): agregar registro de usuarios"
git commit -m "fix(auth): corregir validación de contraseña"
git commit -m "docs(readme): actualizar instrucciones de instalación"
git commit -m "refactor(api): simplificar manejo de errores"
git commit -m "test(users): agregar tests para registro"
git commit -m "chore(deps): actualizar Django"
git commit -m "style(views): formatear código"
git commit -m "ci(github): agregar workflow de tests"
```

---

## Breaking Changes

Si un cambio rompe la compatibilidad con versiones anteriores, se puede indicar con un signo de exclamación (`!`):

```bash
git commit -m "feat(api)!: cambiar estructura de respuesta"
```

También se puede explicar detalladamente en el cuerpo del commit:

```text
feat(api): cambiar estructura de respuesta

BREAKING CHANGE: el campo `user` ahora se devuelve como `data.user`.
```

---

## Flujo Recomendado

```bash
git status
git add .
git commit -m "feat(users): agregar modelo de usuario"
git push
```

---

## Regla Rápida

* **Nueva funcionalidad** → `feat`
* **Bug** → `fix`
* **Documentación** → `docs`
* **Refactor** → `refactor`
* **Tests** → `test`
* **Mantenimiento** → `chore`
* **CI/CD** → `ci`
* **Dependencias/build** → `build`
* **Rendimiento** → `perf`
* **Formato** → `style`