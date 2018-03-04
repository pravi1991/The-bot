import json
import requests
import time

Bots = {'sentient': '518884250:AAHIlw_S3vcHmLR2Eq13ug0JYFBuZfAJSkI',
        'raven': '459238892:AAEliUtpJ91VDESkXPQ70RAQ5xK9FWHVrFg'}


class Mybots:
    def __init__(self, token, name):
        self.Token = token
        self.name = name
        self.url = "https://api.telegram.org/bot" + self.Token
        self.contacts = {}
        self.populate_contacts('load')

    def get_url(self, sub_url):
        get_url = self.url + sub_url
        response = requests.get(get_url)
        return response

    def get_json(self, parameter):
        response = self.get_url(parameter)
        content = json.loads(response.content.decode('utf-8'))['result']
        return content

    def bot_info(self):
        about_bot = self.get_json("/getme")
        print("Username\t:", about_bot['username'])
        print('ID\t\t\t:', about_bot['id'])
        print('First Name\t:', about_bot['first_name'])

    def get_updates(self):
        get_updates = self.get_json("/getUpdates")
        return get_updates

    def get_last_message_parameters(self):
        messages = self.get_updates()
        total_message = len(messages)
        g_last_message = total_message - 1
        g_text = messages[g_last_message]["message"]["text"]
        g_name = messages[g_last_message]["message"]["chat"]["first_name"]
        g_chat_id = messages[g_last_message]["message"]["chat"]["id"]
        return g_name, g_chat_id, g_text

    def populate_contacts(self, action='update'):
        messages = self.get_updates()

        if action == 'update':
            file = open(self.name + '_contacts.txt', 'a')
            for m in range(len(messages)):
                names = messages[m]['message']['chat']['first_name']
                ids = messages[m]['message']['chat']['id']
                if names not in self.contacts.keys():
                    self.contacts[names] = ids
                    file.write(str(names) + ':' + str(ids) + '\n')
            file.close()

        if action == 'load':
            with open(self.name + '_contacts.txt', 'r') as file:
                for lines in file:
                    line = list(lines.split(':'))
                    if line[0] not in self.contacts:
                        self.contacts[line[0]] = line[1].split('\n')[0]
                if self.contacts == {}:
                    print("Contact list is empty... Populating contacts")
                    self.populate_contacts()
        return self.contacts

    def echo_message(self):
        m_name, m_chat_id, m_text = self.get_last_message_parameters()
        self.send_message_to(str(m_name), str(m_text))

    def get_message_from(self, name):
        messages = self.get_updates()
        message_count = 0
        name = name.title()
        for m in range(len(messages)):
            if messages[m]['message']['chat']['first_name'] == name:
                print(messages[m]['message']['chat']['first_name'], ":",
                      messages[m]['message']['text'])
                message_count += 1
        if message_count == 0:
            print("No message for ", name)

    def print_all_messages(self):
        messages = self.get_updates()
        for m in range(len(messages)):
            print(m + 1, ".", messages[m]['message']['chat']['first_name'], ":",
                  messages[m]['message']['text'])

    def send_message_to(self, name, text):
        chat_id = self.contacts[name.title()]
        url = "/sendMessage?text={}&chat_id={}".format(text, chat_id)
        self.get_url(url)

    def broadcast(self, message='test'):
        for names in self.contacts.keys():
            self.send_message_to(name=names, text=message)

    @classmethod
    def bot_create(cls, bot_name):
        print("Creating the bot")
        with open(bot_name+"_contacts.txt",'w') as file:
            pass
        bot = cls(Bots[bot_name], bot_name)
        print("Bot " + bot_name + " created")
        return bot


if __name__ == '__main__':
    sentient_bot = Mybots.bot_create('sentient')
    print(sentient_bot.contacts)
    # sentient_bot.send_message_to(input('To :'), input('Message :'))
    last_message = (None, None)
    try:
        while True:
            name, chat_id, text = sentient_bot.get_last_message_parameters()
            if (chat_id, text) != last_message:
                sentient_bot.echo_message()
                last_message = (chat_id, text)
                # print(last_message)
            time.sleep(2)
    except KeyboardInterrupt:
        print("User Quit..!!")
    except KeyError:
        print("Message unreadable..!!")
