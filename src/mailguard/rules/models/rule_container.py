class RuleContainer:

    def __init__(self,
                 rule_id,
                 account_id,
                 rule):
        self.rule_id = rule_id
        self.account_id = account_id
        self.rule = rule


class Rule:

    def __init__(self,
                 filters,
                 delete,
                 move_to,
                 encrypt,
                 message):
        self.filters = filters
        self.delete = delete
        self.move_to = move_to
        self.encrypt = encrypt
        self.message = message


class Filter:

    def __init__(self,
                 from_address,
                 words,
                 links,
                 tags):
        self.from_address = from_address
        self.words = words
        self.links = links
        self.tags = tags


class Tags:

    def __init__(self,
                 categories,
                 subjects,
                 sentiment,
                 buzzwords,
                 summary):
        self.categories = categories
        self.subjects = subjects
        self.sentiment = sentiment
        self.buzzwords = buzzwords
        self.summary = summary
