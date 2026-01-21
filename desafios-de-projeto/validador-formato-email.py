# Entrada do usuário
email = input().strip()

# TODO: Verifique as regras do e-mail:
if not email.startswith("@") and email.endswith(
    ("@gmail.com", "@outlook.com")
):
    print("E-mail válido")
else:
    print("E-mail inválido")
