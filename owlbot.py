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

common = gcp.CommonTemplates()

default_version = "v1"

for library in s.get_staging_dirs(default_version):
    # Rename `format_` to `format` to avoid breaking change
    s.replace(
        library / "google/cloud/**/types/resources.py",
        "format_",
        "format"
    )
    excludes = ["README.rst", "setup.py", "nox*.py", "docs/index.rst"]
    s.move(library, excludes=excludes)

s.remove_staging_dirs()

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(
    samples=True,
    microgenerator=True,
    cov_level=100,
)
s.move(templated_files, excludes=[".coveragerc"])  # microgenerator has a good .coveragerc file

# ----------------------------------------------------------------------------
# Samples templates
# ----------------------------------------------------------------------------
python.py_samples()

python.configure_previous_major_version_branches()

s.shell.run(["nox", "-s", "blacken"], hide_output=False)

# ----------------------------------------------------------------------------
# Repo specifics replacements
# ----------------------------------------------------------------------------

s.replace(
   "samples/api-client/accesstoken_example/noxfile.py",
   "# Copyright 2019 Google LLC",
   "# Copyright 2021 Google LLC"
)

s.replace(
   "samples/api-client/mqtt_example/noxfile.py",
   "# Copyright 2019 Google LLC",
   "# Copyright 2021 Google LLC"
)

s.replace(
   "scripts/readme-gen/templates/*.rst",
   "GoogleCloudPlatform/python-docs-samples",
   "googleapis/python-iot"
)

s.replace(
   "scripts/readme-gen/templates/*.rst",
   "python-docs-samples",
   "python-iot"
)
