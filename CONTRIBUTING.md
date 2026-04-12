# 🤝 Guía de Contribución

¡Gracias por tu interés en contribuir a GPTSeguros! Este documento describe cómo puedes ayudar al proyecto.

## Código de Conducta

- Sé respetuoso con otros contribuyentes
- Reporta bugs de seguridad en privado (ver SECURITY.md)
- Proporciona feedback constructivo
- Acepta crítica constructiva

## Tipos de Contribución

### 🐛 Reportar Bugs

1. **Verifica si ya existe un issue**: Busca en Issues
2. **Proporciona información útil:**
   - Versión de Python
   - Sistema operativo
   - Steps para reproducir
   - Comportamiento esperado vs actual
   - Logs de error

**Template:**
```markdown
## Descripción del Bug
Breve descripción del problema

## Cómo reproducir
1. Paso 1
2. Paso 2
3. ...

## Comportamiento esperado
Qué debería pasar

## Comportamiento actual
Qué está pasando

## Ambiente
- Python: 3.9
- OS: Windows 11
- Navegador: Chrome 120

## Logs
(Incluir outputs/errores)
```

### 💡 Sugerir Mejoras

Abrir un issue con etiqueta `enhancement`:
- Descripción clara de la idea
- Caso de uso
- Beneficios
- Posibles alternativas

### 📚 Mejorar Documentación

- Corregir errores en README/SETUP/SECURITY
- Agregar ejemplos
- Mejorar claridad
- Traducir a otros idiomas

### 🔧 Desarrollar Características

Ver sección **Workflow de Desarrollo** abajo.

## Workflow de Desarrollo

### 1. Fork y Clonar

```bash
# Fork en GitHub (botón arriba a la derecha)
git clone https://github.com/TU_USUARIO/GPTSeguros.git
cd GPTSeguros
git remote add upstream https://github.com/OWNER/GPTSeguros.git
```

### 2. Crear Rama de Trabajo

```bash
# Actualizar main
git fetch upstream
git rebase upstream/main

# Crear rama descriptiva
git checkout -b fix/bci-login-timeout
# o
git checkout -b feature/add-excel-export
```

Nombrar ramas:
- `fix/` - para correcciones
- `feature/` - para nuevas características  
- `docs/` - para documentación
- `refactor/` - para reorganización de código
- `test/` - para tests

### 3. Hacer Cambios

```bash
# Editar archivos
# ...

# Verificar cambios
git status
git diff

# Agregar cambios
git add archivo_editado.py
git add otra_funcion.py

# NO hacer git add .
# Revisar explícitamente qué estás comiteando
```

### 4. Commit con Mensajes Claros

```bash
git commit -m "Fix: Corregir timeout en login BCI

- Aumentar tiempo de espera a 15 segundos
- Agregar retry logic con exponential backoff
- Registrar logs detallados para debugging

Fixes #123"
```

**Formato de commit:**
```
<tipo>: <descripción corta (máx 50 caracteres)>

<descripción detallada si es necesario>
<puede ser multi-línea>

<referencias a issues: Fixes #123, Related #456>
```

Tipos válidos:
- `feat:` - Nueva característica
- `fix:` - Corrección de bug
- `docs:` - Cambios en documentación
- `style:` - Formato, sin cambiar lógica
- `refactor:` - Reorganización de código
- `perf:` - Mejoras de performance
- `test:` - Agregar/modificar tests
- `chore:` - Tareas de mantenimiento

### 5. Push y Pull Request

```bash
# Push a tu fork
git push origin fix/bci-login-timeout

# Crear PR en GitHub
# (Verás un botón sugiriendo crear PR)
```

**Template de PR:**

```markdown
## Descripción
Qué cambios se hacen y por qué

## Tipo de Cambio
- [ ] Bug fix
- [ ] Nueva característica
- [ ] Breaking change
- [x] Cambio en documentación

## Relacionado a Issues
Fixes #123

## Cómo Probar
1. Paso 1
2. Paso 2
3. Verificar resultado

## Checklist de PR
- [ ] Seguí la guía de estilo
- [ ] Actalizé la documentación
- [ ] No hay credenciales en el código
- [ ] Tests están pasando
- [ ] Sin warnings/errors

## Screenshots (si aplica)
[Opcional: Imágenes del cambio]
```

