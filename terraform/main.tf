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
  source_file_path  = "./server/main_delete.py"
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

######################################
// respones lambda and archive module
######################################
module "respones_archive" {
  source            = "./data_archiver"
  archive_file_tipe = "zip"
  source_file_path  = "./server/main_respones.py"
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

##################################
// process lambda and archive module
##################################
module "process_archive" {
  source            = "./data_archiver"
  archive_file_tipe = "zip"
  source_file_path  = "./server/main_process.py"
  output_file_path  = "./archive/main_process.zip"
}

module "process_lambda" {
  source                   = "./lambda"
  file_name_lambda         = "process_lambda_endpoint"
  aws_iam_role_arn_value   = module.iam.iam_role_arn
  aws_lambda_function_name = "process_lambda"
  archive_base64input      = module.process_archive.archive_base64output
  fuction_handeler         = "main_process.run_process"
}

##################################
// s3 bucket configuration
##################################

module "s3" {
  source             = "./s3_bucket"
  aws_s3_bucket_name = "s3-bucket-rag-6"
}


