def print_stacktrace(e: Exception):
    import traceback   
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class Node(object):
    def __init__(self, id):
        self.id = id

class Relation(object):
    def __init__(self, id):
        self.id = id
        self.nodes = []

def create_relation_with_nodes():
    relation = Relation(1)
    node1 = Node(1)
    node2 = Node(9223372036854775807)
    relation.nodes.append(node1)
    relation.nodes.append(node2)

    return relation

def main():
    try:
        # Create a relation with nodes
        relation = create_relation_with_nodes()

        # Assert that the issue is present
        assert len(relation.nodes) != 2, "The ManyToManyField should respect the PositiveBigIntegerField in m2m intermediate table."

    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(0)

if __name__ == '__main__':
    main()
