from datetime import datetime
from io import StringIO
import json
import os
import re


class Writer:
    def __init__(self, data: dict, format: str, path: str):
        self._buffer = StringIO()
        self._format = format
        self._data = data
        self._path = path

    def _mkdirs(self):
        dir = os.path.dirname(self._path)

        if not os.path.exists(dir):
            os.makedirs(dir, exist_ok=True)

    def write(self):
        self._mkdirs()

        if self._format == "md":
            self.write_md()
        else:
            self.write_json()

        print(f"Concluido! Arquivo salvo em {os.path.abspath(self._path)}")

    def write_md(self):
        name = self._data.get("name")
        url = self._data.get("url")
        avatar_url = self._data.get("avatar_url")

        self._buffer.write(f"# <img src='{avatar_url}' alt='{name}' width='40px' /> [{name}]({url})\n\n")
        if bio := self._data.get("bio"):
            self._buffer.write(f"> {re.sub(r'\r|\n', '', bio) or '`Sem descrição`'}\n")
        if location := self._data.get("location"):
            self._buffer.write(f"- 📍 Localização: {location}\n")
        if email := self._data.get("email"):
            self._buffer.write(f"- ✉ Email: {email}\n")
        if company := self._data.get("company"):
            self._buffer.write(f"- 🏢 Empresa: {company}\n")
        if blog := self._data.get("blog"):
            self._buffer.write(f"- 🌐 Blog: {blog}\n")

        repos = self._data.get("repos", [])
        self._buffer.write(f"## Repositórios ({len(repos)})\n\n")
        for repo in repos:
            self._buffer.write(f"## [{repo.get('full_name')}]({repo.get('url')})\n\n")
            if homepage := repo.get("homepage"):
                self._buffer.write(f"> {homepage}\n\n")

            self._buffer.write(f"> {repo.get('description') or '`Sem descrição`'}\n")
            self._buffer.write(f"```bash\n{repo.get('clone_url')}\n```\n\n")

            self._buffer.write("| Nome | Valor |\n| --- | --- |\n")
            if created_at := repo.get("created_at"):
                created_at = datetime.fromisoformat(created_at).strftime("%d/%m/%Y")
                self._buffer.write(f"| Criado | {created_at} |\n")

            if updated_at := repo.get("updated_at"):
                updated_at = datetime.fromisoformat(updated_at).strftime("%d/%m/%Y")
                self._buffer.write(f"| Atualizado | {updated_at} |\n")

            if pushed_at := repo.get("pushed_at"):
                pushed_at = datetime.fromisoformat(pushed_at).strftime("%d/%m/%Y")
                self._buffer.write(f"| Ultimo push | {pushed_at} |\n")
            self._buffer.write(f"| Linguagem principal | `{repo.get('language') or 'N/A'}` |\n")
            if topics := repo.get("topics"):
                self._buffer.write(f"| Temas | {', '.join(map(lambda x: f'`{x}`', topics))} |\n")

        followers = self._data.get("followers", [])
        self._buffer.write(f"\n## Seguidores ({len(followers)})\n\n")
        for follower in followers:
            name = follower.get("name")
            url = follower.get("url")
            avatar_url = follower.get("avatar_url")

            self._buffer.write(f"- <img src='{avatar_url}' alt='{name}' width='40px' />  [{name}]({url})\n")

        following = self._data.get("following", [])
        self._buffer.write(f"\n## Seguindo ({len(following)})\n\n")
        for following in following:
            name = following.get("name")
            url = following.get("url")
            avatar_url = following.get("avatar_url")
            self._buffer.write(f"- <img src='{avatar_url}' alt='{name}' width='40px' /> [{name}]({url})\n")

        with open(self._path, "w", encoding="utf-8") as f:
            f.write(self._buffer.getvalue())

    def write_json(self):
        with open(self._path, "w", encoding="utf-8") as f:
            f.write(json.dumps(self._data, indent=4, ensure_ascii=False))
