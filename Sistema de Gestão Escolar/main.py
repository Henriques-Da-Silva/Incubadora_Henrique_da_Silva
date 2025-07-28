from customtkinter import *
from tkinter import messagebox
import json
import re
import os

pasta_notas = 'Notas'
pasta_mais = 'Mais'

try:
    os.makedirs(pasta_notas, exist_ok=True)
    os.makedirs(pasta_mais, exist_ok=True)
except PermissionError:
    messagebox.showerror("Erro", "Permissão negada para criar pastas necessárias.")

if not os.path.exists(f'Mais/alunos.json'):
    alunos = list()
    with open("Mais/alunos.json", "w", encoding="utf-8") as f:
        json.dump(alunos, f, ensure_ascii=False, indent=2)

if not os.path.exists(f'Mais/usuariosAdmin.json'):
    users = [{"email": "admin@gmail.com", "senha": "admin"}, {"email": "Admin@gmail.com", "senha": "admin"}]
    with open("Mais/usuariosAdmin.json", "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)


class Sistema_de_Gestao_Escolar():
    def __init__(self): 
        self.alunos = self.carregar_alunos()
        self.users = self.carregar_usuarios()
        self.janela = CTk()
        self.janela.title('Sistema de Gestão Escolar')
        self.janela.geometry('1350x700+5+5')
        self.janela.minsize(width=1300, height=650)
        self.main()
        try:
            self.janela.mainloop()
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

    def carregar_alunos(self):
        try:
            with open("Mais/alunos.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def carregar_usuarios(self):
        try:
            with open("Mais/usuariosAdmin.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return [{"email": "admin@gmail.com", "senha": "admin"}, {"email": "Admin@gmail.com", "senha": "admin"}]

    def mensagem(self, sms):
        messagebox.showinfo('Mensagem', sms)

    def main(self):
        self.frame_esquerdo = CTkFrame(self.janela, width=670)
        self.frame_esquerdo.pack(padx=5, pady=5, fill='both', side='left', expand=True)

        self.frame_direito = CTkFrame(self.janela, width=670)
        self.frame_direito.pack(padx=5, pady=5, fill='both', side='right', expand=True)

        self.label_BemVindo = CTkLabel(self.frame_esquerdo, text='BEM-VINDO AO SEU\nSISTEMA DE GESTÃO\nESCOLAR', font=('Time', 40, 'bold'))
        self.label_BemVindo.pack(pady=250)

        self.frame_login = CTkFrame(self.frame_direito, width=520, height=590)
        self.frame_login.pack(pady=50, padx=5, fill='y', expand=True)

        self.label_login = CTkLabel(self.frame_login, text='LOGIN', font=('Time', 40, 'bold'))
        self.label_login.pack(pady=(80,50))

        self.entry_email = CTkEntry(self.frame_login, placeholder_text='E-mail', corner_radius=100, width=500, height=60)
        self.entry_email.pack(pady=5, padx=50, fill='y')

        self.entry_palavraPasse = CTkEntry(self.frame_login, placeholder_text='Palavra-Passe', corner_radius=100, width=500, height=60, show='•')
        self.entry_palavraPasse.pack(pady=25, padx=50, fill='y')

        self.botao_login = CTkButton(self.frame_login, text='LOGIN', width=500, height=50, corner_radius=100, command=self.Verificar_tipo_de_usuario)
        self.botao_login.pack(pady=50, padx=50, fill='y')

    def Verificar_tipo_de_usuario(self):
        found = False

        email_digitado = self.entry_email.get().strip()
        palavraPasse_digitada = self.entry_palavraPasse.get().strip()

        for dicionario in self.users:
            if dicionario['email'] == email_digitado and dicionario['senha'] == palavraPasse_digitada:
                found = True
                self.mensagem('Login efetuado\nTipo: Admin')
                self.Administrar()
                break

        if not found:
            for aluno in self.alunos:
                if aluno['email'] == email_digitado and aluno['senha'] == palavraPasse_digitada:
                    found = True
                    self.mensagem('Login efetuado\nTipo: Aluno')
                    self.exibir_dados_do_aluno(aluno['nome'])
                    break

        if not found:
            self.mensagem('Palavra-Passe ou E-mail errado.')

    def Administrar(self):
        self.eliminar_widgets1()
        self.eliminar_widgets2()

        self.label_alunos = CTkLabel(self.frame_esquerdo, text='ALUNOS', font=('Time', 40, 'bold'))
        self.label_alunos.pack(pady=40)

        if self.alunos != []:
            alunos_ordenados = sorted(self.alunos, key=lambda aluno: aluno['nome'].lower())

            self.frame_alunos = CTkScrollableFrame(self.frame_esquerdo)
            self.frame_alunos.pack(fill='both', expand=True)
            
            cont=1
            for aluno in alunos_ordenados:
                aluno_button = CTkButton(self.frame_alunos, text=f'    {cont} - {aluno["nome"]}', anchor='w', font=('Time', 15, 'bold'), height=44, width=440, fg_color='#212121', command=lambda aluno=aluno: self.abrir_aluno(aluno))
                aluno_button.pack(pady=3, anchor='w', expand=True, padx=30, fill='x')
                cont += 1
        else:
            self.label_sem_alunos = CTkLabel(self.frame_esquerdo, text='AINDA SEM\nALUNOS\nNO SISTEMA', font=('Time', 40, 'bold'), text_color='red')
            self.label_sem_alunos.pack(pady=100)

        self.footer = CTkFrame(self.frame_esquerdo, fg_color='#1A1A1A', height=50)
        self.footer.pack(side="bottom", fill="x")

        self.botao_adicionar = CTkButton(self.footer, text='+', font=('Time', 35), fg_color='#212121', text_color='white', width=50, height=50, corner_radius=100, hover_color='#121212', command=self.adicionar_aluno)
        self.botao_adicionar.pack(pady=1, padx=5, side='left')

        self.botao_sair = CTkButton(self.footer, text='Sair', font=('Time', 35), fg_color='#212121', text_color='white', width=30, height=50, corner_radius=100, hover_color='#121212', command=self.sair)
        self.botao_sair.pack(pady=1, padx=5, side='right')

    def remover_usuario(self, email):
        confirmacao = messagebox.askyesno("Confirmação", f"Tem certeza que deseja deletar este usuário?")
        
        if not confirmacao:
            self.mensagem("Operação cancelada.")
            return

        for user in self.users:
            if user['email'] == email:
                self.users.remove(user)
                with open("Mais/usuariosAdmin.json", "w", encoding="utf-8") as f:
                    json.dump(self.users, f, ensure_ascii=False, indent=4)
                self.mensagem(f"Usuário administrador com e-mail '{email}' removido com sucesso!")
                self.Administrar()
                return

        for aluno in self.alunos:
            if aluno['email'] == email:
                self.alunos.remove(aluno)
                with open("Mais/alunos.json", "w", encoding="utf-8") as f:
                    json.dump(self.alunos, f, ensure_ascii=False, indent=4)
                self.mensagem(f"Aluno com e-mail '{email}' removido com sucesso!")
                self.Administrar()
                return

        self.mensagem(f"Nenhum usuário encontrado com o e-mail '{email}'.")
    
    def validar_email(self, email):
        """ Valida se o e-mail está no formato correto. Retorna True se for válido, caso contrário, False."""
        padrao = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(padrao, email) is not None

    def adicionar_aluno(self):
        self.eliminar_widgets1()

        self.frame_add = CTkFrame(self.frame_direito, width=520, height=590)
        self.frame_add.pack(pady=50, padx=5, fill='y', expand=True)

        self.label_add = CTkLabel(self.frame_add, text='ADICIONAR ALUNO', font=('Time', 40, 'bold'))
        self.label_add.pack(pady=(80,50))

        self.entry_nome = CTkEntry(self.frame_add, placeholder_text='Nome', corner_radius=100, width=500, height=60)
        self.entry_nome.pack(pady=5, padx=50, fill='y')

        self.entry_email = CTkEntry(self.frame_add, placeholder_text='E-mail', corner_radius=100, width=500, height=60)
        self.entry_email.pack(pady=25, padx=50, fill='y')

        self.entry_palavraPasseAluno = CTkEntry(self.frame_add, placeholder_text='Palavra-Passe para o aluno', corner_radius=100, width=500, height=60)
        self.entry_palavraPasseAluno.pack(pady=5, padx=50, fill='y')

        self.botao_add = CTkButton(self.frame_add, text='Adicionar', width=500, height=50, corner_radius=100, command=self.salvar_aluno)
        self.botao_add.pack(pady=50, padx=50, fill='y')

    def salvar_aluno(self):
        nome = self.entry_nome.get().strip()
        email = self.entry_email.get().strip()
        senha = self.entry_palavraPasseAluno.get().strip()

        if not nome:
            self.mensagem('O nome não pode estar vazio!')
            return

        if not email:
            self.mensagem('O email não pode estar vazio!')
            return

        if not senha:
            self.mensagem('A senha não pode estar vazia!')
            return
        
        if not self.validar_email(email):
            self.mensagem("E-mail inválido! Por favor, insira um e-mail válido.")
            return 

        if any(aluno['email'] == email for aluno in self.alunos):
            self.mensagem("E-mail já cadastrado!")
            return

        novo_aluno = {"nome": nome,
                      "email": email,
                      "senha": senha}

        self.alunos.append(novo_aluno)

        try:
            with open('Mais/Alunos.json', "w", encoding='utf-8') as file:
                json.dump(self.alunos, file, indent=4, ensure_ascii=False)

            self.mensagem('Aluno adicionado com sucesso!')
            self.Administrar()

            self.criar_file_notas(str(nome))
        except Exception as e:
            self.mensagem(f'Erro ao salvar aluno: {str(e)}')

    def abrir_aluno(self, aluno):
        self.eliminar_widgets1()

        label_titulo = CTkLabel(self.frame_direito, text='Editar Aluno', font=('Time', 40, 'bold'))
        label_titulo.pack(pady=(80, 5), padx=60)

        label_nome = CTkLabel(self.frame_direito, text='Nome:', font=('Time', 15, 'bold'))
        label_nome.pack(pady=(50, 5), anchor='w', padx=100)

        self.entry_nome = CTkEntry(self.frame_direito, fg_color='#212121', width=400, height=40)
        self.entry_nome.pack(pady=(5, 10), anchor='w', padx=100)
        self.entry_nome.insert(0, aluno['nome'])

        label_email = CTkLabel(self.frame_direito, text='Email:', font=('Time', 15, 'bold'))
        label_email.pack(pady=(50, 5), anchor='w', padx=100)

        self.entry_email = CTkEntry(self.frame_direito, fg_color='#212121', width=400, height=40)
        self.entry_email.pack(pady=5, anchor='w', padx=100)
        self.entry_email.insert(0, aluno['email'])

        label_senha = CTkLabel(self.frame_direito, text='Senha:', font=('Time', 15, 'bold'))
        label_senha.pack(pady=(50, 5), anchor='w', padx=100)

        self.entry_senha = CTkEntry(self.frame_direito, fg_color='#212121', width=400, height=40)
        self.entry_senha.pack(pady=5, anchor='w', padx=100)
        self.entry_senha.insert(0, aluno['senha'])

        footer2 = CTkFrame(self.frame_direito, fg_color='#1A1A1A')
        footer2.pack(side='bottom', fill='x')
        frame_botoes = CTkFrame(footer2, fg_color='#1A1A1A')
        frame_botoes.pack(pady=5, anchor='center')

        n = aluno['nome']
        e = aluno['email']
        
        botao_salvar = CTkButton(frame_botoes, text='Salvar', font=('Time', 35), hover_color='#2E2E2E', fg_color='#333333', corner_radius=100, command=lambda: self.salvar_edicao_aluno(aluno))
        botao_salvar.pack(pady=1, side='left', padx=(0,25))

        botao_notas = CTkButton(frame_botoes, text='Notas', font=('Arial', 35), hover_color='#2E2E2E', fg_color='#333333', corner_radius=100, command=lambda: self.exibir_notas(n))
        botao_notas.pack(pady=1, side='left')
        
        botao_remover = CTkButton(frame_botoes, text='Deletar', font=('Arial', 35), hover_color='#2E2E2E', fg_color='#333333', corner_radius=100, command=lambda: self.remover_usuario(e))
        botao_remover.pack(pady=1, side='left', padx=(25,0))

        botao_cancelar = CTkButton(frame_botoes, text='Cancelar', font=('Arial', 35), hover_color='#2E2E2E', fg_color='#333333', corner_radius=100, command=self.cancelar)
        botao_cancelar.pack(pady=1, side='left', padx=(25,0))

    def cancelar(self):
        for widget in self.frame_direito.winfo_children():
            widget.destroy()

    def salvar_edicao_aluno(self, aluno_antigo):
        novo_nome = self.entry_nome.get()
        novo_email = self.entry_email.get()
        nova_senha = self.entry_senha.get()

        # Verifica se o e-mail já pertence a outro aluno
        for aluno in self.alunos:
            if aluno['email'] == novo_email and aluno != aluno_antigo:
                self.mensagem('E-mail já pertence a outro aluno!')
                return

        aluno_antigo['nome'] = novo_nome
        aluno_antigo['email'] = novo_email
        aluno_antigo['senha'] = nova_senha

        with open('Mais/Alunos.json', "w", encoding='utf-8') as file:
            json.dump(self.alunos, file, indent=4)

        self.mensagem('Aluno editado com sucesso!')
        self.Administrar()

    def criar_file_notas(self, nome):
        ficheiro = f'Notas/{nome.strip()}.json'

        data = [
                {"disciplina": "Matemática", "nota": 0},
                {"disciplina": "Português", "nota": 0},
                {"disciplina": "Ciências", "nota": 0},
                {"disciplina": "História", "nota": 0},
                {"disciplina": "Geografia", "nota": 0}
               ]

        with open(ficheiro, "w", encoding='utf-8') as f:
            json.dump(data, f)

    def exibir_notas(self, aluno):
        ficheiro = f'Notas/{aluno.strip()}.json'

        with open(ficheiro, "r", encoding='utf-8') as f:
            notas = json.load(f)

        self.eliminar_widgets1()

        label_titulo = CTkLabel(self.frame_direito, text=f'Notas do(a) {aluno}', font=('Time', 40, 'bold'))
        label_titulo.pack(pady=(80, 5), padx=40)
        
        label_info = CTkLabel(self.frame_direito, text='Disciplina\t\t\t\t\tNota', font=('Time', 20, 'bold'))
        label_info.pack(pady=(40, 0), padx=20)

        self.frame_boletim1 = CTkScrollableFrame(self.frame_direito)
        self.frame_boletim1.pack(pady=(5, 0), padx= 40, fill='both', expand=True)

        for item in notas:
            frame_linha = CTkFrame(self.frame_boletim1, fg_color='#212121', height=50)
            frame_linha.pack(pady=5, padx=20, fill='x')

            label_disciplina = CTkLabel(frame_linha, text=f'{item["disciplina"]}', font=('Time', 18, 'bold'), width=20)
            label_disciplina.pack(side='left', padx=(70,50), pady=10)

            entry_nota = CTkEntry(frame_linha, fg_color='#212121', width=50, height=30)
            entry_nota.pack(side='right', padx=(10,70), pady=10)
            entry_nota.insert(0, float(item['nota']))

        list_notas = []
        for item in notas:
            list_notas.append(float(item['nota']))
        media = self.calcular_media(list_notas)
            
        label_media = CTkLabel(self.frame_direito, text=f'Média: {media}', font=('Time', 30, 'bold'))
        label_media.pack(pady=40, padx=20)
            
        footer = CTkFrame(self.frame_direito, fg_color='#1A1A1A')
        footer.pack(side='bottom', fill='x')

        botao_salvar = CTkButton(footer, text='Salvar', font=('Time', 35), width=40, hover_color='#2E2E2E', fg_color='#333333', corner_radius=100, command=lambda: self.salvar_notas(ficheiro))
        botao_salvar.pack(pady=1, side='left', padx=70)

        botao_cancelar = CTkButton(footer, text='Cancelar', font=('Arial', 35), width=40, hover_color='#2E2E2E', fg_color='#333333', corner_radius=100, command=self.cancelar)
        botao_cancelar.pack(pady=1, side='right', padx=70)

    def salvar_notas(self, file):
        lista_notas = []

        for widget in self.frame_boletim1.winfo_children():
            if widget.winfo_children():
                for wdg in widget.winfo_children():
                    if isinstance(wdg, CTkEntry):
                        try:
                            nota = float(wdg.get())
                            if nota < 0 or nota > 20:
                                self.mensagem('Notas devem estar entre 0 e 20.')
                                return
                            lista_notas.append(nota)
                        except ValueError:
                            self.mensagem('Por favor, insira apenas números válidos nas notas.')
                            return

        with open(file, "r", encoding='utf-8') as f:
            notas = json.load(f)

        if len(lista_notas) != len(notas):
            self.mensagem('Erro: O número de notas inseridas não corresponde ao número de disciplinas.')
            return

        for i, item in enumerate(notas):
            item['nota'] = lista_notas[i]

        with open(file, "w", encoding='utf-8') as fich:
            json.dump(notas, fich, ensure_ascii=False, indent=4)

        self.mensagem('Notas editadas com Sucesso!')
        self.cancelar()

    def eliminar_widgets1(self):
        for widget in self.frame_direito.winfo_children():
            widget.destroy()

    def eliminar_widgets2(self):
        for widget in self.frame_esquerdo.winfo_children():
            widget.destroy()


#Funções para Tipo de Usuário: Aluno

    def calcular_media(self, notas):
        if not notas:
            return 0
        return sum(notas) / len(notas)

    def exibir_dados_do_aluno(self, aluno):
        self.eliminar_widgets1()
        self.eliminar_widgets2()

        self.label_dados_aluno = CTkLabel(self.frame_esquerdo, text='DADOS DO ALUNO', font=('Time', 40, 'bold'))
        self.label_dados_aluno.pack(pady=40)

        ficheiro = f'Notas/{aluno.strip()}.json'

        with open(ficheiro, "r", encoding='utf-8') as f:
            notas = json.load(f)

        list_notas = []
        for item in notas:
            list_notas.append(float(item['nota']))

        media = self.calcular_media(list_notas)

        self.label_nome = CTkLabel(self.frame_esquerdo, text=f'Nome: {aluno}', font=('Time', 25, 'bold'))
        self.label_nome.pack(pady=20, padx=100, anchor='w')

        self.frame_media = CTkFrame(self.frame_esquerdo, width=520, height=590)
        self.frame_media.pack(pady=(40, 20), padx=100, fill='both', expand=True)

        self.label_sua_media = CTkLabel(self.frame_media, text='Sua média:', font=('Time', 24, 'bold'))
        self.label_sua_media.pack(pady=20, padx=20, anchor='w')

        self.label_desempenho = CTkLabel(self.frame_media, 
                                         text='👍🏽Bom Desempenho!' if media >= 12 
                                         else('😊Suficiente, mas dá pra melhorar!' if 10 <= media < 12 else '🙁Mau Desempenho, Estude Mais!'), 
                                         font=('Time', 15, 'bold'))
        self.label_desempenho.pack(pady=20, padx=20, anchor='center')

        self.canvas_media = CTkCanvas(self.frame_media, width=150, height=150, bg='#333333', highlightthickness=0)
        self.canvas_media.pack(pady=25)

        self.canvas_media.create_oval(10, 10, 140, 140, fill='#333333', outline='#4169E1', width=10)
        self.canvas_media.create_text(75, 75, text=f'{media:.2f}', font=('Time', 25, 'bold'), fill='white')
        self.canvas_media.create_text(75, 95, text='Média do aluno', font=('Time', 7, 'bold'), fill='white')

        self.footer = CTkFrame(self.frame_esquerdo, fg_color='#1A1A1A', height=50)
        self.footer.pack(side="bottom", fill="x")

        self.botao_sair = CTkButton(self.footer, text='Sair', font=('Time', 35), fg_color='#212121', text_color='white', width=30, height=50, corner_radius=100, hover_color='#121212', command=self.sair)
        self.botao_sair.pack(pady=1, padx=5, side='right')

        self.exibir_boletim(ficheiro)

    def sair(self):
        for widget in self.janela.winfo_children():
            widget.destroy()
        self.main()

    def exibir_boletim(self, file):
        with open(file, "r", encoding='utf-8') as f:
            notas = json.load(f)

        self.label_boletim = CTkLabel(self.frame_direito, text='BOLETIM', font=('Time', 35, 'bold'))
        self.label_boletim.pack(pady=(40, 10))

        label_info = CTkLabel(self.frame_direito, text='Disciplina\t\tNota', font=('Time', 20, 'bold'))
        label_info.pack(pady=(30, 0), padx=20)

        self.frame_boletim = CTkScrollableFrame(self.frame_direito, width=400)
        self.frame_boletim.pack(pady=(5, 30), padx= 100, fill='both', expand=True)
        
        for item in notas:
            frame_linha = CTkFrame(self.frame_boletim, fg_color='#212121', height=50)
            frame_linha.pack(pady=5, padx=70, fill='x')
            
            label_disciplina = CTkLabel(frame_linha, text=f"{item['disciplina']}", font=('Time', 15, 'bold'))
            label_disciplina.pack(pady=5, padx=20, side='left')
            
            label_nota = CTkLabel(frame_linha, text=f"{float(item['nota'])}", font=('Time', 15, 'bold'))
            label_nota.pack(pady=5, padx=20, side='right')


Sistema_de_Gestao_Escolar()