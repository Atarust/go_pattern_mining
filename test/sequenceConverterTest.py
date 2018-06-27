'''
Created on Jun 24, 2018

@author: jonas
'''
import unittest

from src.move import Move, Player
from src.sequenceConverter import all_prefix, file_to_sgf, create_window_seq, to_matrix, find_all_patterns


class Test(unittest.TestCase):

    def test_all_prefix(self):
        self.assertTrue(all_prefix(['a', 'b', 'c']) == [['a'], ['a', 'b']])
        self.assertTrue(all_prefix(['a', 'b']) == [['a']])
        self.assertTrue(all_prefix(['a']) == [])

    def test_eq(self):
        self.assertEquals(Move(Player.w, 0, 0), Move(Player.w, 0, 0))
        self.assertNotEqual(Move(Player.w, 0, 1), Move(Player.w, 1, 0))
        self.assertNotEqual(Move(Player.w, 0, 1), Move(Player.b, 0, 1))

    def test_file_to_sgf(self):
        content = "(;GM[1]FF[4]  SZ[19]  GN[韩国女?围甲?赛]  DT[2017-05-07]  PB[藤泽里?]  PW[?유진]  BR[P3段]  WR[P1段]  KM[0]HA[0]RU[Japanese]AP[GNU Go:3.8]RE[B+7.5]TM[3600]TC[5]TT[40]AP[foxwq]  ;B[ab];B[bb];B[cc];W[cf];B[ss];W[as])"      
        game = file_to_sgf(content)
        
        self.assertEquals(Move(Player.w, 0, 18), game[5])
        self.assertEquals(Move(Player.b, 0, 1), game[0])

    def test_create_window_seq(self):
        content = "(;GM[1]FF[4]  SZ[19]  GN[韩国女?围甲?赛]  DT[2017-05-07]  PB[藤泽里?]  PW[?유진]  BR[P3段]  WR[P1段]  KM[0]HA[0]RU[Japanese]AP[GNU Go:3.8]RE[B+7.5]TM[3600]TC[5]TT[40]AP[foxwq]  ;B[aa];B[bb];B[cc])"      
        game = file_to_sgf(content)
        seq = create_window_seq(game)
        
        # without influence of normalization
        self.assertEqual(seq[0], [Move(Player.b, 0, 0), Move(Player.b, 1, 1), Move(Player.b, 2, 2)])
        
        # with prefixes
        self.assertEqual(seq[1], [Move(Player.b, 0, 0)], 'Prefis is missing!')
        self.assertEqual(seq[2], [Move(Player.b, 0, 0), Move(Player.b, 1, 1)])
        
        # with normalization (the second window
        self.assertEqual(seq[3], [Move(Player.b, 1, 0), Move(Player.b, 2, 1)], 'Maybe normalization is wrong?')
        self.assertEqual(seq[4], [Move(Player.b, 1, 0)])
        self.assertEqual(seq[5], [Move(Player.b, 2, 0)])

    def test_to_matrix(self):
        content = "(;GM[1]FF[4]  SZ[19]  GN[韩国女?围甲?赛]  DT[2017-05-07]  PB[藤泽里?]  PW[?유진]  BR[P3段]  WR[P1段]  KM[0]HA[0]RU[Japanese]AP[GNU Go:3.8]RE[B+7.5]TM[3600]TC[5]TT[40]AP[foxwq]  ;B[aa];B[bb];B[cc])"      
        game = file_to_sgf(content)
        seq = create_window_seq(game)
        matrix = to_matrix(seq[0])
        
        m_move1 = [Player.b, Player.empty, Player.empty,
                   Player.empty, Player.empty, Player.empty,
                   Player.empty, Player.empty, Player.empty]
        
        m_move2 = [Player.b, Player.empty, Player.empty,
                   Player.empty, Player.b, Player.empty,
                   Player.empty, Player.empty, Player.empty]
        
        m_move3 = [Player.b, Player.empty, Player.empty,
                   Player.empty, Player.b, Player.empty,
                   Player.empty, Player.empty, Player.b]
        
        self.assertEquals(matrix == m_move1 or matrix == m_move2 or matrix == m_move3) 
        
    def test_find_all_patterns(self):
        content = "(;GM[1]FF[4]  SZ[19]  GN[韩国女?围甲?赛]  DT[2017-05-07]  PB[藤泽里?]  PW[?유진]  BR[P3段]  WR[P1段]  KM[0]HA[0]RU[Japanese]AP[GNU Go:3.8]RE[B+7.5]TM[3600]TC[5]TT[40]AP[foxwq]  ;B[aa];B[bb];B[cc])"      
        game = file_to_sgf(content)
        seq = create_window_seq(game)
        pattern1 = ['B', '_', '_',
                   '_', 'B', '_',
                   '_', '_', 'B']
        pattern1 = 'B___B___B'
        pattern1 = list(map(lambda p: Player(p), pattern1))
        s1 = find_all_patterns(pattern1, seq)
        self.assertEqual(len(s1), 1)
        
        pattern2 = ['B', '_', '_',
                    '_', 'B', '_',
                    '_', '_', '?']
        pattern2 = list(map(lambda p: Player(p), pattern2))
        s2 = find_all_patterns(pattern2, seq)
        self.assertEqual(len(s2), 3, 'Should be 3. First two because of first window, second because of the prefix and third because of second window.')
        
        pattern3 = ['B', '_', '_',
                    '_', 'W', '_',
                    '_', '_', '?']
        pattern3 = list(map(lambda p: Player(p), pattern3))
        s3 = find_all_patterns(pattern3, seq)
        self.assertEqual(len(s3), 0)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
