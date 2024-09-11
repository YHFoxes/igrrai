from telegram import InputPollOption


class Poll:
    def __init__(self, data):
        self.options = []
        self.question = ""
        self.is_anonymous = False
        self.multiple_answers = False

        self.get_options(data)

    def get_options(self, data):
        self.question = data["question"]
        self.is_anonymous = data["anonymous"]
        self.multiple_answers = data["multiple"]

        for option in data["answers"]:
            self.options.append(InputPollOption(option["text"]))
