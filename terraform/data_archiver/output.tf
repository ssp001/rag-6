
output "archive_output_path" {
  value = data.archive_file.this.output_path
}

output "archive_base64output" {
  value = data.archive_file.this.output_base64sha256
}
