# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import copy
from taskgraph.transforms.base import TransformSequence
from taskgraph.util.schema import resolve_keyed_by

transforms = TransformSequence()

@transforms.add
def replace_bitrise_scheme_for_release_task(config, tasks):
    """
    This replaces `<release-type-scheme>` in all bitrise inputs to:

    - "FirefoxBeta" if the current release-type is beta
    - "Firefox" otherwise
    """

    # TODO: Replace this with `resolve_keyed_by` when https://github.com/taskcluster/taskgraph/pull/608 is merged

    schemes = ["FirefoxBeta"]
    if config.params.get("release_type") != "beta":
        schemes.append("Firefox")

    for task in tasks:
        task.setdefault("attributes", {})["release-type"] = config.params.get("release_type")

        for scheme in schemes:
            new_task = copy.deepcopy(task)
            new_task.setdefault("attributes", {})["build-type"] = scheme
            new_task['treeherder']['symbol'] = "Bb" if scheme == 'FirefoxBeta' else "B"
            new_task['name'] = new_task['name'] + '-' + scheme
            for workflow in new_task.get('bitrise', {}).get('workflows', {}):
                if isinstance(workflow, str):
                    continue
                for name, params in workflow.items():
                    for param in params:
                        for param_name, param_value in param.items():
                            param_value = param_value.replace("<release-type-scheme>", scheme)
                            param[param_name] = param_value

            yield new_task
