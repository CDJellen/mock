import matplotlib.pyplot as plt

from base64 import b64encode
from datetime import datetime
from io import BytesIO

from app.utility.base_object import BaseObject


class Trial(BaseObject):

    @property
    def unique(self):
        return self.hash('%s' % self.name)

    @property
    def display(self):
        return dict(name=self.name, number=self.number, start=self.start.strftime('%Y-%m-%d %H:%M:%S'),
                    operations=[o.display for o in self.operations], charts=self._calculate_charts())

    def __init__(self, name, number):
        self.name = name
        self.number = number
        self.start = datetime.now()
        self.operations = []

    def store(self, ram):
        existing = self.retrieve(ram['trials'], self.unique)
        if not existing:
            ram['trials'].append(self)
            return self.retrieve(ram['trials'], self.unique)

    """ PRIVATE """

    def _calculate_charts(self):
        plt.plot([1, 2, 3, 4, 8, 12, 20])
        plt.xlabel('some numbers')
        plt.ylabel('some numbers')
        temp_file = BytesIO()
        plt.savefig(temp_file, format='png')
        encoded = b64encode(temp_file.getvalue()).decode('utf-8')
        return ['<img src=\'data:image/png;base64,{}\'>'.format(encoded)]
