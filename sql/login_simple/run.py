import secrets
import os
import subprocess
import argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Run webapp (optionally with tests)')
    parser.add_argument('--test', action=argparse.BooleanOptionalAction, help='Run webapp tests instead of running the webapp')

    args = parser.parse_args()
    webapp_compose = "docker-compose.yml"
    test_compose = "docker-compose.test.yml"
    
    # Generate random passwords each run
    os.environ["DB_ROOT_PASSWORD"] = secrets.token_urlsafe()
    os.environ["DB_USER_PASSWORD"] = secrets.token_urlsafe()

    subprocess.run(["docker", "compose", "down", "-v"])
    if args.test:
        # The test_compose file reuses, but overrides, the webapp_compose file
        subprocess.run(["docker", "compose", "-f", webapp_compose, "-f", test_compose, "up", "--abort-on-container-exit"])
    else:
        subprocess.run(["docker", "compose", "up", "--abort-on-container-exit"])
