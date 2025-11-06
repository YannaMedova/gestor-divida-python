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

Empacotamento: PyInstaller

4. Como Executar (Para Desenvolvedores)

Para executar o projeto localmente a partir do código-fonte, siga estes passos:

Clone o repositório:

git clone [https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git](https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git)
cd SEU-REPOSITORIO


Crie e ative um ambiente virtual:

# Windows
python -m venv venv
.\venv\Scripts\activate


Instale as dependências:

pip install -r requirements.txt


Execute a aplicação:
Para rodar o programa com a splash screen (como no executável):

python Splash.py


Para rodar o programa principal diretamente (para depuração rápida):

python Divida_Mayara.py


5. Lições Aprendidas e Próximos Passos

Esta seção substitui a antiga "Desafios e Aprendizados".

5.1 Lições Aprendidas

Este projeto foi uma jornada de aprendizado intensiva em depuração e integração de bibliotecas.

Integração de Bibliotecas: Integrar o Matplotlib com o CustomTkinter, especialmente para garantir que o fundo do gráfico mudasse junto com o tema, exigiu uma lógica de destruir e recriar o canvas do gráfico a cada troca.

Programação Concorrente (UI): Resolvi um bug de "condição de corrida" (TclError) que ocorria ao trocar o tema. Aprendi a usar o método .after(10, ...) para agendar a recriação do gráfico, dando tempo para a troca de tema ser concluída primeiro.

Comunicação entre Processos: Para a splash screen (Splash.exe) fechar no momento certo, implementei um sistema de sinalização baseado em arquivo (signal.tmp), onde o app principal (Divida_Mayara.exe) cria um arquivo para "avisar" a splash que ela pode fechar.

Empacotamento: Aprendi a usar a função resource_path (com sys._MEIPASS) para garantir que o .exe final sempre encontrasse seus arquivos "assets" (ícone, JSON, imagens), independentemente de onde fosse executado.

5.2 Próximos Passos

Como todo projeto, sempre há espaço para melhorias. Algumas ideias para o futuro incluem:

Campo de "Observação": Adicionar um campo de texto opcional para notas em cada pagamento.

Edição da Dívida Inicial: Permitir que o usuário altere o valor da dívida inicial através da própria interface.

Instalador: Criar um instalador .msi completo em vez de depender de um arquivo .zip com a pasta do programa.
