import unittest
from core import WordUtil
from pprint import pprint as pp

class TestWordUtility(unittest.TestCase):
    def setUp(self):
        self.textUtil = WordUtil()

    def testGetSimilarMeaning(self):
        words = ['refactor', 'commence', 'deploy', 'scrutinize', 'integrate']
        for word in words:
            result = self.textUtil.getSimilarMeaning(word)
            self.assertTrue(result is not None, msg=f"getSimilarMeaning() returns None on {word}")

    def testGetSimilarSounding(self):
        words = ['learn', 'hyphen', 'dextrose', 'comma', 'lean', 'confidant', 'confident']
        for word in words:
            result = self.textUtil.getSimilarSounding(word)
            self.assertTrue(result is not None, msg=f'getSimilarSounding() returns None on {word}')

    def testGetSimilarSpelling(self):
        words = ['gate', 'philanthropy', 'matter', 'candidate', 'hamstring', 'royal', 'kotlin']
        for word in words:
            result = self.textUtil.getSimilarSpelling(word)
            self.assertTrue(result is not None, msg=f'getSimilarSpelling() returns None on {word}')

    def testGetDescriptiveAdjs(self):
        words = ['ball', 'mice', 'bear', 'seam', 'crest', 'fold', 'smart', 'giraffe']
        for word in words:
            result = self.textUtil.getDescriptiveAdjs(word)
            self.assertTrue(result is not None, msg=f'getDescriptiveAdj() returns None for {word}')

    def testGetOftenDescribedBy(self):
        words = ['heavy', 'greed', 'lard', 'mad', 'hell', 'spontaneous', 'love']
        for word in words:
            result = self.textUtil.getOftenDescribedBy(word)
            self.assertTrue(result is not None, msg=f'getOftenDescribedBy() returns None on {word}')


    def testGetOftenFollowedBy(self):
        words = ['with', 'usually', 'thank you', 'in the', 'revise', 'hurt']
        for word in words:
            result = self.textUtil.getOftenFollowedBy(word)
            self.assertTrue(result is not None, msg=f'getOftenFollowedBy() returns None for {word}')

    def testGetCorrectedText(self):
        textErrors = [
            "This tetx is errorneous. It needs to being corrected.",
            "This text have erroneous grammers and spellign. It needs being corrected.",
            "This text has erroneous punctuation, it need to bee corrected.\'"
        ]
        expected = [
            'This text is erroneous. It needs to be corrected.',
            'This text has erroneous grammar and spelling. It needs to be corrected.',
            'This text has erroneous punctuation, it needs to be corrected.'
        ]
        for text in textErrors:
            result = self.textUtil.getCorrectedText(text)
            print(result)
            self.assertTrue(result in expected, msg=f'getCorrectedText() returns unexpected text, or None for text: {text}')
            pp(f'original sentence: {text}\n corrected sentence: {result}', indent=2)



if '__main__'==__name__:
    textUtilTest = TestWordUtility()
    textUtilTest.testGetSimilarMeaning()
    textUtilTest.testGetSimilarSounding()
    textUtilTest.testGetDescriptiveAdjs()
    textUtilTest.testGetOftenDescribedBy()
    textUtilTest.testGetOftenFollowedBy()
    textUtilTest.testGetCorrectedText()