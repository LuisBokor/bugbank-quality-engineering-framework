# language: pt

Funcionalidade: Saldo, extrato e sessão

  Cenário: TC_09 - Consultar Saldo da Conta
    Dado que o usuário está autenticado
    Quando acessar a página inicial da conta
    Então o saldo disponível deverá ser exibido
    E o valor exibido deverá corresponder ao saldo da conta

  Cenário: TC_12 - Fluxo E2E Completo de Transferência, Extrato, Saldo e Logout
    Dado que existe uma transferência realizada entre o usuário A e o usuário B
    Quando o usuário A realizar login
    E acessar seu extrato
    Então deverá visualizar o registro da transferência enviada
    Quando consultar seu saldo
    Então o saldo deverá refletir o débito da transferência
    Quando realizar logout
    Então deverá retornar para a tela de login
    Quando o usuário B realizar login
    E acessar seu extrato
    Então deverá visualizar o recebimento da transferência
    Quando consultar seu saldo
    Então o saldo deverá refletir o crédito recebido
    Quando realizar logout
    Então deverá retornar para a tela de login
