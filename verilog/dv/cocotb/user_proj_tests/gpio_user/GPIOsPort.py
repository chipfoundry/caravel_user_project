import cocotb
from cocotb.triggers import ClockCycles
from cocotb.binary import BinaryValue


class GPIOsPort:
    def __init__(self,caravelEnv, pins):
        self.pins = pins
        self.caravelEnv = caravelEnv

    async def wait_gpio_pin(self, pin, data: int) -> None:
        is_list = isinstance(pin, (list, tuple))
        data_s = str(data) if not is_list else format(data, f'0{pin[0] - pin[1] + 1}b')
        while True:
            if is_list:
                if data_s == self.monitor_gpio(pin[0], pin[1]).binstr:
                    break
            else:
                if data_s == self.monitor_gpio(pin).binstr:
                    break
            await ClockCycles(self.caravelEnv.clk, 1)

    def monitor_gpio(self, h_bit, l_bit=None) -> BinaryValue:
        if l_bit is None:
            return self.caravelEnv.monitor_gpio(self.pins[h_bit])
        else:
            bins_arr = [self.pins[i] for i in range(h_bit, l_bit-1, -1)]
            return cocotb.binary.BinaryValue(value=self.caravelEnv.monitor_discontinuous_gpios(bins_arr))

    def drive_gpio_in(self, pins, data: int):
        is_list = isinstance(pins, (list, tuple))
        if is_list:
            cocotb.log.debug(f"[{self.__class__.__name__}] drive gpio in ({self.pins[pins[0]]}, {self.pins[pins[1]]}) with data {data}")
            self.caravelEnv.drive_gpio_in((self.pins[pins[0]], self.pins[pins[1]]), data)
        else:
            cocotb.log.debug(f"[{self.__class__.__name__}] drive gpio in ({self.pins[pins]}) with data {data}")
            self.caravelEnv.drive_gpio_in(self.pins[pins], data)

    def release_gpio(self, pins):
        is_list = isinstance(pins, (list, tuple))
        if is_list:
            self.caravelEnv.release_gpio((self.pins[pins[0]], self.pins[pins[1]]))
        else:
            self.caravelEnv.release_gpio(self.pins[pins])