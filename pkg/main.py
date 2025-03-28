from cloudcoil.models.kubernetes.core.v1 import Pod, PodSpec, Container, ResourceRequirements, Node


# Create a Pod using Cloudcoil's object model
pod = Pod(
    metadata={
        "name": "nginx-pod",
        "namespace": "default"
    },
    spec=PodSpec(
        containers=[
            Container(
                name="nginx",
                image="nginx:latest",
                resources=ResourceRequirements(
                    limits={
                        "cpu": "500m",    # 500 milliCPU (0.5 CPU)
                        "memory": "512Mi" # 512 Mebibytes
                    },
                    requests={
                        "cpu": "200m",    # 200 milliCPU (0.2 CPU)
                        "memory": "256Mi" # 256 Mebibytes
                    }
                )
            )
        ]
    )
)

# Optional: Build and print the Pod definition
final_pod = pod.builder()
print(pod)

# To create this Pod in your Kubernetes cluster (uncomment if you have Cloudcoil configured)
pod.create()