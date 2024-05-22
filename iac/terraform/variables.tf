// Variables to use accross the project
// which can be accessed by var.project_id
variable "project_id" {
  description = "The project ID to host the cluster in"
  default     = "notional-device-422008-e2"
}

variable "region" {
  description = "The region the cluster in"
  default     = "us-central1-a"
} 

# variable "bucket" {
#   description = "GCS bucket for project capstone"
#   default     = "viet-poem-generation"
# }
