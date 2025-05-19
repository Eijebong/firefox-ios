import copy
from taskgraph.transforms.base import TransformSequence
from taskgraph.util.schema import resolve_keyed_by


transforms = TransformSequence()

@transforms.add
def replace_bitrise_scheme_for_release_task(config, tasks):
    for task in tasks:
        resolve_keyed_by(task, 'treeherder.symbol', task["name"], **{'build-type': task['attributes']['build-type']})
        yield task
