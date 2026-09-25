# language: pt

Funcionalidade: Autenticação

  @regression
  Cenário: TC_02 - Acessar a Conta
    Dado que existe uma conta cadastrada
    Quando o usuário informar um e-mail válido
    E informar uma senha válida
    E clicar em "Acessar"
    Então o usuário deverá ser autenticado com sucesso

  @regression
  Cenário: TC_07 - Realizar Login com Senha Inválida
    Dado que existe uma conta cadastrada
    Quando o usuário informar um e-mail válido
    E informar uma senha inválida
    E clicar em "Acessar"
    Então o sistema deverá exibir uma mensagem de autenticação inválida
    E o usuário não deverá ser autenticado

  @regression
  Cenário: TC_08 - Realizar Logout da Aplicação
    Dado que o usuário está autenticado
    Quando clicar na opção de logout
    Então a sessão deverá ser encerrada
    E o usuário deverá ser redirecionado para a tela de login
