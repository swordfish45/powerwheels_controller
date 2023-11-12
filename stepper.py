from TMC_2209.TMC_2209_StepperDriver import *

class stepper:

    def __init__(self):
        self.tmc = TMC_2209(21, 16, 20)

        self.tmc.set_direction_reg(False)
        self.tmc.set_current(750)
        self.tmc.set_interpolation(True)
        self.tmc.set_spreadcycle(True)
        self.tmc.set_microstepping_resolution(2)
        self.tmc.set_internal_rsense(False)

        self.tmc.set_acceleration(4000)
        self.tmc.set_max_speed(2000)

        self.tmc.set_motor_enabled(True)
        self.on = True


    def move(self, positive, rposition):

        if(not self.on):
            self.tmc.set_motor_enabled(True)
            self.on = True

        if(positive):
            self.tmc.run_to_position_steps(rposition, MovementAbsRel.RELATIVE)
        else:
            self.tmc.run_to_position_steps(-rposition, MovementAbsRel.RELATIVE)
        

    def off(self):
        if(self.on):
            self.tmc.set_motor_enabled(False)
            self.on = False


            