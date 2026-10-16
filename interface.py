# Interface Tkinter: clientes, fornecedores, produtos, pedidos e encomendas.

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import re
import base_dados as DB


def validar_nif(nif):
    return re.fullmatch(r"\d{9}", nif) is not None

def validar_nome(nome):
    return re.fullmatch(r"[A-Za-zÀ-ÿ\s]{3,50}", nome) is not None

def validar_preco(preco):
    return re.fullmatch(r"\d+(\.\d{1,2})?", preco) is not None

def validar_id(id_):
    return re.fullmatch(r"\d+", id_) is not None



def Supermat():
    jn = Tk()
    jn.title("Sistema Supermat - Administração")
    jn.geometry("950x600")
    jn.configure(bg="#EDEDED")


    style = ttk.Style()
    style.theme_use("clam")

    style.configure("TLabel", background="#EDEDED", foreground="#222", font=("Arial", 12))
    style.configure("Title.TLabel", background="#EDEDED", foreground="#111", font=("Arial", 18, "bold"))
    style.configure("TButton", font=("Arial", 11), padding=6)


    sidebar = Frame(jn, bg="#1E1E1E", width=220)
    sidebar.pack(side=LEFT, fill=Y)

    Label(sidebar, text="Supermat Admin", bg="#1E1E1E", fg="white",
          font=("Arial", 16, "bold")).pack(pady=30)


    conteudo_frame = ttk.Frame(jn)
    conteudo_frame.pack(side=LEFT, fill=BOTH, expand=True)

    def limpar_conteudo():
        for widget in conteudo_frame.winfo_children():
            widget.destroy()


    def mostrar_inicio():
        limpar_conteudo()
        ttk.Label(conteudo_frame, text="Sistema de Administração do Supermercado",
                  style="Title.TLabel").pack(pady=60)
        ttk.Label(conteudo_frame,
                  text="Use o menu lateral para gerir clientes, produtos,\n"
                       "fornecedores, pedidos e encomendas.",
                  justify="center").pack()

    # ============================================================
    #  CLIENTES
    # ============================================================
    def menu_clientes():
        limpar_conteudo()
        ttk.Label(conteudo_frame, text="Gestão de Clientes", style="Title.TLabel").pack(pady=10)

        nome = ttk.Entry(conteudo_frame, width=35)
        senha = ttk.Entry(conteudo_frame, width=35, show="*")
        id_cliente = ttk.Entry(conteudo_frame, width=35)

        for label, entry in [("Nome:", nome), ("Senha:", senha), ("NIF:", id_cliente)]:
            ttk.Label(conteudo_frame, text=label).pack()
            entry.pack(pady=4)

        def adicionar():
            try:
                if not validar_nif(id_cliente.get()):
                    return messagebox.showerror("Erro", "NIF inválido (9 dígitos).")

                if not validar_nome(nome.get()):
                    return messagebox.showerror("Erro", "Nome inválido (mínimo 3 letras).")

                if len(senha.get()) < 4:
                    return messagebox.showerror("Erro", "Senha muito curta (mínimo 4 caracteres).")

                DB.adicionar_cliente(id_cliente.get(), nome.get(), senha.get())
                messagebox.showinfo("Sucesso", f"Cliente '{nome.get()}' adicionado!")

            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao adicionar cliente:\n{e}")

        def remover():
            try:
                if not validar_nif(id_cliente.get()):
                    return messagebox.showerror("Erro", "NIF inválido.")

                DB.remover_cliente(id_cliente.get())
                messagebox.showinfo("Sucesso", "Cliente removido!")

            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao remover cliente:\n{e}")

        def atualizar():
            try:
                if not validar_nif(id_cliente.get()):
                    return messagebox.showerror("Erro", "NIF inválido.")

                if not validar_nome(nome.get()):
                    return messagebox.showerror("Erro", "Nome inválido.")

                DB.atualizar_cliente(id_cliente.get(), nome.get(), senha.get())
                messagebox.showinfo("Sucesso", "Cliente atualizado!")

            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao atualizar cliente:\n{e}")

        def listar():
            try:
                clientes = DB.listar_clientes()
                for c in clientes:
                    ttk.Label(conteudo_frame,
                              text=f"NIF: {c[0]} | Nome: {c[1]} | Senha: {c[2]}").pack()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao listar clientes:\n{e}")

        def procurar():
            try:
                if not validar_nome(nome.get()):
                    return messagebox.showerror("Erro", "Nome inválido para pesquisa.")

                clientes = DB.procurar_cliente(nome.get())

                if not clientes:
                    return messagebox.showwarning("Aviso", "Nenhum cliente encontrado.")

                for c in clientes:
                    ttk.Label(conteudo_frame,
                              text=f"NIF: {c[0]} | Nome: {c[1]} | Senha: {c[2]}").pack()

            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao procurar cliente:\n{e}")

        for txt, cmd in [("Adicionar", adicionar), ("Remover", remover),
                         ("Atualizar", atualizar), ("Listar", listar),
                         ("Procurar", procurar)]:
            ttk.Button(conteudo_frame, text=txt, command=cmd).pack(pady=4)

    # ============================================================
    #  PRODUTOS
    # ============================================================
    def menu_produtos():
        limpar_conteudo()
        ttk.Label(conteudo_frame, text="Gestão de Produtos", style="Title.TLabel").pack(pady=10)

        nome = ttk.Entry(conteudo_frame, width=35)
        preco = ttk.Entry(conteudo_frame, width=35)
        categoria = ttk.Entry(conteudo_frame, width=35)
        id_prod = ttk.Entry(conteudo_frame, width=35)

        for label, entry in [("Nome:", nome), ("Preço:", preco),
                             ("Categoria:", categoria), ("ID:", id_prod)]:
            ttk.Label(conteudo_frame, text=label).pack()
            entry.pack(pady=4)

        def adicionar():
            try:
                if not validar_nome(nome.get()):
                    return messagebox.showerror("Erro", "Nome inválido.")

                if not validar_preco(preco.get()):
                    return messagebox.showerror("Erro", "Preço inválido. Ex: 12.50")

                DB.adicionar_produto(nome.get(), preco.get(), categoria.get())
                messagebox.showinfo("Sucesso", "Produto adicionado!")

            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao adicionar produto:\n{e}")

        def remover():
            try:
                if not validar_id(id_prod.get()):
                    return messagebox.showerror("Erro", "ID inválido.")

                DB.remover_produto(id_prod.get())
                messagebox.showinfo("Sucesso", "Produto removido!")

            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao remover produto:\n{e}")

        def atualizar():
            try:
                if not validar_id(id_prod.get()):
                    return messagebox.showerror("Erro", "ID inválido.")

                if not validar_nome(nome.get()):
                    return messagebox.showerror("Erro", "Nome inválido.")

                if not validar_preco(preco.get()):
                    return messagebox.showerror("Erro", "Preço inválido.")

                DB.atualizar_produto(id_prod.get(), nome.get(), preco.get(), categoria.get())
                messagebox.showinfo("Sucesso", "Produto atualizado!")

            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao atualizar produto:\n{e}")

        def listar():
            try:
                produtos = DB.listar_produtos()
                for p in produtos:
                    ttk.Label(conteudo_frame,
                              text=f"ID: {p[0]} | Nome: {p[1]} | Preço: {p[2]} | Categoria: {p[3]}").pack()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao listar produtos:\n{e}")

        def procurar():
            try:
                if not validar_nome(nome.get()):
                    return messagebox.showerror("Erro", "Nome inválido para pesquisa.")

                produtos = DB.procurar_produto(nome.get())

                if not produtos:
                    return messagebox.showwarning("Aviso", "Nenhum produto encontrado.")

                for p in produtos:
                    ttk.Label(conteudo_frame,
                              text=f"ID: {p[0]} | Nome: {p[1]} | Preço: {p[2]} | Categoria: {p[3]}").pack()

            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao procurar produto:\n{e}")

        for txt, cmd in [("Adicionar", adicionar), ("Remover", remover),
                         ("Atualizar", atualizar), ("Listar", listar),
                         ("Procurar", procurar)]:
            ttk.Button(conteudo_frame, text=txt, command=cmd).pack(pady=4)

    # ============================================================
    #  FORNECEDORES
    # ============================================================
    def menu_fornecedores():
        limpar_conteudo()
        ttk.Label(conteudo_frame, text="Gestão de Fornecedores", style="Title.TLabel").pack(pady=10)

        nome = ttk.Entry(conteudo_frame, width=35)
        contato = ttk.Entry(conteudo_frame, width=35)
        categoria = ttk.Entry(conteudo_frame, width=35)
        id_forn = ttk.Entry(conteudo_frame, width=35)

        for label, entry in [("Nome:", nome), ("Contato:", contato),
                             ("Categoria:", categoria), ("ID:", id_forn)]:
            ttk.Label(conteudo_frame, text=label).pack()
            entry.pack(pady=4)

        def adicionar():
            try:
                if not validar_nome(nome.get()):
                    return messagebox.showerror("Erro", "Nome inválido.")

                DB.adicionar_fornecedor(nome.get(), contato.get(), categoria.get())
                messagebox.showinfo("Sucesso", "Fornecedor adicionado!")

            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao adicionar fornecedor:\n{e}")

        def remover():
            try:
                if not validar_id(id_forn.get()):
                    return messagebox.showerror("Erro", "ID inválido.")

                DB.remover_fornecedor(id_forn.get())
                messagebox.showinfo("Sucesso", "Fornecedor removido!")

            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao remover fornecedor:\n{e}")

        def atualizar():
            try:
                if not validar_id(id_forn.get()):
                    return messagebox.showerror("Erro", "ID inválido.")

                if not validar_nome(nome.get()):
                    return messagebox.showerror("Erro", "Nome inválido.")

                DB.atualizar_fornecedor(id_forn.get(), nome.get(), contato.get(), categoria.get())
                messagebox.showinfo("Sucesso", "Fornecedor atualizado!")

            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao atualizar fornecedor:\n{e}")

        def listar():
            try:
                fornecedores = DB.listar_fornecedores()
                for f in fornecedores:
                    ttk.Label(conteudo_frame,
                              text=f"ID: {f[0]} | Nome: {f[1]} | Contato: {f[2]} | Categoria: {f[3]}").pack()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao listar fornecedores:\n{e}")

        def procurar():
            try:
                if not validar_nome(nome.get()):
                    return messagebox.showerror("Erro", "Nome inválido para pesquisa.")

                fornecedores = DB.procurar_fornecedor(nome.get())

                if not fornecedores:
                    return messagebox.showwarning("Aviso", "Nenhum fornecedor encontrado.")

                for f in fornecedores:
                    ttk.Label(conteudo_frame,
                              text=f"ID: {f[0]} | Nome: {f[1]} | Contato: {f[2]} | Categoria: {f[3]}").pack()

            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao procurar fornecedor:\n{e}")

        for txt, cmd in [("Adicionar", adicionar), ("Remover", remover),
                         ("Atualizar", atualizar), ("Listar", listar),
                         ("Procurar", procurar)]:
            ttk.Button(conteudo_frame, text=txt, command=cmd).pack(pady=4)

    # ============================================================
    #  PEDIDOS
    # ============================================================
    def menu_pedidos():
        limpar_conteudo()
        ttk.Label(conteudo_frame, text="Gestão de Pedidos", style="Title.TLabel").pack(pady=10)

        cli_id = ttk.Entry(conteudo_frame, width=35)
        prod_id = ttk.Entry(conteudo_frame, width=35)
        valor = ttk.Entry(conteudo_frame, width=35)
        qtd = ttk.Entry(conteudo_frame, width=35)

        for label, entry in [("Cliente ID:", cli_id), ("Produto ID:", prod_id),
                             ("Valor:", valor), ("Quantidade:", qtd)]:
            ttk.Label(conteudo_frame, text=label).pack()
            entry.pack(pady=4)

        def adicionar():
            try:
                if not validar_id(cli_id.get()):
                    return messagebox.showerror("Erro", "Cliente ID inválido.")

                if not validar_id(prod_id.get()):
                    return messagebox.showerror("Erro", "Produto ID inválido.")

                if not validar_preco(valor.get()):
                    return messagebox.showerror("Erro", "Valor inválido.")

                if not validar_id(qtd.get()):
                    return messagebox.showerror("Erro", "Quantidade inválida.")

                DB.adicionar_pedido(cli_id.get(), prod_id.get(), valor.get(), qtd.get())
                messagebox.showinfo("Sucesso", "Pedido adicionado!")

            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao adicionar pedido:\n{e}")

        def remover():
            try:
                if not validar_id(cli_id.get()) or not validar_id(prod_id.get()):
                    return messagebox.showerror("Erro", "IDs inválidos.")

                DB.remover_pedido(cli_id.get(), prod_id.get())
                messagebox.showinfo("Sucesso", "Pedido removido!")

            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao remover pedido:\n{e}")

        def listar():
            try:
                pedidos = DB.listar_pedidos()
                for p in pedidos:
                    ttk.Label(conteudo_frame,
                              text=f"cliente_id: {p[0]} | Nome: {p[1]} | produto_id: {p[2]} | "
                                   f"Produto_nome: {p[3]} | valor: {p[4]} | quantidade: {p[5]} | data: {p[6]}").pack()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao listar pedidos:\n{e}")

        for txt, cmd in [("Adicionar", adicionar), ("Listar", listar), ("Remover", remover)]:
            ttk.Button(conteudo_frame, text=txt, command=cmd).pack(pady=4)

    # ============================================================
    #  ENCOMENDAS
    # ============================================================
    def menu_encomendas():
        limpar_conteudo()
        ttk.Label(conteudo_frame, text="Gestão de Encomendas", style="Title.TLabel").pack(pady=10)

        forn_id = ttk.Entry(conteudo_frame, width=35)
        prod_id = ttk.Entry(conteudo_frame, width=35)
        valor = ttk.Entry(conteudo_frame, width=35)
        id_enc = ttk.Entry(conteudo_frame, width=35)

        for label, entry in [("Fornecedor ID:", forn_id), ("Produto ID:", prod_id),
                             ("Valor:", valor), ("ID Encomenda:", id_enc)]:
            ttk.Label(conteudo_frame, text=label).pack()
            entry.pack(pady=4)

        def adicionar():
            try:
                if not validar_id(forn_id.get()):
                    return messagebox.showerror("Erro", "Fornecedor ID inválido.")

                if not validar_id(prod_id.get()):
                    return messagebox.showerror("Erro", "Produto ID inválido.")

                if not validar_preco(valor.get()):
                    return messagebox.showerror("Erro", "Valor inválido.")

                DB.adicionar_encomenda(forn_id.get(), prod_id.get(), valor.get())
                messagebox.showinfo("Sucesso", "Encomenda adicionada!")

            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao adicionar encomenda:\n{e}")

        def remover():
            try:
                if not validar_id(id_enc.get()):
                    return messagebox.showerror("Erro", "ID da encomenda inválido.")

                DB.remover_encomenda(id_enc.get())
                messagebox.showinfo("Sucesso", "Encomenda removida!")

            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao remover encomenda:\n{e}")

        def listar():
            try:
                encomendas = DB.listar_encomendas()
                for q in encomendas:
                    ttk.Label(conteudo_frame,
                              text=f"E_ID: {q[0]} | F_Nome: {q[1]} | Produto_nome: {q[2]} | "
                                   f"E_Valor: {q[3]} | Data: {q[4]} | Forn_id: {q[5]} | Prod_id: {q[6]}").pack()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao listar encomendas:\n{e}")

                for txt, cmd in [("Adicionar", adicionar), ("Remover", remover), ("Listar", listar)]:
                    ttk.Button(conteudo_frame, text=txt, command=cmd).pack(pady=4)

    def add_button(text, command):
        return Button(sidebar, text=text, command=command,
                      bg="#333333", fg="white", activebackground="#555555",
                      font=("Arial", 12), width=18, height=2, bd=0)

    add_button("Início", mostrar_inicio).pack(pady=5)
    add_button("Clientes", menu_clientes).pack(pady=5)
    add_button("Fornecedores", menu_fornecedores).pack(pady=5)
    add_button("Produtos", menu_produtos).pack(pady=5)
    add_button("Pedidos", menu_pedidos).pack(pady=5)
    add_button("Encomendas", menu_encomendas).pack(pady=5)
    add_button("Sair", jn.quit).pack(pady=40)

    mostrar_inicio()
    jn.mainloop()

if __name__ == "__main__":
    Supermat()
