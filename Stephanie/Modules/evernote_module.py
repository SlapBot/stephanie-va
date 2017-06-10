import evernote.edam.type.ttypes as NoteType
from evernote.api.client import EvernoteClient
from Stephanie.Modules.base_module import BaseModule


# Written by Jason van Eunen - jasonvaneunen.com

class EvernoteModule(BaseModule):
    def __init__(self, *args):
        super(EvernoteModule, self).__init__(*args)
        self.auth_token = self.get_configuration('evernote_auth_token')
        if self.auth_token:
            self.client = EvernoteClient(token=self.auth_token, sandbox=False)
            self.user_store = self.client.get_user_store()
            self.note_store = self.client.get_note_store()
        else:
            return False

    def write_note(self):
        note = NoteType.Note()  # Creates a new note
        note.title = "Stephanie Note"

        self.assistant.say("What would you like me to write down?")
        the_note = self.assistant.listen().decipher()  # Listens to the input and stores it

        note.content = '<?xml version="1.0" encoding="UTF-8"?>'
        note.content += '<!DOCTYPE en-note SYSTEM ' \
                        '"http://xml.evernote.com/pub/enml2.dtd">'
        note.content += '<en-note>Note:<br/>'
        note.content += ('%s' % the_note)
        note.content += '</en-note>'

        try:
            created_note = self.note_store.createNote(note)  # Stores the new note in Evernote
        except:
            response = ("Note wasn't created successfully, you probably didn't spelled anything or spelled really "
                        "bad, Not my fault okay? It's never a program's fault.")
            print(response)
            return response
        if created_note:
            return "I successfully wrote down your note."
        else:
            response = ("Note wasn't created successfully, you probably didn't spelled anything or spelled really "
                        "bad, Not my fault okay? It's never a program's fault. /s Refer back to docs.")
            print(response)
            return response

