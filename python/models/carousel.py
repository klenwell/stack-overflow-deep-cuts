"""
Not really a model. More of a utility. But putting it here will do for now.
"""
class Carousel(object):
    # Based on https://stackoverflow.com/a/2777223/1093087
    # Because Python 3 iters don't have a next method and next(iter) conflicts with
    # pdb's next method.
    def __init__(self, collection):
        self.collection = collection
        self.index = 0

    @property
    def current(self):
        return self.collection[self.index]

    @property
    def first(self):
        self.index = 0
        return self.current

    @property
    def last(self):
        self.index = len(self.collection) - 1
        return self.current

    @property
    def next(self):
        try:
            result = self.collection[self.index]
            self.index += 1
        except IndexError:
            print("You've reached last item. Returning to first item.")
            self.index = 0
            result = self.next()
        return result

    @property
    def prev(self):
        self.index -= 1
        if self.index < 0:
            print("You've reached first item. Going to last item.")
            self.index = len(self.collection)
            return self.prev()
        return self.current

    def __iter__(self):
        return self

    def __len__(self):
        return len(self.collection)
