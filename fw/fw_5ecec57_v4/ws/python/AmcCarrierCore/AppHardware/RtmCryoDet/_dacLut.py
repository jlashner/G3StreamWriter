#!/usr/bin/env python
#-----------------------------------------------------------------------------
# Title      : PyRogue CRYO RTM: SPI MAX
#-----------------------------------------------------------------------------
# File       : _spiMax.py
# Created    : 2017-04-03
#-----------------------------------------------------------------------------
# Description:
# PyRogue Cryo Amc Core
#-----------------------------------------------------------------------------
# This file is part of the rogue software platform. It is subject to
# the license terms in the LICENSE.txt file found in the top-level directory
# of this distribution and at:
#    https://confluence.slac.stanford.edu/display/ppareg/LICENSE.html.
# No part of the rogue software platform, including this file, may be
# copied, modified, propagated, or distributed except according to the terms
# contained in the LICENSE.txt file.
#-----------------------------------------------------------------------------

import pyrogue as pr

class LutMem(pr.Device):
    def __init__(   self,       
        name        = "LutMem",
        description = "Container for LUT Memory",
        ADDR_WIDTH_G = 11,
        **kwargs):
        
        super().__init__(name=name,description=description,**kwargs)

        self.addRemoteVariables(       
            name        = 'MEM', 
            offset      = 0x0, 
            number      =  2**ADDR_WIDTH_G, 
            bitSize     =  20, 
            bitOffset   =  0, 
            stride      =  4,
            mode        = "RW", 
            base         = pr.Int,
            hidden      = True,
        )

        self.add(pr.LinkVariable(
            name         = 'MemArray',
            hidden       = True,
            description  = "LUT mem array",
            dependencies = [self.node(f'MEM[{i}]') for i in range(2**ADDR_WIDTH_G)],
            linkedGet    = lambda dev, var, read: dev.getArray(dev, var, read),
            linkedSet    = lambda dev, var, value: dev.setArray(dev, var, value),
            typeStr      = "List[Int20]",
        ))

    @staticmethod
    def setArray(dev, var, value):
        for variable, setpoint in zip(var.dependencies, value):
            variable.set(setpoint, write=False)
        dev.writeBlocks()
        dev.verifyBlocks()
        dev.checkBlocks()

    @staticmethod
    def getArray(dev, var, read):
        if read:
           dev.readBlocks(variable=var.dependencies)
           dev.checkBlocks(variable=var.dependencies)
        return [variable.value() for variable in var.dependencies]

        
