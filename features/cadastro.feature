# language: pt

Funcionalidade: Cadastro de contas

  Cenário: TC_01 - Criar Conta
    Dado que o usuário está na tela de cadastro
    Quando informar nome, e-mail, senha e confirmação de senha válidos
    E clicar em "Cadastrar"
    Então a conta deverá ser criada com sucesso

  Cenário: TC_03 - Criar Conta com Saldo Inicial
    Dado que o usuário está na tela de cadastro
    Quando informar nome, e-mail, senha e confirmação de senha válidos
    E selecionar a opção "Criar conta com saldo"
    E clicar em "Cadastrar"
    Então a conta deverá ser criada com sucesso
    E a conta deverá possuir saldo inicial disponível

  Cenário: TC_04 - Validar Campos Obrigatórios do Cadastro
    Dado que o usuário está na tela de cadastro
    Quando deixar os campos obrigatórios em branco
    E clicar em "Cadastrar"
    Então mensagens de validação deverão ser apresentadas
    E a conta não deverá ser criada

  Cenário: TC_05 - Cadastrar Conta com E-mail Já Utilizado
    Dado que existe uma conta cadastrada com determinado e-mail
    Quando o usuário tentar criar uma nova conta utilizando o mesmo e-mail
    E preencher os demais campos obrigatórios corretamente
    Então o sistema deverá exibir uma mensagem de erro
    E a conta não deverá ser criada

  Cenário: TC_06 - Cadastrar Conta com Confirmação de Senha Divergente
    Dado que o usuário está na tela de cadastro
    Quando informar uma senha válida
    E informar uma confirmação de senha diferente
    E clicar em "Cadastrar"
    Então o sistema deverá exibir uma mensagem de erro
    E a conta não deverá ser criada
