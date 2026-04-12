# 🔐 Guía de Seguridad - GPTSeguros

## Resumen Ejecutivo

Este documento describe las prácticas de seguridad implementadas en GPTSeguros y cómo mantener el proyecto seguro.

## Credenciales y Datos Sensibles

### ❌ Lo que NO Debe Cometerse

**Nunca** incluir en el repositorio:

- Archivos `.env` con credenciales reales
- Archivos `credentials.json`
- Claves privadas SSL/TLS (`.pem`, `.key`)
- API Keys o tokens
- Contraseñas en código
- Patches de corrector automático con datos reales
- RUTs o datos personales de clientes

### ✅ Cómo Manejo de Credenciales

1. **Usar `.env.example` como plantilla**
   ```bash
   cp .env.example .env
   # Editar .env con credenciales reales (locales solamente)
   ```

2. **El archivo `.env` está en `.gitignore`**
   ```
   # En .gitignore
   .env
   .env.local
   .env.*.local
   ```

3. **Variables de entorno en `config.py`**
   ```python
   # selenium_gpt/config.py
   import os
   from dotenv import load_dotenv
   
   load_dotenv()  # Cargar desde .env
   BCI_USUARIO = os.getenv('BCI_USUARIO', '')
   BCI_CONTRASENA = os.getenv('BCI_CONTRASENA', '')
   ```

## Configuración Segura en Producción

### Django Settings

- **SECRET_KEY**: Generar una nueva en producción
  ```bash
  python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
  ```
  
- **DEBUG = False** en producción

- **ALLOWED_HOSTS**: Especificar exactamente los dominios permitidos
  ```env
  ALLOWED_HOSTS=api.gptseguros.cl,www.gptseguros.cl
  ```

- **SECURE_SSL_REDIRECT = True** en producción

- **SESSION_COOKIE_SECURE = True** en HTTPS

### Base de Datos

En producción, usar:
- PostgreSQL en lugar de SQLite
- Contenedor Docker con volúmenes montados
- Backups automatizados
- Contraseñas fuertes aleatorias

## Datos de Aseguradoras

### Rotación de Credenciales

Se recomienda rotar credenciales cada 3-6 meses:

```bash
# 1. Cambiar credencial en la plataforma de la aseguradora
# 2. Actualizar .env localmente
# 3. No hay necesidad de comitear cambios (está en .gitignore)
```

### Múltiples Entornos

Para manejar credenciales de múltiples entornos:

```env
# .env.development
BCI_USUARIO=test_dev_user
BCI_CONTRASENA=test_dev_password

# .env.staging (no comitear)
BCI_USUARIO=test_staging_user
BCI_CONTRASENA=test_staging_password

# .env.production (no comitear)
BCI_USUARIO=prod_user
BCI_CONTRASENA=prod_password
```

Cargar según ambiente:
```python
from dotenv import load_dotenv

env = os.getenv('ENVIRONMENT', 'development')
load_dotenv(f'.env.{env}')
```

## Auditoría y Monitoreo

### Verificar Antes de Comitear

```bash
# Buscar potenciales credenciales en el código
grep -r "password\|token\|secret\|key" selenium_gpt/ \
  --include="*.py" | grep -v "config.py\|#"

# Revisar cambios antes de comitear
git diff --cached
```

### Hooks Pre-commit

Crear `.git/hooks/pre-commit`:

```bash
#!/bin/bash

# Prevenir comitear archivos .env
if git diff --cached --name-only | grep -E '\.env.*' > /dev/null; then
    echo "ERROR: Intentaste comitear un archivo .env"
    exit 1
fi

# Buscar patrones de credenciales
FILES=$(git diff --cached --name-only --diff-filter=d)
for FILE in $FILES; do
    if grep -E "(password|secret|token|key|usuario|contrasena)\s*=" "$FILE" 2>/dev/null | \
       grep -v "config.py" | grep -v "# " > /dev/null; then
        echo "WARNING: Posible credencial en $FILE"
    fi
done
```

## Acceso y Permisos

### Por Rol

| Rol | Acceso | Credenciales |
|---|---|---|
| Desarrollador Local | Código público | `.env` local |
| CI/CD Pipeline | Código público | Secrets de GitHub/GitLab |
| Producción | API interna | Secrets del orquestador |
| Público | README solo | Ninguna |

### CI/CD (GitHub Actions)

Almacenar secretos en Settings → Secrets and variables:

```yaml
# .github/workflows/deploy.yml
env:
  BCI_USUARIO: ${{ secrets.BCI_USUARIO }}
  BCI_CONTRASENA: ${{ secrets.BCI_CONTRASENA }}
```

Nunca hacer:
```yaml
# ❌ MAL
env:
  BCI_USUARIO: user123
  BCI_CONTRASENA: password123
```

## Limpieza de Historial

Si se detecta que se comiteó una credencial accidentalmente:

```bash
# 1. Cambiar la credencial en la plataforma de la aseguradora INMEDIATAMENTE

# 2. Remover del historial Git
git filter-branch --tree-filter \
  'rm -f .env' HEAD

# 3. Force push (cuidado: afecta otros desarrolladores)
git push origin --force --all

# 4. Avisar al equipo que haga git pull
```

Mejor usando `git-filter-repo`:
```bash
pip install git-filter-repo
git filter-repo --path .env --invert-paths
```

## Respuesta ante Incidente

Si se filtra una credencial:

1. **Inmediato** (0-5 min)
   - Cambiar credencial en la plataforma de la aseguradora
   - Notificar a responsables

2. **Corto plazo** (5-30 min)
   - Remover de historial Git (si fue comiteado)
   - Buscar logs de acceso con credencial comprometida

3. **Medio plazo** (1-24h)
   - Revisar qué información se expuso
   - Auditar accesos no autorizados
   - Documentar el incidente

4. **Seguimiento** (1-7 días)
   - Implementar prevenciones adicionales
   - Capacitación del equipo
   - Actualizar procesos

## Dependencias Seguras

### Mantener Dependencias Actualizadas

```bash
# Verificar vulnerabilidades
pip install safety
safety check

# Pip audit (integrado en Python 3.12+)
pip-audit

# Actualizar dependencias
pip install -U -r requirements.txt
```

### Auditar Paquetes Desconocidos

Antes de instalar:
```bash
pip index versions package_name  # Verificar historial
pip show package_name             # Metadata del paquete
```

## Documentación de Seguridad

- [Django Security](https://docs.djangoproject.com/en/stable/topics/security/)
- [Selenium Best Practices](https://selenium.dev/documentation/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Python Security](https://python.readthedocs.io/en/stable/library/security_warnings.html)

## Preguntas Frecuentes

**P: ¿Puedo compartir mi `.env` con otros desarrolladores?**
R: No. Usa un gestor de secretos como:
- 1Password, LastPass, Bitwarden
- GitHub/GitLab Secrets (para CI/CD)
- HashiCorp Vault (producción)

**P: ¿Cómo configuro credenciales en CI/CD?**
R: Usa Secrets del proveedor (GitHub, GitLab, etc.) sin comitear en el repositorio.

**P: ¿Y si necesito usar la app sin credenciales?**
R: Implementar modo "demo" con datos simulados o aseguradoras de prueba.

---

**Última revisión**: Abril 2026
**Mantener este documento actualizado con nuevas prácticas**
