#############################
// cognito service
#############################

resource "aws_cognito_user_pool" "this" {
  name                     = var.cognito_user_pool_name
  username_attributes      = ["email"]
  auto_verified_attributes = ["email"]
}


#############################
// cognito user pool domain service
#############################
resource "aws_cognito_user_pool_domain" "this" {
  domain       = var.cognito_domain_name
  user_pool_id = aws_cognito_user_pool.this.id

}

#############################
// cognito user pool client service
#############################
resource "aws_cognito_user_pool_client" "this" {
  name            = var.cognito_user_pool_client
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
    "localw8oyoh"
  ]

  logout_urls = [
    "localdhwiudh"
  ]


  supported_identity_providers = [
    "COGNITO"
  ]
}

data "aws_region" "current" {}
