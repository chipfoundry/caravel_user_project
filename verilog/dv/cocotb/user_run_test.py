from caravel_cocotb.scripts.verify_cocotb.RunTest import RunTest



class UserRunTest(RunTest):
    
    def hex_riscv_command_gen(self):
        GCC_PATH = "/opt/riscv/bin/"
        GCC_PREFIX = "riscv32-unknown-elf"
        GCC_COMPILE = f"{GCC_PATH}/{GCC_PREFIX}"
        SOURCE_FILES = (
            f"{self.paths.FIRMWARE_PATH}/crt0_vex.S {self.paths.FIRMWARE_PATH}/isr.c"
        )

        LINKER_SCRIPT = f"-Wl,-Bstatic,-T,{self.test.linker_script_file},--strip-debug "
        CPUFLAGS = "-O2 -g -march=rv32im_zicsr -mabi=ilp32 -D__vexriscv__ -ffreestanding -nostdlib"
        # CPUFLAGS = "-O2 -g -march=rv32imc_zicsr -mabi=ilp32 -D__vexriscv__ -ffreestanding -nostdlib"
        includes = [
            f"-I{ip}" for ip in self.get_ips_fw()
        ] + [
            f"-I{self.paths.FIRMWARE_PATH}",
            f"-I{self.paths.FIRMWARE_PATH}/APIs",
            f"-I{self.paths.USER_PROJECT_ROOT}/verilog/dv/cocotb",
            f"-I{self.paths.VERILOG_PATH}/dv/generated",
            f"-I{self.paths.VERILOG_PATH}/dv/",
            f"-I{self.paths.VERILOG_PATH}/common/",
        ]
        includes = f" -I{self.paths.FIRMWARE_PATH} -I{self.paths.FIRMWARE_PATH}/APIs -I{self.paths.VERILOG_PATH}/dv/generated  -I{self.paths.VERILOG_PATH}/dv/ -I{self.paths.VERILOG_PATH}/common -I{self.paths.USER_PROJECT_ROOT}/ip/EFIS/Drivers -I{self.paths.USER_PROJECT_ROOT}/ip/EFIS/Drivers/Include"
        includes += f" -I{self.paths.USER_PROJECT_ROOT}/verilog/dv/cocotb {' '.join([f'-I{ip}' for ip in self.get_ips_fw()])}"
        elf_command = (
            f"{GCC_COMPILE}-gcc  {includes} {CPUFLAGS} {LINKER_SCRIPT}"
            f" -o {self.hex_dir}/{self.test.name}.elf {SOURCE_FILES} {self.c_file}"
        )
        lst_command = f"{GCC_COMPILE}-objdump -d -S {self.hex_dir}/{self.test.name}.elf > {self.hex_dir}/{self.test.name}.lst "
        hex_command = f"{GCC_COMPILE}-objcopy -O verilog {self.hex_dir}/{self.test.name}.elf {self.hex_dir}/{self.test.name}.hex "
        sed_command = f'sed -ie "s/@10/@00/g" {self.hex_dir}/{self.test.name}.hex'
        return f" {elf_command} && {lst_command} && {hex_command} && {sed_command}"
