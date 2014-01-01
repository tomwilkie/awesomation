import unittest, gae_channel, urllib2, talkparser

class TalkParserTest(unittest.TestCase):
    def test_string_match(self):
        match = talkparser._dquote_search.search('"23\\"567"]', pos=1)
        self.assertEqual(8, match.start())

        match = talkparser._squote_search.search("'23\\'567']", pos=1)
        self.assertEqual(8, match.start())


        msg = repr('te\" \ndf\' st')
        string =  talkparser._match_str(msg, pos=0)
        # string matcher should return repr(msg) without quotes
        self.assertEqual("'%s'" % string, msg)

    def test_tokenizer(self):
        msg = '[123, "test"]'
        tokens = list(talkparser._tokenize(msg))
        expected_tokens = ['[', 123, ',', talkparser._StringToken("test"), ']']
        self.assertEqual(tokens, expected_tokens)
        

    def test_parser(self):
        msg = [12,["c",['clid',["ae","pingmsg\n[test]\"bla\"\n"]]]]
        parsed =  talkparser.parse(repr(msg))
        self.assertEqual(msg, parsed)

        




class TestChannel(unittest.TestCase):
    # TODO: write some tests
    def test_impl(self):
        pass



