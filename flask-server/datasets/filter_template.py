class filter_template:
    def __init__(self):
        self.index = ''
        self.field = {}
        self.filter = {
            "continuous": [],
            "categorical": []
        }
        self.group_by = []
        self.aggregate = []