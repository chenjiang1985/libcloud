# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from libcloud.storage.types import Provider
from libcloud.storage.providers import get_driver

OSSDriver = get_driver(Provider.ALIYUN_OSS)

your_access_key_id = 'LTAI4FkVoatEeoJJSazFLY1h'
your_access_key_secret = 'zACYKVmUi7wyLo8YI3JhtTRQGqaxJX'
oss = OSSDriver('oss-cn-beijing.aliyuncs.com', your_access_key_id, your_access_key_secret)

container_name = 'medusa-bkt'
#object_name = 'me'
object_name = 'iZ2ze25p95hhdgrda1hcm7Z/1/meta/tokenmap.json'
local_file_path = '/Users/chenjiang/git/libcloud/LICENSE'
upload_object_name = 'OBJECT_NAME_FOR_UPLOAD_FILE'


obj = oss.get_object(container_name, object_name)
print('Got object %s:' % obj)


#for container in oss.iterate_containers():
#    print('container: %s' % container)

c1 = oss.get_container(container_name)
print('Got container %s:' % c1)




objects = c1.list_objects()
count = len(objects)
print('Has %d objects' % count)




objects = oss.list_container_objects(c1, ex_prefix='en')
print('Has %d objects with prefix "en"' % len(objects))
for each in objects:
    print(each)


obj = oss.get_object(container_name, object_name)
print('Got object %s:' % obj)

# Download object
oss.download_object(obj, "downloadfile", overwrite_existing=True)

for trunk in oss.download_object_as_stream(obj):
    print(trunk)

# Upload object
obj = oss.upload_object(local_file_path, c1, upload_object_name)

# Upload multipart
uploads = list(oss.ex_iterate_multipart_uploads(c1))
print('Found %d incompleted uploads' % len(uploads))
if len(uploads) > 0:
    oss.ex_abort_all_multipart_uploads(c1)
    print('Abort them all')


def data_iter(limit):
    i = 0
    while True:
        yield str(i).encode("utf-8")
        i += 1
        if i >= limit:
            break


print('Starting to upload 1MB using multipart api')
one_mb = 1024
obj = oss.upload_object_via_stream(data_iter(one_mb), c1, upload_object_name)
print('Finish uploading')

obj = oss.get_object(container_name, upload_object_name)
print('Got object %s:' % obj)

# Delete objects
#print('Delete object %s' % obj)
#oss.delete_object(obj)

# Create container
#  c2 = oss.create_container(container_name='20160117')
#  c2 = oss.create_container(container_name='20160117',
#  ex_location='oss-cn-beijing')
#  c2_got = oss.get_container('20160117')
