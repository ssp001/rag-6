############################
// s3 bucket
############################
resource "aws_s3_bucket" "this" {
  bucket = var.aws_s3_bucket_name
}
