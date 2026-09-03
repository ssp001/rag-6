resource "aws_lambda_function" "this" {
  filename      = var.file_name_lambda
  function_name = var.aws_lambda_function_name
  role          = var.aws_iam_role_arn_value
  handler       = var.fuction_handeler
  code_sha256   = var.archive_base64input

  runtime = "python3.13"

}

