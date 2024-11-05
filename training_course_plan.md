# GPU Programming Workshop: Practical Foundations and Applications

## Workshop Objectives  
- Understand what the key differences between writing code for a CPU and GPU are.
- Understand the differences between a compiled and interpreted language and the nuances involved with working between them.
- Comfortable with the use of common auxiliary tools, such as Spack and profile analysers, for use in developing GPU code.
- Equip participants with hands-on experience in writing and optimising GPU code.
- Foster collaborative problem-solving to solidify understanding of GPU programming concepts.
- Encourage participants to explore real-world applications and implement solutions.

## Target Audience  
- Programmers with a basic understanding of parallel computing or data science.
- Researchers, data scientists, or software developers interested in leveraging GPU power for computational tasks.

## Prerequisites  
- Familiarity with basic programming concepts in C/C++ or Python.
- Basic knowledge of parallel computing principles is helpful but not mandatory.

### Supporting Tools 

Spack and the environment management. 


## Workshop Outline

---

### 1. Getting Started with GPUs and Compiled Code (1 Hour)

- **Activity: Explore GPU Capabilities**  
  - *Setup:* Each participant checks GPU specs on their workstation.
  - *Discussion:* Compare CPU vs. GPU specs in pairs, then discuss key differences as a group.
  - *Hands-On:* Run a pre-written code snippet that demonstrates CPU and GPU speed differences (e.g., simple vector addition).

- **Intro to Compiled Code and GPUs**  
  - **Brief Overview of Compiled Code**  
    - What compiled code is, and how it differs from interpreted code.
    - Why compiled languages (e.g., C/C++, CUDA) are commonly used in high-performance computing.
  - **Relevance to GPUs**  
    - Discuss how compiled code translates directly to machine code, which enables better optimization and speed, crucial for high-performance applications on GPUs.
    - Advantages of CUDA (compiled) over Python libraries (interpreted) for performance-intensive tasks.
  
- **Group Challenge:**  
  - In pairs, participants predict which types of applications benefit most from GPU acceleration.  
  - *Outcome:* Groups share insights, building an understanding of GPU use cases.

---

### 2. GPU Architecture and Memory Concepts (1 Hour)

- **Short Interactive Demo (5-10 Minutes):**  
  - Show how threads, blocks, and grids are structured with visual aids.
  - Participants simulate “threads” and “blocks” with cards/paper to visualize thread distribution.

- **Collaborative Coding Exercise:**  
  - *Task:* Participants write a simple kernel function (e.g., vector addition) to practice defining grid and block dimensions.
  - *Peer Review:* Pairs review each other's code, discussing grid/block choices and identifying memory access patterns.

- **Quick Recap and Group Reflection:**  
  - Participants share their “aha!” moments and challenges.

---

### 3. Core GPU Programming with CUDA (1.5 Hours)

- **Coding Lab:**  
  - *Setup:* Write a CUDA program for vector addition and matrix multiplication. Skeleton code provided, but participants must fill in key components.
  - *Checkpoints and Mentor Support:* Facilitators provide tips on block/grid sizing, kernel functions, and memory management.

- **Group Debugging Challenge:**  
  - Small groups are given “buggy” CUDA code. Each group debugs and optimizes the code, focusing on understanding errors and improving performance.

- **Guided Reflection:**  
  - Groups discuss debugging strategies and the benefits of optimized code.

---

### Lunch Break (1 Hour)

---

### 4. Intermediate CUDA Programming and Optimization (1.5 Hours)

- **Memory Management Activity:**  
  - *Task:* Each participant practices optimizing memory use by converting a basic program to use shared memory.
  - *Experiment:* Measure performance with/without shared memory. Discuss the results in small groups.

- **Mini-Workshop: Profiling for Performance**  
  - *Exercise:* Participants profile the matrix multiplication code to identify bottlenecks using CUDA profiling tools.
  - *Optimization Sprint:* Each participant applies one optimization, then benchmarks and shares results with peers.

- **Reflection on Best Practices:**  
  - In groups, participants compile a list of memory management and performance optimization techniques.

---

### 5. Package Management with Spack (30 Minutes)

- **Introduction to Spack**  
  - What Spack is and why it’s essential for package management in high-performance computing.
  - How Spack helps manage dependencies and ensures compatibility, especially when working with complex software stacks.

- **Hands-On Lab:**  
  - *Setup:* Install Spack on local systems (if feasible) and configure it to manage GPU-related packages (e.g., CUDA Toolkit, cuDNN).
  - **Practical Exercise**: Use Spack to install and configure dependencies for a sample CUDA project.

- **Discussion:**  
  - Benefits of using Spack for managing dependencies in GPU programming and other HPC contexts.
  - Explore how Spack can facilitate multi-GPU configurations or versions in high-performance environments.

---

### 6. Exploring Python-based GPU Programming with CuPy and Numba (1 Hour)

- **Hands-On Lab:**  
  - Participants use CuPy/Numba to replicate their previous CUDA exercises in Python.
  - Experiment with running a simple image filter and compare GPU vs. CPU execution time.

- **Code Sharing and Discussion:**  
  - Groups share different approaches and discuss when Python-based GPU programming is more practical or preferable than CUDA.

---

### 7. Real-world Applications and Group Projects (1 Hour)

- **Group Project: Real-world Case Study**  
  - Participants choose between two project scenarios (e.g., a simple 2D physics simulation or a machine learning mini-benchmark).
  - Groups implement the project, applying GPU programming techniques and optimization learned throughout the day.

- **Project Presentation and Peer Review:**  
  - Each group presents their project, highlighting code choices, challenges, and results.
  - Peer groups ask questions and offer constructive feedback.

---

### 8. Debugging, Profiling, and Best Practices Discussion (45 Minutes)

- **Debugging Activity:**  
  - Each participant is provided a problematic code snippet. The challenge is to identify and fix the issues, using debugging strategies and tools covered.

- **Roundtable Discussion: Best Practices**  
  - Each participant shares one lesson or tip they found most valuable from the day.

- **Wrap-Up Q&A:**  
  - Open forum for questions, sharing resources, and future learning pathways.

---

## Post-Workshop Resources and Next Steps

- **Resource Sharing**  
  - A curated list of tutorials, example projects, and documentation.

- **Suggestions for Continued Practice**  
  - Ideas for personal projects, deeper dives into CUDA or OpenCL, and other advanced GPU programming topics.

---

This interactive structure emphasizes exploration, collaboration, and application over traditional lectures, making the workshop engaging and highly practical. Participants will leave with hands-on experience and confidence in GPU programming essentials.
