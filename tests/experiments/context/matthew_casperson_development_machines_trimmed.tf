resource "octopusdeploy_cloud_region_deployment_target" "target_pos_dev_client_1" {
  id                                = "Machines-18467"
  environments                      = ["${octopusdeploy_environment.environment_development.id}"]
  name                              = "pos-dev-client-1"
  roles                             = ["pos-client"]
  default_worker_pool_id            = "WorkerPools-1107"
  health_status                     = "Healthy"
  is_disabled                       = false
  shell_name                        = "Unknown"
  shell_version                     = "Unknown"
  tenant_tags                       = []
  tenanted_deployment_participation = "Tenanted"
  tenants                           = []
  thumbprint                        = ""
  depends_on                        = []
}

resource "octopusdeploy_cloud_region_deployment_target" "target_pos_dev_client_2" {
  id                                = "Machines-18469"
  environments                      = ["${octopusdeploy_environment.environment_development.id}"]
  name                              = "pos-dev-client-2"
  roles                             = ["pos-client"]
  default_worker_pool_id            = "WorkerPools-1107"
  health_status                     = "Healthy"
  is_disabled                       = false
  shell_name                        = "Unknown"
  shell_version                     = "Unknown"
  tenant_tags                       = []
  tenanted_deployment_participation = "Tenanted"
  tenants                           = []
  thumbprint                        = ""
  depends_on                        = []
}

resource "octopusdeploy_cloud_region_deployment_target" "target_pos_dev_server" {
  id                                = "Machines-18468"
  environments                      = ["${octopusdeploy_environment.environment_development.id}"]
  name                              = "pos-dev-server"
  roles                             = ["pos-server"]
  default_worker_pool_id            = "WorkerPools-1107"
  health_status                     = "Healthy"
  is_disabled                       = false
  shell_name                        = "Unknown"
  shell_version                     = "Unknown"
  tenant_tags                       = []
  tenanted_deployment_participation = "Tenanted"
  tenants                           = []
  thumbprint                        = ""
  depends_on                        = []
}

resource "octopusdeploy_cloud_region_deployment_target" "target_pos_dev_client_3" {
  id                                = "Machines-18464"
  environments                      = ["${octopusdeploy_environment.environment_development.id}"]
  name                              = "pos-dev-client-3"
  roles                             = ["pos-client"]
  default_worker_pool_id            = "WorkerPools-1107"
  health_status                     = "Healthy"
  is_disabled                       = false
  shell_name                        = "Unknown"
  shell_version                     = "Unknown"
  tenant_tags                       = []
  tenanted_deployment_participation = "Tenanted"
  tenants                           = []
  thumbprint                        = ""
  depends_on                        = []
}


resource "octopusdeploy_environment" "environment_development" {
  id                           = "Environments-1022"
  name                         = "Development"
  description                  = ""
  allow_dynamic_infrastructure = true
  use_guided_failure           = true
  sort_order                   = 0

  jira_extension_settings {
    environment_type = "development"
  }

  jira_service_management_extension_settings {
    is_enabled = false
  }

  servicenow_extension_settings {
    is_enabled = true
  }
}


resource "octopusdeploy_git_credential" "gitcredential_demo_space_creator_app" {
  id       = "GitCredentials-923"
  name     = "Demo Space Creator App"
  type     = "UsernamePassword"
  username = "x-access-token"
  password = "${var.gitcredential_demo_space_creator_app}"
}
variable "gitcredential_demo_space_creator_app" {
  type        = string
  nullable    = false
  sensitive   = true
  description = "The secret variable value associated with the git credential \"Demo Space Creator App\""
}


resource "octopusdeploy_git_credential" "gitcredential_cac" {
  id       = "GitCredentials-221"
  name     = "CaC"
  type     = "UsernamePassword"
  username = "mcasperson"
  password = "${var.gitcredential_cac}"
}
variable "gitcredential_cac" {
  type        = string
  nullable    = false
  sensitive   = true
  description = "The secret variable value associated with the git credential \"CaC\""
}


resource "octopusdeploy_cloud_region_deployment_target" "target_pos_dev_client_5" {
  id                                = "Machines-18470"
  environments                      = ["${octopusdeploy_environment.environment_development.id}"]
  name                              = "pos-dev-client-5"
  roles                             = ["pos-client"]
  default_worker_pool_id            = "WorkerPools-1107"
  health_status                     = "Healthy"
  is_disabled                       = false
  shell_name                        = "Unknown"
  shell_version                     = "Unknown"
  tenant_tags                       = []
  tenanted_deployment_participation = "Tenanted"
  tenants                           = []
  thumbprint                        = ""
  depends_on                        = []
}


