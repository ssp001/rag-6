
module "cognito" {
  source                   = "./cognito"
  cognito_user_pool_name   = "rag-6-pool"
  cognito_user_pool_client = "rag-6-client-pool"
  cognito_domain_name      = "rag-6-domain"

}

module "api_getway" {
  source                          = "./api_getway"
  aws_rest_api_id                 = "rag-6-api"
  api_getway_authorizer           = "geteway-authorizer"
  aws_cognito_user_pool_arn_value = module.cognito.aws_cognito_user_pool_arn
}

module "s3" {
  source             = "./s3_bucket"
  aws_s3_bucket_name = "s3-bucket-rag-6"
}


