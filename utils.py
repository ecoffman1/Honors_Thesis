from rdflib import Graph, Namespace, URIRef, Literal

MODBUS = Namespace("http://example.org/modbus#")

def add_context(value):
    g = Graph()
    modbus_device = URIRef("http://example.org/device/1")
    g.add((modbus_device, MODBUS.hasValue, Literal(value)))
    return g.serialize(format="turtle")
