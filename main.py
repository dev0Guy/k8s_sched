from hugsy_scheduler.k8s.resource import Resource, ResourcesUsage

def main() -> None:
    print(Resource(10, 20, 3, 1))


if __name__ == '__main__':
    main()