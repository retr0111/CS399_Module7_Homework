from math import sqrt
from time import process_time


class Word:
    def __init__(self, text: str, vector: list[float]) -> None:
        self.text = text
        self.vector = vector

    def __repr__(self) -> str:
        vector_preview = ' '.join(map(str, self.vector[:2]))
        return f"{self.text} [{vector_preview} ...]"

    def norm(self) -> float:
        return sqrt(sum([x * x for x in self.vector]))

    def normalize(self) -> None:
        length = self.norm()
        self.vector = [x / length for x in self.vector]

    def similarity(self, w) -> float:
        return self * w

    def __add__(self, w) -> 'Word':
        return Word("", [x + y for x, y in zip(self.vector, w.vector)])

    def __sub__(self, w) -> 'Word':
        return Word("", [x - y for x, y in zip(self.vector, w.vector)])

    def __mul__(self, w: 'Word') -> float:
        return sum([x * y for x, y in zip(self.vector, w.vector)])


class Model(list):
    features = 300

    def __init__(self, inp_file_name: str) -> None:
        super().__init__()
        print(f"Loading model from {inp_file_name} ...")
        t0 = process_time()
        with open(inp_file_name) as inp_file:
            for line in inp_file:
                sa = line.split()
                if len(sa) != Model.features + 1:
                    continue
                self.append(Word(sa[0], [float(x) for x in sa[1:]]))
        print(f"Loaded in {process_time() - t0} secs")

    def find_word(self, text: str) -> Word | None:
        for w in self:
            if w.text == text:
                return w

    def find_similar_words(self, word: Word, n: int = 10) -> list[Word]:
        return sorted(self, key=lambda w: w.similarity(word), reverse=True)[:n]

    def __repr__(self) -> str:
        return f"Model({len(self)} words)"

    def __getitem__(self, text: str) -> Word:
        return self.find_word(text)

    def __contains__(self, text: str) -> bool:
        return self.find_word(text) is not None
