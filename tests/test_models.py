import pytest

from anom import Key, Model

from .models import Person


def test_constructor_params_must_be_valid_properties():
    with pytest.raises(TypeError):
        Person(name="Jim")


def test_model_adapter_instantiates_a_default_adapter_if_none_was_set():
    assert Person._adapter


def test_model_delete_fails_if_the_entity_was_never_saved():
    with pytest.raises(RuntimeError):
        person = Person()
        person.delete()


def test_model_instances_can_be_equal():
    person = Person()
    assert person == person
    assert Person(key=Key("Person", 1)) == Person(key=Key("Person", 1))
    assert Person(key=Key("Person", 1), first_name="John") == Person(key=Key("Person", 1), first_name="John")


def test_model_instances_can_not_be_equal():
    assert Person() != {}
    assert Person(key=Key("Person", 1)) != Person(key=Key("Person", 2))


def test_models_cannot_have_overlapping_kinds():
    class Overlapping(Model):
        pass

    with pytest.raises(TypeError):
        class Overlapping(Model):  # noqa
            pass


def test_model_reprs_can_be_used_to_rebuild_them():
    assert repr(Person(email="foo@example.com")) == "Person(key=Key('Person', parent=None, namespace=None), email='foo@example.com', first_name=None, last_name=None, parent=None)"  # noqa


def test_models_can_get_entities_by_id(person):
    assert Person.get_by_id(person.key.int_id) == person
