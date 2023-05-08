<!-- "Copyright 2023 ClearBlade Inc."

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
https://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
Copyright 2018 Google LLC
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
https://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
Copyright 2023 ClearBlade Inc.
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
https://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
Copyright 2018 Google LLC
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
https://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License. -->

# 2.0.0 Migration Guide

The 2.0 release of the `clearblade-cloud-iot` client is a significant upgrade based on addition of two new classes in **iot_v1**:

- **DeviceCredential**
- **PublicKeyCredential**

The release also includes enhancements to these classes already present in **iot_v1**:

- **DeviceConfig**
- **DeviceState**

The version was made with the intent of minimizing required code changes. **However these changes should be considrered Breaking changes**.

#

1. If **device** is an object of class **Device**.

   **Before**:
   device.credentials is of type **[dict]** (i.e. list of dicts).

   **After**:
   device.credentials is of type **[DeviceCredential]** (i.e. list of objects of class DeviceCredential).

   The **DeviceCredential** class has these features for usability:

   - A **get** method that mimics the **get** method of a dict.
   - Allows accessing attributes using dot notation OR square-brackets.
   - Supports camel-case as well as snake-case for accessing attributes:

   e.g. All these are valid for retrieving the public key:

   - **public_key = device.credentials[0]['publicKey']**
   - **public_key = device.credentials[0]['public_key']**
   - **public_key = device.credentials[0].get('publicKey')**
   - **public_key = device.credentials[0].get('public_key')**
   - **public_key = device.credentials[0].publicKey**
   - **public_key = device.credentials[0].public_key**

#

2. This refers to pub_key mentioned in the previous section.

   **Before**:
   public_key was of type **dict**.

   **After**:
   public_key is an object of class **PublicKeyCredential**.

   The **PublicKeyCredential** class has these features for usability:

   - A **get** method that mimics the **get** method of a dict.
   - Allows accessing attributes using dot notation OR square-brackets.

   e.g. All these are valid for retrieving the public key format:

   - **format = public_key['format']**
   - **format = public_key.get('format')**
   - **format = public_key.format**

#

3. This section refers to **dev_config** which holds device config.

   **Before**:
   dev_config is of type **dict**.

   **After**:
   dev_config is an object of class **DeviceConfig**.

   The **DeviceConfig** class has these features for usability:

   - A **get** method that mimics the **get** method of a dict.
   - Allows accessing attributes using dot notation OR square-brackets.
   - Supports camel-case as well as snake-case for accessing attributes:

   e.g. All these are valid for retrieving the cloud_update_time:

   - **cloud_update_time = device.credentials[0]['cloudUpdateTime']**
   - **cloud_update_time = device.credentials[0]['cloud_update_time']**
   - **cloud_update_time = device.credentials[0].get('cloudUpdateTime')**
   - **cloud_update_time = device.credentials[0].get('cloud_update_time')**
   - **cloud_update_time = device.credentials[0].cloudUpdateTime**
   - **cloud_update_time = device.credentials[0].cloud_update_time**

#

4. This section refers to **dev_state** which contains device state.

   **Before**:
   dev_state is of type **dict**.

   **After**:
   dev_state is an object of class **DeviceState**.

   The **DeviceState** class has these features for usability:

   - A **get** method that mimics the **get** method of a dict.
   - Allows accessing attributes using dot notation OR square-brackets.
   - Supports camel-case as well as snake-case for accessing attributes:

   e.g. All these are valid for retrieving the binary_data:

   - **binary_data = device.credentials[0]['binaryData']**
   - **binary_data = device.credentials[0]['binary_data']**
   - **binary_data = device.credentials[0].get('binaryData')**
   - **binary_data = device.credentials[0].get('binary_data')**
   - **binary_data = device.credentials[0].binaryData**
   - **binary_data = device.credentials[0].binary_data**
