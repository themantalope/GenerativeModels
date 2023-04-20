
# Copyright (c) MONAI Consortium
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# To build with a different base image
# please run `docker build` using the `--build-arg PYTORCH_IMAGE=...` flag.
ARG PYTORCH_IMAGE=nvcr.io/nvidia/pytorch:22.10-py3
FROM ${PYTORCH_IMAGE}

LABEL maintainer="matthew.antalek@gmail.com"

WORKDIR /opt/monai 

COPY . .

RUN pip install -r requirements-dev.txt

RUN pip install -e .

ENV PATH=${PATH}:/opt/tools
ENV USERNAME="monai-docker-dev"

RUN ["chmod", "+x", "/opt/monai/docker-entrypoint.sh"]
ENTRYPOINT [ "/bin/bash", "/opt/monai/docker-entrypoint.sh" ]
CMD ["Docker"]
