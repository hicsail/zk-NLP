# Create an image
# [reference documentation](https://www.packer.io/docs/templates)

# Execution:
# AWS_ACCESS_KEY_ID=$(aws configure get aws_access_key_id)
# AWS_SECRET_ACCESS_KEY=$(aws configure get aws_secret_access_key)
# packer build ami_gen.pkr.hcl


locals { timestamp = regex_replace(timestamp(), "[- TZ:]", "") }

# source blocks configure your builder plugins; your source is then used inside
# build blocks to create resources. A build block runs provisioners and
# post-processors on an instance created by the source.
source "amazon-ebs" "sieve_ta1" {
  ami_name      = "sieve_ta1 ${local.timestamp}"
  instance_type = "t2.micro"
  region        = "us-east-1"
  source_ami_filter {
    filters = {
      name = "amzn2-ami-hvm-*-x86_64-gp2"
    }
    most_recent = true
    # Indicate that only an ami from Amazon should be used
    owners = ["137112412989"]
  }
  ssh_username = "ec2-user"
}

# a build block invokes sources and runs provisioning steps on them.
# https://www.elastic.co/guide/en/beats/metricbeat/current/setup-repositories.html
build {
  sources = ["source.amazon-ebs.sieve_ta1"]

  # Packaging necessary modules into tar file
  provisioner "shell-local" {
    inline = [
      "echo 'Removing existing ../tmp-mini'",
      "rm -rf ../tmp-mini",
      "git clone git@github.mit.edu:sieve-all/TA1.git ../tmp-mini",
      ""
    ]
  }
  # Uploading compressed package into AWS server
  provisioner "file" {
    source      = "../tmp-mini/"
    destination = "/tmp/"
  }

  # Todo: Setup AWS env
  provisioner "shell" {
    inline = [
      "cd /tmp",
      "echo $(ls)",
      "cp /tmp/testcase-generation/generate_statements /tmp/testcase-generation/*.py /home/ec2-user/",
      "sudo yum -y update",
      "pip3 install . --no-cache-dir",
      "cd /home/ec2-user",
      "./generate_statements /tmp/TA1/testcase-generation/config.json",
      ""
    ]
  }
}