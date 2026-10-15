# Quiz 01: Docker Containerization

## Topic Overview
This quiz covers containerization fundamentals for AI services: the image, container, and registry model; Dockerfile anatomy and layer caching; multi-stage builds; Compose orchestration with health gates and volumes; resource limits; image security; and GPU passthrough for CUDA workloads.

---

## Questions

### Question 1
**What is the correct relationship between an image and a container?**

- A) A container is a mutable image that updates in place
- B) A container is a running process created from an immutable image
- C) An image is a running container that has been paused
- D) An image and a container are two names for the same artifact

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** An image is an immutable stack of filesystem layers plus configuration metadata. A container is a running instance of that image, given its own namespaces and cgroups, with a single writable top layer that is discarded when the container is removed. Images are never mutated; changing anything produces a new image.
</details>

---

### Question 2
**Why should dependency manifests be copied into an image before application source code?**

- A) Python imports fail if source code is copied first
- B) It makes the image smaller regardless of content
- C) The dependency install layer stays cached when only source files change
- D) Docker refuses to build if the order is wrong

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: C**

**Explanation:** Docker caches each layer keyed on the instruction and all prior layers. Copying manifests first and installing in a separate `RUN` means editing a `.py` file does not invalidate the expensive install layer. The reverse order re-installs every dependency on every source edit.
</details>

---

### Question 3
**In a multi-stage build, what happens to the builder stage in the final image?**

- A) It is compressed into a single layer at the end
- B) It is included but hidden behind a mount point
- C) It is discarded unless you explicitly copy from it
- D) It is merged into the runtime stage automatically

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: C**

**Explanation:** Only the last stage becomes the final image unless `--target` selects an earlier one. Files reach the final image only via an explicit `COPY --from=<stage>`. Everything else, including compilers, headers, and caches, stays in the discarded builder stage.
</details>

---

### Question 4
**What is the practical effect of using the shell form of CMD instead of the exec form?**

- A) The container starts faster
- B) The application becomes a grandchild of a shell, so SIGTERM does not reach it
- C) The image size increases by the size of the shell
- D) Docker cannot override CMD at run time

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** `CMD uvicorn app:app` is wrapped in `/bin/sh -c`, making the shell PID 1 and the application its child. Shells do not forward signals by default, so `docker stop` kills the shell and orphans the application. The exec form `CMD ["uvicorn", "app:app"]` makes the application PID 1 and it receives SIGTERM directly.
</details>

---

### Question 5
**In a Compose file, what does `depends_on` with `condition: service_healthy` do that a plain `depends_on` list does not?**

- A) Restarts the dependency if it crashes
- B) Waits until the dependency's health check passes, not merely until its process starts
- C) Allocates more memory to the dependency
- D) Exposes the dependency's ports to the host

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** A plain `depends_on` returns as soon as the dependency's container process is running, which is usually before the service inside it is accepting connections. `condition: service_healthy` waits until the health check passes, so the dependent service does not race a half-initialized database.
</details>

---

### Question 6
**Inside a Compose stack, how should one service address a sibling service?**

- A) `http://localhost:6333`
- B) `http://qdrant:6333` using the service name as a hostname
- C) `http://172.17.0.2:6333` using the container's IP address
- D) `http://host.docker.internal:6333`

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Compose creates a user-defined network where service names resolve as DNS names. `localhost` inside a container refers to the container itself, not a sibling. Container IP addresses are assigned dynamically and are not stable across restarts, so hardcoding them breaks.
</details>

---

### Question 7
**A `COPY . .` instruction placed before a `pip install` causes which concrete problem?**

- A) pip refuses to install in a non-empty directory
- B) Every edit to any source file invalidates the install layer and re-runs it
- C) Docker cannot resolve the `.` source path
- D) The image becomes multi-stage automatically

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** `COPY . .` is keyed on the content of the entire context. Any file change alters that layer's hash, which invalidates it and every layer after it, including the `pip install`. For an AI service with heavy dependencies such as torch, this turns a one-second rebuild into a multi-minute one.
</details>

---

### Question 8
**Why is a secret written with `RUN echo "KEY=..." > /app/.env` unsafe even if a later instruction deletes the file?**

- A) The file reappears when the container restarts
- B) Earlier layers remain in image history and are recoverable
- C) Docker encrypts the file but stores the key alongside it
- D) It only affects images built with BuildKit

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Deleting a file in a later layer does not remove it from earlier layers; it only hides it from the merged view. Every layer is stored and can be extracted with `docker history --no-trunc` or an image explorer. Secrets must be injected at runtime, never written into a build layer.
</details>

---

### Question 9
**What is the correct split of responsibility between a CUDA image and the host when running GPU containers?**

