from connection import Connection

class Register():
    def __init__(self, unit=1, reg_start=0, reg_lenght=10, data_type="int", qty=5):
        self.unit=unit
        self.reg_start=reg_start
        self.reg_lenght=reg_lenght
        self.data_type=data_type
        self.qty=qty



    def holding_read(self,client):
        print('holding')
        massure = client.read_input_registers(self.reg_start, self.reg_lenght, self.unit)
        data = massure.registers[0:]
        return data

    def input_read(self):
        print('input')
        massure = client.read_input_registers(self.reg_start, self.reg_lenght, self.unit)
        data = massure.registers[0:]







    def print_output(self):
        print('output')




class Modbus_master(Connection):
    def __init__(self, method, port, speed, stopbits, parity, bytesize, timeout):

        super().__init__(method, port, speed, stopbits, parity, bytesize, timeout)


        self.reg=Register()




if __name__=="main":
    connection=Modbus_master()