class LutCtrl(pr.Device):
    def __init__(   self,       
        name        = "LutCtrl",
        description = "Container for LUT Memory Controls",
        NUM_CH_G     = 2,
        ADDR_WIDTH_G = 11,
        BASE_ADDR_G  = 0,
        **kwargs):
        
        super().__init__(name=name,description=description,**kwargs)
        
        for i in range(NUM_CH_G):        
            self.add(pr.RemoteVariable(
                name         = f'DacAxilAddr[{i}]', 
                description  = 'AXI-Lite Address of the DAC Spi',
                offset       = 4*i,
                bitSize      = 32, 
                mode         = 'RW',
                enum         = {
                   0                   : "Disabled",
                   BASE_ADDR_G + 0x004 : "Dac[1]",
                   BASE_ADDR_G + 0x024 : "Dac[2]",
                   BASE_ADDR_G + 0x044 : "Dac[3]",
                   BASE_ADDR_G + 0x064 : "Dac[4]",
                   BASE_ADDR_G + 0x084 : "Dac[5]",
                   BASE_ADDR_G + 0x0A4 : "Dac[6]",
                   BASE_ADDR_G + 0x0C4 : "Dac[7]",
                   BASE_ADDR_G + 0x0E4 : "Dac[8]",
                   BASE_ADDR_G + 0x104 : "Dac[9]",
                   BASE_ADDR_G + 0x124 : "Dac[10]",
                   BASE_ADDR_G + 0x144 : "Dac[11]",
                   BASE_ADDR_G + 0x164 : "Dac[12]",
                   BASE_ADDR_G + 0x184 : "Dac[13]",
                   BASE_ADDR_G + 0x1A4 : "Dac[14]",
                   BASE_ADDR_G + 0x1C4 : "Dac[15]",
                   BASE_ADDR_G + 0x1E4 : "Dac[16]",
                   BASE_ADDR_G + 0x204 : "Dac[17]",
                   BASE_ADDR_G + 0x224 : "Dac[18]",
                   BASE_ADDR_G + 0x244 : "Dac[19]",
                   BASE_ADDR_G + 0x264 : "Dac[20]",
                   BASE_ADDR_G + 0x284 : "Dac[21]",
                   BASE_ADDR_G + 0x2A4 : "Dac[22]",
                   BASE_ADDR_G + 0x2C4 : "Dac[23]",
                   BASE_ADDR_G + 0x2E4 : "Dac[24]",
                   BASE_ADDR_G + 0x304 : "Dac[25]",
                   BASE_ADDR_G + 0x324 : "Dac[26]",
                   BASE_ADDR_G + 0x344 : "Dac[27]",
                   BASE_ADDR_G + 0x364 : "Dac[28]",
                   BASE_ADDR_G + 0x384 : "Dac[29]",
                   BASE_ADDR_G + 0x3A4 : "Dac[30]",
                   BASE_ADDR_G + 0x3C4 : "Dac[31]",
                   BASE_ADDR_G + 0x3E4 : "Dac[32]",
                },
            ))         
            
        self.add(pr.RemoteVariable(
            name         = 'NUM_CH_G', 
            description  = 'Value of NUM_CH_G FW generic',
            offset       = 0x20,
            bitSize      = 8, 
            bitOffset    = 0, 
            mode         = 'RO',
        ))  

        self.add(pr.RemoteVariable(
            name         = 'ADDR_WIDTH_G', 
            description  = 'Value of ADDR_WIDTH_G FW generic',
            offset       = 0x20,
            bitSize      = 8, 
            bitOffset    = 8, 
            mode         = 'RO',
        )) 

        self.add(pr.RemoteVariable(
            name         = 'Busy', 
            description  = '0x0 r.state=IDLE_S else 0x1',
            offset       = 0x20,
            bitSize      = 1, 
            bitOffset    = 16, 
            mode         = 'RO',
            pollInterval = 1, 
        )) 

        self.add(pr.RemoteVariable(
            name         = 'TrigCnt', 
            description  = 'Accepted Trigger Counter',
            offset       = 0x24,
            bitSize      = 16, 
            mode         = 'RO',
            pollInterval = 1, 
        ))    

        self.add(pr.RemoteVariable(
            name         = 'DropTrigCnt', 
            description  = 'Accepted Trigger Counter',
            offset       = 0x28,
            bitSize      = 16, 
            mode         = 'RO',
            pollInterval = 1, 
        ))            
        
        self.add(pr.RemoteVariable(
            name         = 'Continuous', 
            description  = 'continuous mode flag',
            offset       = 0x40,
            bitSize      = 1, 
            mode         = 'RW',
        )) 

        self.add(pr.RemoteVariable(
            name         = 'MaxAddr', 
            description  = 'Max address used in the looping through the timing/trigger pattern LUTs',
            offset       = 0x44,
            bitSize      = ADDR_WIDTH_G, 
            mode         = 'RW',
        ))        
        
        self.add(pr.RemoteVariable(
            name         = 'TimerSize', 
            description  = 'Sets the timer\'s timeout configuration size between sample updates',
            offset       = 0x48,
            bitSize      = 24, 
            mode         = 'RW',
            units        = '6.4ns',
        ))        
        
        self.add(pr.RemoteVariable(
            name         = 'EnableCh', 
            description  = 'Mask to enable channel updates (1-bit per channel)',
            offset       = 0x4C,
            bitSize      = NUM_CH_G, 
            mode         = 'RW',
        ))      

        self.add(pr.RemoteCommand(  
            name        = "SwTrig",
            description = "One-shot trigger the FSM",
            offset      = 0xF8,
            bitSize     = 1,
            function    = lambda cmd: cmd.post(1),
        ))

        self.add(pr.RemoteCommand(  
            name        = "CntRst",
            description = "Counter reset",
            offset      = 0xFC,
            bitSize     = 1,
            function    = lambda cmd: cmd.post(1),
        ))        

class DacLut(pr.Device):
    def __init__(   self,       
        name        = "LutCtrl",
        description = "Container for LUT Memory Controls",
        NUM_CH_G     = 2,
        ADDR_WIDTH_G = 11,
        BASE_ADDR_G  = 0,
        **kwargs):
        
        super().__init__(name=name,description=description,**kwargs)
        
        self.add(LutCtrl(
            name         = 'Ctrl', 
            offset       = 0x00000, 
            NUM_CH_G     = NUM_CH_G,
            ADDR_WIDTH_G = ADDR_WIDTH_G,
            BASE_ADDR_G  = BASE_ADDR_G,
            expand       = False,
        ))
        
        for i in range(NUM_CH_G):
            self.add(LutMem(
                name         = f'Lut[{i}]', 
                offset       = 0x10000+i*0x10000, 
                ADDR_WIDTH_G = ADDR_WIDTH_G,
                expand       = False,
            ))            
            
