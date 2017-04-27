# -*- coding: utf-8 -*-
# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:

from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import unittest
import gdb

from crash.infra import delayed_init, exporter, export

# The delayed init tests check for presence of an attribute in the instance
# dict (or class dict for class attributes) since hasattr() will call
# __getattr__, causing delayed initialization to occur.

class TestInfra(unittest.TestCase):
    def test_delayed_init_valid_attribute(self):
        @delayed_init
        class test_class(object):
            def __init__(self):
                self.x = 100

        inst = test_class()

        self.assertFalse('x' in inst.__dict__)
        self.assertTrue(inst.x == 100)
        self.assertTrue('x' in inst.__dict__)

    def test_delayed_init_invalid_attribute(self):
        @delayed_init
        class test_class(object):
            def __init__(self):
                self.x = 100

        inst = test_class()

        self.assertFalse('x' in inst.__dict__)
        with self.assertRaises(AttributeError):
            y = inst.y
        self.assertTrue(inst.x == 100)

    def test_delayed_init_with_initial_assignment(self):
        @delayed_init
        class test_class(object):
            def __init__(self):
                self.is_valid = True
                self.x = 100
                self.y = 100

        inst = test_class()
        self.assertFalse('x' in inst.__dict__)
        inst.x = 101
        self.assertTrue(inst.x == 101)
        self.assertTrue(inst.y == 100)

    def test_delayed_init_with_class_attributes(self):
        @delayed_init
        class test_class(object):
            classattr = 'someval'
            def __init__(self):
                self.is_valid = True

        inst1 = test_class()
        inst2 = test_class()

        self.assertFalse('is_valid' in inst1.__dict__)
        self.assertFalse('someval' in inst1.__dict__)
        self.assertFalse('classattr' in inst1.__dict__)
        self.assertTrue('classattr' in inst1.__class__.wrapped_class.__dict__)

        self.assertTrue(inst1.classattr == 'someval')
        self.assertFalse('is_valid' in inst1.__dict__)

        inst1.someval = False
        self.assertTrue(inst1.is_valid)

        self.assertTrue(inst1.classattr == 'someval')
        self.assertTrue(hasattr(inst1, 'is_valid'))
        self.assertTrue(inst1.is_valid == True)

        self.assertTrue(inst2.classattr == 'someval')
        self.assertFalse('is_valid' in inst2.__dict__)

    def test_delayed_init_with_class_attributes_assigned_after_creation(self):
        @delayed_init
        class test_class(object):
            def __init__(self):
                self.is_valid = True
                setattr(test_class, 'classattr', 'someval')

        inst1 = test_class()
        inst2 = test_class()

        self.assertFalse('classattr' in inst1.__dict__)
        self.assertFalse('classattr' in inst1.__class__.__dict__)
        self.assertTrue(inst1.classattr == 'someval')
        self.assertTrue(inst1.is_valid == True)

        self.assertFalse('classattr' in inst1.__dict__)
        self.assertTrue('classattr' in inst1.__class__.__dict__)
        self.assertTrue(inst2.classattr == 'someval')

    def test_exporter_alone(self):
        @exporter
        class test_class(object):
            @export
            def test_func(self):
                return 101

        self.assertTrue(test_func() == 101)

    def test_exporter_baseline_without_delayed_init(self):
        @exporter
        class test_class(object):
            inited = False
            def __init__(self):
                self.retval = 1020
                setattr(self.__class__, 'inited', True)
            @export
            def test_func(self):
                return self.retval

        x = test_class()
        self.assertTrue(x.inited)

        self.assertTrue(test_class.inited)
        self.assertTrue(test_func() == 1020)
        self.assertTrue(test_class.inited)

    def test_exporter_then_delayed_init(self):
        @delayed_init
        @exporter
        class test_class(object):
            inited = False
            def __init__(self):
                self.retval = 1021
                setattr(self.__class__, 'inited', True)
            @export
            def test_func(self):
                return self.retval

        x = test_class()
        self.assertFalse(x.inited)

        self.assertFalse(test_class.inited)
        self.assertTrue(test_func() == 1021)
        self.assertTrue(test_class.inited)

    def test_delayed_init_then_exporter(self):
        @exporter
        @delayed_init
        class test_class(object):
            inited = False
            def __init__(self):
                self.retval = 1022
                setattr(self.__class__, 'inited', True)
            @export
            def test_func(self):
                return self.retval

        x = test_class()
        self.assertFalse(x.inited)

        self.assertFalse(test_class.inited)
        self.assertTrue(test_func() == 1022)
        self.assertTrue(test_class.inited)

    def test_export_normal(self):
        @exporter
        class test_class(object):
            @export
            def test_func(self):
                return 104

        self.assertTrue(test_func() == 104)

    def test_static_export(self):
        @exporter
        class test_class(object):
            @staticmethod
            @export
            def test_func():
                return 1050

        self.assertTrue(test_func() == 1050)

    def test_export_static(self):
        @exporter
        class test_class(object):
            @export
            @staticmethod
            def test_func():
                return 105

        self.assertTrue(test_func() == 105)

    def test_export_class(self):
        @exporter
        class test_class(object):
            @classmethod
            @export
            def test_func(self):
                return 106

        self.assertTrue(test_func() == 106)

    def test_export_multiple_exports_one_instance(self):
        @exporter
        class test_class(object):
            instances = 0
            def __init__(self):
                setattr(self.__class__, 'instances', self.instances + 1)

            @export
            def test_func(self):
                return 1060
            @export
            def test_func2(self):
                return 1061

        self.assertTrue(test_class.instances == 0)
        self.assertTrue(test_func() == 1060)
        self.assertTrue(test_class.instances == 1)
        self.assertTrue(test_func() == 1060)
        self.assertTrue(test_class.instances == 1)
        self.assertTrue(test_func2() == 1061)
        self.assertTrue(test_class.instances == 1)
        self.assertTrue(test_func2() == 1061)
        self.assertTrue(test_class.instances == 1)

    def test_delayed_init_with_getattr(self):
        @delayed_init
        class test_class(object):
            def __getattr__(self, name):
                if name == 'foo':
                    return 'bar'
                raise AttributeError

        x = test_class()

        self.assertTrue(x.foo == 'bar')

    def test_delayed_init_with_parent(self):
        class test_parent_class(object):
            def __init__(self):
                self.x = 107
                pass

        @delayed_init
        class test_class(test_parent_class):
            def __init__(self):
                test_parent_class.__init__(self)

        x = test_class()
        self.assertTrue(x.x == 107)

    def test_delayed_init_with_super(self):
        class test_parent_class(object):
            def __init__(self):
                pass

        @delayed_init
        class test_class(test_parent_class):
            def __init__(self):
                super(test_class, self).__init__() # infinite recursion

        x = test_class()
        with self.assertRaises(RuntimeError):
            print(x.x)
