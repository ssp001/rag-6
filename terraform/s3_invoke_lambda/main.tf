resource "aws_iam_role" "this" {
  name = var.iam_role_name
  assume_role_policy = jsonencode(
    {
      Version = "2012-10-17"
      Statement = [
        {
          Action = "sts:AssumeRole"
          Effect = "Allow"
          Principal = {
            Service = "lambda.amazonaws.com"
          }
          Principal = {
            service = "s3.amazonaws.com"
          }
        }
      ]
    }
  )
}


resource "aws_iam_policy" "this" {
  name = var.iam_policy_name
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "lambda:InvokeFunction",
          "lambda:InvokeAsync",
          "lambda:InvokeFunctionUrl"
        ]
        Effect = "Allow"
        # Security Note: It is best practice to replace "*" with specific Lambda function ARNs 
        # to restrict what this identity can invoke.
        Resource = "*"
      },
    ]
  })
}

resource "aws_iam_role_policy_attachment" "this" {
  role       = aws_iam_role.this.name
  policy_arn = aws_iam_policy.this.arn
}
