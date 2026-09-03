
output "aws_cognito_user_pool_arn" {
  value = aws_cognito_user_pool.this.arn
}
output "cognito_client_id" {
  value = aws_cognito_user_pool_client.this.id
}


