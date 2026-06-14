# Jenkins Support for SkyNetX

This folder contains a simple declarative Jenkins pipeline for the SkyNetX DevOps college project.

## Purpose
The pipeline demonstrates how source code moves through a basic CI/CD flow:

- checkout project source from GitHub
- verify that Python, Docker, and kubectl are available
- install Python dependencies
- run basic application checks
- build the Docker image
- apply Kubernetes manifests
- verify rollout status
- show running pods and services

## Pipeline File
- `Jenkinsfile`

## Demo Notes
- The pipeline is intentionally simple for local college demonstration.
- It uses the existing image name `skynetx-app:1.0`.
- It applies the already working Kubernetes manifests from the `kubernetes/` folder.
- It does not push images to Docker Hub or any cloud registry yet.

## Typical Jenkins Flow
1. Create a Pipeline job in Jenkins.
2. Connect the job to the GitHub repository.
3. Point Jenkins to `jenkins/Jenkinsfile` or copy the pipeline content into the job.
4. Run the pipeline.

## Expected Outcome
After a successful run, Jenkins should:

- confirm tools are installed
- validate the Flask application at a basic level
- build the Docker image
- apply Kubernetes manifests
- show SkyNetX pods and service details in the console output
