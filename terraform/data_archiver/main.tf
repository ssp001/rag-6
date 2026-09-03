data "archive_file" "this" {
  type        = "zip"
  source_file = var.source_file_path
  output_path = var.output_file_path
}
