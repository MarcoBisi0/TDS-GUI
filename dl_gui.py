#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 25 16:51:38 2014
@author: marco
"""
### CHANGELOG
'''
### 2014-10-10
    cambiato callback in pressione MOTOR GO per gestire ritorno della slitta alla posizione di partenza
'''
### TODO
''' '''
from Tkinter import *

### declaration and initialization of variables used by widgets
def widgets_variables(self, SKIP_measure):
    self.SKIP_measure = SKIP_measure
    self.motor_status = StringVar()
    self.motor_status.set('f') # motor off
    
    self.step_mode = StringVar()
    self.step_mode.set('1') # full step

    self.direction = StringVar()
    self.direction.set('0') # rotation CCW, towards sw_CCW
    
    self.steps = StringVar() # will hold steps to go
    self.steps_counted = StringVar() # will hold counted steps
    
    self.go_abs_pos = StringVar()
    
    self.start_v = StringVar()

    self.max_v = StringVar()

    self.max_a = StringVar()

    self.sw_CCW_state = IntVar()
    self.sw_CCW_state.set(1) # sw_CCW active

    self.sw_CW_state = IntVar()
    self.sw_CW_state.set(1) # sw_CW active
    
    self.measure_state = IntVar() # misura con voltmetro
    self.measure_state.set(int(not(self.SKIP_measure))) #0) # non misura
    
    self.pos_absolute = DoubleVar()
    self.pos_absolute.set(0.)
    self.pos_absolute_reset = DoubleVar()
    self.pos_absolute_reset.set(0.)
    
    self.pos_relative = DoubleVar()
    self.pos_relative.set(0.)
    
    self.measurement_delay = StringVar()
    self.measurement_delay.set('0')
    
    self.measurement_mode = StringVar()
    self.measurement_mode.set('OFF')
    
    self.filename = StringVar()
    self.filename.set('')
    
    self.nrep = IntVar()
    
    self.dl_cycle_start_pos = StringVar()
    self.dl_cycle_start_pos.set('1000')
    
    self.dl_cycle_stop_pos = StringVar()
    self.dl_cycle_stop_pos.set('119000')

    self.dl_cycle_rep = IntVar()
    self.dl_cycle_rep.set(1e12) # almost an endless loop?
    
### widgets declaration
def widgets_declare(self):
    ### cols&rows widgets position
    col_start_v_get_text = 0; row_start_v_get_text = 0
    col_max_v_get_text = 0; row_max_v_get_text = 1
    col_max_a_get_text = 0; row_max_a_get_text = 2
    col_set_va = 0; row_set_va = 3
    col_top_mid_sep = 0; row_top_mid_sep = 4
    col_motor_text = 0; row_motor_text = 5
    col_motor_button_off = 0; row_motor_button_off = 6
    col_motor_button_standby = 0; row_motor_button_standby = 7
    col_motor_button_on = 0; row_motor_button_on = 8
    #9
    #10
    col_bot_mid_sep = 0; row_bot_mid_sep = 11
    col_meas_mode_off = 0; row_meas_mode_off =12
    col_meas_mode_cont = 0; row_meas_mode_cont =13

    col_start_v_get = 1; row_start_v_get = 0
    col_max_v_get = 1; row_max_v_get = 1
    col_max_a_get = 1; row_max_a_get = 2
    col_default_va = 1; row_default_va = 3
    #4 separator
    col_step_mode_text = 1; row_step_mode_text = 5
    col_step_mode_full = 1; row_step_mode_full = 6
    col_step_mode_half = 1; row_step_mode_half = 7
    col_step_mode_quarter = 1; row_step_mode_quarter = 8
    col_step_mode_eigth = 1; row_step_mode_eigth = 9
    #10
    col_meas_mode_fast = 1; row_meas_mode_fast = 11
    col_meas_mode_step = 1; row_meas_mode_step =12
    col_meas_mode_scan = 1; row_meas_mode_scan =13
    

    col_sw_CCW_find_button = 2; row_sw_CCW_find_button = 0
    col_sw_CW_find_button = 2; row_sw_CW_find_button = 1
    col_step_go = 2; row_step_go = 2
    col_step_stop = 2; row_step_stop = 3
    #4 separator
    #col_steps_text = 2; row_steps_text = 5        
    col_step_get_text = 2; row_step_get_text = 5#6
    col_step_get = 2; row_step_get = 6#7 # (3,6)
    col_go_abs_pos_get_text = 2; row_go_abs_pos_get_text = 7
    col_go_abs_pos_get = 2; row_go_abs_pos_get = 8
    #col_full_travel_button = 2; row_full_travel_button = 8
    col_steps_counted_text = 2; row_steps_counted_text = 9
    col_steps_counted_show = 2; row_steps_counted_show = 10
    #11 separator
    col_delay_get_text = 2; row_delay_get_text = 12
    col_delay_get = 2; row_delay_get = 13

    col_plus_one_step = 3; row_plus_one_step = 0
    col_minus_one_step = 3; row_minus_one_step = 1
    col_plus_ten_step = 3; row_plus_ten_step = 2
    col_minus_ten_step = 3; row_minus_ten_step = 3
    #4 separator
    col_pos_absolute_text = 3; row_pos_absolute_text = 5
    col_pos_absolute_show = 3; row_pos_absolute_show = 6
    col_pos_relative_text = 3; row_pos_relative_text = 7
    col_pos_relative_show = 3; row_pos_relative_show = 8
    col_pos_absolute_reset_button = 3; row_pos_absolute_reset_button = 9 # (4,10)
    #10
    #11 separator
    col_filename_get_text = 3; row_filename_get_text = 12
    col_filename_get = 3; row_filename_get = 13
    
    col_dl_cycle_start_pos_text = 4; row_dl_cycle_start_pos_text = 0
    col_dl_cycle_start_pos_get = 4; row_dl_cycle_start_pos_get = 1
    col_dl_cycle_stop_pos_text = 4; row_dl_cycle_stop_pos_text = 2
    col_dl_cycle_stop_pos_get = 4; row_dl_cycle_stop_pos_get = 3
    col_dl_cycle_rep_text = 4; row_dl_cycle_rep_text = 4
    col_dl_cycle_rep_get = 4; row_dl_cycle_rep_get = 5
    col_dl_cycle1way = 4; row_dl_cycle1way = 6
    col_dl_cycle2way = 4; row_dl_cycle2way = 7
    col_dl_cycle_stop = 4; row_dl_cycle_stop = 8
    # 9
    col_meas_on_point_stop = 4; row_meas_on_point_stop = 10
    col_meas_on_point = 4; row_meas_on_point = 11
    col_nrep_get_text = 4; row_nrep_get_text = 12
    col_nrep_get = 4; row_nrep_get = 13
    
    ### widgets position
    ## Top-Mid Separator
    self.top_mid_sep_lbl = (Label(self, anchor = CENTER, text = '-----------------------------------------------------------------------\
            --------------------------------------------------------------------------------')\
            .grid(row = row_top_mid_sep, column = col_top_mid_sep, columnspan = 4))#7)

    ### motor
    self.motor_text = (Label(self, width = 5, height = 1, text = 'motor').grid(column = col_motor_text, row = row_motor_text))
        
    self.motor_button_off = (Radiobutton(self, text = 'off', variable = self.motor_status, value = 'f',\
            command = self.motor_status_set).grid(column = col_motor_button_off, row = row_motor_button_off))

    self.motor_button_standby = (Radiobutton(self, text = 'standby', variable = self.motor_status, value = 'b',\
            command = self.motor_status_set).grid(column =  col_motor_button_standby, row = row_motor_button_standby))
    self.motor_button_on = (Radiobutton(self, text = 'on', variable = self.motor_status, value = 'n',\
            command = self.motor_status_set).grid(column = col_motor_button_on, row = row_motor_button_on))
    
    ### step mode
    self.step_mode_text = (Label(self, width = 9, height = 1, text = 'step mode')\
            .grid(column = col_step_mode_text, row = row_step_mode_text))

    self.step_mode_full = (Radiobutton(self, text = '1', variable = self.step_mode, value = '1', command = self.set_step_mode)\
            .grid(column = col_step_mode_full, row = row_step_mode_full))#self.set_step_mode)
    self.step_mode_half = (Radiobutton(self, text = '1/2', variable = self.step_mode, value = '2', command = self.set_step_mode)\
            .grid(column = col_step_mode_half, row = row_step_mode_half))
    self.step_mode_quarter = (Radiobutton(self, text = '1/4', variable = self.step_mode, value = '3', command = self.set_step_mode)\
            .grid(column = col_step_mode_quarter, row = row_step_mode_quarter))#self.set_step_mode)
    self.step_mode_eigth = (Radiobutton(self, text = '1/8', variable = self.step_mode, value = '4', command = self.set_step_mode)\
            .grid(column = col_step_mode_eigth, row = row_step_mode_eigth))#self.set_step_mode)
    
    ### steps to go
    self.step_get_text = (Label(self, width = 20, height = 2, text = 'steps to go CTRL+g\nSTEP MODE dependant!')\
            .grid(column = col_step_get_text, row = row_step_get_text))
    self.step_get = Entry(self, width = 6, textvariable = self.steps)
    self.step_get.grid(column = col_step_get, row = row_step_get)

    ### 2013-11-06 go to absolute position
    self.go_abs_pos_get_text = (Label(self, width = 23, text = 'go to absolute position\nCTRL+a')\
            .grid(column = col_go_abs_pos_get_text, row = row_go_abs_pos_get_text))
    self.go_abs_pos_get = Entry(self, width = 6, textvariable = self.go_abs_pos)
    self.go_abs_pos_get.grid(column = col_go_abs_pos_get, row = row_go_abs_pos_get)
    
    self.step_go_color = 'cyan'
    ### 2014-10-10 self.step_go = Button(self, bg = self.step_go_color, text = 'MOTOR\nGO', command = self.motor_go_steps)
    self.step_go = Button(self, bg = self.step_go_color, text = 'MOTOR\nGO', command = self.vai_motore)
    self.step_go.grid(column = col_step_go, row = row_step_go)
    
    self.step_stop_color = 'cyan'
    self.step_stop = Button(self, bg = self.step_stop_color, text = 'MOTOR\nSTOP', command = self.motor_stop)
    self.step_stop.grid(column = col_step_stop, row = row_step_stop)

    ### +1 step
    self.plus_one_step = Button(self, text = '+1 step', command = lambda: self.tune_delay('1')) # LAMBDA, altrimenti esegue subito il callback e poi niente più ref: http://stackoverflow.com/questions/6920302/passing-argument-in-python-tkinter-button-command
    self.plus_one_step.grid(column = col_plus_one_step, row = row_plus_one_step)
    ### -1 step
    self.minus_one_step = Button(self, text = '-1 step', command = lambda: self.tune_delay('-1')) # LAMBDA, altrimenti esegue subito il callback e poi niente più ref: http://stackoverflow.com/questions/6920302/passing-argument-in-python-tkinter-button-command
    self.minus_one_step.grid(column = col_minus_one_step, row = row_minus_one_step)
    ### +10 step
    self.plus_ten_step = Button(self, text = '+10 step', command = lambda: self.tune_delay('10')) # LAMBDA, altrimenti esegue subito il callback e poi niente più ref: http://stackoverflow.com/questions/6920302/passing-argument-in-python-tkinter-button-command
    self.plus_ten_step.grid(column = col_plus_ten_step, row = row_plus_ten_step)
    ### -10 step
    self.minus_ten_step = Button(self, text = '-10 step', command = lambda: self.tune_delay('-10')) # LAMBDA, altrimenti esegue subito il callback e poi niente più ref: http://stackoverflow.com/questions/6920302/passing-argument-in-python-tkinter-button-command
    self.minus_ten_step.grid(column = col_minus_ten_step, row = row_minus_ten_step)
    
    ### counted steps
    self.steps_counted_text = (Label(self, width = 13, height = 1, text = 'counted steps', fg = 'magenta')\
            .grid(column = col_steps_counted_text, row = row_steps_counted_text))
    self.steps_counted_show = Entry(self, width = 6, textvariable = self.steps_counted, bg = 'magenta')
    self.steps_counted_show.grid(column = col_steps_counted_show, row = row_steps_counted_show)
    #self.steps_counted_show = Label(self, width = 6, text = '')

    ### velocity and acceleration
    self.start_v_get_text = (Label(self, width = 13, height = 1, text = 'start vel (%)')\
            .grid(column = col_start_v_get_text, row = row_start_v_get_text))
    self.start_v_get = (Entry(self, width = 3, textvariable = self.start_v)\
            .grid(column = col_start_v_get, row = row_start_v_get))
    
    self.max_v_get_text = (Label(self, width = 11, height = 1, text = 'max vel (%)')\
            .grid(column = col_max_v_get_text, row = row_max_v_get_text))
    self.max_v_get = (Entry(self, width = 3, textvariable = self.max_v)\
            .grid(column = col_max_v_get, row = row_max_v_get))
    
    self.max_a_get_text = (Label(self, width = 11, height = 1, text = 'max acc (%)')\
            .grid(column = col_max_a_get_text, row = row_max_a_get_text))
    self.max_a_get = (Entry(self, width = 3, textvariable = self.max_a)\
            .grid(column = col_max_a_get, row = row_max_a_get))
    
    self.set_va = (Button(self, text = 'set', command = lambda arg1 = self.start_v, arg2 = self.max_v, arg3 = self.max_a:\
            self.va(arg1, arg2, arg3)).grid(column = col_set_va, row = row_set_va))
    
    self.default_va = (Button(self, text = 'default', command = lambda arg1 = self.start_v, arg2 = self.max_v, arg3 = self.max_a:\
            self.va_set_default(arg1, arg2, arg3)).grid(column = col_default_va, row = row_default_va))
    
    ### switches
    self.sw_CCW_find_button = (Button(self, text = 'sw_CCW find', command = self.sw_CCW_find)\
            .grid(column = col_sw_CCW_find_button, row = row_sw_CCW_find_button))
    self.sw_CW_find_button = (Button(self, text = 'sw_CW find (motor side)', command = self.sw_CW_find)\
            .grid(column = col_sw_CW_find_button, row = row_sw_CW_find_button))

    '''self.bot_mid_sep_lbl = (Label(self, anchor = W, text = 'measurement mode   ------------------------------------------------------------------------------------------------------------------                                        ')\
            .grid(row = row_bot_mid_sep, column = col_bot_mid_sep, columnspan = 4))#7) row 12'''
    self.bot_mid_sep_lbl = (Label(self, anchor = W, text = 'measurement mode')\
            .grid(row = row_bot_mid_sep, column = col_bot_mid_sep))
    
    ### measurement mode
    self.measurement_mode_off = (Radiobutton(self, text = 'OFF', variable = self.measurement_mode, value = 'OFF',\
        command = lambda: self.measure_state.set(0))).grid(column = col_meas_mode_off, row = row_meas_mode_off)
    self.measurement_mode_continuous = (Radiobutton(self, text = 'continuous', variable = self.measurement_mode,\
        value = 'continuous', command = lambda: self.measure_state.set(1))).grid(column = col_meas_mode_cont, row = row_meas_mode_cont)
    self.measurement_mode_step = (Radiobutton(self, text = 'step', variable = self.measurement_mode,\
        value = 'step', command = lambda: self.measure_state.set(1))).grid(column = col_meas_mode_step, row = row_meas_mode_step)
    self.measurement_mode_scan = (Radiobutton(self, text = 'scan', variable = self.measurement_mode,\
        value = 'scan', command = lambda: self.measure_state.set(1))).grid(column = col_meas_mode_scan, row = row_meas_mode_scan)
    self.measurement_mode_fast = (Radiobutton(self, text = 'fast', variable = self.measurement_mode,\
        value = 'fast', command = lambda: self.measure_state.set(1))).grid(column = col_meas_mode_fast, row = row_meas_mode_fast)
    self.measurement_delay_get_text = Label(self, text = 'delay between\nmeasurements').grid(column = col_delay_get_text, row = row_delay_get_text)
    self.measurement_delay_get = Entry(self, width = 6, textvariable = self.measurement_delay).grid(column = col_delay_get, row = row_delay_get)

    ### file name
    self.filename_get_text = Label(self, text = 'file name suffix').grid(column = col_filename_get_text, row = row_filename_get_text)
    self.filename_get = Entry(self, width = 20, textvariable = self.filename).grid(column = col_filename_get, row = row_filename_get)

    ### pos_absolute
    self.pos_absolute_text = (Label(self, width = 21, height = 2, text = 'absolute position\n(steps, 1 step = 2.5 um)')\
            .grid(column = col_pos_absolute_text, row = row_pos_absolute_text))
    self.pos_absolute_show = Label(self, relief = 'sunken', bg = 'gray', width = 10, textvariable = self.pos_absolute) # bg = '#f8f8f8'
    self.pos_absolute_show.grid(column = col_pos_absolute_show, row = row_pos_absolute_show)
    self.pos_absolute_reset_button = Button(self, text = 'reset\nposition', command = self.pos_absolute_reset_action)
    self.pos_absolute_reset_button.grid(column = col_pos_absolute_reset_button, row = row_pos_absolute_reset_button)

    ### pos_relative
    self.pos_relative_text = (Label(self, width = 21, height = 2, text = 'relative position\n(steps, 1 step = 2.5 um)')\
            .grid(column = col_pos_relative_text, row = row_pos_relative_text))
    self.pos_relative_show = Entry(self, width = 10, textvariable = self.pos_relative)
    self.pos_relative_show.grid(column =  col_pos_relative_show, row = row_pos_relative_show)
    
    ### DL cycle
    self.dl_cycle_start_pos_text =(Label(self, width = 14, height = 1, text = 'start position'))\
            .grid(column = col_dl_cycle_start_pos_text, row = row_dl_cycle_start_pos_text)
    self.dl_cycle_start_pos_get = Entry(self, width = 12, textvariable = self.dl_cycle_start_pos)
    self.dl_cycle_start_pos_get.grid(column = col_dl_cycle_start_pos_get, row = row_dl_cycle_start_pos_get)
    self.dl_cycle_stop_pos_text =(Label(self, width = 14, height = 1, text = 'stop position'))\
            .grid(column = col_dl_cycle_stop_pos_text, row = row_dl_cycle_stop_pos_text)
    self.dl_cycle_stop_pos_get = Entry(self, width = 12, textvariable = self.dl_cycle_stop_pos)
    self.dl_cycle_stop_pos_get.grid(column = col_dl_cycle_stop_pos_get, row = row_dl_cycle_stop_pos_get)
    self.dl_cycle_rep_text =(Label(self, width = 14, height = 1, text = 'repetitions'))\
            .grid(column = col_dl_cycle_rep_text, row = row_dl_cycle_rep_text)
    self.dl_cycle_rep_get = Entry(self, width = 12, textvariable = self.dl_cycle_rep)
    self.dl_cycle_rep_get.grid(column = col_dl_cycle_rep_get, row = row_dl_cycle_rep_get)

    self.dl_cycle_button = Button(self, text = '1-way cycle', command = self.dl_cycle_action1)
    self.dl_cycle_button.grid(column = col_dl_cycle1way, row = row_dl_cycle1way)
    self.dl_cycle_button = Button(self, text = '2-way cycle', command = self.dl_cycle_action2)
    self.dl_cycle_button.grid(column = col_dl_cycle2way, row = row_dl_cycle2way)
    self.dl_cycle_stop_button = Button(self, text = 'stop\ncycle DL', command = self.dl_cycle_stop_action)
    self.dl_cycle_stop_button.grid(column = col_dl_cycle_stop, row = row_dl_cycle_stop)

    ### measure on point
    self.meas_on_point_stop_button = Button(self, text = 'stop\non point', command = self.measure_on_point_stop_action)
    self.meas_on_point_stop_button.grid(column = col_meas_on_point_stop, row = row_meas_on_point_stop)
    self.meas_on_point_button = Button(self, text = 'measure\non point', command = self.measure_on_point_action)
    self.meas_on_point_button.grid(column = col_meas_on_point, row = row_meas_on_point)
    self.nrep_get_text = Label(self, width = 9, height = 2, text = 'number of\nrepetions')\
            .grid(column = col_nrep_get_text, row = row_nrep_get_text)
    self.nrep_get = Entry(self, width = 9, textvariable = self.nrep)
    self.nrep_get.grid(column = col_nrep_get, row = row_nrep_get)
    
    ### say goodbye
    '''say goodbay self.quitButton = Button(self, text='Quit', command =  )        
    self.quitButton.grid()'''
