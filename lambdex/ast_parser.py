import ast
import typing
import inspect
import astcheck
import astsearch

__all__ = ['lambda_to_ast']


def _shallow_match_ast(node, pattern):
    if astcheck.is_ast_like(node, pattern):
        yield node

    for field, value in ast.iter_fields(node):
        if isinstance(value, list):
            for item in value:
                if isinstance(item, ast.AST):
                    yield from _shallow_match_ast(item, pattern)
        elif isinstance(value, ast.AST):
            yield from _shallow_match_ast(value, pattern)


def lambda_to_ast(lambda_object: typing.Callable, *, keyword: str, identifier: str = ''):
    source_str = inspect.getsource(lambda_object.__code__)
    tree = ast.parse(source_str).body[0]
    pattern = astsearch.prepare_pattern('{}{}(?)'.format(keyword, '.' + identifier if identifier else ''))
    matched = list(_shallow_match_ast(tree, pattern))

    if not len(matched):
        raise SyntaxError('Cannot parse lambda for unknown reason')

    if len(matched) > 1:
        raise SyntaxError('Ambiguious identifier {!r}'.format(identifier))

    assert isinstance(matched[0], ast.Call)

    return matched[0]
