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
source "amazon-ebs" "example" {
  ami_name      = "sieve_ami_example_basic ${local.timestamp}"
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
  sources = ["source.amazon-ebs.example"]

  # Todo: Setup AWS env
  provisioner "shell" {
    inline = [
      "sleep 30",
      "echo 'Creating tmp directory'",
      "mkdir /tmp/SIEVE",
      "echo 'Starting to install dependencies'",
      # "sudo yum update -y",
      # "sudp yum install build-essential python3 python3-pip python3-dev python3-numpy git cmake make libssl-dev bash musl-dev nano wget unzip uuid-dev default-jdk"
    ]
  }

  # Upload relevant files
  provisioner "file" {
    source      = "../../SIEVE/"
    destination = "/tmp/SIEVE"
  }

  # Give permissions for access to the uploaded files
  provisioner "shell" {
    inline = [
      "echo 'Installing python packages'",

      "sudo pip3 install -r /tmp/SIEVE/requirements.txt",
      "sudo python3 /tmp/SIEVE/install.py --deps --tool --ot --zk",
      "sudo ldconfig",
      "sudo /tmp/SIEVE/wiztoolkit/make",
      "sudo /tmp/SIEVE/wiztoolkit/make install",
    ]
  }

  # Run the tests
  provisioner "shell" {
    inline = [
      "echo 'Running ",
      "cd /tmp/SIEVE/testcase-generation",
      "python3 generate_statements_ta1"
    ]
  }
}