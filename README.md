# RoboSearch

RoboSearch is a staged course project for building an active visual search agent aimed at RoboCup@Home style object-finding tasks.

## Project Goal

The project targets a reusable active visual search module that can sit between perception and robot execution. The long-term goal is to support RoboCup@Home-style tasks such as:

- receive a target object label
- observe the current scene
- detect whether the target is visible
- query search memory
- choose the next best local view or search waypoint
- continue until success or failure

The current implementation is still in the early staged-development phase and focuses on a low-cost software validation pipeline before moving to real hardware and real MindSpore inference.

## Current Progress

### Stage 0 Completed

Stage 0 established:

- project structure
- shared data types
- config loading
- minimal demo entrypoint

Stage 0 demo:

```bash
python -m demos.mock_search_demo
```

### Stage 1 Completed: MockDetector

Stage 1 implemented a configurable mock detector for controlled testing without a real model.

Current supported mock scenarios:

- target present
- target absent
- low-confidence target
- different target labels produce different `matched_target` results in the same scene

Stage 1 demo:

```bash
python -m demos.image_detection_demo
```

### Stage 2 In Progress: Memory Lite

The current Memory Lite implementation supports:

- recording an observation
- storing last-seen object memory by target label
- tracking searched views
- tracking searched target-specific views
- preserving the last successful memory when a later observation does not find the target
- JSON persistence and reload

Current Stage 2 demo:

```bash
python -m demos.memory_demo
```

## Recommended Development Environment

The project is currently being developed primarily in WSL with Conda.

Recommended environment:

```bash
conda create -n robosearch python=3.10 -y
conda activate robosearch
pip install -r requirements.txt
```

## Demos

### 1. Minimal Project Startup

```bash
python -m demos.mock_search_demo
```

Expected purpose:

- verify package imports
- verify YAML config loading
- verify minimum project bootstrap flow

### 2. Mock Detection Scenarios

```bash
python -m demos.image_detection_demo
```

Expected purpose:

- verify mock detector behavior
- verify target-present / target-absent / low-confidence cases
- verify different target labels against the same scene
 
### 3. Memory Lite Demo

```bash
python -m demos.memory_demo
```

Expected purpose:

- verify observation recording
- verify JSON persistence
- verify last-seen memory lookup
- verify searched-view lookup
- verify searched-target-view lookup

## Current Module Boundaries

To keep later stages maintainable, the project currently follows these responsibilities:

- `JsonStore`: file persistence only
- `MemoryManager`: memory-related business logic only
- `MockDetector`: controlled perception simulation only
- `demos/`: validation and stage demos only
- `SearchAgent`: reserved for later closed-loop integration

## Current Repository Structure

```text
robosearch/
├── README.md
├── requirements.txt
├── configs/
├── demos/
├── logs/
├── robosearch/
├── tests/
├── outputs/
└── work/
```

## Next Planned Stage

The next implementation target is `NBV Lite`, including:

- discrete local view ordering
- low-confidence re-check behavior
- local observation action selection without full navigation
```
```
