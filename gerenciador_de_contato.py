from copy import copy
import re
from typing import TypedDict

class Contato(TypedDict):
    nome: str
    telefone: str
    email: str
    favorito: bool

def gerenciar_contatos():
    contatos: list[Contato] = []

    while True:
        imprimir_opcoes()
        opcao: int = ler_opcao()

        if opcao == 7:
            break

        executar_opcao(opcao, contatos)


def imprimir_opcoes():
    print("\nGerenciador de contatos:\n"
          "1) Listar os contatos\n"
          "2) Listar os contatos favoritos\n"
          "3) Adicionar um novo contato\n"
          "4) Editar um contato\n"
          "5) Favoritar um contato\n"
          "6) Apagar um contato\n"
          "7) Sair")


def executar_opcao(opcao: int, contatos: list[Contato]):
    match opcao:
        case 1:
            listar_contatos(contatos)
        case 2:
            listar_contatos(contatos, True)
        case 3:
            adicionar_contato(contatos)
        case 4:
            editar_contato(contatos)
        case 5:
            favoritar_contato(contatos)
        case 6:
            apagar_contato(contatos)


def ler_opcao() -> int:
    while True:
        opcao_str: str = input("\nDigite a opção que deseja: ")
        if not opcao_str.isdigit() or int(opcao_str) < 0 or int(opcao_str) > 7:
            print("A opção deve ser um número entre 1 e 7.")
        else:
            return int(opcao_str)


def listar_contatos(contatos: list[Contato], filtrar_favorito: bool = False):
    if nao_ha_contatos(contatos, filtrar_favorito):
        return

    mensagem_adicional: str = " favoritos" if filtrar_favorito else ""
    print(f"\nLista de contatos{mensagem_adicional}:")

    indice: int = 1
    for contato in contatos:
        if filtrar_favorito and not contato["favorito"]:
            continue
        imprimir_contato(contato, indice)
        indice += 1


def imprimir_contato(contato: Contato, indice: int):
    print(f"\n{indice}. {contato["nome"]}\n"
          f"Telefone: {contato["telefone"]}\n"
          f"Email: {contato["email"]}\n"
          f"Favorito: {"Sim" if contato["favorito"] else "Não"}\n")


def adicionar_contato(contatos: list[Contato]):

    def imprimir_erro():
        print("\nCadastro falhou. Tente novamente.")

    nome: str = input("\nDigite o nome: ")
    if not validar_nome(nome):
        imprimir_erro()
        return

    telefone: str =  input("\nDigite o telefone: ")
    if not validar_telefone(telefone):
        imprimir_erro()
        return

    email: str = input("\nDigite o email: ")
    if not validar_email(email):
        imprimir_erro()
        return

    novo_contato: Contato = {
        "nome": nome,
        "telefone": telefone,
        "email": email,
        "favorito": False
    }

    contatos.append(novo_contato)
    print(f"\nContato do {novo_contato["nome"]} cadastrado com sucesso.")


def editar_contato(contatos: list[Contato]):
    if nao_ha_contatos(contatos):
        return

    listar_contatos(contatos)
    
    indice: int | None = ler_indice("Digite o contato que queira editar: ")
    if indice is None:
        return
    
    if nao_ha_contatos(contatos) or not validar_indice(contatos, indice):
        return

    contato_existente: Contato = copy(contatos[indice - 1])

    valido: bool = True
    nome = input("\nDigite o nome (aperta enter caso não queira atualizar): ")
    telefone = input("\nDigite o telefone (aperta enter caso não queira atualizar): ")
    email = input("\nDigite o email (aperta enter caso não queira atualizar): ")

    if len(nome.strip()) > 0 and validar_nome(nome):
        contato_existente["nome"] = nome
    else:
        valido = len(nome.strip()) == 0

    if valido and len(telefone.strip()) > 0 and validar_telefone(telefone):
        contato_existente["telefone"] = telefone
    else:
        valido = len(telefone.strip()) == 0

    if valido and len(email.strip()) > 0 and validar_email(email):
        contato_existente["email"] = email
    else:
        valido = len(email.strip()) == 0

    if valido:
        contatos[indice - 1] = contato_existente
        nome_mensagem: str = contato_existente["nome"]
        print(f"\nContato {nome_mensagem} atualizado com sucesso.\nResultado:")
        imprimir_contato(contato_existente, indice)


def favoritar_contato(contatos: list[Contato]):
    if nao_ha_contatos(contatos):
        return

    listar_contatos(contatos)

    indice: int | None = ler_indice("Digite o contato que queira favoritar: ")
    if indice is None:
        return

    if nao_ha_contatos(contatos) or not validar_indice(contatos, indice):
        return

    contatos[indice - 1]["favorito"] = True
    nome_mensagem: str = contatos[indice - 1]["nome"]
    print(f"\nContato {nome_mensagem} favoritado com sucesso.")


def apagar_contato(contatos: list[Contato]):
    if nao_ha_contatos(contatos):
        return

    listar_contatos(contatos)

    indice: int | None = ler_indice("Digite o contato que queira apagar: ")
    if indice is None:
        return
    
    if nao_ha_contatos(contatos) or not validar_indice(contatos, indice):
        return

    nome_mensagem: str = contatos.pop(indice - 1)["nome"]
    print(f"\nContato {nome_mensagem} apagado com sucesso.")


def validar_contato(contato: Contato) -> bool:
    nome_valido: bool = validar_nome(contato["nome"])
    telefone_valido: bool = validar_telefone(contato["telefone"])
    email_valido = validar_email(contato["email"])

    return nome_valido and telefone_valido and email_valido


def validar_nome(nome: str) -> bool:
    if re.match(r"^[A-Za-z\s]+$", nome) is None:
        print("\nNome não pode ser vazio e deve ter letras.")
        return False

    return True


def validar_telefone(telefone: str) -> bool:
    if re.match(r"^(\([0-9]{2}\))?\s?([0-9]{4,5})[-]?([0-9]{4})$", telefone) is None:
        print("\nTelefone deve estar no seguinte formato: (62) 99999-9999.")
        return False

    return True


def validar_email(email: str) -> bool:
    if re.match(r"^\S+@\S+\.\S+$", email) is None:
        print("\nEmail deve estar no seguinte formato: exemplo@gmail.com.")
        return False

    return True


def validar_indice(contatos: list[Contato], indice: int) -> bool:
    tamanho: int = len(contatos)
    if indice <= 0 or indice > tamanho:
        print(f"Indíce inválido. Tem {tamanho} contatos.")
        return False

    return True


def nao_ha_contatos(contatos: list[Contato], filtrar_favorito: bool = False) -> bool:
    if len(contatos) == 0:
        print("\nNão há contatos.")
        return True
    
    if filtrar_favorito and not any(c["favorito"] for c in contatos):
        print("\nNão há contatos favoritos.")
        return True
    
    return False


def ler_indice(mensagem: str) -> int | None:
    indice_str: str = input(f"\n{mensagem}")
    if not indice_str.isdigit():
        print("\nDeve ser somente número.")
        return None

    return int(indice_str)

gerenciar_contatos()