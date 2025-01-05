# Getting Started with MCP System

## Overview
MCP System is a comprehensive monitoring and analysis platform that combines system metrics collection with advanced data science capabilities.

## Quick Start
```bash
# Create conda environment
conda create -n mcp-system python=3.9
conda activate mcp-system

# Install package
pip install -e .[dev]
```

## First Analysis
```python
from mcp_demo.analysis import MetricsAnalyzer

# Initialize analyzer
analyzer = MetricsAnalyzer()

# Collect and analyze metrics
results = analyzer.analyze_system(duration='1h')
```

## Next Steps
1. Review the [Architecture Guide](architecture.md)
2. Check out example [Notebooks](../notebooks/)
3. Read about [Advanced Features](advanced_features.md)