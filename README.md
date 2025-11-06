Projeto: Gestor de Dívida Pessoal (Desktop App)

<img width="1914" height="1027" alt="AppModoClaro" src="https://github.com/user-attachments/assets/b17e5612-aed4-4e83-812f-4d9704f6ebb2" />
<img width="1913" height="1027" alt="AppModoEscuro" src="https://github.com/user-attachments/assets/f4dcc075-07d2-4265-9e40-be63074a38b6" />

1. Resumo do Projeto

Este é um projeto de estudo pessoal desenvolvido com o objetivo de aplicar e aprofundar meus conhecimentos em Python e desenvolvimento de interfaces gráficas (GUI). A aplicação substitui o acompanhamento manual de um empréstimo (feito anteriormente em uma planilha) por uma solução de desktop completa, funcional e interativa.

O projeto foi construído de forma incremental, começando com uma lógica simples e evoluindo para uma aplicação robusta com funcionalidades avançadas, como visualização de dados e empacotamento para distribuição.

2. Funcionalidades Principais

Interface Gráfica Moderna: UI limpa e amigável construída com a biblioteca CustomTkinter.

Gestão de Pagamentos (CRUD): O usuário pode Criar, Ler, Atualizar e Deletar lançamentos de pagamento.

Cálculos Dinâmicos: A aplicação recalcula automaticamente o total pago, o valor restante e o saldo devedor acumulado a cada alteração.

Persistência de Dados: Todos os dados são salvos localmente em um arquivo JSON, garantindo que as informações não se percam ao fechar o app.

Visualização de Dados: Um gráfico de pizza dinâmico (usando Matplotlib) é atualizado em tempo real, mostrando a porcentagem da dívida já paga vs. o valor restante.

Exportação de Relatórios: Funcionalidade para exportar o histórico completo de pagamentos para um arquivo .CSV, que pode ser aberto no Excel ou Google Sheets.

Recursos Avançados de UI:

Seletor de Tema: Botão para alternar instantaneamente entre os modos "Light" (Claro) e "Dark" (Escuro).

Efeitos de Hover: Feedback visual interativo na lista de histórico de pagamentos.

Atalhos de Teclado: A tecla "Enter" pode ser usada para submeter formulários.

Distribuição: O projeto foi empacotado em um executável (.exe) usando PyInstaller, incluindo uma Splash Screen profissional durante o carregamento.

3. Tecnologias Utilizadas

Linguagem Principal: Python 3

Interface Gráfica (GUI): CustomTkinter

Visualização de Dados: Matplotlib

Manipulação de Dados: JSON (para persistência), CSV (para exportação)

Bibliotecas Nativas: subprocess, os, sys, tkinter (para messagebox, filedialog e after), uuid

Imagens: PIL (Pillow) (para a splash screen)

Empacotamento: PyInstaller (através do auto-py-to-exe)

4. Desafios e Aprendizados

Este projeto foi uma jornada de aprendizado intensiva em depuração e integração de bibliotecas.

Desafio: Integrar o gráfico do Matplotlib com a interface do CustomTkinter, especialmente garantindo que o fundo do gráfico mudasse junto com o tema (Claro/Escuro).

Solução: Desenvolvi uma lógica para destruir e recriar completamente o canvas do gráfico a cada troca de tema, garantindo uma atualização visual correta.

Desafio: Resolver um bug de "condição de corrida" (TclError) que ocorria ao trocar o tema, onde a interface tentava acessar um widget que estava sendo recriado.

Solução: Aprendi e implementei o método .after(10, ...) para agendar a recriação do gráfico, dando tempo para a troca de tema do CustomTkinter ser concluída primeiro.

Desafio: Fazer a comunicação entre os dois executáveis (Splash.exe e Divida_Mayara.exe) para que a splash screen fechasse no momento certo.

Solução: Implementei um sistema de sinalização baseado em arquivo (signal.tmp), onde o app principal cria um arquivo para "avisar" a splash screen que ela pode fechar.

Desafio: Garantir que o .exe final encontrasse todos os seus arquivos (ícone, JSON, imagem da splash) ao ser executado.

Solução: Criei uma função resource_path usando sys._MEIPASS para garantir que o programa sempre encontrasse seus "assets", tanto no ambiente de desenvolvimento quanto no executável empacotado.
