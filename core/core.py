import io
from data import Question, QuestionType, Flashcard
from core.utils import WordUtil
from google.cloud import vision
import nltk


class DocumentHandler(object):
    def __init__(self):
        self._client = vision.ImageAnnotatorClient()
        self._image = None
        self._response = None
        self.wordUtil = WordUtil()

    def digitizeDocument(self, imgPath):
        with io.open(imgPath, 'rb') as img_file:
            content = img_file.read()
            image = vision.types.Image(content=content)
            detectedText = self._client.text_detection(
                image=image).text_annotations[0].description
            res = self.wordUtil.getCorrectedText(detectedText)
            return res


    def parseSentences(self, text):
        sentences = nltk.sent_tokenize(text)
        return sentences

    def tokenizeWords(self, sentences):
        for sentence in sentences:
            words = nltk.word_tokenize(sentence)
            tags = nltk.pos_tag(words)
            chunks = nltk.ne_chunk(tags)
            return chunks

    def getTextWithPOS(self, text):
        sentences = self.parseSentences(text)
        return self.tokenizeWords(sentences)

    def discernQuestion(self):
        pass


class Questionizer(object):
    '''
    Strategy for questionizer is to use several commonly used forms of each Wh- and How question as templates,
    to fit any given sentence.

    Given sentence s:
      interrogative = None
      det = s.determiner
      if det is pronoun (PRP | PRON):
          if det is not plural (NNPS | PROPN):
              if det is person:
                  interrogative = [Who, Whom]
              elif det is nonhuman:
                  interrogative = [What]
          else:
              interrogative = [Which]
      elif det is pro-adverb:
          if det is location:
              interrogative = [Where]
          elif det is time:
              interrogative = [When]
          elif det is manner:
              interrogative = [How]
          elif det is reason:
              interrogative = [Why]


    # Spacy Named Entity Recognition (NER) models are organized by their correlative Wh-Interrogative word type, in an enum.

    Interrogatives(Enum):
        What(PRODUCT, FAC, OR, LOC, EVENT, LAW, NORP, LANGUAGE, WORK_OF_ART, PERCENT ),
        When(TIME, DATE),
        Who(PERSON),
        Where(LOC, GPE, ORG, FAC),
        How(
            much(QUANTITY, PERCENT, MONEY),
            many(QUANTITY, PERCENT, TIME),
            long(QUANTITY, TIME),
            far(QUANTITY),
            old(QUANTITY, TIME, DATE)
        )
    '''
    def __init__(self):
        pass


typeErr = 'Provided answer(s) must be included within the list of supplied options'

class FlashcardBuilder(object):
    def __init__(self):
        pass

    @staticmethod
    def buildMultiChoiceCard(subject:str, question:str, options:list, answer:str, hint=None):
        if FlashcardBuilder.includesAnswer(answer, options) is False:
            raise TypeError(typeErr)
        else:
            question = Question(
                question_type=QuestionType.MULTIPLE_CHOICE, question=question, options=options, answer=answer
            )
            return Flashcard(subject=subject, question=question, hint=hint, correct=False)

    @staticmethod
    def buildMultiSelectCard(subject:str, question:str, options:list, answers:list, hint=None):
        if FlashcardBuilder.includesAnswer(answers, options) is False:
            raise TypeError(typeErr)
        else:
            question = Question(
                question_type=QuestionType.MULTIPLE_SELECT, question=question, options=options, answer=answers
            )
            return Flashcard(subject=subject, question=question, hint=hint, correct=False)

    @staticmethod
    def buildBlankFillCard(self, statement=str, answer=str):
        pass

    @staticmethod
    def buildTrueFalseCard(self, statement=str, answer=bool):
        pass

    @staticmethod
    def includesAnswer(answer, options):
        ''' flashcards aren't flashcards without answers. '''
        options = [o.lower() for o in options]
        if isinstance(answer, list):
            answer = [a.lower() for a in answer]
            return set(options).issuperset(answer)
        else:
            answer.lower()
            return answer in options
