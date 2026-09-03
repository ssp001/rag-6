resource "aws_lambda_permission" "apigw_lambda" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = var.aws_lambda_permission_name
  principal     = "://amazonaws.com"

  # Restricts execution strictly to your specific API Gateway deployment
  source_arn = "${var.aws_api_getway_api_arn}/*/*"
}
