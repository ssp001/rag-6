
#############################
// apigetway service
#############################
resource "aws_api_gateway_rest_api" "this" {
  name = var.aws_rest_api_id
}
resource "aws_api_gateway_authorizer" "this" {
  name        = var.api_getway_authorizer
  type        = "COGNITO_USER_POOLS"
  rest_api_id = aws_api_gateway_rest_api.this.id
  provider_arns = [
    var.aws_cognito_user_pool_arn_value
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

