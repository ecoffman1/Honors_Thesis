from rdflib import Graph, Namespace, URIRef, Literal

MODBUS = Namespace("http://example.org/modbus#")

def add_context(register, function, value, data_type, notes):
    g = Graph()
    modbus_device = URIRef(f"http://example.org/modbus/register/{register}")
    g.add((modbus_device, MODBUS.function, Literal(function)))
    g.add((modbus_device, MODBUS.value, Literal(value)))
    g.add((modbus_device, MODBUS.type, Literal(data_type)))
    g.add((modbus_device, MODBUS.notes, Literal(notes)))

    return g.serialize(format="turtle")