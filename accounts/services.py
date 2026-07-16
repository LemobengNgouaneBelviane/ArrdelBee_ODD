from django.core.mail import send_mail
from django.conf import settings


def send_code_via_email_service(email: str, code: str, type_: str = "reset") -> None:
    subjects = {
        "reset": "Code de réinitialisation — ArrdelBee",
        "verify": "Code de vérification — ArrdelBee",
    }
    subject = subjects.get(type_, "Code — ArrdelBee")
    message = (
        f"Bonjour,\n\n"
        f"Votre code est : {code}\n"
        f"Il expire dans 10 minutes.\n\n"
        f"Si vous n'avez pas demandé ce code, ignorez ce message.\n\n"
        f"— L'équipe ArrdelBee"
    )
    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "no-reply@arrdelbee.cm")
    send_mail(subject, message, from_email, [email], fail_silently=False)
