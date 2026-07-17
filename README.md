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

### Stage 3 Completed: NBV Lite

Stage 3 implemented a lightweight next-best-view module for local search decisions.

Current supported NBV features:

- discrete local view sequencing
- low-confidence target re-check actions
- target-aware view filtering based on memory
- decision-style output for later agent integration

Stage 3 demo:

```bash
python -m demos.nbv_demo
```

### Stage 4 In Progress: Search Planner Lite

The current Search Planner Lite implementation supports:

- semantic prior loading from configuration
- candidate waypoint scoring
- visited-history penalty handling
- failure-history penalty handling
- ranked candidate output
- explainable `SearchDecision` output

Current Stage 4 demo:

```bash
python -m demos.search_planner_demo
```

## Recommended Development Environment

The project is currently being developed primarily in WSL with Conda.

Recommended environment:

```bash
conda create -n robosearch python=3.10 -y
conda activate robosearch
python -m pip install -r requirements.txt
python -m pip install -r requirements-dev.txt
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

### 4. NBV Lite Demo

```bash
python -m demos.nbv_demo
```

Expected purpose:

- verify local next-view selection
- verify target-aware filtering with memory
- verify low-confidence re-check action generation

### 5. Search Planner Lite Demo

```bash
python -m demos.search_planner_demo
```

Expected purpose:

- verify semantic prior scoring
- verify ranked waypoint output
- verify explainable planner decisions
- verify deterministic selection behavior

## Testing

Run tests with the active project Python environment:

```bash
python -m pytest tests/test_search_planner.py
```

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
|-- README.md
|-- requirements.txt
|-- requirements-dev.txt
|-- configs/
|-- demos/
|-- logs/
|-- robosearch/
|-- tests/
|-- outputs/
`-- work/
```

## Next Planned Stage

The next implementation target is `Planner integration into the V0 search loop`, including:

- `SearchPlanner` integration into the existing state-machine flow
- multi-waypoint mock search execution
- planner-driven waypoint transitions
- preparation for later real detector replacement
```
