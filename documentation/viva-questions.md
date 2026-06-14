# SkyNetX Viva Questions

## Business and Project Basics
1. What is Project SkyNetX and which business problem does it solve?
2. Why is drone traffic management important for logistics, emergency response, agriculture, and government use cases?

## Flask Application
3. What are the major modules in the SkyNetX Flask application?
4. Why is the `/health` endpoint important?
5. Why is the `/metrics` endpoint important?

## Docker
6. Why did you containerize the application?
7. What is the role of the Dockerfile?
8. Why does the Flask app run on `0.0.0.0` inside Docker?

## Jenkins
9. What is CI/CD?
10. What stages are present in your Jenkins pipeline?
11. Why do you build the Docker image in Jenkins?

## Kubernetes
12. What is the role of the namespace in Kubernetes?
13. What is the difference between Deployment and Service?
14. Why did you use NodePort?
15. What do readiness and liveness probes do?
16. What is the purpose of the HPA?

## Terraform
17. What is Infrastructure as Code?
18. What is Terraform’s role in this project?
19. Why are the Terraform resources kept basic in this demo?

## Prometheus and Grafana
20. How does Prometheus collect SkyNetX metrics?
21. What can you visualize in Grafana?
22. What alert rules did you define?

## ELK Stack
23. What is the purpose of Elasticsearch, Logstash, and Kibana?
24. What kinds of SkyNetX logs are important to collect?

## Vault
25. Why should secrets not be stored in source code or GitHub?
26. What secrets are demonstrated in your Vault setup?

## Disaster Recovery
27. What is the difference between RTO and RPO?
28. How would you recover from a bad deployment?
29. How would you handle pod failure or traffic spike?
30. What steps would you take after a secret compromise or cybersecurity incident?
