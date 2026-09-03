####################################
// cognito configuration
####################################
module "cognito" {
  source                   = "./cognito"
  cognito_user_pool_name   = "rag-6-pool"
  cognito_user_pool_client = "rag-6-client-pool"
  cognito_domain_name      = "rag-6-domain"
}

#########################################
// api getway configuration
#########################################
module "api_getway" {
  source                          = "./api_getway"
  aws_rest_api_id                 = "rag-6-api"
  api_getway_authorizer           = "geteway-authorizer"
  aws_cognito_user_pool_arn_value = module.cognito.aws_cognito_user_pool_arn
  s3_bucket_name_traget           = module.s3.s3_bucket_name
  aws_iam_role_this_gw_arn        = module.api_getway_role_for_s3.iam_role_arn_s3
}

##################################
// iam configuraion
##################################
module "iam" {
  source        = "./iam"
  iam_role_name = "lambda_process_role"
}

##############################
// delete lambda and archive module
##############################
module "delete_archive" {
  source            = "./data_archiver"
  archive_file_tipe = "zip"
  source_file_path  = "../server/main_delete.py"
  output_file_path  = "./archive/main_delete.zip"
}

module "delete_lambda" {
  source                   = "./lambda"
  file_name_lambda         = "delete_lambda_endpoint"
  aws_iam_role_arn_value   = module.iam.iam_role_arn
  aws_lambda_function_name = "delete_lambda"
  archive_base64input      = module.delete_archive.archive_base64output
  fuction_handeler         = "main_delete.delete_vector_points"
}

module "api_getway_lambda_ivokation_access_delete" {
  source                     = "./lambda_permission"
  aws_api_getway_api_arn     = module.api_getway.api_getway_excution_arn
  aws_lambda_permission_name = "delete_lambda_permission"
}


######################################
// respones lambda and archive module
######################################
module "respones_archive" {
  source            = "./data_archiver"
  archive_file_tipe = "zip"
  source_file_path  = "../server/main_respones.py"
  output_file_path  = "./archive/main_respones.zip"
}

module "respones_lambda" {
  source                   = "./lambda"
  file_name_lambda         = "respones_lambda_endpoint"
  aws_iam_role_arn_value   = module.iam.iam_role_arn
  aws_lambda_function_name = "respones_lambda"
  archive_base64input      = module.respones_archive.archive_base64output
  fuction_handeler         = "main_respones.chat"
}
module "api_getway_lambda_ivokation_access_respones" {
  source                     = "./lambda_permission"
  aws_api_getway_api_arn     = module.api_getway.api_getway_excution_arn
  aws_lambda_permission_name = "respones_lambda_permission"
}


##################################
// process lambda and archive module
##################################

// archiving process

module "process_archive" {
  source            = "./data_archiver"
  archive_file_tipe = "zip"
  source_file_path  = "../server/main_process.py"
  output_file_path  = "./archive/main_process.zip"
}

module "process_lambda" {
  source                   = "./lambda"
  file_name_lambda         = "process_lambda_endpoint"
  aws_iam_role_arn_value   = module.iam_role_integration.aws_iam_role_arn
  aws_lambda_function_name = "process_lambda"
  archive_base64input      = module.process_archive.archive_base64output
  fuction_handeler         = "main_process.run_process"
}

// api getway invokation allowence
module "api_getway_lambda_ivokation_access_process" {
  source                     = "./lambda_permission"
  aws_api_getway_api_arn     = module.api_getway.api_getway_excution_arn
  aws_lambda_permission_name = "process_lambda_permission"
}

##################################
// s3 bucket configuration
##################################

module "s3" {
  source             = "./s3_bucket"
  aws_s3_bucket_name = "s3-bucket-rag-6"
}


// s3 lambda access iam role

module "iam_role_integration" {
  source          = "./s3_invoke_lambda"
  iam_role_name   = "s3_lambda_invoke_role"
  iam_policy_name = "s3_lambda_invoke_policy"
}


###############################
// s3 role and policy for api getway invokation
###############################
module "api_getway_role_for_s3" {
  source                     = "./iam_s3"
  s3_integration_role_name   = "s3_iam_role_for_apigetway"
  s3_integration_policy_name = "s3_iam_policy_for_apigetway"
}
