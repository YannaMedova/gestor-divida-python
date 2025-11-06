<!-- Imagem de Banner -->

<p align="center">
</p>

<!-- Título e Badges -->

<h1 align="center">Gestor de Dívida Pessoal (Desktop App)</h1>

<p align="center">
<img alt="Status do Projeto" src="https://www.google.com/search?q=https://img.shields.io/badge/status-conclu%C3%ADdo-brightgreen">
<img alt="Linguagem" src="https://www.google.com/search?q=https://img.shields.io/badge/Python-3.x-blue">
<img alt="UI" src="https://www.google.com/search?q=https://img.shields.io/badge/UI-CustomTkinter-blueviolet">
<img alt="Gráficos" src="https://www.google.com/search?q=https://img.shields.io/badge/Gr%C3%A1ficos-Matplotlib-orange">
<img alt="Licença" src="https://www.google.com/search?q=https://img.shields.io/badge/Licen%C3%A7a-MIT-informational">
</p>

<!-- Índice -->

<p align="center">
<a href="#-sobre-o-projeto">Sobre o Projeto</a> •
<a href="#-funcionalidades-principais">Funcionalidades</a> •
<a href="#-tecnologias-utilizadas">Tecnologias</a> •
<a href="#-screenshots">Screenshots</a> •
<a href="#-lições-e-próximos-passos">Aprendizados</a> •
<a href="#-licença">Licença</a>
</p>

🚀 Sobre o Projeto

Este é um projeto de estudo pessoal desenvolvido com o objetivo de aplicar e aprofundar meus conhecimentos em Python e desenvolvimento de interfaces gráficas (GUI). A aplicação substitui o acompanhamento manual de um empréstimo (feito anteriormente em uma planilha) por uma solução de desktop completa, funcional e interativa.

O projeto foi construído de forma incremental, começando com uma lógica simples e evoluindo para uma aplicação robusta com funcionalidades avançadas, como visualização de dados e empacotamento para distribuição.

✨ Funcionalidades Principais

Interface Gráfica Moderna: UI limpa e amigável construída com a biblioteca CustomTkinter.

Gestão de Pagamentos (CRUD): O usuário pode Criar, Ler, Atualizar e Deletar lançamentos de pagamento.

Cálculos Dinâmicos: A aplicação recalcula automaticamente o total pago, o valor restante e o saldo devedor acumulado a cada alteração.

Persistência de Dados: Todos os dados são salvos localmente em um arquivo JSON.

Visualização de Dados: Um gráfico de pizza dinâmico (usando Matplotlib) é atualizado em tempo real.

Exportação de Relatórios: Funcionalidade para exportar o histórico completo para um arquivo .CSV.

Recursos Avançados de UI:

Seletor de Tema (Light/Dark).

Efeitos de Hover interativos na lista.

Atalhos de Teclado (uso da tecla "Enter").

Distribuição: O projeto foi empacotado em um executável (.exe) usando PyInstaller, incluindo uma Splash Screen profissional durante o carregamento.

🛠️ Tecnologias Utilizadas

Abaixo estão as principais tecnologias e bibliotecas usadas neste projeto:

Linguagem Principal: Python 3

Interface Gráfica (GUI): CustomTkinter

Visualização de Dados: Matplotlib

Manipulação de Dados: JSON (para persistência), CSV (para exportação)

Bibliotecas Nativas: subprocess, os, sys, tkinter, uuid

Imagens: PIL (Pillow)

Empacotamento: PyInstaller

📸 Screenshots

Modo Claro
<img width="1914" height="1027" alt="AppModoClaro" src="https://github.com/user-attachments/assets/b17e5612-aed4-4e83-812f-4d9704f6ebb2" />

Modo Escuro
<img width="1913" height="1027" alt="AppModoEscuro" src="https://github.com/user-attachments/assets/f4dcc075-07d2-4265-9e40-be63074a38b6" />


🧠 Lições e Próximos Passos

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
