import requests


class Requester:
    def __init__(self, username: str):
        self._username = username

    def _get(self):
        print(f"♣ Requisitando API principal, usuário '{self._username}'")
        res = requests.get(f"https://api.github.com/users/{self._username}")

        if not res.ok:
            raise Exception(f"Requisição falhou: {res.status_code}")

        return res

    def _get_repos(self):
        print(f"♣ Requisitando API de repositório, usuário '{self._username}'")
        res = requests.get(f"https://api.github.com/users/{self._username}/repos")

        if not res.ok:
            raise Exception(f"Requisição falhou: {res.status_code}")

        return res

    def _get_follows(self):
        print(f"♣ Requisitando API de seguidores e seguindos, usuário '{self._username}'")
        res_following = requests.get(f"https://api.github.com/users/{self._username}/following")

        if not res_following.ok:
            raise Exception(f"Requisição falhou: {res_following.status_code}")

        res_followers = requests.get(f"https://api.github.com/users/{self._username}/followers")

        if not res_followers.ok:
            raise Exception(f"Requisição falhou: {res_followers.status_code}")

        return res_followers, res_following

    def get_data(self):
        data = {}

        main = self._get().json()
        repos = self._get_repos().json()
        followers, following = self._get_follows()

        data["name"] = main.get("name")
        data["url"] = main.get("html_url")
        data["avatar_url"] = main.get("avatar_url")
        data["bio"] = main.get("bio")
        data["location"] = main.get("location")
        data["email"] = main.get("email")
        data["company"] = main.get("company")
        data["blog"] = main.get("blog")
        data["followers"] = []
        for follower in followers.json():
            data["followers"].append(
                {
                    "name": follower.get("login"),
                    "url": follower.get("html_url"),
                    "avatar_url": follower.get("avatar_url"),
                }
            )

        data["following"] = []
        for following in following.json():
            data["following"].append(
                {
                    "name": following.get("login"),
                    "url": following.get("html_url"),
                    "avatar_url": following.get("avatar_url"),
                }
            )
        data["repos"] = []
        for repo in repos:
            data["repos"].append(
                {
                    "name": repo.get("name"),
                    "full_name": repo.get("full_name"),
                    "url": repo.get("html_url"),
                    "homepage": repo.get("homepage"),
                    "description": repo.get("description"),
                    "clone_url": repo.get("clone_url"),
                    "created_at": repo.get("created_at"),
                    "updated_at": repo.get("updated_at"),
                    "pushed_at": repo.get("pushed_at"),
                    "language": repo.get("language"),
                    "topics": repo.get("topics"),
                }
            )

        return data
