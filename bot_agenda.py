#09:25 05/04/2025 Miguel Antonio Barbosa Caetano
#Importando a biblioteca de datas
from datetime import datetime, timedelta
#Código inicial advindo do arquivo
from telegram import Update 
    #Lista de eventos já marcados
eventosAgendados = []
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes 
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE): 
    await update.message.reply_text("Olá! Eu sou seu assistente pessoal\nUse /agendar para agendar novos eventos fornecendo DD/MM/AA HH:MM e duração\n/consultar para ver eventos já agendados fornecendo no formato DD/MM/AA\n/cancelar para cancelar um evento fonecendo data no formato HH:MM\n/sugerir para receber sugestões de horários em uma data específica fornecendo DD/MM/AA e duração. ") 
async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE): 
    await update.message.reply_text("Olá, Mundo! ") 
#Função de agendar
async def agendar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #Data e hora virão em strings diferentes porém em um mesmo bloco 
    dia, mes, ano = context.args[0].split("/")
    hora, minutos = context.args[1].split(":")
    duracao = int(context.args[2])
    #Definindo início e fim do evento
    inicioEvento = datetime(int(ano), int(mes), int(dia), int(hora), int(minutos))
    fimEvento = inicioEvento + timedelta(minutes = duracao)
    for evento in eventosAgendados:
        #Verifica se existe conflito com outros eventos, olhando se o horário está dentro do intervalo de outro
        if inicioEvento < evento["final"] and fimEvento > evento["comeco"]:
            await update.message.reply_text("Há um evento agendado nesse horário. Use a função /sugerir para ver horários recomendados e disponíveis.")
            return
    #Adicionando o novo evento pós verificação
    eventosAgendados.append({'comeco': inicioEvento, 'final': fimEvento})
    await update.message.reply_text("Evento agendado com sucesso!")
async def consultar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #Criando flag e lista de eventos na data determinada, assim como coletando a data.
    flag = 0
    dia, mes, ano = context.args[0].split("/")
    eventosDia = []
    for evento in eventosAgendados:
        #Verificando se tem eventos agendados na data fornecida.
        if int(ano) == evento['comeco'].year and int(mes) == evento['comeco'].month and int(dia) == evento['comeco'].day:
            #Se sim flag levanta 
            flag = 1
            #Melhorando o formato dos eventos e adicionando eles à lista que será exibida
            inicio = evento['comeco'].strftime('%H:%M')
            fim = evento['final'].strftime('%H:%M')
            eventosDia.append(f"Inicio: {inicio} - Fim: {fim}") 
            eventosDia.sort()
    if flag == 0:
        #Caso não tenha eventos na data
        await update.message.reply_text("Não há eventos agendados nesta data utilize /agendar para agendar um novo evento!") 
        return
    else:
        #Caso tenha exibe eles para o usuário
        await update.message.reply_text(f"Há eventos agendados nos horários: {eventosDia}") 
async def cancelar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #Organizando o evento que deve ser cancelado da mesma forma que foi salvo os eventos com /agendar
    dia, mes, ano = context.args[0].split("/")
    hora, minutos = context.args[1].split(":")
    cancelar = datetime(int(ano), int(mes), int(dia), int(hora), int(minutos))
    #Variável que pega a posição do evento equivalente ao evento da entrada
    posicao = 0
    for evento in eventosAgendados:
        #Verificando se existe algum evento salvo cujo evento fornecido se encaixa no intervalo
        if cancelar <= evento['final'] and cancelar >= evento['comeco']:
            #Caso sim retiramos com .pop(posiçâo)
            eventosAgendados.pop(posicao)
            await update.message.reply_text("Evento retirado da agenda.")
            return
        else:
            #Caso não mandamos o usuário verififcar se a entrada de fato corresponde a algum evento naquela data
            await update.message.reply_text("Não há nenhum evento agendado no horário especificado. Use /consultar para acessar os eventos marcados em um data determinada!")
        posicao += 1
async def sugerir(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #Armazenando os dados recebidos normalmente
    dia, mes, ano = context.args[0].split("/")
    duracao = int(context.args[1])
    duracao_TD = timedelta(minutes = duracao)
    #Ordenando a lista de eventos para facilitar o serviço para facilitar 
    eventosAgendados.sort(key=lambda evento: evento['comeco'])
    #Criando lista que armazenará os intervalos
    intervalos = []
    #ultimoHorario é uma variável que vai servir para controlar o início do próximo intervalo se baseando no fim do último, por isso começa às 00:00
    ultimoHorario = datetime(int(ano), int(mes), int(dia), 00, 00)
    for evento in eventosAgendados:
        #Primeiro iremos procurar por eventos agendados na mesma data recebida, pois eles serão nossos obstáculos
        if evento['comeco'].date() == datetime(int(ano), int(mes), int(dia)).date():
            #Aqui é necessário ver se o intervalo gerado entre o fim do último obstáculo e o início do próximo é maior do quê a duração recebida, se não o intervalo não é válido para sugestão
            if evento['comeco'] - ultimoHorario >= duracao_TD:
                #Caso sim colocamos na lista de intervalos e atualizamos a variável ultimoHorario
                intervalos.append({'comeco': ultimoHorario, 'final': evento['comeco'] - duracao_TD})
                ultimoHorario = evento['final']
    #Aqui verificamos se há mais um intervalo válido entre o fim do último obstáculo e o fim do dia
    fimDia = datetime(int(ano), int(mes), int(dia), 23, 59)
    if (fimDia - ultimoHorario) >= duracao_TD:
        intervalos.append({'comeco': ultimoHorario, 'final': fimDia})
    #Aqui melhoramos um pouco o formato dos intervalos
    intervalosBeauty = [f"{intervalo['comeco'].strftime('%H:%M')} - {intervalo['final'].strftime('%H:%M')}" for intervalo in intervalos]
    #.join transforma o dicionário em string melhorando um pouco a saída
    await update.message.reply_text(f"Você pode marcar eventos com essa duração nos intervalos: {', '.join(intervalosBeauty)}")        
def main(): 
    app = ApplicationBuilder().token("token aqui").build()
    app.add_handler(CommandHandler("start", start)) 
    app.add_handler(CommandHandler("hello", hello)) 
    app.add_handler(CommandHandler("agendar", agendar))
    app.add_handler(CommandHandler("consultar", consultar))
    app.add_handler(CommandHandler("cancelar", cancelar))
    app.add_handler(CommandHandler("sugerir", sugerir))
    app.run_polling() 
if __name__ == "__main__": 
    main()