resource "octopusdeploy_cloud_region_deployment_target" "target_pos_dev_client_4" {
  id                                = "Machines-18466"
  environments                      = ["${octopusdeploy_environment.environment_development.id}"]
  name                              = "pos-dev-client-4"
  roles                             = ["pos-client"]
  default_worker_pool_id            = "WorkerPools-1107"
  health_status                     = "Healthy"
  is_disabled                       = false
  shell_name                        = "Unknown"
  shell_version                     = "Unknown"
  tenant_tags                       = []
  tenanted_deployment_participation = "Tenanted"
  tenants                           = []
  thumbprint                        = ""
  depends_on                        = []
}

resource "octopusdeploy_polling_tentacle_deployment_target" "target_azure_iis" {
  id                                = "Machines-12387"
  environments                      = ["${octopusdeploy_environment.environment_development.id}"]
  name                              = "azure-iis"
  roles                             = ["azure-iss"]
  tentacle_url                      = "poll://4mz9qfd62rypjv59yj2p/"
  is_disabled                       = false
  shell_name                        = "PowerShell"
  shell_version                     = "5.1.17763.4840"
  tenant_tags                       = []
  tenanted_deployment_participation = "Untenanted"
  tenants                           = []

  tentacle_version_details {
  }

  thumbprint = "84D0CA1BBB7436381018A73FE2C385DA0296DE50"
  depends_on = []
}


resource "octopusdeploy_cloud_region_deployment_target" "target_belfast_client_5" {
  id                                = "Machines-18521"
  environments                      = [""]
  name                              = "belfast-client-5"
  roles                             = ["pos-client"]
  default_worker_pool_id            = "WorkerPools-1107"
  health_status                     = "Healthy"
  is_disabled                       = false
  shell_name                        = "Unknown"
  shell_version                     = "Unknown"
  tenant_tags                       = []
  tenanted_deployment_participation = "Tenanted"
  tenants                           = []
  thumbprint                        = ""
  depends_on                        = []
}


resource "octopusdeploy_cloud_region_deployment_target" "target_dallas_server" {
  id                                = "Machines-18503"
  environments                      = [""]
  name                              = "dallas-server"
  roles                             = ["pos-server"]
  default_worker_pool_id            = "WorkerPools-1107"
  health_status                     = "Healthy"
  is_disabled                       = false
  shell_name                        = "Unknown"
  shell_version                     = "Unknown"
  tenant_tags                       = []
  tenanted_deployment_participation = "Tenanted"
  tenants                           = []
  thumbprint                        = ""
  depends_on                        = []
}


resource "octopusdeploy_cloud_region_deployment_target" "target_melbourne_client_5" {
  id                                = "Machines-18506"
  environments                      = [""]
  name                              = "melbourne-client-5"
  roles                             = ["pos-client"]
  default_worker_pool_id            = "WorkerPools-1107"
  health_status                     = "Healthy"
  is_disabled                       = false
  shell_name                        = "Unknown"
  shell_version                     = "Unknown"
  tenant_tags                       = []
  tenanted_deployment_participation = "Tenanted"
  tenants                           = []
  thumbprint                        = ""
  depends_on                        = []
}


resource "octopusdeploy_cloud_region_deployment_target" "target_vancouver_client_3" {
  id                                = "Machines-18458"
  environments                      = [""]
  name                              = "vancouver-client-3"
  roles                             = ["pos-client"]
  default_worker_pool_id            = "WorkerPools-1107"
  health_status                     = "Healthy"
  is_disabled                       = false
  shell_name                        = "Unknown"
  shell_version                     = "Unknown"
  tenant_tags                       = []
  tenanted_deployment_participation = "Tenanted"
  tenants                           = []
  thumbprint                        = ""
  depends_on                        = []
}


resource "octopusdeploy_cloud_region_deployment_target" "target_calgary_client_4" {
  id                                = "Machines-18496"
  environments                      = [""]
  name                              = "calgary-client-4"
  roles                             = ["pos-client"]
  default_worker_pool_id            = "WorkerPools-1107"
  health_status                     = "Healthy"
  is_disabled                       = false
  shell_name                        = "Unknown"
  shell_version                     = "Unknown"
  tenant_tags                       = []
  tenanted_deployment_participation = "Tenanted"
  tenants                           = []
  thumbprint                        = ""
  depends_on                        = []
}