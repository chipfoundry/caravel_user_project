# SPDX-FileCopyrightText: 2023 Efabless Corporation

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#      http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# SPDX-License-Identifier: Apache-2.0


from caravel_cocotb.caravel_interfaces import test_configure
from caravel_cocotb.caravel_interfaces import report_test
import cocotb 
from cocotb.triggers import ClockCycles, First, Combine
from user_proj_tests.gpio_user.GPIOsPort import GPIOsPort


@cocotb.test()
@report_test
async def gpio_user(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=59844)
    cocotb.log.info("[TEST] Start gpio test")
    # wait for start of sending
    await caravelEnv.release_csb()
    await caravelEnv.wait_mgmt_gpio(1)
    cocotb.log.info("[TEST] finish configuration")
    # check output
    await wait_update(caravelEnv)
    gpio8 = GPIOsPortUser(caravelEnv)
    code = gpio8.monitor_gpio(7, 0).integer
    if code == 0x55:
        cocotb.log.info("[TEST] read right output 0x55")
    else:
        cocotb.log.error(f"[TEST] wrong read {code} instead of 0x55")
    await wait_update(caravelEnv)
    code = gpio8.monitor_gpio(7, 0).integer
    if code == 0xAA:
        cocotb.log.info("[TEST] read right output 0xAA")
    else:
        cocotb.log.error(f"[TEST] wrong read {code} instead of 0xAA")
    # software waiting for 0xAA
    await cocotb.start(drive_after_time(gpio8, caravelEnv, 100, 0xAA))
    code = await wait_update_timeout(caravelEnv, caravelEnv, 3000)
    if code == "timeout":
        cocotb.log.error("[TEST] get time out when waiting for update")
    else:
        cocotb.log.info("[TEST] get update")
    await cocotb.start(drive_after_time(gpio8, caravelEnv, 3000, 0x55))
    code = await wait_update_timeout(caravelEnv, caravelEnv, 1000)
    if code == "ok_updated":
        cocotb.log.error("[TEST] get update when waiting for time out")
    else:
        cocotb.log.info("[TEST] get timeout")
    
    await cocotb.start(drive_after_time(gpio8, caravelEnv, 100, 0xFF))
    code = await wait_update_timeout(caravelEnv, caravelEnv, 3000)
    if code == "timeout":
        cocotb.log.error("[TEST] get time out when waiting for update")
    else:
        cocotb.log.info("[TEST] get update")
        
    # test 1 bit change
    await cocotb.start(drive_after_time(gpio8, caravelEnv, 100, 0xFB))
    code = await wait_update_timeout(caravelEnv, caravelEnv, 3000)
    if code == "timeout":
        cocotb.log.error("[TEST] get time out when waiting for update")
    else:
        cocotb.log.info("[TEST] get update")
         
    await cocotb.start(drive_after_time(gpio8, caravelEnv, 3000, 0xF3))
    code = await wait_update_timeout(caravelEnv, caravelEnv, 1000)
    if code == "ok_updated":
        cocotb.log.error("[TEST] get update when waiting for time out")
    else:
        cocotb.log.info("[TEST] get timeout")


async def wait_update(caravelEnv):
    await caravelEnv.wait_mgmt_gpio(1)
    cocotb.log.info("[DEBUG] mgmt gpio 1")
    await caravelEnv.wait_mgmt_gpio(0)
    cocotb.log.info("[DEBUG] mgmt gpio 0")
    return "ok_updated"


async def wait_update_timeout(gpio_h, caravelEnv, timeout_cycles):
    update_fork = await cocotb.start(wait_update(gpio_h))
    time_out_fork = await cocotb.start(clock_cycles(caravelEnv, timeout_cycles))
    cocotb.log.info("[DEBUG]  start time out count")
    code = await First(update_fork, time_out_fork)
    if code == "timeout":
        await update_fork
    return code


async def clock_cycles(caravelEnv, timeout_cycles):
    await ClockCycles(caravelEnv.clk, timeout_cycles)
    return "timeout"


async def drive_after_time(gpio_user, caravelEnv, timeout_cycles, value):
    await clock_cycles(caravelEnv, timeout_cycles)
    gpio_user.drive_gpio_in((7, 0), value)

class GPIOsPortUser(GPIOsPort):
    def __init__(self, caravelEnv):
        super().__init__(caravelEnv, pins=[16,17,18,19,20,21,22,23])
