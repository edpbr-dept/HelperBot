import re
import time
import utils
import telepot
from telepot.loop import MessageLoop
from telepot.delegate import pave_event_space, per_chat_id, create_open, include_callback_query_chat_id


## MACROS
# Token API
TOKEN = 
# # Set API proxy
# telepot.api.set_proxy(proxy)
# thread-safe dict
propose_records = telepot.helper.SafeDict()  


# Comandos do BOT
PATTERN_BOT_LOC = re.compile('locais|/locais')
PATTERN_BOT_MED = re.compile('medidores|/medidores')


'''
VARIABLES HELPER:
-----------------
    + _chat_state:
        00 -> Nada
        01 -> Esperando o nome da localidade (p/ pegar código do TorezaniBot)
        01 -> Esperando o nome da localidade (p/ pegar o nº de trafo/instalação)
'''


class EDPBR_HelperBot(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(EDPBR_HelperBot, self).__init__(*args, **kwargs)

        # Recuperar do banco de dados
        global propose_records

        # Se a conversa com o usuário está em aberto
        if self.id in propose_records:
            self._count, self._edit_msg_ident = propose_records[self.id]
            self._editor = telepot.helper.Editor(self.bot, self._edit_msg_ident) if self._edit_msg_ident else None
        
        # Se a conversa é nova
        else:
            self._edit_msg_ident = None
            self._editor = None
            self._chat_state = 0        # Tipo de reply esperada


    def _handle_message(self, msg):
        # Ler conteúdo da mensagem
        msg_text = msg['text']
        msg_from = msg['from']
        user_id = msg_from['id']

        
        if self._chat_state == 1:
            sent = self.sender.sendMessage(utils.torezaniBot_locations(msg_text))
            self.close()

        elif self._chat_state == 2:
            sent = self.sender.sendMessage(utils.medidores(msg_text))
            self.close()

        elif bool(PATTERN_BOT_LOC.match(msg_text.lower())):
            sent = self.sender.sendMessage('Digite o nome da localidade.')
            self._chat_state = 1

        elif bool(PATTERN_BOT_MED.match(msg_text.lower())):
            sent = self.sender.sendMessage('Digite o nome da localidade.')
            self._chat_state = 2
            
        # Comando não reconhecido
        else:
            sent = self.sender.sendMessage('Comando desconhecido.')
            self.close()


    def _cancel_last(self):
        if self._editor:
            self._editor.editMessageReplyMarkup(reply_markup=None)
            self._editor = None
            self._edit_msg_ident = None


    def on_chat_message(self, msg):
        content_type, _, _ = telepot.glance(msg)
        if content_type == 'text':
            self._handle_message(msg)

    
    def on__idle(self, event):
        self.sender.sendMessage('Tempo esgotado!')
        self.close()

    
    def on_close(self, ex):
        global propose_records


bot = telepot.DelegatorBot(TOKEN, [
    include_callback_query_chat_id(
        pave_event_space())(
            per_chat_id(types=['private']), create_open, EDPBR_HelperBot, timeout=300),
])
MessageLoop(bot).run_as_thread()
print('Listening ...')


while True:
    time.sleep(300)
