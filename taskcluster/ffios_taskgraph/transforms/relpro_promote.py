# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from taskgraph.transforms.base import TransformSequence
from taskgraph.util.schema import resolve_keyed_by

transforms = TransformSequence()

@transforms.add
def this_should_mostly_be_an_optimization_but_pain(config, tasks):
    # TODO: Replace this with `resolve_keyed_by` when https://github.com/taskcluster/taskgraph/pull/608 is merged

    scheme = "Firefox"
    if config.params.get("release_type") == "beta":
        scheme = "FirefoxBeta"

    for task in tasks:
        print(task)
        if config.params.get("release_type") == "beta":
            if task["attributes"]["build-type"] == "release":
                continue

        task.setdefault("attributes", {})["release-type"] = config.params.get("release_type")

        yield task
