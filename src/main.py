#!/usr/bin/env python3
"""Smart Entryway Offline Automation: runnable simulation-first controller."""

from __future__ import annotations

import argparse
import json
import math
import time
from dataclasses import asdict, dataclass

PROJECT_ID = 16
MODE = "closed_loop_control"
DEFAULT_THRESHOLD = 0.61


@dataclass(frozen=True)
class Snapshot:
    timestamp: float
    values: list[float]
    score: float
    valid: bool


class Controller:
    def __init__(self, threshold: float = DEFAULT_THRESHOLD, confirmations: int = 2) -> None:
        if not 0.0 <= threshold <= 1.0:
            raise ValueError("threshold must be between 0 and 1")
        self.threshold = threshold
        self.confirmations_required = max(1, confirmations)
        self.confirmations = 0
        self.output_active = False

    def evaluate(self, values: list[float], timestamp: float | None = None) -> Snapshot:
        valid = bool(values) and all(math.isfinite(value) and 0.0 <= value <= 1.0 for value in values)
        score = sum(values) / len(values) if valid else 0.0
        condition = valid and score >= self.threshold
        self.confirmations = min(self.confirmations + 1, self.confirmations_required) if condition else 0
        self.output_active = valid and self.confirmations >= self.confirmations_required
        return Snapshot(timestamp or time.time(), values, score, valid)



from .policy import MotionRule
def run(iterations: int, interval: float, threshold: float = DEFAULT_THRESHOLD) -> None:
    # Retained CLI threshold only applies to the compatibility Controller API.
    rule=MotionRule(start=0)
    for step in range(iterations):
        now=step*10.0
        record=rule.sample(now, bool(step%4 in (1,2)))
        print(json.dumps({"project_id":16,"mode":"simulation",**record},sort_keys=True))
        if interval>0: time.sleep(interval)
if __name__=="__main__":
    parser=argparse.ArgumentParser(description="Local PIR-to-pointer rule, optional BLE, explicit hardware mode")
    parser.add_argument("--iterations",type=int,default=10)
    parser.add_argument("--interval",type=float,default=0.5)
    parser.add_argument("--threshold",type=float,default=DEFAULT_THRESHOLD)
    parser.add_argument("--hardware",action="store_true")
    parser.add_argument("--ble",action="store_true")
    options=parser.parse_args()
    if options.hardware:
        import asyncio
        from .hardware import operate
        asyncio.run(operate(options.iterations,max(0.05,options.interval),options.ble))
    else: run(max(1,options.iterations),max(0,options.interval),options.threshold)
