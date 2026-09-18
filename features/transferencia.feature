# language: pt

Funcionalidade: Transferências

  Cenário: TC_10 - Realizar Transferência sem Saldo Suficiente
    Dado que o usuário está autenticado
    E possui saldo insuficiente para realizar uma transferência
    Quando informar uma conta destinatária válida
    E informar um valor superior ao saldo disponível
    E confirmar a transferência
    Então o sistema deverá exibir uma mensagem de saldo insuficiente
    E a transferência não deverá ser realizada
    E o saldo da conta deverá permanecer inalterado

  Cenário: TC_11 - Fluxo E2E de Cadastro, Login e Transferência entre Contas
    Dado que o usuário A está na tela de cadastro
    Quando criar uma conta com saldo inicial
    Então a conta deverá ser criada com sucesso
    Dado que o usuário B está na tela de cadastro
    Quando criar uma segunda conta válida
    Então a segunda conta deverá ser criada com sucesso
    Quando o usuário A realizar login
    E acessar a funcionalidade de transferência
    E informar os dados da conta do usuário B
    E informar um valor válido
    E confirmar a operação
    Então a transferência deverá ser realizada com sucesso
    E o saldo do usuário A deverá ser atualizado
