# Supermat — Gestão de Supermercado

Aplicação em Python (Tkinter + SQLite) para gerir clientes, fornecedores, produtos, pedidos e encomendas de um supermercado.

## Funcionalidades

- Login de clientes
- CRUD de clientes, fornecedores e produtos
- Pedidos de clientes e encomendas a fornecedores
- Validação dos dados antes de gravar (campos obrigatórios, valores numéricos)
- Chaves estrangeiras ativas no SQLite para manter a integridade dos dados

## Como executar

```bash
python criar_base_dados.py   # cria BDs/Supermat.db
python main.py
```

## Ficheiros

| Ficheiro | O que faz |
|---|---|
| `main.py` | Ponto de entrada |
| `interface.py` | Janelas e formulários em Tkinter |
| `base_dados.py` | Funções de acesso à base de dados |
| `criar_base_dados.py` | Cria as tabelas |
