from utils.Requester import Requester
from utils.Writer import Writer

username = input("Digite o nome de usuário: ").strip()
if not username:
    raise Exception("Por favor, digite um nome de usuário.")

req = Requester(username)


valid_formats = ["md", "json"]
print(f"Escolha o formato de saída: [{' | '.join(valid_formats)}]")
format = input().strip().lower()
if format not in valid_formats:
    raise Exception("Formato de saída inválido.")

writer = Writer(req.get_data(), format, f"output/{username}.{format}")
writer.write()
