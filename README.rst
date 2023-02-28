.. Copyright 2023 ClearBlade Inc.
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
        http://www.apache.org/licenses/LICENSE-2.0
    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
    Copyright 2022 Google LLC
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
        http://www.apache.org/licenses/LICENSE-2.0
    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
 
Python Client for ClearBlade Internet of Things (IoT) Core API
================================================================

Quick Start
-----------

In order to use this library, you first need to go through the following steps:

1. Install pip package - ```pip install clearblade-cloud-iot```


2. Set an environment variable **CLEARBLADE_CONFIGURATION** which should point to your clearblade service account json file.

3. Optionally set an environment variable **BINARYDATA_AND_TIME_GOOGLE_FORMAT** to True. Look at **Note about types of times and binaryData** below for details. 

Installation
~~~~~~~~~~~~

Install this library in a `virtualenv`_ using pip. `virtualenv`_ is a tool to
create isolated Python environments. The basic problem it addresses is one of
dependencies and versions, and indirectly permissions.

With `virtualenv`_, it's possible to install this library without needing system
install permissions, and without clashing with the installed system
dependencies.

.. _`virtualenv`: https://virtualenv.pypa.io/en/latest/


Code samples and snippets
~~~~~~~~~~~~~~~~~~~~~~~~~

Code samples and snippets live in the `samples/clearblade` folder.


Supported Python Versions
^^^^^^^^^^^^^^^^^^^^^^^^^
Our client libraries are compatible with all current `active`_ and `maintenance`_ versions of
Python.

Python >= 3.7

.. _active: https://devguide.python.org/devcycle/#in-development-main-branch
.. _maintenance: https://devguide.python.org/devcycle/#maintenance-branches

Unsupported Python Versions
^^^^^^^^^^^^^^^^^^^^^^^^^^^
Python <= 3.6

If you are using an `end-of-life`_
version of Python, we recommend that you update as soon as possible to an actively supported version.

.. _end-of-life: https://devguide.python.org/devcycle/#end-of-life-branches

Mac/Linux
^^^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    source <your-env>/bin/activate


Windows
^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    <your-env>\Scripts\activate

Next Steps
~~~~~~~~~~

- clone the github repository.

- and execute the setup.py file like , python setup.py install.

- mostly if you change you imports from from google.cloud to clearblade.cloud everything else should work.

Note about types of times and binaryData
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- By default the following parameters are returned as the shown types:

1. All time parameters (e.g. **cloudUpdateTime**, **deviceAckTime**, **updateTime**): **RFC3339** strings (e.g. "2023-01-12T23:38:07.732Z")
2. **CONFIG binaryData**: **base64-encoded string**
3. **STATE binaryData**: **NON-base64-encoded string**


- To return these parameters using the same types used by the **Google IoTCore Python SDK**, set environment variable **BINARYDATA_AND_TIME_GOOGLE_FORMAT** to **True** (case-insensitive string). This will ensure the following parameters are returned as the shown types:

1. All times: **DatetimeWithNanoseconds** (defined in the **proto.datetime_helpers** module)
2. All **binaryData** (CONFIG, STATE etc.): **BYTE ARRAYS**

- If this environment variable is not set, or is set to any unexpeced values, then the default types listed previously are used.