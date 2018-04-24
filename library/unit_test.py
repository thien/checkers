
import os
from core import checkers, game, mongo, population, tournament
from decision import mcts, splash, minimax
from agents import agent, geodude, human, magikarp, slowpoke
import random
random.seed(1)

import unittest

# class TestStringMethods(unittest.TestCase):

#   def test_upper(self):
#     self.assertEqual('foo'.upper(), 'FOO')

#   def test_isupper(self):
#     self.assertTrue('FOO'.isupper())
#     self.assertFalse('Foo'.isupper())

#   def test_split(self):
#     s = 'hello world'
#     self.assertEqual(s.split(), ['hello', 'world'])
#     # check that s.split fails when the separator is not a string
#     with self.assertRaises(TypeError):
#       s.split(2)

class PopulationTestCase(unittest.TestCase):
  def setUp(self):
    self.population = population.Population(15,4)

  def test_champSaveLocations(self):
    # checks champion save location
    k = os.path.realpath(self.population.folderDirectory)
    l = os.path.join("..","results","champions")
    l = os.path.realpath(l)
    self.assertEqual(k,l)

  def test_createMutations(self):
    self.assertEqual(1,1)

  def test_allocatePoints(self):
    before = self.population.printCurrentPopulationByPoints()
    for _ in range(0,100):
      k = random.choice(self.population.currentPopulation)
      l = random.choice(self.population.currentPopulation)
      # some fake result
      res = {"Winner" : k}
      self.population.allocatePoints(res, k,l)
    after = self.population.printCurrentPopulationByPoints()
    self.assertNotEqual(before, after)

  def test_safeMutations(self):
    self.population.debug = True
    self.population.safeMutations = True
    # generate fake moves
    (fakeMoves, coefs) = self.population.generateFakeMoves()
    for player_id in self.population.currentPopulation:
    # overload their neural net with fake coef and moves
      self.population.players[player_id].bot.nn.loadCoefficents(coefs)
      self.population.players[player_id].bot.cache = fakeMoves
    for _ in range(0,100):
      k = random.choice(self.population.currentPopulation)
      l = random.choice(self.population.currentPopulation)
      # some fake result
      res = {"Winner" : k}
      self.population.allocatePoints(res, k,l)

    self.population.sortCurrentPopulationByPoints()
    print(self.population.printCurrentPopulationByPoints())
    # generate the next population
    self.population.generateNextPopulation()
    # self.assert

def Testing():
  p = population.Population(15, 1)
  p.safeMutations = True
  
  (fakeMoves, coefs) = p.generateFakeMoves()
  
  for player_id in p.currentPopulation:
    # overload their neural net with fake coef and moves
    p.players[player_id].bot.nn.loadCoefficents(coefs)
    p.players[player_id].bot.cache = fakeMoves
  # overload fake tournament results
  for _ in range(0,100):
    k = random.choice(p.currentPopulation)
    l = random.choice(p.currentPopulation)
    # some fake result
    res = {"Winner" : k}
    p.allocatePoints(res, k,l)
  p.sortCurrentPopulationByPoints()
  print(p.printCurrentPopulationByPoints())
  p.addChampion()
  # generate the next population
  p.generateNextPopulation()
  print(p.currentPopulation)

if __name__ == '__main__':
  # unittest.main()
  Testing()