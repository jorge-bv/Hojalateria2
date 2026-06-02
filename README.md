# 🔧 MetalArt — Hojalatería Web App (Flask)

## Estructura del proyecto

```
metalart/
├── app.py              ← servidor Flask + envío de correos
├── requirements.txt    ← dependencias
├── templates/
│   └── index.html      ← página web completa
└── README.md
```

---

## ⚙️ Instalación paso a paso

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Configurar el correo (Gmail)

Abre `app.py` y edita estas 3 líneas:

```python
EMAIL_ORIGEN   = "tu_correo@gmail.com"      # tu Gmail
EMAIL_DESTINO  = "tu_correo@gmail.com"      # donde recibirás las cotizaciones
EMAIL_PASSWORD = "tu_contraseña_de_app"     # contraseña de aplicación (ver abajo)
```

### 3. Crear contraseña de aplicación en Gmail

Para que Gmail permita enviar correos desde Python:

1. Ve a **myaccount.google.com**
2. Seguridad → Verificación en dos pasos (actívala si no la tienes)
3. Seguridad → **Contraseñas de aplicación**
4. Selecciona "Otra" → escribe "MetalArt Flask"
5. Copia la contraseña de 16 caracteres que te da
6. Pégala en `EMAIL_PASSWORD` en `app.py`

---

## ▶️ Ejecutar

```bash
python app.py
```

Abre tu navegador en: **http://localhost:5000**

---

## 📧 Cómo funciona el formulario

Cuando alguien llena el formulario:
1. Flask recibe los datos en `/contacto`
2. Se envía un correo HTML a tu email con todos los datos del cliente
3. El correo tiene un botón **"Responder al cliente"** para contestarle directamente
4. La página muestra un mensaje de éxito al visitante

---

## 🌐 Publicar en internet (opcional)

Para que tu web sea pública puedes usar:

- **Railway.app** — gratis, fácil, conecta con GitHub
- **Render.com** — gratis, ideal para Flask
- **PythonAnywhere** — gratis, específico para Python

En todos solo subes los archivos y listo.
