from caravel_cocotb.caravel_interfaces import * # import python APIs
import cocotb


async def base_function(caravelEnv):
    await caravelEnv.wait_mgmt_gpio(1)
    start_time = cocotb.utils.get_sim_time("ns")
    cocotb.log.info(f"[TEST] start test time: {start_time}ns")
    await caravelEnv.wait_mgmt_gpio(0)
    end_time = cocotb.utils.get_sim_time("ns")
    cocotb.log.info(f"[TEST] end test time: {end_time}ns")
    clk_period = caravelEnv.get_clock_obj().period/1000
    cocotb.log.info(f"[TEST] time: {end_time - start_time}ns number of cycles : {(end_time - start_time)/clk_period} period :{clk_period}")


@cocotb.test()
@report_test
async def test_aes_sbox(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=1175080)
    await base_function(caravelEnv)


@cocotb.test()
@report_test
async def test_chacha(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=1161557)
    await base_function(caravelEnv)


@cocotb.test()
@report_test
async def test_hash(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=11123843)
    await base_function(caravelEnv)


@cocotb.test()
@report_test
async def test_stress(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=1161466)
    await base_function(caravelEnv)


@cocotb.test()
@report_test
async def test_xtea(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=1560380)
    await base_function(caravelEnv)


@cocotb.test()
@report_test
async def soft_float(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=111789183)
    await base_function(caravelEnv)