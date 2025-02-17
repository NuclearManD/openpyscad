# -*- coding: utf-8 -*-
import unittest
import os 
from openpyscad import *


class TestBaseObject(unittest.TestCase):

    def test_init(self):
        c = Cube(size=[10, 10, 10])
        self.assertEqual(c.dumps(), "cube(size=[10, 10, 10]);\n")

    def test_retrieve_value(self):
        o = BaseObject()
        setattr(o, "test", None)
        self.assertIsNone(o._retrieve_value("test"))

        setattr(o, "test", "value")
        self.assertEqual(o._retrieve_value("test"), "\"value\"")

        setattr(o, "test", 123)
        self.assertEqual(o._retrieve_value("test"), "123")

    def test_get_params(self):
        o = Cylinder(r=10, _fn=10)
        self.assertEqual(o._get_params(), "r=10, $fn=10")

        o = Color("Red")
        self.assertEqual(o._get_params(), "\"Red\"")

    def test_get_children_content(self):
        o = Union()
        self.assertEqual(o._get_children_content(), "")

        o = Union().append(Cube(10))
        self.assertEqual(o._get_children_content(), "cube(size=10);\n")
        self.assertEqual(o._get_children_content(1), "    cube(size=10);\n")

    def test_get_content(self):
        o = Union()
        self.assertEqual(o._get_content(), "")

        o = Union().append(Cube(10))
        self.assertEqual(o._get_content(), "{\n    cube(size=10);\n}")
        self.assertEqual(o._get_content(1), "{\n        cube(size=10);\n    }")

    def test_append(self):
        o = Cube(size=10)
        with self.assertRaises(TypeError):
            o.append(Cube(size=10))

        c1 = Cube(size=10)
        c2 = Cube(size=20)
        o = Union()
        o.append((c1, c2))
        self.assertEqual(o.children, [c1, c2])

        o = Union()
        o.append(c1)
        self.assertEqual(o.children, [c1])

    def test_dump(self):
        try:
            from StringIO import StringIO
        except ImportError:
            from io import StringIO
        sio = StringIO()
        c1 = Cube(size=10)
        c1.dump(sio)
        self.assertEqual(sio.getvalue(), "cube(size=10);\n")

    def test_dumps(self):
        c1 = Cube(size=10)
        self.assertEqual(c1.dumps(), "cube(size=10);\n")

    def test_write(self):
        from unittest.mock import mock_open, patch
        c1 = Cube(size=10)
        m_open = mock_open()
        try:
            with patch("__builtin__.open", m_open):
                c1.write("sample", with_print=True)
        except:
            with patch("builtins.open", m_open):
                c1.write("sample", with_print=True)
        

        m_open.assert_called_once_with("sample", "w")
        handle = m_open()
        handle.write.assert_called_once_with("cube(size=10);\n")

    def test_clone(self):
        c1 = Cube(size=10)
        c2 = c1.clone()
        self.assertEqual(c1.size, c2.size)

    def test_equals(self):
        c1 = Cube(size=10)
        c2 = Cube(size=10)
        self.assertTrue(c1.equals(c2))

        c2 = Cylinder(10)
        self.assertFalse(c1.equals(c2))

        c2 = Cube(size=20)
        self.assertFalse(c1.equals(c2))

    def test_str(self):
        c1 = Cube(size=10)
        self.assertEqual(str(c1), "cube(size=10);\n")

    def test_add_3d(self):
        o = Empty()
        c1 = Cube(10)
        self.assertTrue((o + c1).equals(c1))
        
        u = Union()
        u1 = u + c1
        self.assertTrue(u1.children[0].equals(c1))
        
        c2 = Cube(20)
        u2 = c1 + c2
        self.assertTrue(u2.children[0].equals(c1))
        self.assertTrue(u2.children[1].equals(c2))

    def test_sub_3d(self):
        o = Empty()
        c1 = Cube(10)
        self.assertTrue((o - c1).equals(c1))

        d = Difference()
        d1 = d - c1
        self.assertTrue(d1.children[0].equals(c1))

        c2 = Cube(20)
        d2 = c1 - c2
        self.assertTrue(d2.children[0].equals(c1))
        self.assertTrue(d2.children[1].equals(c2))

    def test_add_2d(self):
        o = Empty()
        c1 = Square(10)
        self.assertTrue((o + c1).equals(c1))

        u = Union()
        u1 = u + c1
        self.assertTrue(u1.children[0].equals(c1))

        c2 = Square(20)
        u2 = c1 + c2
        self.assertTrue(u2.children[0].equals(c1))
        self.assertTrue(u2.children[1].equals(c2))

    def test_sub_2d(self):
        o = Empty()
        c1 = Square(10)
        self.assertTrue((o - c1).equals(c1))

        d = Difference()
        d1 = d - c1
        self.assertTrue(d1.children[0].equals(c1))

        c2 = Square(20)
        d2 = c1 - c2
        self.assertTrue(d2.children[0].equals(c1))
        self.assertTrue(d2.children[1].equals(c2))

    def test_and(self):
        o = Empty()
        c1 = Cube(10)
        self.assertTrue((o & c1).equals(c1))

        i = Intersection()
        i1 = i & c1
        self.assertTrue(i1.children[0].equals(c1))

        c2 = Cube(20)
        i2 = c1 & c2
        self.assertTrue(i2.children[0].equals(c1))
        self.assertTrue(i2.children[1].equals(c2))

    def test_translate(self):
        o = Cube(10)
        o1 = o.translate([10, 10, 10])
        self.assertTrue(isinstance(o1, Translate))
        self.assertEqual(o1.children, [o])
        self.assertEqual(o1.v, [10, 10, 10])
        
    def test_rotate(self):
        o = Cube(10)
        o1 = o.rotate([10, 10, 10])
        self.assertTrue(isinstance(o1, Rotate))
        self.assertEqual(o1.children, [o])
        self.assertEqual(o1.a, [10, 10, 10])
        
    def test_scale(self):
        o = Cube(10)
        o1 = o.scale([10, 10, 10])
        self.assertTrue(isinstance(o1, Scale))
        self.assertEqual(o1.children, [o])
        self.assertEqual(o1.v, [10, 10, 10])

    def test_resize(self):
        o = Cube(10)
        o1 = o.resize([10, 10, 10])
        self.assertTrue(isinstance(o1, Resize))
        self.assertEqual(o1.children, [o])

    def test_mirror(self):
        o = Cube(10)
        o1 = o.mirror([1, 1, 1])
        self.assertTrue(isinstance(o1, Mirror))
        self.assertEqual(o1.children, [o])
        
    def test_color(self):
        o = Cube(10)
        o1 = o.color("Red")
        self.assertTrue(isinstance(o1, Color))
        self.assertEqual(o1.children, [o])

    def test_offset(self):
        o = Circle(10)
        o1 = o.offset([10, 10, 10])
        self.assertTrue(isinstance(o1, Offset))
        self.assertEqual(o1.children, [o])

        o = Cube(10)
        with self.assertRaises(TypeError):
            o.offset([10, 10, 10])

    def test_hull(self):
        c = Cube(10)
        s = Sphere(3)
        s = s.translate([8, 0, 0])
        h = (c + s).hull()
        self.assertTrue('hull' in h.dumps())

    def test_minkowski(self):
        c = Cube(10)
        s = Sphere(3)
        s = s.translate([8, 0, 0]) 
        h = (c + s).minkowski()
        self.assertTrue('minkowski' in h.dumps())

    def test_linear_extrude(self):
        o = Circle(10)
        o1 = o.linear_extrude(height=1.6)
        self.assertTrue(isinstance(o1, Linear_Extrude))
        self.assertEqual(o1.children, [o])
    
    def test_rotate_extrude(self):
        o = Circle(10)
        o1 = o.rotate_extrude()
        self.assertTrue(isinstance(o1, Rotate_Extrude))
        self.assertEqual(o1.children, [o])
    
    def test_scad_write(self):
        sc = Scad(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','example','example.scad')) 
        self.assertTrue('example' in sc.dumps())
        sc.write('example_module.scad')

    def test_scad(self):
        o = Sphere(3)
        sc = Scad(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','example','example.scad'))
        osc = o + sc 
        self.assertTrue('example' in osc.dumps())

    def test_import(self):
        o = Sphere(3)
        sc = Import(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','example','example.stl'))
        osc = o + sc 
        self.assertTrue('example.stl' in osc.dumps())

    def test_is_2d(self):
        s1 = Square(10)
        s2 = Square(20)
        c1 = Cube(10)
        c2 = Cube(20)

        d1 = s1 - s2
        self.assertTrue(d1._is_2d())

        d2 = c1 - c2
        self.assertFalse(d2._is_2d())

        a1 = s1 + s2
        self.assertTrue(a1._is_2d())

        a2 = c1 + c2
        self.assertFalse(a2._is_2d())
