import requests


def notify(name, home, guest, winner):
    """Use this function to send notifications via TG bot
    """

    # Selecting the bot & chat 
    bot_token = '739094059:AAFTJOeh61nstCgedtXx-oZqj1oWfgQGlwk'
    bot_chatID = "@AlmanacBets"

    # Sending bot a message
    send_text = 'https://api.telegram.org/bot' + \
        bot_token + '/sendMessage?chat_id=' + bot_chatID + \
        '&parse_mode=Markdown&text=' + '№4\nБаскетбол' + '\n' + name + '\n' + \
        home + ' - ' + guest + '\n' + '2 четверть ' + winner
    requests.get(send_text)
