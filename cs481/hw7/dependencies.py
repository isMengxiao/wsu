"""
This module provides several functions to examine dependencies in mappings
(usually dictionaries).
>>> pass # Trivial module self-test: See individual self-tests.
"""


class CyclicDependency(Exception):
    """raised by allDependencies() when a cycle is detected.
    """
    pass


def dependersOn(node, deps):
    """returns all nodes that depend on `node`

    If a cycle is detected, it raises the `CyclicDependency` exception.

    Case 1: normal dependencies (using tuples)
    >>> allDependencies('c', { 'a': ('b', 'c'), 'd': ('a', 'c'), 'f': () })
    ['a', 'd']

    Case 2: direct dependence on itself (using a tuple)
    >>> allDependencies('a', { 'a': ('a',) })
    Traceback (most recent call last):
        ...
    CyclicDependency

    Case 3: indirect dependence on itself (using a tuple)
    >>> allDependencies('a', { 'a': ('b',), 'b': ('a',) })
    Traceback (most recent call last):
        ...
    CyclicDependency

    Case 4: dependency where order matters
    >>> deps = { 'b': ('a',) , 'd': ('a',), 'c': ('a',), 'd': ('c',)}
    >>> seq = allDependencies('a', deps)
    >>> seq
    ['b', 'c', 'd']
    >>> ordered(seq, deps)
    True

"""
    result = []
    for subNode in deps:
        if dependsOn(subNode, node, deps):
            if subNode == node:
                # Iff `node` has a `name` attribute, include it in the
                # exception's message.
                if 'name' in dir(node):
                    raise CyclicDependency(
                        "dependency cycle on {} detected".format(node.name))
                else:
                    raise CyclicDependency(
                        "dependency cycle detected")
            result.append(subNode)

    # Now do a swap sort to put the result in dependency order.
    swapped = True
    while swapped:
        swapped = False
        for i in range(1, len(result)):
            if dependsOn(result[i-1], result[i], deps):
                (result[i-1], result[i]) = (result[i], result[i-1])
                swap = True

    return result


def ordered(seq, deps):
    """returns True iff `seq` is in dependency-free order

    This means that no element in `seq` is preceded by any element that
    depends on it, so updating can occur in an in that order.
"""
    for i in range(len(seq)):
        for j in range(i, len(seq)):
            if dependsOn(seq[i], seq[j], deps):
                return False
    return True


def dependsOn(node, targetNode, deps):
    """detects when the calculation of one node depends on another

    It returns true iff `node` depends on `targetNode`. For
    instance, if "b = a + 3", then `b` depends on `a` but, unless
    there's a cycle (which would not be permitted), `a` does not depend
    on `b`. It does this by descending the dependency tree below
    `node` looking for a dependency on `targetNode`.

    Case 1: direct dependence on itself (using a tuple)
    >>> dependsOn('a', 'a', { 'a': ('a',) })
    True

    Case 2: one level of dependence (using sets)
    >>> dependsOn('a', 'c', { 'a': {'b', 'c'} })
    True

    Case 3: one level of independence (using sets)
    >>> dependsOn('b', 'a', { 'a': {'b',} })
    False

    Case 4: three levels of dependence (using sets)
    >>> dependsOn('a', 'c', { 'a': {'b',}, 'b': {'c',}, 'c': {'d',} })
    True

    Case 5: two levels of independence (using sets)
    >>> dependsOn('c', 'a', { 'a': {'b',}, 'b': {'c',}, 'c': {'d',} })
    False
"""
    if node not in deps:
        return False # `node` has no dependencies.

    # For each `childOfNode` that `node` depends on...
    for childOfNode in deps[node]:

        # If `targetNode` is `childOfNode`, there's a dependency: return True.
        if childOfNode == targetNode:
            return True

        # If `childOfNode` has dependencies and if there's a dependency below
        # `childOfNode`, we're done: return True.
        if childOfNode in deps and dependsOn(childOfNode, targetNode, deps):
            return True

    return False


def isCyclic(node, deps):
    """detects cyclic dependencies in mappings `node` -> sequence

    returns True iff a mapping of dependences `deps` contains cycles
    in the dependencies of `node`

    Case 1: direct dependence on itself (using a tuple)
    >>> isCyclic('a', { 'a': ('a',), 'b': (), 'c': () })
    True

    Case 2: one level of indirect dependence (using sets)
    >>> isCyclic('a', { 'a': {'b'}, 'b': {'a'}, 'c': () })
    True

    Case 3: three levels of indirect dependence (using sets)
    >>> isCyclic('a', { 'a': {'b'}, 'b': {'c'}, 'c': {'d'}, 'd': {'a'} })
    True

    Case 4: no dependence (using lists)
    >>> isCyclic('a', { 'a': ['b'], 'c': ['d'] })
    False
"""
    # A node that depends on itself is the definition of cyclic dependency.
    return dependsOn(node, node, deps)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
