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
from user_proj_tests.uart import ML_UART_BASE
import string
import random

@cocotb.test()
@report_test
async def uart0(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=159844)

    cocotb.log.info(f"[TEST] Start counter_la test")  
    # wait for start of sending
    await caravelEnv.release_csb()
    uart = UART_USER(caravelEnv, prescaler=2)
    await caravelEnv.wait_mgmt_gpio(1)
    cocotb.log.info(f"[TEST] finish configuration") 
    # generate rondom msg
    chars = string.ascii_letters + string.digits
    msg = ''.join(random.choice(chars) for _ in range(10))
    cocotb.log.info(f"[TEST] random msg = {msg}")
    # send random msg
    await uart.uart_send_line(msg)
    # recieve random msg
    msg_rec = await uart.get_line()
    if msg != msg_rec:
        cocotb.log.error(f"[TEST] test failed, recieved msg != sent msg, recieved: {msg_rec}, sent: {msg}")
    await caravelEnv.wait_mgmt_gpio(0)


class UART_USER(ML_UART_BASE):
    def __init__(self, caravelEnv, uart_pins={"tx": 13, "rx": 12}, prescaler=0):
        super().__init__(caravelEnv, uart_pins, prescaler)
        pass
