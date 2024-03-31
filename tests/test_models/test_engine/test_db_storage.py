#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8
import unittest
DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""
        state1 = State(name="New York")
        state2 = State(name="California")
        city1 = City(name="New York City", state_id=state1.id)
        city2 = City(name="Los Angeles", state_id=state2.id)

        # Add objects to storage
        models.storage.new(state1)
        models.storage.new(state2)
        models.storage.new(city1)
        models.storage.new(city2)
        models.storage.save()

        # Retrieve all objects without passing a class
        all_objects = models.storage.all()

        # Check that all objects are retrieved
        self.assertEqual(len(all_objects), 4)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""
        state = State(name="New York")

        # Add the object to storage
        models.storage.new(state)
        models.storage.save()

        # Retrieve the State object using get method
        retrieved_state = models.storage.get(State, state.id)

        # Check if retrieved object is the same as the original
        self.assertEqual(retrieved_state, state)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""
        state = State(name="New York")

        # Add the object to storage
        models.storage.new(state)
        models.storage.save()

        # Reload storage to ensure saved changes are reflected
        models.storage.reload()

        # Retrieve the State object using get method
        retrieved_state = models.storage.get(State, state.id)

        # Check if retrieved object is the same as the original
        self.assertEqual(retrieved_state, state)

    def test_get_existing_object(self):
        """Test retrieving an existing object"""
        # Create a new State object
        state = State(name="California")
        storage.new(state)
        storage.save()

        # Retrieve the State object using get method
        retrieved_state = storage.get(State, state.id)

        # Check if retrieved object is the same as the original
        self.assertEqual(retrieved_state, state)

    def test_get_non_existing_object(self):
        """Test retrieving a non-existing object"""
        # Retrieve a non-existing City object
        retrieved_city = storage.get(City, "non_existing_id")

        # Check that the retrieved object is None
        self.assertIsNone(retrieved_city)

    def test_count_all_objects(self):
        """Test counting all objects in storage"""
        # Create some objects
        state1 = State(name="New York")
        state2 = State(name="Texas")
        city1 = City(name="New York City", state_id=state1.id)
        city2 = City(name="Houston", state_id=state2.id)

        # Add objects to storage
        storage.new(state1)
        storage.new(state2)
        storage.new(city1)
        storage.new(city2)
        storage.save()

        # Count all objects in storage
        count = storage.count()

        # Check that count matches the total number of objects
        self.assertEqual(count, 4)

    def test_count_objects_by_class(self):
        """Test counting objects of a specific class in storage"""
        # Create some objects
        state1 = State(name="California")
        state2 = State(name="Florida")
        city1 = City(name="Los Angeles", state_id=state1.id)
        city2 = City(name="Miami", state_id=state2.id)

        # Add objects to storage
        storage.new(state1)
        storage.new(state2)
        storage.new(city1)
        storage.new(city2)
        storage.save()

        # Count State objects in storage
        state_count = storage.count(State)

        # Check that state_count matches the number of State objects
        self.assertEqual(state_count, 2)

        # Count City objects in storage
        city_count = storage.count(City)

        # Check that city_count matches the number of City objects
        self.assertEqual(city_count, 2)
