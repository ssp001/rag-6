variable "aws_rest_api_id" {
  type        = string
  description = "rest api id name"
}

variable "api_getway_authorizer" {
  type        = string
  description = "api getway authorizer name"
}

variable "aws_cognito_user_pool_arn_value" {
  type    = string
  default = "arn value for cognito user pool"
}

variable "s3_bucket_name_traget" {
  type        = string
  description = "s3 name"
}
variable "aws_iam_role_this_gw_arn" {
  type        = string
  description = "aws iam role apigw s3 role arn value"
}

variable "region" {
  type    = string
  default = "ap-south-1"
}
