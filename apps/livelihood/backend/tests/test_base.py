import unittest
import numpy as np
from apps.livelihood.backend.base import BaseEntity
class TestBaseEntity(unittest.TestCase):

    def test_init_all(self):
        entity=BaseEntity(yearly=24000, monthly=2000,weekly=500)
        self.assertEqual(entity.YEARLY,24000)
        self.assertEqual(entity.MONTHLY,2000)
        self.assertEqual(entity.WEEKLY,500)
    
    def test_init_year(self):
        entity=BaseEntity(yearly=24000)
        self.assertEqual(entity.YEARLY,24000)
        self.assertEqual(entity.MONTHLY,2000)
        self.assertEqual(entity.WEEKLY,500)
    
    def test_init_month(self):
        entity=BaseEntity(monthly=2000)
        self.assertEqual(entity.YEARLY,24000)
        self.assertEqual(entity.MONTHLY,2000)
        self.assertEqual(entity.WEEKLY,500)
    
    def test_init_week(self):
        entity=BaseEntity(weekly=500)
        self.assertEqual(entity.YEARLY,24000)
        self.assertEqual(entity.MONTHLY,2000)
        self.assertEqual(entity.WEEKLY,500)
    
    def test_offset(self):
        entity=BaseEntity(offset=1000)
        entity.OFFSET_MONTHLY = 1000/(4*12)
        entity.OFFSET_WEEKLY = 1000/(4*12)
    
    def test_cum_yearly(self):
        entity=BaseEntity(yearly=1000)
        yearly_cumulative=entity.cum_yearly(5)
        excepted = np.array([1000,2000,3000,4000,5000], np.float64)
        assert np.array_equal(yearly_cumulative, excepted)
    
    def test_cum_yearly_with_increase(self):
        entity=BaseEntity(yearly=1000, increase=500)
        yearly_cumulative=entity.cum_yearly(5)
        excepted = np.array([1000,2500,4500,7000,10000], np.float64)
        assert np.array_equal(yearly_cumulative, excepted)
    
    def test_cum_yearly_with_increase_and_offset(self):
        entity=BaseEntity(yearly=1000, increase=500, offset=10000)
        yearly_cumulative=entity.cum_yearly(5)
        excepted = np.array([11000, 12500,14500,17000,20000], np.float64)
        assert np.array_equal(yearly_cumulative, excepted)
