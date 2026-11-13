provider "aws" { region = "eu-central-1" }

provider "aws" {
  alias  = "replica"
  region = "eu-west-1"
}
