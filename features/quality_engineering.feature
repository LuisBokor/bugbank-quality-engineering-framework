# language: pt

Funcionalidade: Quality Engineering - Avaliação de Qualidade

  Cenário: TC_13 - Financial Reconciliation Assessment
    Dado que a conta A está autenticada com saldo inicial
    E a conta B possui saldo inicial
    E a conta C não possui saldo inicial
    Quando a conta A transferir 300 reais para a conta B
    Então a transferência da conta A deverá ser concluída com sucesso
    Quando a conta B transferir 100 reais para a conta C
    Então a transferência da conta B deverá ser concluída com sucesso
    Então o saldo final da conta A deverá ser o inicial menos 300
    E o extrato da conta A deverá conter um único débito de 300
    E o saldo final da conta B deverá ser o inicial mais 300 menos 100
    E o extrato da conta B deverá conter exatamente um crédito de 300 e um débito de 100
    E o saldo final da conta C deverá ser 100
    E o extrato da conta C deverá conter um único crédito de 100
    E o total financeiro do sistema deverá estar reconciliado

  Cenário: TC_14 - Session Integrity Assessment
    Dado que o usuário está autenticado
    Quando clicar na opção de logout
    Então a sessão deverá ser encerrada
    E o usuário deverá ser redirecionado para a tela de login
    Quando pressionar o botão voltar do navegador
    Então o acesso à área protegida deverá ser bloqueado
    Quando atualizar a página
    Então o acesso à área protegida deverá permanecer bloqueado
    Quando tentar acessar diretamente a URL da área logada
    Então o acesso à área protegida deverá ser bloqueado
    E a sessão deverá permanecer encerrada

  Cenário: TC_15 - Concurrent Transaction Assessment
    Dado que o usuário remetente está autenticado com saldo inicial suficiente
    E existe uma conta receptora válida
    Quando preencher uma transferência válida de 50 reais
    E acionar a confirmação da transferência 5 vezes em rápida sucessão
    Então o saldo do remetente deverá ter sido debitado exatamente uma vez
    E o extrato do remetente deverá conter um único débito da operação
    E o saldo do receptor deverá ter sido creditado exatamente uma vez
    E o extrato do receptor deverá conter um único crédito da operação
    E não deverá existir operação financeira duplicada

  Cenário: TC_16 - Data Persistence Assessment
    Dado que o usuário A está autenticado com saldo inicial
    E existe uma conta destinatária válida para transferência
    Quando o usuário A realizar uma transferência de valor válido
    Então a transferência deverá ser concluída com sucesso
    E o saldo do usuário A deverá ser atualizado com o débito
    Quando registrar o extrato da conta
    E realizar logout da conta
    E o usuário A realizar login novamente
    Então o saldo anterior deverá estar preservado
    E as movimentações do extrato deverão estar preservadas
