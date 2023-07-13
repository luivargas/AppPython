import requests
from kivy.app import App


class MyFireBase:
    API_KEY = "AIzaSyBR2wRZPiZArll4zyYtPxFgNci1Ow3SH3Y"

    def criar_conta(self, email, senha):
        link = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={self.API_KEY}"

        info = {"email": email,
                "password": senha,
                "returnSecureToken": True}
        requisicao = requests.post(link, data=info)
        requisicao_dic = requisicao.json()

        if requisicao.ok:
            print("Usuario Criado")
            id_token = requisicao_dic["idToken"]
            refresh_token = requisicao_dic["refreshToken"]
            local_id = requisicao_dic["localId"]

            my_app = App.get_running_app()
            my_app.id_token = id_token
            my_app.local_id = local_id

            with open("refreshtoken.txt", "w") as arquivo:
                arquivo.write(refresh_token)

            req_id = requests.get(f"https://projetoapp-5335a-default-rtdb.firebaseio.com/proximo_id_vendedor.json?auth={id_token}")
            id_vendedor = req_id.json()

            link = f"https://projetoapp-5335a-default-rtdb.firebaseio.com/{local_id}.json?auth={id_token}"
            info_usuario = f'{{"avatar": "foto3.png", "equipe": "", "total_vendas": "0", "vendas": "", "id_vendedor": "{id_vendedor}"}}'
            requisicao_usuario = requests.patch(link, data=info_usuario)

            # atualizar o valor do proximo_id_vendedor
            proximo_id_vendedor = int(id_vendedor) + 1
            info_id_vendedor = f'{{"proximo_id_vendedor": "{proximo_id_vendedor}"}}'
            requests.patch(f"https://projetoapp-5335a-default-rtdb.firebaseio.com/.json?auth={id_token}", data=info_id_vendedor)

            my_app.carregar_infos_usuario()
            my_app.mudar_tela("homepage")

        else:
            mensagem_erro = requisicao_dic["error"]["message"]
            meu_aplicativo = App.get_running_app()
            pagina_login = meu_aplicativo.root.ids["loginpage"]
            pagina_login.ids["mensagem_login"].text = mensagem_erro
            pagina_login.ids["mensagem_login"].color = (1, 0, 0, 1)

    def fazer_login(self, email, senha):
        link = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={self.API_KEY}"
        info = {"email": email,
                "password": senha,
                "returnSecureToken": True}
        requisicao = requests.post(link, data=info)
        requisicao_dic = requisicao.json()
        if requisicao.ok:
            id_token = requisicao_dic["idToken"]
            refresh_token = requisicao_dic["refreshToken"]
            local_id = requisicao_dic["localId"]

            my_app = App.get_running_app()
            my_app.id_token = id_token
            my_app.local_id = local_id

            with open("refreshtoken.txt", "w") as arquivo:
                arquivo.write(refresh_token)

            my_app.carregar_infos_usuario()
            my_app.mudar_tela("homepage")

        else:
            mensagem_erro = requisicao_dic["error"]["message"]
            meu_aplicativo = App.get_running_app()
            pagina_login = meu_aplicativo.root.ids["loginpage"]
            pagina_login.ids["mensagem_login"].text = mensagem_erro
            pagina_login.ids["mensagem_login"].color = (1, 0, 0, 1)

    def trocar_token(self, refresh_token):
        link = f"https://securetoken.googleapis.com/v1/token?key={self.API_KEY}"

        info = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token
        }
        requisicao = requests.post(link, data=info)
        requisicao_dic = requisicao.json()
        if "error" in requisicao_dic:
            print(requisicao_dic["error"])
            local_id = 0
            id_token = 0
            return local_id, id_token
        else:
            local_id = requisicao_dic["user_id"]
            id_token = requisicao_dic["id_token"]
            print(requisicao_dic)
            return local_id, id_token
