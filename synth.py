# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This script is used to synthesize generated parts of this library."""
import synthtool as s
from synthtool import gcp
from synthtool.languages import python

gapic = gcp.GAPICBazel()
common = gcp.CommonTemplates()
excludes = ["README.rst", "setup.py", "nox*.py", "docs/index.rst"]

# ----------------------------------------------------------------------------
# Generate iot GAPIC layer
# ----------------------------------------------------------------------------
library = gapic.py_library(
    service="iot",
    version="v1",
    bazel_target="//google/cloud/iot/v1:iot-v1-py",
    include_protos=True,
)
s.copy(library, excludes=excludes)

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(
    samples=True,
    microgenerator=True,
    cov_level=98,
)
s.move(templated_files, excludes=[".coveragerc"])  # microgenerator has a good .coveragerc file

# Rename `format_` to `format` to avoid breaking change
s.replace(
    "google/cloud/**/types/resources.py",
    "format_",
    "format"
)

# ----------------------------------------------------------------------------
# Samples templates
# ----------------------------------------------------------------------------
python.py_samples()


s.shell.run(["nox", "-s", "blacken"], hide_output=False)
