from caravel_cocotb.caravel_interfaces import UART
import cocotb
from cocotb.triggers import Timer, FallingEdge

class ML_UART_BASE(UART):
    def __init__(self, caravelEnv, uart_pins={"tx": 21,  "rx": 22}, prescaler=0):
        super().__init__(caravelEnv, uart_pins)
        self.prescaler = prescaler
        self.bit_time_ns = self.calculate_bit_time(self.period, self.prescaler)
        cocotb.log.info(f"[{self.__class__.__name__}] bit time: {self.bit_time_ns}")
        self.caravelEnv.drive_gpio_in(self.uart_pins["rx"], 1)

    @staticmethod
    def calculate_bit_time(clk_period, prescaler):
        """
        Calculates the bit time for a given clock period and prescaler value.
        Args:
            clk_period (float): the clock period in any units.
            prescaler (int): the prescaler value.

        Returns:
            float: the calculated bit time in the same unit as clk_period.
        """
        bit_time = clk_period * (prescaler + 1) * 8
        cocotb.log.info(f"[{ML_UART_BASE.__name__}] bit time: {bit_time}")
        return bit_time

    def change_prescaler(self, prescaler):
        self.prescaler = prescaler
        self.bit_time_ns = ML_UART_BASE.calculate_bit_time(self.period, self.prescaler)
        cocotb.log.info(f"[{self.__class__.__name__}] new bit time: {self.bit_time_ns} after prescaler change to {prescaler}")

    async def start_of_tx(self):
        while True:
            await FallingEdge(self.caravelEnv.dut._id(f"gpio{self.uart_pins['tx']}_monitor", False))
            await Timer(2, units="ns")
            if self.caravelEnv.dut._id(f"gpio{self.uart_pins['tx']}_monitor", False).value == 1:
                continue  # to skip latches
            await Timer(self.bit_time_ns - 2, units="ns")
            await Timer(int(self.bit_time_ns / 2), units="ns")  # read the bit from the middle
            break
    
    async def get_line(self):
        """Read line sent through UART (msg is sent by the software)

        - Line is a bunch of ASCII sybmols ended by linefeed '\\\\n'"""
        line = ""
        while True:
            new_char = await self.get_char()
            if new_char == "\n":
                break
            cocotb.log.info(f"[UART] new char = {new_char}")
            line += new_char
            cocotb.log.debug(f"[UART] part of the line recieved = {line}")
        cocotb.log.info(f"[UART] line recieved = {line}")
        return line


