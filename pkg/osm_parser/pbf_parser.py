"""Parser for osm pbf."""
from osmread import parse_file, Way, Node


def pbf_parser(file):
    """Pbf parser."""
    for entity in parse_file(file):
        if isinstance(entity, Node):
            print(f"Node: {entity}")
        if isinstance(entity, Way):
            print(f"Way: {entity}")
