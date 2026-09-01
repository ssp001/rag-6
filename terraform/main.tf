provider "aws" {
  region = "ap-south-1"
}


#############################
// cognito service
#############################

resource "aws_cognito_user_pool_domain" "this" {
  domain       = "rag-6-domain"
  user_pool_id = aws_cognito_user_pool.this.id

}

resource "aws_cognito_user_pool_client" "this" {
  name            = "rag-6-client"
  user_pool_id    = aws_cognito_user_pool.this.id
  generate_secret = false
  allowed_oauth_flows = [
    "code"
  ]
  allowed_oauth_scopes = [
    "openid",
    "email",
    "profile"
  ]

  allowed_oauth_flows_user_pool_client = true
  callback_urls = [
    "http://localhost:8501"
  ]

  logout_urls = [
    "http://localhost:8501"
  ]

  supported_identity_providers = [
    "COGNITO"
  ]
}

resource "aws_cognito_user_pool" "this" {
  name                     = "rag-6-user-pool"
  username_attributes      = ["email"]
  auto_verified_attributes = ["email"]
}


#############################
// apigetway service
#############################
resource "aws_api_gateway_authorizer" "this" {
  name        = "rag-6-authorizer"
  type        = "COGNITO_USER_POOLS"
  rest_api_id = aws_api_gateway_rest_api.this.id
  provider_arns = [
    aws_cognito_user_pool.this.arn
  ]
  identity_source = "method.request.header.Authorization"
}
resource "aws_api_gateway_resource" "this_process" {
  rest_api_id = aws_api_gateway_rest_api.this.id
  parent_id   = aws_api_gateway_rest_api.this.root_resource_id
  path_part   = "Home/process"
}
resource "aws_api_gateway_resource" "this_delete" {
  rest_api_id = aws_api_gateway_rest_api.this.id
  parent_id   = aws_api_gateway_rest_api.this.root_resource_id
  path_part   = "Home/delete"
}

resource "aws_api_gateway_resource" "this_respones" {
  rest_api_id = aws_api_gateway_rest_api.this.id
  parent_id   = aws_api_gateway_rest_api.this.root_resource_id
  path_part   = "Home/respones"
}

resource "aws_api_gateway_resource" "health_chek" {
  rest_api_id = aws_api_gateway_rest_api.this.id
  parent_id   = aws_api_gateway_rest_api.this.root_resource_id
  path_part   = "Home"
}

#############################
// getway endpoints
#############################

resource "aws_api_gateway_method" "this_home" {
  resource_id   = aws_api_gateway_rest_api.this.id
  rest_api_id   = aws_api_gateway_rest_api.this.id
  http_method   = "GET"
  authorization = "COGNITO_USER_POOLS"
  authorizer_id = aws_api_gateway_authorizer.this.id
  depends_on = [
    aws_api_gateway_authorizer.this
  ]
}



resource "aws_api_gateway_method" "post_respones" {
  rest_api_id   = aws_api_gateway_rest_api.this.id
  resource_id   = aws_api_gateway_resource.this_respones.id
  http_method   = "POST"
  authorization = "COGNITO_USER_POOLS"
  authorizer_id = aws_api_gateway_authorizer.this.id
  depends_on = [
    aws_api_gateway_authorizer.this
  ]
}

resource "aws_api_gateway_method" "this_process" {
  rest_api_id   = aws_api_gateway_rest_api.this.id
  resource_id   = aws_api_gateway_resource.this_process.id
  http_method   = "POST"
  authorization = "COGNITO_USER_POOLS"
  authorizer_id = aws_api_gateway_authorizer.this.id
  depends_on = [
    aws_api_gateway_authorizer.this
  ]
}

resource "aws_api_gateway_method" "Delete" {
  rest_api_id   = aws_api_gateway_rest_api.this.id
  resource_id   = aws_api_gateway_resource.this_delete.id
  http_method   = "DELETE"
  authorization = "COGNITO_USER_POOLS"
  authorizer_id = aws_api_gateway_authorizer.this.id
  depends_on = [
    aws_api_gateway_authorizer.this
  ]
}


resource "aws_api_gateway_rest_api" "this" {
  name = "rest_api_getway"
}

output "cognito_login_url" {
  value = "https://${aws_cognito_user_pool_domain.this.domain}.auth.${data.aws_region.current.name}.amazoncognito.com/login"
}

data "aws_region" "current" {}
output "cognito_client_id" {
  value = aws_cognito_user_pool_client.this.id
}


// https://rag-6-domain.auth.ap-south-1.amazoncognito.com/login?client_id=19lvgtfb519giaaimhnkvdv7b1&response_type=code&scope=openid+email&redirect_uri=http%3A%2F%2Flocalhost%3A8501
