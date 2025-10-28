# DevOps Tools Assignment – Ticket Booking Application

This repository contains a simple Flask‑based ticket booking application and
supporting artefacts demonstrating a complete DevOps workflow.  The goal of
this assignment is to showcase how version control, containerisation,
continuous integration/continuous delivery (CI/CD) and orchestration
integrate together to enable rapid and reliable software delivery.

## Contents

| File or Folder            | Description                                                |
|---------------------------|------------------------------------------------------------|
| `app.py`                  | Minimal Flask web application with booking form            |
| `requirements.txt`        | Python dependencies                                        |
| `Dockerfile`              | Container definition for building the application image    |
| `Jenkinsfile`             | Declarative pipeline for building, testing and deploying   |
| `k8s/deployment.yaml`     | Kubernetes Deployment manifest (with image placeholder)    |
| `k8s/service.yaml`        | Kubernetes Service manifest                                |
| `.gitignore`              | Files and folders ignored by Git                           |
| `README.md`               | This documentation                                         |

## 1. Version Control and Branching

1. **Initialise Git repository** – run `git init` in the root of the project.
2. **GitFlow branching** – follow the [GitFlow](https://nvie.com/posts/a-successful-git-branching-model/) model:
   - The `main` branch holds stable, production‑ready code.
   - The `develop` branch contains the latest development changes.
   - Feature branches (`feature/*`) are branched off `develop` for new
     functionality.
   - Release branches (`release/*`) prepare for production releases.
   - Hotfix branches (`hotfix/*`) are branched off `main` to quickly address
     production issues.
3. **Committing changes** – after implementing a feature, commit changes
   locally and push the branch to GitHub.  Create a pull request into
   `develop` or `main` as appropriate and merge using a squash or merge
   commit strategy.

## 2. Containerisation

1. **Dockerfile** – defines a container image using Python 3.10 and
   installs dependencies listed in `requirements.txt`.  The application
   code is copied into `/app` and port 5000 is exposed.  The default command
   runs `python app.py`.
2. **Building the image locally** – run the following commands:

   ```sh
   docker build -t yourdockeruser/ticket-booking-app:latest .
   docker run -p 5000:5000 yourdockeruser/ticket-booking-app:latest
   ```

   Navigate to `http://localhost:5000` to verify the application works.

## 3. Continuous Integration and Continuous Delivery

**Jenkins** automates the build, test and deployment pipeline via the
`Jenkinsfile` located at the project root.  A typical pipeline execution
performs the following stages:

1. **Checkout** – retrieves code from the repository.
2. **Install dependencies** – uses `pip` to install requirements.
3. **Run tests** – executes unit tests (placeholder in this project).
4. **Build Docker image** – builds an image tagged with the Jenkins
   build number.
5. **Push Docker image** – authenticates to Docker Hub using credentials
   stored in Jenkins and pushes the image.
6. **Deploy to Kubernetes** – dynamically replaces `<IMAGE_PLACEHOLDER>` in
   the deployment manifest with the built image tag, then applies the
   deployment and service manifests using `kubectl apply`.

The pipeline also cleans up dangling Docker images to conserve disk space.

To integrate Jenkins with this repository:

1. Install Jenkins and the Docker and Kubernetes CLI tools on your Jenkins
   agents.
2. Configure credentials:
   - **docker-hub-pass** – Docker Hub username and password for pushing images.
   - **kube-config** – Kubernetes config file for cluster access (optional if
     the Jenkins agent already has access).
3. Create a new **Pipeline** job pointing at this GitHub repository and
   select “Pipeline from SCM” with `Jenkinsfile` as the script.
4. Enable GitHub webhook or set Jenkins to poll Git for changes so the
   pipeline triggers automatically when code is pushed.

## 4. Deployment and Orchestration

Kubernetes is used to orchestrate the containerised application.  The
manifests live in the `k8s` folder:

1. **`deployment.yaml`** – defines a Deployment with three replicas and a
   placeholder `<IMAGE_PLACEHOLDER>` for the Docker image.  The Jenkins
   pipeline generates a temporary manifest replacing this placeholder with
   the correct image tag.
2. **`service.yaml`** – exposes the Deployment internally on port 80 and
   forwards traffic to port 5000 on the pods.  Change the `type` to
   `LoadBalancer` or `NodePort` if you need external access.

To deploy manually without Jenkins:

```sh
# Replace the placeholder with your image
sed "s|<IMAGE_PLACEHOLDER>|yourdockeruser/ticket-booking-app:latest|g" k8s/deployment.yaml > deployment.prod.yaml
kubectl apply -f deployment.prod.yaml
kubectl apply -f k8s/service.yaml
```

## Screenshots and Evidence

Include screenshots of your Git branching strategy, Docker image builds,
Jenkins pipeline runs and Kubernetes dashboard in this section when
submitting the assignment.  These screenshots demonstrate that each
component of the workflow executes successfully.

## Conclusion

This repository demonstrates how a simple web application can be placed
under source control, containerised, automatically built and tested, and
deployed to a container orchestration platform.  By following this
end‑to‑end workflow you achieve faster feedback loops, repeatable builds and
reliable deployments.
