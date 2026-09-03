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
