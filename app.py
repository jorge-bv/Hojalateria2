from flask import Flask, render_template, request, jsonify
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv

# Cargar variables de entorno desde .env si existe
load_dotenv()

app = Flask(__name__)

# ── CONFIGURACIÓN DE SENDGRID ───────────────────────────────────────
# Obtén tu API Key desde https://app.sendgrid.com/settings/api_keys
SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY", "")
SENDGRID_FROM_EMAIL = "noreply@hojalateriabravo.cl"  # Email verificado en SendGrid
EMAIL_DESTINO = "bravov.jo@gmail.com"  # Donde recibirás las cotizaciones
# ────────────────────────────────────────────────────────────────────


def enviar_correo(nombre, email, telefono, mensaje):
    """Envía el correo con los datos del formulario usando SendGrid."""
    if not SENDGRID_API_KEY:
        raise Exception("SENDGRID_API_KEY no está configurada")
    
    html_content = f"""
    <html><body style="font-family:Arial,sans-serif;background:#f5f5f5;padding:20px;">
      <div style="max-width:580px;margin:auto;background:#1a1f2e;color:#f0f2f5;border-radius:6px;overflow:hidden;">
        <div style="background:#f05a1a;padding:20px 30px;">
          <h1 style="margin:0;font-size:22px;letter-spacing:2px;">Hojalateria Agustin Bravo — Nueva Cotización</h1>
        </div>
        <div style="padding:30px;">
          <table style="width:100%;border-collapse:collapse;">
            <tr><td style="padding:8px 0;color:#8892a4;font-size:12px;text-transform:uppercase;letter-spacing:1px;">Nombre</td>
                <td style="padding:8px 0;font-weight:bold;">{nombre}</td></tr>
            <tr><td style="padding:8px 0;color:#8892a4;font-size:12px;text-transform:uppercase;letter-spacing:1px;">Email</td>
                <td style="padding:8px 0;"><a href="mailto:{email}" style="color:#f05a1a;">{email}</a></td></tr>
            <tr><td style="padding:8px 0;color:#8892a4;font-size:12px;text-transform:uppercase;letter-spacing:1px;">Teléfono</td>
                <td style="padding:8px 0;"><a href="tel:{telefono}" style="color:#f05a1a;">{telefono}</a></td></tr>
          </table>
          <div style="margin-top:20px;padding:16px;background:#252b3b;border-left:3px solid #f05a1a;border-radius:3px;">
            <p style="margin:0 0 6px;color:#8892a4;font-size:11px;text-transform:uppercase;letter-spacing:1px;">Mensaje</p>
            <p style="margin:0;line-height:1.6;">{mensaje or "Sin mensaje adicional."}</p>
          </div>
          <div style="margin-top:24px;text-align:center;">
            <a href="mailto:{email}" style="background:#f05a1a;color:#fff;padding:12px 28px;text-decoration:none;border-radius:3px;font-weight:bold;letter-spacing:1px;font-size:14px;">
              RESPONDER AL CLIENTE →
            </a>
          </div>
        </div>
        <div style="padding:16px 30px;background:#0e1320;font-size:11px;color:#8892a4;text-align:center;">
          Hojalatería Agustin Bravo · contacto@hojalateriabravo.cl
        </div>
      </div>
    </body></html>
    """
    
    message = Mail(
        from_email=SENDGRID_FROM_EMAIL,
        to_emails=EMAIL_DESTINO,
        subject=f"🔧 Nueva cotización desde la web — {nombre}",
        html_content=html_content,
        reply_to_email=email
    )
    
    sg = SendGridAPIClient(SENDGRID_API_KEY)
    response = sg.send(message)
    return response


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/contacto", methods=["POST"])
def contacto():
    try:
        data = request.form
        enviar_correo(
            nombre   = data.get("nombre", ""),
            email    = data.get("email", ""),
            telefono = data.get("telefono", ""),
            mensaje  = data.get("mensaje", ""),
        )
        print("✅ Correo enviado exitosamente via SendGrid")
        return jsonify({"ok": True, "message": "Cotización enviada correctamente"})
    except ValueError as e:
        error_msg = "Error de configuración: falta SENDGRID_API_KEY en el servidor"
        print(f"❌ {error_msg}: {str(e)}")
        return jsonify({"ok": False, "error": error_msg}), 500
    except Exception as e:
        error_msg = f"Error al enviar email: {str(e)}"
        print(f"❌ {error_msg}")
        return jsonify({"ok": False, "error": error_msg}), 500


if __name__ == "__main__":
    print("🔧 Hojalatería Agustin Bravo corriendo en http://localhost:5000")
    app.run(debug=True)
