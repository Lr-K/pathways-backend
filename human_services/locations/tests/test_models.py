import unittest
from django.test import TestCase
from django.core import exceptions
from django.db import utils as django_utils
from human_services.locations.tests.helpers import LocationBuilder, ServiceLocationBuilder
from human_services.organizations.tests.helpers import OrganizationBuilder
from human_services.services.tests.helpers import ServiceBuilder

def validate_save_and_reload(instance):
    instance.save()
    instance.refresh_from_db()
    return instance

class TestLocationModel(TestCase):
    def setUp(self):
        self.organization = OrganizationBuilder().build()
        self.organization.save()

    def test_has_id_field(self):
        location_id = 'the_id'
        location = LocationBuilder(self.organization).with_id(location_id).build()
        location_from_db = validate_save_and_reload(location)
        self.assertEqual(location_from_db.id, location_id)

    def test_id_cannot_be_none(self):
        null_id = None
        location = LocationBuilder(self.organization).with_id(null_id).build()
        with self.assertRaises(exceptions.ValidationError):
            location.full_clean()

    def test_id_cannot_be_empty(self):
        empty_id = ''
        location = LocationBuilder(self.organization).with_id(empty_id).build()
        with self.assertRaises(exceptions.ValidationError):
            location.full_clean()

    def test_id_cannot_contain_space(self):
        location_id = 'the id'
        location = LocationBuilder(self.organization).with_id(location_id).build()
        with self.assertRaises(exceptions.ValidationError):
            location.full_clean()

    def test_has_name(self):
        name = 'The location name'
        location = LocationBuilder(self.organization).with_name(name).build()
        location_from_db = validate_save_and_reload(location)
        self.assertEqual(location_from_db.name, name)

    @unittest.expectedFailure
    def test_cannot_be_empty(self):
        name = ''
        location = LocationBuilder(self.organization).with_name(name).build()
        with self.assertRaises(exceptions.ValidationError):
            location.full_clean()

    def test_name_cannot_be_none(self):
        null_name = None
        location = LocationBuilder(self.organization).with_name(null_name).build()
        # Note that we're getting an integrity error from the database here,
        # haven't figured out how to make this fail validation which would be cleaner
        # and would also allow us invalidate on the empty string.
        with self.assertRaises(django_utils.IntegrityError):
            validate_save_and_reload(location)

    def test_has_latitude(self):
        latitude = 123.456
        location = LocationBuilder(self.organization).with_latitude(latitude).build()
        location_from_db = validate_save_and_reload(location)
        self.assertAlmostEqual(location_from_db.latitude, latitude)

    def test_has_longitude(self):
        longitude = 234.567
        location = LocationBuilder(self.organization).with_longitude(longitude).build()
        location_from_db = validate_save_and_reload(location)
        self.assertAlmostEqual(location_from_db.longitude, longitude)

    def test_latitude_and_longitude_can_both_be_null(self):
        location = (LocationBuilder(self.organization)
                    .with_latitude(None)
                    .with_longitude(None)
                    .build())
        location_from_db = validate_save_and_reload(location)
        self.assertEqual(location_from_db.latitude, None)
        self.assertEqual(location_from_db.longitude, None)

    def test_only_latitude_cannot_be_null(self):
        location = (LocationBuilder(self.organization)
                    .with_latitude(None)
                    .with_longitude(0.0)
                    .build())
        with self.assertRaises(exceptions.ValidationError):
            location.full_clean()

    def test_only_longitude_cannot_be_null(self):
        location = (LocationBuilder(self.organization)
                    .with_latitude(0.0)
                    .with_longitude(None)
                    .build())
        with self.assertRaises(exceptions.ValidationError):
            location.full_clean()

    def test_can_set_description(self):
        description = 'The location description'
        location = LocationBuilder(self.organization).with_description(description).build()
        location_from_db = validate_save_and_reload(location)
        self.assertEqual(location_from_db.description, description)

    def test_description_can_be_none(self):
        null_description = None
        location = LocationBuilder(self.organization).with_description(null_description).build()
        location_from_db = validate_save_and_reload(location)
        self.assertEqual(location_from_db.description, null_description)

    @unittest.expectedFailure
    def test_empty_description_is_saved_as_null(self):
        empty_description = ''
        null_description = None
        location = LocationBuilder(self.organization).with_description(empty_description).build()
        location_from_db = validate_save_and_reload(location)
        self.assertEqual(location_from_db.description, null_description)

    def test_description_is_multilingual(self):
        location = LocationBuilder(self.organization).build()

        self.set_description_in_language(location, 'en', 'In English')
        self.set_description_in_language(location, 'fr', 'En français')
        location_from_db = validate_save_and_reload(location)

        self.assert_description_in_language_equals(location_from_db, 'en', 'In English')
        self.assert_description_in_language_equals(location_from_db, 'fr', 'En français')

    def set_description_in_language(self, location, language, text):
        location.set_current_language(language)
        location.description = text

    def assert_description_in_language_equals(self, location, language, expected_text):
        location.set_current_language(language)
        self.assertEqual(location.description, expected_text)

class TestServiceLocationModel(TestCase):
    def setUp(self):
        self.organization = OrganizationBuilder().build()
        self.organization.save()

        self.service = ServiceBuilder(self.organization).build()
        self.service.save()

        self.location = LocationBuilder(self.organization).build()
        self.location.save()

    def test_has_service_field(self):
        service_at_location = ServiceLocationBuilder(self.service, self.location).build()
        service_location_from_db = validate_save_and_reload(service_at_location)
        self.assertEqual(service_location_from_db.service, self.service)

    def test_service_cannot_be_none(self):
        service_at_location = ServiceLocationBuilder(None, self.location).build()
        with self.assertRaises(exceptions.ValidationError):
            service_at_location.full_clean()

    def test_has_location_field(self):
        service_at_location = ServiceLocationBuilder(self.service, self.location).build()
        service_location_from_db = validate_save_and_reload(service_at_location)
        self.assertEqual(service_location_from_db.location, self.location)

    def test_location_cannot_be_none(self):
        service_at_location = ServiceLocationBuilder(self.service, None).build()
        with self.assertRaises(exceptions.ValidationError):
            service_at_location.full_clean()