## Estándares de Código

### Python Style Guide (PEP 8)

```python
# ✅ BIEN
def cotizar_bci(usuario, contrasena):
    """Obtiene cotización de BCI Seguros."""
    if not usuario:
        raise ValueError("Usuario no puede ser vacío")
    
    driver = configure_webdriver()
    try:
        login(driver, usuario, contrasena)
        cotizacion = get_quote(driver)
        return cotizacion
    finally:
        driver.quit()

# ❌ MAL
def cotizar(u,c):
    d=webdriver.Chrome()
    d.get(URL)
    # ... código sin estructura
```

### Docstrings

```python
def process_vehicle_data(vehicle_info: dict) -> dict:
    """
    Procesa información del vehículo.
    
    Args:
        vehicle_info: Diccionario con datos del vehículo
            - patente (str): Placa del vehículo
            - marca (str): Marca del vehículo
            - modelo (str): Modelo específico
            
    Returns:
        dict: Datos procesados
        
    Raises:
        ValueError: Si falta información requerida
        
    Example:
        >>> result = process_vehicle_data({
        ...     'patente': 'FBGH14',
        ...     'marca': 'Mazda'
        ... })
    """
    # Implementación
```

### Type Hints

```python
from typing import Dict, List, Optional

def save_quotes(quotes: List[Dict[str, str]]) -> Optional[str]:
    """Guarda cotizaciones en archivo."""
    if not quotes:
        return None
    
    return write_to_file(quotes)
```

## Testing

### Escribir Tests

```python
# tests/test_bci.py
import unittest
from selenium_gpt.bci import bci_cotizador

class TestBCICotizador(unittest.TestCase):
    
    def setUp(self):
        """Configuración antes de cada test."""
        self.test_data = {
            'patente': 'FBGH14',
            'marca': 'Mazda'
        }
    
    def test_successful_login(self):
        """Verifica que el login sea exitoso."""
        # Arrange
        # Act
        result = login_bci('usuario', 'password')
        # Assert
        self.assertTrue(result)
    
    def test_invalid_credentials(self):
        """Verifica manejo de credenciales inválidas."""
        with self.assertRaises(AuthenticationError):
            login_bci('', '')

if __name__ == '__main__':
    unittest.main()
```

### Correr Tests

```bash
# Todos los tests
python -m pytest

# Solo un archivo
python -m pytest tests/test_bci.py

# Con coverage
pip install pytest-cov
pytest --cov=selenium_gpt
```

## Revisar tu Código

Antes de hacer PR:

```bash
# 1. Linting
pip install pylint
pylint selenium_gpt/

# 2. Formatting
pip install black
black selenium_gpt/

# 3. Type checking (opcional)
pip install mypy
mypy selenium_gpt/

# 4. Tests
pytest tests/

# 5. Ver cambios finales
git diff upstream/main
```

## Guía de Revisión de Código

Como revisor, busca:

- ✅ El código sigue PEP 8
- ✅ Hay tests unitarios
- ✅ La documentación está actualizada
- ✅ No hay credenciales hardcodeadas
- ✅ El commit message es claro
- ✅ Sin dependencias innecesarias
- ✅ Performance razonable

Si hay cambios requeridos:
```markdown
## Cambios solicitados

1. **Docstring incompleto**: Agregar descripción de parámetros en `cotizar()`

2. **Test faltante**: Faltan tests para el caso error en `login()`

3. **Security issue**: No usar `os.system()`, mejor usar `subprocess`
```

## Contacto y Preguntas

- **Preguntas sobre el proyecto**: Abrir Discussion
- **Bugs de seguridad**: Email privado (NO abrir issue público)
- **Ayuda con PR**: Comentarios en el PR

## Licencia

Al contribuir, aceptas que tu código sea licenciado bajo la misma licencia del proyecto.

## Agradecimientos

Todos los contribuyentes serán reconocidos en el archivo CONTRIBUTORS.md

---

**¡Gracias por contribuir a GPTSeguros! 🙌**

Última actualización: Abril 2026
