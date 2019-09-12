import unittest
import torch
import os
import heat as ht

ht.use_device(os.environ.get('DEVICE'))

if os.environ.get('DEVICE') == 'gpu':
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class TestOperations(unittest.TestCase):
    def test___binary_op_broadcast(self):

        # broadcast without split
        left_tensor = ht.ones((4, 1))
        right_tensor = ht.ones((1, 2))
        result = left_tensor + right_tensor
        self.assertEqual(result.shape, (4, 2))
        result = right_tensor + left_tensor
        self.assertEqual(result.shape, (4, 2))

        # broadcast with split=0 for both operants 
        left_tensor = ht.ones((4, 1), split=0)
        right_tensor = ht.ones((1, 2), split=0)
        result = left_tensor + right_tensor
        self.assertEqual(result.shape, (4, 2))
        result = right_tensor + left_tensor
        self.assertEqual(result.shape, (4, 2))

        # broadcast with split=1 for both operants
        left_tensor = ht.ones((4, 1), split=1)
        right_tensor = ht.ones((1, 2), split=1)
        result = left_tensor + right_tensor
        self.assertEqual(result.shape, (4, 2))
        result = right_tensor + left_tensor
        self.assertEqual(result.shape, (4, 2))

        # broadcast with split=1 for second operant
        left_tensor = ht.ones((4, 1))
        right_tensor = ht.ones((1, 2), split=1)
        result = left_tensor - right_tensor
        self.assertEqual(result.shape, (4, 2))
        result = right_tensor + left_tensor
        self.assertEqual(result.shape, (4, 2))

        # broadcast with split=0 for first operant
        left_tensor = ht.ones((4, 1), split=0)
        right_tensor = ht.ones((1, 2))
        result = left_tensor - right_tensor
        self.assertEqual(result.shape, (4, 2))
        result = right_tensor + left_tensor
        self.assertEqual(result.shape, (4, 2))

        # broadcast with unequal dimensions and one splitted tensor
        left_tensor = ht.ones((2, 4, 1), split=0)
        right_tensor = ht.ones((1, 2))
        result = left_tensor + right_tensor
        self.assertEqual(result.shape, (2, 4, 2))
        result = right_tensor - left_tensor
        self.assertEqual(result.shape, (2, 4, 2))

        # broadcast with unequal dimensions and two splitted tensors
        left_tensor = ht.ones((4, 1, 3, 1, 2), split=0, dtype=torch.uint8)
        right_tensor = ht.ones((1, 3, 1), split=0, dtype=torch.uint8)
        result = left_tensor + right_tensor
        self.assertEqual(result.shape, (4, 1, 3, 3, 2))
        result = right_tensor + left_tensor
        self.assertEqual(result.shape, (4, 1, 3, 3, 2))

        with self.assertRaises(TypeError):
            ht.add(ht.ones((1, 2)), 'wrong type')
        with self.assertRaises(NotImplementedError):
            ht.add(ht.ones((1, 2), split=0), ht.ones((1, 2), split=1))
