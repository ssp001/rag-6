data "aws_region" "current" {}
#############################
// apigetway service
#############################
resource "aws_api_gateway_rest_api" "this" {
  name               = var.aws_rest_api_id
  binary_media_types = ["application/pdf"]
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

// api getway s3 invoke andput acess
resource "aws_api_gateway_resource" "this_upload_s3" {
  rest_api_id = aws_api_gateway_rest_api.this.id
  parent_id   = aws_api_gateway_rest_api.this.root_resource_id
  path_part   = "{folder}" # Dynamic path parameter for S3 file naming
}


resource "aws_api_gateway_method" "put_pdf" {
  rest_api_id   = aws_api_gateway_rest_api.this.id
  resource_id   = aws_api_gateway_resource.this_upload_s3.id
  http_method   = "PUT"
  authorization = "COGNITO_USER_POOLS" # Secure this in production (e.g., using Cognito)

  request_parameters = {
    "method.request.path.folder" = true
  }
}


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

##########################################
// Route the incoming API Gateway traffic directly to S3.
##########################################

resource "aws_api_gateway_integration" "this" {
  rest_api_id = aws_api_gateway_rest_api.this.id
  resource_id = aws_api_gateway_resource.this_upload_s3.id
  http_method = aws_api_gateway_method.put_pdf.http_method

  # Type must be AWS (not AWS_PROXY) for direct service integrations
  type                    = "AWS"
  integration_http_method = "PUT"
  uri                     = "arn:aws:apigateway:${data.aws_region.current.name}:s3:path/${var.s3_bucket_name_traget}/{bucket}"
  credentials             = var.aws_iam_role_this_gw_arn
  # Map the URL path variable from API Gateway into the S3 file path
  request_parameters = {
    "integration.request.path.bucket" = "method.request.path.folder"
  }
}

# Standard deployment block to activate your API endpoints
resource "aws_api_gateway_deployment" "this" {
  rest_api_id = aws_api_gateway_rest_api.this.id
  depends_on  = [aws_api_gateway_integration.this]
}

resource "aws_api_gateway_stage" "this" {
  deployment_id = aws_api_gateway_deployment.this.id
  rest_api_id   = aws_api_gateway_rest_api.this.id
  stage_name    = "prod"
}


