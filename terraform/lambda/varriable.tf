variable "aws_iam_role_arn_value" {
  type        = string
  description = "aws iam role arn value"
}
variable "aws_lambda_function_name" {
  type        = string
  description = "aws lambda name"
}

variable "fuction_handeler" {
  type        = string
  description = "fuction handeler name"
}

variable "archive_base64input" {
  type        = string
  description = "base64 input"
}

variable "file_name_lambda" {
  type        = string
  description = "file name for lambda"
}
