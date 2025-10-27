# 🤖 Bot de Agenda para Telegram

Este projeto é um chatbot para o Telegram que funciona como uma agenda pessoal. Desenvolvido em Python para a cadeira de Introdução à Programação, o bot permite que o usuário gerencie seus compromissos diretamente pelo chat, oferecendo funcionalidades para agendar, consultar, cancelar e até mesmo receber sugestões de horários disponíveis.

---

## ✨ Funcionalidades Principais

O bot foi desenvolvido para ser um assistente pessoal prático, respondendo aos seguintes comandos:

- **/agendar**: Adiciona um novo evento, verificando automaticamente se há conflitos de horário.
- **/consultar**: Lista todos os eventos agendados para uma data específica.
- **/cancelar**: Remove um evento da agenda.
- **/sugerir**: Analisa os horários vagos em um dia e sugere os melhores encaixes para um novo compromisso.

---

## 📁 Estrutura do Projeto

O repositório está organizado de forma simples e direta:

📂 telegram-agenda
│
├── 🐍 bot_agenda.py      # Script principal com toda a lógica do bot
├── 📄 README.md          # Este arquivo

---

## 💬 Exemplos de Uso

A interação com o bot é feita através de comandos simples e diretos no chat do Telegram:

1.  **Para agendar um evento de 1h às 15:00 do dia 05/07/2025:**
    - `> /agendar 05/07/2025 15:00 60`

2.  **Para ver todos os compromissos do dia 05/07/2025:**
    - `> /consultar 05/07/2025`

3.  **Para receber sugestões de horários para um evento de 45min no dia 05/07/2025:**
    - `> /sugerir 05/07/2025 45`

**Conclusão da Interação:** O bot responde a cada comando com uma mensagem de confirmação ou com a informação solicitada, tornando o gerenciamento da agenda rápido e eficiente.

---

## ▶️ Como Executar o Projeto

1.  **Clone o repositório em sua máquina local:**
    ```bash
    git clone [https://github.com/seu-usuario/telegram-agenda.git](https://github.com/seu-usuario/telegram-agenda.git)
    cd telegram-agenda
    ```
2.  **Instale a biblioteca necessária:**
    ```python
    pip install python-telegram-bot
    ```
3.  **Configure seu Token e execute o script:**
    - Abra o arquivo `bot_agenda.py` e insira o token do seu bot na linha `app = ApplicationBuilder().token("token aqui").build()`.
    - Execute o arquivo com `python bot_agenda.py`.

---

Desenvolvido com 🧠 por Miguel Antônio Barbosa Caetano  
📧 miguelantoniobsk@gmail.com | 💼 www.linkedin.com/in/miguel-antoniobc
