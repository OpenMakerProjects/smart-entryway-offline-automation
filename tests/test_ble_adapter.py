import unittest
from src.ble import schema,SERVICE,STATUS,CONTROL,publish
class FakeCharacteristic:
 value=None
class Fake:
 def __init__(self):self.characteristic=FakeCharacteristic();self.updated=False
 def get_characteristic(self,uuid):assert uuid==STATUS;return self.characteristic
 def update_value(self,service,uuid):assert service==SERVICE and uuid==STATUS;self.updated=True
class BLETests(unittest.TestCase):
 def test_status_encoding(self):
  s=Fake();publish(s,{"active":False});self.assertEqual(bytes(s.characteristic.value),b'{"active":false}');self.assertTrue(s.updated)
 def test_dependency_schema(self):
  try:import bless
  except ImportError:self.skipTest("BLE dependency smoke runs in completion CI")
  s=schema();self.assertEqual(set(s[SERVICE]),{STATUS,CONTROL})
