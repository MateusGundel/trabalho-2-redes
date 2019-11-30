# Trabalho de REDES

Desenvolver uma aplicação cliente servidor utilizando sockets (TCP e UDP) em linguagem a sua escolha que deverá 
realizar as seguintes tarefas:

- a. Manter um backup remoto atualizado e sincronizado entre cliente e servidor de todos os arquivos que forem criados, 
alterados ou excluídos em uma pasta especificada.

- b. Sempre que ocorrem alterações destes arquivos, devera ser enviado
um e-mail (utilizando o protocolo POP/SMTP/ IMAP) e notificação ao
administrador, informando o nome do arquivo e a data e hora da
modificação. Esta tarefa pode ser acumulativa e programada.

- c. Deverá ser implementado um sistema de monitoramento utilizando
um sistema de Ping com socket UDP/ICMP.
O sistema devera informar ao administrador, via e-mail, caso ocorra
alguma indisponibilidade do sistema.

- Extra I:
Cadastro de múltiplos clientes para sincronizar os dados com o
servidor. Cada cliente devera ter sua própria pasta de sincronismo.
- Extra II:
Implementar o sistema através de webserver.
- Extra III:
Implementar paralelamente um sistema de chat entre cliente e
administrador. Este sistema não substitui o sistema de notificação
por e-mail.