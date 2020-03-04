"""Generated client library for speech version v1p1beta1."""
# NOTE: This file is autogenerated and should not be edited by hand.
from apitools.base.py import base_api
from googlecloudsdk.third_party.apis.speech.v1p1beta1 import speech_v1p1beta1_messages as messages


class SpeechV1p1beta1(base_api.BaseApiClient):
  """Generated client library for service speech version v1p1beta1."""

  MESSAGES_MODULE = messages
  BASE_URL = u'https://speech.googleapis.com/'
  MTLS_BASE_URL = u'https://speech.mtls.googleapis.com/'

  _PACKAGE = u'speech'
  _SCOPES = [u'https://www.googleapis.com/auth/cloud-platform']
  _VERSION = u'v1p1beta1'
  _CLIENT_ID = '1042881264118.apps.googleusercontent.com'
  _CLIENT_SECRET = 'x_Tw5K8nnjoRAqULM9PFAC2b'
  _USER_AGENT = 'x_Tw5K8nnjoRAqULM9PFAC2b'
  _CLIENT_CLASS_NAME = u'SpeechV1p1beta1'
  _URL_VERSION = u'v1p1beta1'
  _API_KEY = None

  def __init__(self, url='', credentials=None,
               get_credentials=True, http=None, model=None,
               log_request=False, log_response=False,
               credentials_args=None, default_global_params=None,
               additional_http_headers=None, response_encoding=None):
    """Create a new speech handle."""
    url = url or self.BASE_URL
    super(SpeechV1p1beta1, self).__init__(
        url, credentials=credentials,
        get_credentials=get_credentials, http=http, model=model,
        log_request=log_request, log_response=log_response,
        credentials_args=credentials_args,
        default_global_params=default_global_params,
        additional_http_headers=additional_http_headers,
        response_encoding=response_encoding)
    self.operations = self.OperationsService(self)
    self.projects_locations_datasets = self.ProjectsLocationsDatasetsService(self)
    self.projects_locations_log_data_stats = self.ProjectsLocationsLogDataStatsService(self)
    self.projects_locations_models = self.ProjectsLocationsModelsService(self)
    self.projects_locations_operations = self.ProjectsLocationsOperationsService(self)
    self.projects_locations = self.ProjectsLocationsService(self)
    self.projects = self.ProjectsService(self)
    self.speech = self.SpeechService(self)

  class OperationsService(base_api.BaseApiService):
    """Service class for the operations resource."""

    _NAME = u'operations'

    def __init__(self, client):
      super(SpeechV1p1beta1.OperationsService, self).__init__(client)
      self._upload_configs = {
          }

    def Get(self, request, global_params=None):
      r"""Gets the latest state of a long-running operation.  Clients can use this.
method to poll the operation result at intervals as recommended by the API
service.

      Args:
        request: (SpeechOperationsGetRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Operation) The response message.
      """
      config = self.GetMethodConfig('Get')
      return self._RunMethod(
          config, request, global_params=global_params)

    Get.method_config = lambda: base_api.ApiMethodInfo(
        flat_path=u'v1p1beta1/operations/{operationsId}',
        http_method=u'GET',
        method_id=u'speech.operations.get',
        ordered_params=[u'name'],
        path_params=[u'name'],
        query_params=[],
        relative_path=u'v1p1beta1/operations/{+name}',
        request_field='',
        request_type_name=u'SpeechOperationsGetRequest',
        response_type_name=u'Operation',
        supports_download=False,
    )

    def List(self, request, global_params=None):
      r"""Lists operations that match the specified filter in the request. If the.
server doesn't support this method, it returns `UNIMPLEMENTED`.

NOTE: the `name` binding allows API services to override the binding
to use different resource name schemes, such as `users/*/operations`. To
override the binding, API services can add a binding such as
`"/v1/{name=users/*}/operations"` to their service configuration.
For backwards compatibility, the default name includes the operations
collection id, however overriding users must ensure the name binding
is the parent resource, without the operations collection id.

      Args:
        request: (SpeechOperationsListRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ListOperationsResponse) The response message.
      """
      config = self.GetMethodConfig('List')
      return self._RunMethod(
          config, request, global_params=global_params)

    List.method_config = lambda: base_api.ApiMethodInfo(
        http_method=u'GET',
        method_id=u'speech.operations.list',
        ordered_params=[],
        path_params=[],
        query_params=[u'filter', u'name', u'pageSize', u'pageToken'],
        relative_path=u'v1p1beta1/operations',
        request_field='',
        request_type_name=u'SpeechOperationsListRequest',
        response_type_name=u'ListOperationsResponse',
        supports_download=False,
    )

  class ProjectsLocationsDatasetsService(base_api.BaseApiService):
    """Service class for the projects_locations_datasets resource."""

    _NAME = u'projects_locations_datasets'

    def __init__(self, client):
      super(SpeechV1p1beta1.ProjectsLocationsDatasetsService, self).__init__(client)
      self._upload_configs = {
          }

    def Create(self, request, global_params=None):
      r"""Creates a new dataset for custom model training. The name of created.
dataset is stored in `response.metadata.works_on` field. Metadata type
is SpeechOperationMetadata. Response type is Empty.

      Args:
        request: (SpeechProjectsLocationsDatasetsCreateRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Operation) The response message.
      """
      config = self.GetMethodConfig('Create')
      return self._RunMethod(
          config, request, global_params=global_params)

    Create.method_config = lambda: base_api.ApiMethodInfo(
        flat_path=u'v1p1beta1/projects/{projectsId}/locations/{locationsId}/datasets',
        http_method=u'POST',
        method_id=u'speech.projects.locations.datasets.create',
        ordered_params=[u'parent'],
        path_params=[u'parent'],
        query_params=[],
        relative_path=u'v1p1beta1/{+parent}/datasets',
        request_field=u'dataset',
        request_type_name=u'SpeechProjectsLocationsDatasetsCreateRequest',
        response_type_name=u'Operation',
        supports_download=False,
    )

    def Delete(self, request, global_params=None):
      r"""Deletes the named automl dataset. Returns an Empty response.

      Args:
        request: (SpeechProjectsLocationsDatasetsDeleteRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Operation) The response message.
      """
      config = self.GetMethodConfig('Delete')
      return self._RunMethod(
          config, request, global_params=global_params)

    Delete.method_config = lambda: base_api.ApiMethodInfo(
        flat_path=u'v1p1beta1/projects/{projectsId}/locations/{locationsId}/datasets/{datasetsId}',
        http_method=u'DELETE',
        method_id=u'speech.projects.locations.datasets.delete',
        ordered_params=[u'name'],
        path_params=[u'name'],
        query_params=[],
        relative_path=u'v1p1beta1/{+name}',
        request_field='',
        request_type_name=u'SpeechProjectsLocationsDatasetsDeleteRequest',
        response_type_name=u'Operation',
        supports_download=False,
    )

    def Get(self, request, global_params=None):
      r"""Get the dataset associated with the dataset resource.

      Args:
        request: (SpeechProjectsLocationsDatasetsGetRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Dataset) The response message.
      """
      config = self.GetMethodConfig('Get')
      return self._RunMethod(
          config, request, global_params=global_params)

    Get.method_config = lambda: base_api.ApiMethodInfo(
        flat_path=u'v1p1beta1/projects/{projectsId}/locations/{locationsId}/datasets/{datasetsId}',
        http_method=u'GET',
        method_id=u'speech.projects.locations.datasets.get',
        ordered_params=[u'name'],
        path_params=[u'name'],
        query_params=[u'includeModelInfo'],
        relative_path=u'v1p1beta1/{+name}',
        request_field='',
        request_type_name=u'SpeechProjectsLocationsDatasetsGetRequest',
        response_type_name=u'Dataset',
        supports_download=False,
    )

    def List(self, request, global_params=None):
      r"""Fetch the list of dataset associated with this project.

      Args:
        request: (SpeechProjectsLocationsDatasetsListRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ListDatasetsResponse) The response message.
      """
      config = self.GetMethodConfig('List')
      return self._RunMethod(
          config, request, global_params=global_params)

    List.method_config = lambda: base_api.ApiMethodInfo(
        flat_path=u'v1p1beta1/projects/{projectsId}/locations/{locationsId}/datasets',
        http_method=u'GET',
        method_id=u'speech.projects.locations.datasets.list',
        ordered_params=[u'parent'],
        path_params=[u'parent'],
        query_params=[u'filter', u'includeModelInfo', u'pageSize', u'pageToken'],
        relative_path=u'v1p1beta1/{+parent}/datasets',
        request_field='',
        request_type_name=u'SpeechProjectsLocationsDatasetsListRequest',
        response_type_name=u'ListDatasetsResponse',
        supports_download=False,
    )

    def RefreshData(self, request, global_params=None):
      r"""Refresh data for a dataset. Returns an Empty response.

      Args:
        request: (SpeechProjectsLocationsDatasetsRefreshDataRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Operation) The response message.
      """
      config = self.GetMethodConfig('RefreshData')
      return self._RunMethod(
          config, request, global_params=global_params)

    RefreshData.method_config = lambda: base_api.ApiMethodInfo(
        flat_path=u'v1p1beta1/projects/{projectsId}/locations/{locationsId}/datasets/{datasetsId}:refreshData',
        http_method=u'POST',
        method_id=u'speech.projects.locations.datasets.refreshData',
        ordered_params=[u'name'],
        path_params=[u'name'],
        query_params=[],
        relative_path=u'v1p1beta1/{+name}:refreshData',
        request_field=u'refreshDataRequest',
        request_type_name=u'SpeechProjectsLocationsDatasetsRefreshDataRequest',
        response_type_name=u'Operation',
        supports_download=False,
    )

  class ProjectsLocationsLogDataStatsService(base_api.BaseApiService):
    """Service class for the projects_locations_log_data_stats resource."""

    _NAME = u'projects_locations_log_data_stats'

    def __init__(self, client):
      super(SpeechV1p1beta1.ProjectsLocationsLogDataStatsService, self).__init__(client)
      self._upload_configs = {
          }

    def List(self, request, global_params=None):
      r"""Lists all log data stats associated with requested project.

      Args:
        request: (SpeechProjectsLocationsLogDataStatsListRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ListLogDataStatsResponse) The response message.
      """
      config = self.GetMethodConfig('List')
      return self._RunMethod(
          config, request, global_params=global_params)

    List.method_config = lambda: base_api.ApiMethodInfo(
        flat_path=u'v1p1beta1/projects/{projectsId}/locations/{locationsId}/log_data_stats',
        http_method=u'GET',
        method_id=u'speech.projects.locations.log_data_stats.list',
        ordered_params=[u'parent'],
        path_params=[u'parent'],
        query_params=[],
        relative_path=u'v1p1beta1/{+parent}/log_data_stats',
        request_field='',
        request_type_name=u'SpeechProjectsLocationsLogDataStatsListRequest',
        response_type_name=u'ListLogDataStatsResponse',
        supports_download=False,
    )

  class ProjectsLocationsModelsService(base_api.BaseApiService):
    """Service class for the projects_locations_models resource."""

    _NAME = u'projects_locations_models'

    def __init__(self, client):
      super(SpeechV1p1beta1.ProjectsLocationsModelsService, self).__init__(client)
      self._upload_configs = {
          }

    def Create(self, request, global_params=None):
      r"""Creates a new custom model. Metadata type is SpeechOperationMetadata.
Response type is Model.

      Args:
        request: (SpeechProjectsLocationsModelsCreateRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Operation) The response message.
      """
      config = self.GetMethodConfig('Create')
      return self._RunMethod(
          config, request, global_params=global_params)

    Create.method_config = lambda: base_api.ApiMethodInfo(
        flat_path=u'v1p1beta1/projects/{projectsId}/locations/{locationsId}/models',
        http_method=u'POST',
        method_id=u'speech.projects.locations.models.create',
        ordered_params=[u'parent'],
        path_params=[u'parent'],
        query_params=[u'name'],
        relative_path=u'v1p1beta1/{+parent}/models',
        request_field=u'model',
        request_type_name=u'SpeechProjectsLocationsModelsCreateRequest',
        response_type_name=u'Operation',
        supports_download=False,
    )

    def Delete(self, request, global_params=None):
      r"""Deletes the named automl model. Returns an Empty response.

      Args:
        request: (SpeechProjectsLocationsModelsDeleteRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Operation) The response message.
      """
      config = self.GetMethodConfig('Delete')
      return self._RunMethod(
          config, request, global_params=global_params)

    Delete.method_config = lambda: base_api.ApiMethodInfo(
        flat_path=u'v1p1beta1/projects/{projectsId}/locations/{locationsId}/models/{modelsId}',
        http_method=u'DELETE',
        method_id=u'speech.projects.locations.models.delete',
        ordered_params=[u'name'],
        path_params=[u'name'],
        query_params=[],
        relative_path=u'v1p1beta1/{+name}',
        request_field='',
        request_type_name=u'SpeechProjectsLocationsModelsDeleteRequest',
        response_type_name=u'Operation',
        supports_download=False,
    )

    def Deploy(self, request, global_params=None):
      r"""Performs asynchronous model deployment of the model: receive results.
via the google.longrunning.Operations interface. After the operation is
completed this returns either an `Operation.error` in case of error or
a `google.protobuf.Empty` if the deployment was successful.

      Args:
        request: (SpeechProjectsLocationsModelsDeployRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Operation) The response message.
      """
      config = self.GetMethodConfig('Deploy')
      return self._RunMethod(
          config, request, global_params=global_params)

    Deploy.method_config = lambda: base_api.ApiMethodInfo(
        flat_path=u'v1p1beta1/projects/{projectsId}/locations/{locationsId}/models/{modelsId}:deploy',
        http_method=u'POST',
        method_id=u'speech.projects.locations.models.deploy',
        ordered_params=[u'name'],
        path_params=[u'name'],
        query_params=[],
        relative_path=u'v1p1beta1/{+name}:deploy',
        request_field=u'deployModelRequest',
        request_type_name=u'SpeechProjectsLocationsModelsDeployRequest',
        response_type_name=u'Operation',
        supports_download=False,
    )

    def Evaluate(self, request, global_params=None):
      r"""Performs asynchronous evaluation of the model: receive results.
via the google.longrunning.Operations interface. After the operation is
completed this returns either an `Operation.error` in case of error or
a `EvaluateModelResponse` with the evaluation results.

      Args:
        request: (SpeechProjectsLocationsModelsEvaluateRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Operation) The response message.
      """
      config = self.GetMethodConfig('Evaluate')
      return self._RunMethod(
          config, request, global_params=global_params)

    Evaluate.method_config = lambda: base_api.ApiMethodInfo(
        flat_path=u'v1p1beta1/projects/{projectsId}/locations/{locationsId}/models/{modelsId}:evaluate',
        http_method=u'POST',
        method_id=u'speech.projects.locations.models.evaluate',
        ordered_params=[u'name'],
        path_params=[u'name'],
        query_params=[],
        relative_path=u'v1p1beta1/{+name}:evaluate',
        request_field=u'evaluateModelRequest',
        request_type_name=u'SpeechProjectsLocationsModelsEvaluateRequest',
        response_type_name=u'Operation',
        supports_download=False,
    )

    def List(self, request, global_params=None):
      r"""Fetch the list of models associated with this project.

      Args:
        request: (SpeechProjectsLocationsModelsListRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ListModelsResponse) The response message.
      """
      config = self.GetMethodConfig('List')
      return self._RunMethod(
          config, request, global_params=global_params)

    List.method_config = lambda: base_api.ApiMethodInfo(
        flat_path=u'v1p1beta1/projects/{projectsId}/locations/{locationsId}/models',
        http_method=u'GET',
        method_id=u'speech.projects.locations.models.list',
        ordered_params=[u'parent'],
        path_params=[u'parent'],
        query_params=[u'filter', u'pageSize', u'pageToken'],
        relative_path=u'v1p1beta1/{+parent}/models',
        request_field='',
        request_type_name=u'SpeechProjectsLocationsModelsListRequest',
        response_type_name=u'ListModelsResponse',
        supports_download=False,
    )

  class ProjectsLocationsOperationsService(base_api.BaseApiService):
    """Service class for the projects_locations_operations resource."""

    _NAME = u'projects_locations_operations'

    def __init__(self, client):
      super(SpeechV1p1beta1.ProjectsLocationsOperationsService, self).__init__(client)
      self._upload_configs = {
          }

    def Get(self, request, global_params=None):
      r"""Gets the latest state of a long-running operation.  Clients can use this.
method to poll the operation result at intervals as recommended by the API
service.

      Args:
        request: (SpeechProjectsLocationsOperationsGetRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Operation) The response message.
      """
      config = self.GetMethodConfig('Get')
      return self._RunMethod(
          config, request, global_params=global_params)

    Get.method_config = lambda: base_api.ApiMethodInfo(
        flat_path=u'v1p1beta1/projects/{projectsId}/locations/{locationsId}/operations/{operationsId}',
        http_method=u'GET',
        method_id=u'speech.projects.locations.operations.get',
        ordered_params=[u'name'],
        path_params=[u'name'],
        query_params=[],
        relative_path=u'v1p1beta1/{+name}',
        request_field='',
        request_type_name=u'SpeechProjectsLocationsOperationsGetRequest',
        response_type_name=u'Operation',
        supports_download=False,
    )

    def List(self, request, global_params=None):
      r"""Lists operations that match the specified filter in the request. If the.
server doesn't support this method, it returns `UNIMPLEMENTED`.

NOTE: the `name` binding allows API services to override the binding
to use different resource name schemes, such as `users/*/operations`. To
override the binding, API services can add a binding such as
`"/v1/{name=users/*}/operations"` to their service configuration.
For backwards compatibility, the default name includes the operations
collection id, however overriding users must ensure the name binding
is the parent resource, without the operations collection id.

      Args:
        request: (SpeechProjectsLocationsOperationsListRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ListOperationsResponse) The response message.
      """
      config = self.GetMethodConfig('List')
      return self._RunMethod(
          config, request, global_params=global_params)

    List.method_config = lambda: base_api.ApiMethodInfo(
        flat_path=u'v1p1beta1/projects/{projectsId}/locations/{locationsId}/operations',
        http_method=u'GET',
        method_id=u'speech.projects.locations.operations.list',
        ordered_params=[u'name'],
        path_params=[u'name'],
        query_params=[u'filter', u'pageSize', u'pageToken'],
        relative_path=u'v1p1beta1/{+name}/operations',
        request_field='',
        request_type_name=u'SpeechProjectsLocationsOperationsListRequest',
        response_type_name=u'ListOperationsResponse',
        supports_download=False,
    )

  class ProjectsLocationsService(base_api.BaseApiService):
    """Service class for the projects_locations resource."""

    _NAME = u'projects_locations'

    def __init__(self, client):
      super(SpeechV1p1beta1.ProjectsLocationsService, self).__init__(client)
      self._upload_configs = {
          }

    def LogData(self, request, global_params=None):
      r"""Purges all log data associated with requested project. Operation response.
type is google.protobuf.Empty.

Since logs are stored by asynchronous writer process, buffered log data
might still end up in storage, even after this call. To ensure all data is
purged, call this method 3 days after last recognition call.

      Args:
        request: (SpeechProjectsLocationsLogDataRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Operation) The response message.
      """
      config = self.GetMethodConfig('LogData')
      return self._RunMethod(
          config, request, global_params=global_params)

    LogData.method_config = lambda: base_api.ApiMethodInfo(
        flat_path=u'v1p1beta1/projects/{projectsId}/locations/{locationsId}/log_data',
        http_method=u'DELETE',
        method_id=u'speech.projects.locations.log_data',
        ordered_params=[u'parent'],
        path_params=[u'parent'],
        query_params=[u'bucketName'],
        relative_path=u'v1p1beta1/{+parent}/log_data',
        request_field='',
        request_type_name=u'SpeechProjectsLocationsLogDataRequest',
        response_type_name=u'Operation',
        supports_download=False,
    )

  class ProjectsService(base_api.BaseApiService):
    """Service class for the projects resource."""

    _NAME = u'projects'

    def __init__(self, client):
      super(SpeechV1p1beta1.ProjectsService, self).__init__(client)
      self._upload_configs = {
          }

  class SpeechService(base_api.BaseApiService):
    """Service class for the speech resource."""

    _NAME = u'speech'

    def __init__(self, client):
      super(SpeechV1p1beta1.SpeechService, self).__init__(client)
      self._upload_configs = {
          }

    def Longrunningrecognize(self, request, global_params=None):
      r"""Performs asynchronous speech recognition: receive results via the.
google.longrunning.Operations interface. Returns either an
`Operation.error` or an `Operation.response` which contains
a `LongRunningRecognizeResponse` message.
For more information on asynchronous speech recognition, see the
[how-to](https://cloud.google.com/speech-to-text/docs/async-recognize).

      Args:
        request: (LongRunningRecognizeRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Operation) The response message.
      """
      config = self.GetMethodConfig('Longrunningrecognize')
      return self._RunMethod(
          config, request, global_params=global_params)

    Longrunningrecognize.method_config = lambda: base_api.ApiMethodInfo(
        http_method=u'POST',
        method_id=u'speech.speech.longrunningrecognize',
        ordered_params=[],
        path_params=[],
        query_params=[],
        relative_path=u'v1p1beta1/speech:longrunningrecognize',
        request_field='<request>',
        request_type_name=u'LongRunningRecognizeRequest',
        response_type_name=u'Operation',
        supports_download=False,
    )

    def Recognize(self, request, global_params=None):
      r"""Performs synchronous speech recognition: receive results after all audio.
has been sent and processed.

      Args:
        request: (RecognizeRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (RecognizeResponse) The response message.
      """
      config = self.GetMethodConfig('Recognize')
      return self._RunMethod(
          config, request, global_params=global_params)

    Recognize.method_config = lambda: base_api.ApiMethodInfo(
        http_method=u'POST',
        method_id=u'speech.speech.recognize',
        ordered_params=[],
        path_params=[],
        query_params=[],
        relative_path=u'v1p1beta1/speech:recognize',
        request_field='<request>',
        request_type_name=u'RecognizeRequest',
        response_type_name=u'RecognizeResponse',
        supports_download=False,
    )
