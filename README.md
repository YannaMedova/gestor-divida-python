<h1 align="center">💰 Gestor de Dívida Pessoal (Desktop App)</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Status-Concluído-brightgreen" alt="Status">
  <img src="https://img.shields.io/badge/Python-3.x-blue" alt="Python">
  <img src="https://img.shields.io/badge/GUI-CustomTkinter-blueviolet" alt="CustomTkinter">
  <img src="https://img.shields.io/badge/Gráficos-Matplotlib-orange" alt="Matplotlib">
</p>

---

## 📌 Sobre o Projeto

Este é um projeto de estudo pessoal desenvolvido com o objetivo de substituir um acompanhamento manual de pagamentos (antes feito em planilha) por uma aplicação desktop **mais organizada, automatizada e intuitiva**.

O app permite cadastrar pagamentos, calcular saldo devedor automaticamente e visualizar o progresso em gráficos, tudo em uma interface moderna e funcional.

---

## ✨ Funcionalidades Principais

| Funcionalidade | Descrição |
|---|---|
| 🖥 Interface Gráfica Moderna | Construída com **CustomTkinter** (Light/Dark Mode). |
| 📄 CRUD Completo | Criar, visualizar, editar e remover pagamentos. |
| 🔢 Cálculos Automáticos | Atualiza total pago, saldo e restante devido. |
| 💾 Persistência de Dados | Armazenamento local em **JSON**. |
| 📊 Visualização | Gráfico dinâmico atualizado em tempo real (Matplotlib). |
| 📤 Exportação | Exporta histórico de pagamentos em **CSV**. |
| 🚀 Empacotado em Executável | Gerado via **PyInstaller**, com **splash screen** personalizada. |

---

## 🛠 Tecnologias Utilizadas

| Área | Ferramentas |
|---|---|
| Linguagem | Python 3 |
| Interface | CustomTkinter |
| Visualização | Matplotlib |
| Dados | JSON (persistência), CSV (exportação) |
| Imagens | Pillow (PIL) |
| Empacotamento | PyInstaller |

---

## 🖼 Screenshots

### 🌞 Modo Claro
![Modo Claro](https://github.com/user-attachments/assets/b17e5612-aed4-4e83-812f-4d9704f6ebb2)

### 🌙 Modo Escuro
![Modo Escuro](https://github.com/user-attachments/assets/f4dcc075-07d2-4265-9e40-be63074a38b6)

---

## 🧠 Lições e Aprendizados

- Aprendi a integrar **CustomTkinter + Matplotlib** mantendo responsividade e atualização visual.
- Resolvi erros de **condição de corrida** durante troca de temas, usando `widget.after()`.
- Usei gestão de recursos com `sys._MEIPASS` para garantir paths corretos no executável.
- Desenvolvi lógica de **comunicação entre processos** para controlar a splash screen.

---

## 🔮 Próximos Passos

- Adicionar **observações opcionais por pagamento**.
- Permitir edição da dívida inicial diretamente pela interface.
- Criar **instalador .msi** para distribuição simplificada.

---

## 👩‍💻 Autor

**Yanna Medova**  
Brasília / DF  
Estudante de Defesa Cibernética (3º Semestre)  
LinkedIn: *adicione aqui quando quiser*

---
