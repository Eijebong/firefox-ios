# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import copy
from taskgraph.transforms.base import TransformSequence
from taskgraph.util.schema import resolve_keyed_by

transforms = TransformSequence()

@transforms.add
def replace_bitrise_scheme_for_release_task(config, tasks):
    for task in tasks:
        resolve_keyed_by(task, 'treeherder.symbol', task["name"], **{'build-type': task['attributes']['build-type']})
        yield task
