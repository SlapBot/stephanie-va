import imaplib
import email
import re
from dateutil import parser
from Stephanie.Modules.base_module import BaseModule


class GmailModule(BaseModule):
    def __init__(self, *args):
        super(GmailModule, self).__init__(*args)
        self.gmail_address = self.get_configuration('gmail_address')
        self.password = self.get_configuration('gmail_password')
        self.conn = None
        if self.gmail_address and self.password:
            self.do_init()
        else:
            return False

    def do_init(self):
        try:
            self.conn = imaplib.IMAP4_SSL('imap.gmail.com')
            self.conn.debug = 0
            self.conn.login(self.gmail_address, self.password)
        except:
            response = ("Either your credentials are wrong mate, or there is some problem going on, do me a favor, I know "
                        "you won't but whatever, just inform me in the forums.")
            print(response)
            return response

    def fetch_unread_emails(self, since=None, markRead=False, limit=None):
        """
            Fetches a list of unread email objects from a user's Gmail inbox.
            Arguments:
            profile -- contains information related to the user (e.g., Gmail
                       address)
            since -- if provided, no emails before this date will be returned
            markRead -- if True, marks all returned emails as read in target inbox
            Returns:
            A list of unread email objects.
        """
        self.conn.select(readonly=(not markRead))

        msgs = []
        (retcode, messages) = self.conn.search(None, '(UNSEEN)')

        if retcode == 'OK' and messages != ['']:
            num_unread = len(messages[0].split())
            # if limit and num_unread > limit:
            #     return num_unread
            i = 0
            for num in messages[0].split():
                # parse email RFC822 format
                if i > 5:
                    break
                ret, data = self.conn.fetch(num, '(RFC822)')
                correct_format_message = data[0][1].decode("utf-8")
                msg = email.message_from_string(correct_format_message)

                if not since or self.get_date(msg) > since:
                    msgs.append(msg)
                i += 1
        self.conn.close()
        self.conn.logout()

        return num_unread, msgs

    @staticmethod
    def get_sender(email_found):
        """
            Returns the best-guess sender of an email.
            Arguments:
            email -- the email whose sender is desired
            Returns:
            Sender of the email.
        """
        sender = email_found['From']
        m = re.match(r'(.*)\s<.*>', sender)
        if m:
            return m.group(1)
        return sender

    @staticmethod
    def get_date(email_found):
        return parser.parse(email_found.get('date'))

    @staticmethod
    def get_most_recent_date(emails):
        """
            Returns the most recent date of any email in the list provided.
            Arguments:
            emails -- a list of emails to check
            Returns:
            Date of the most recent email.
        """
        dates = [GmailModule.get_date(e) for e in emails]
        dates.sort(reverse=True)
        if dates:
            return dates[0]
        return None

    def handle(self):
        """
            Responds to user-input, typically speech text, with a summary of
            the user's Gmail inbox, reporting on the number of unread emails
            in the inbox, as well as their senders.
            Arguments:
            text -- user-input, typically transcribed speech
            self.assistant -- used to interact with the user (for both input and output)
            profile -- contains information related to the user (e.g., Gmail
                       address)
        """
        try:
            num_unread, msgs = self.fetch_unread_emails(limit=5)

            if num_unread > 5:
                response = "You have %d unread emails, out of which 5 latest ones are as follows, please wait a second, as I process" % num_unread
                self.assistant.say(response)
            senders = []
            for e in msgs:
                senders.append(self.get_sender(e))
        except imaplib.IMAP4.error:
            return "I'm sorry. I'm not authenticated to work with your Gmail."

        if not senders:
            return "You have no unread emails."
        elif len(senders) == 1:
            return "You have one unread email from " + senders[0] + "."
        else:
            response = "You have %d unread emails" % len(
                senders)
            unique_senders = list(set(senders))
            if len(unique_senders) > 1:
                unique_senders[-1] = 'and ' + unique_senders[-1]
                response += ". Senders include: "
                response += '...'.join(senders)
            else:
                response += " from " + unique_senders[0]

            return response
