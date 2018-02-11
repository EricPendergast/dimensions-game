import unittest
from physical.integer_physics import *
from physical.environment import *

class BlockTests(unittest.TestCase):
    def shares_no_references(self, l1, l2):
        for a in l1:
            for b in l2:
                if a is b:
                    return False
        return True
    
    def test_shares_no_references(self):
        self.assertTrue(self.shares_no_references([1,3,4], {2,5,70}))
        ref = "hello"
        
        self.assertFalse(self.shares_no_references({ref, 5}, [0, ref]))
                
    def test_bucket_to_future_bucket(self):
        block = Block(GravityBlock, Vec(0,0), Vec(0,0))


        future_buckets = Grid.FutureBuckets(1,1)
        
        block.update(None, future_buckets)
        
        result_block = future_buckets._buckets_mat[0][0]._bucket[0]
        
        
        self.assertTrue(self.shares_no_references([block.pos, block.vel], [result_block.pos, result_block.vel]))
        
        future_buckets._buckets_mat[0][0].collapse(block)
        
        print "This test is not finished"
        

if __name__=='__main__':
    unittest.main()
