from pydispatch import dispatcher


class EventDispatcher:
    def __init__(self):
        self.dispatcher = dispatcher
        self.sleep_status = False
        self.active_status = False

    def close(self):
        return self.sleep_status

    def sleep(self, sender):
        self.sleep_status = True
        print("The virtual assistant is going to sleep by %s method" % sender)
        return self

    def quit(self, sender):
        self.active_status = True
        print("The virtual assistant is being quit by %s method" % sender)

    def add(self, handle_name):
        handle_event = getattr(self, handle_name)
        self.dispatcher.connect(handle_event, signal=handle_name, sender=self.dispatcher.Any)
        return self

    def trigger(self, handle):
        self.dispatcher.send(signal=handle, sender=handle)