- A) The image provides the GPU driver; the host provides CUDA libraries
- B) The image provides CUDA user-space libraries; the host provides the driver
- C) Both the image and the host provide complete, independent CUDA stacks
- D) Neither provides anything; GPU access requires a bare-metal install

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** The NVIDIA Container Toolkit mounts the host GPU device into the container and injects the CUDA user-space libraries the image needs. The kernel driver always comes from the host. The two must be compatible, which is why a container CUDA runtime newer than the host driver fails.
</details>

---

### Question 10
**Which health check command correctly reports unhealthy on an HTTP 500 response?**

- A) `curl http://127.0.0.1:8000/health`
- B) `wget http://127.0.0.1:8000/health`
- C) `curl -fsS http://127.0.0.1:8000/health || exit 1`
- D) `echo ok`

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: C**

**Explanation:** `curl` without `-f` returns exit code 0 on any completed HTTP exchange, including 500 responses, so Docker records the container as healthy while it is failing. `curl -fsS` fails on HTTP errors, and the `|| exit 1` guarantees a non-zero exit when the command itself cannot run.
</details>

---

### Question 11
**What happens to a container's writable layer when the container is removed?**

- A) It is preserved as a new image
- B) It is moved to a named volume automatically
- C) It is discarded, and any files written to it are lost
- D) It is copied to the host's current directory

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: C**

**Explanation:** The writable top layer is ephemeral and is deleted with the container. Anything a database or service wrote there is gone. Durable state must live on a named volume or a bind mount, both of which exist independently of the container lifecycle.
</details>

---

### Question 12
**On which host-side condition does the error `could not select device driver "" with capabilities: [[gpu]]` depend?**

- A) The image is missing the CUDA runtime
- B) The NVIDIA Container Toolkit is not installed, or the Docker daemon was not restarted after installing it
- C) The Compose file lacks an `expose` entry
- D) The container is running as root

**Difficulty:** Hard

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** This error is raised before any image content matters. Docker is being asked to attach a GPU but has no runtime registered that can do it, which means the NVIDIA Container Toolkit is absent or its runtime was not registered with the daemon, typically because the daemon was not restarted after installation.
</details>

---

### Question 13
**Why is `docker compose down -v` more dangerous than `docker compose down`?**

- A) It stops containers without removing them
- B) It deletes named volumes and the persistent data stored in them
- C) It removes the Compose file from the host
- D) It force-removes images from the local registry

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Plain `down` removes containers and networks but leaves named volumes intact. The `-v` flag also removes the volumes declared in the Compose file, destroying database files, vector indexes, and any other persistent state stored there.
</details>

---

### Question 14
**What is the primary security advantage of running a container as a non-root user?**

- A) It makes the image smaller
- B) It speeds up container startup
- C) It limits the privileges an attacker gains from a container escape
- D) It allows the container to bind ports below 1024

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: C**

**Explanation:** Container isolation is not a perfect boundary. If an attacker escapes the container and the process is root, they inherit broad privileges on the host. Running as an unprivileged user with a fixed UID applies least privilege and satisfies most compliance scanners. Size and startup speed are unrelated.
</details>

---

### Question 15
**What does a `.dockerignore` entry exclude?**

- A) Files from the built image only
- B) Files from the build context sent to the daemon
- C) Files from the running container at runtime
- D) Files from the registry during push

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** `.dockerignore` filters the build context before it reaches the daemon, so excluded files are never available to `COPY` or `ADD`. This both speeds up builds and prevents accidental inclusion of `.env` files, virtualenvs, and model weights in image layers.
</details>

---

## Score Tracking

| Question | Difficulty | Your Answer | Correct? |
|----------|------------|-------------|----------|
| 1 | Easy | | |
| 2 | Easy | | |
| 3 | Easy | | |
| 4 | Medium | | |
| 5 | Medium | | |
| 6 | Medium | | |
| 7 | Easy | | |
| 8 | Medium | | |
| 9 | Medium | | |
| 10 | Medium | | |
| 11 | Easy | | |
| 12 | Hard | | |
| 13 | Easy | | |
| 14 | Easy | | |
| 15 | Easy | | |

**Score:** ____/15

---

## Answer Key

| Q | Answer | Q | Answer | Q | Answer |
|---|--------|---|--------|---|--------|
| 1 | B | 6 | B | 11 | C |
| 2 | C | 7 | B | 12 | B |
| 3 | C | 8 | B | 13 | B |
| 4 | B | 9 | B | 14 | C |
| 5 | B | 10 | C | 15 | B |

---

*Generated for AI Engineer Lab DevOps Track - Quiz 01 of 04*
