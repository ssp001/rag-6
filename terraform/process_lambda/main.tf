data "archive_file" "example" {
  type        = "zip"
  source_file = "../server/main_process.py"
  output_path = "../archive/main_process.zip"
}

# Lambda function
resource "aws_lambda_function" "this" {
  filename      = data.archive_file.example.output_path
  function_name = var.aws_lambda_function_name
  role          = var.aws_iam_role_arn_value
  handler       = "main_process.run_process"
  code_sha256   = data.archive_file.example.output_base64sha256

  runtime = "python3.13"

}

