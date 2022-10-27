import numpy as np
from lib.grid_world import grid_world_2x2 as env
from lib.sarsa_app import SarsaApp

import ipywidgets as widgets
from IPython.display import display

import matplotlib.pyplot as plt


def sarsa_wrapper():
    env.reset()
    initial_q_table = np.zeros((len(env.states), 4))

    btn = widgets.Button(description='Next step')
    finish_episode_btn = widgets.Button(description='Finish episode')
    epsilon_slider = widgets.FloatSlider(min=0, max=1, step=0.1, description='Epsilon:', value=1)
    epsilon_textbox = widgets.BoundedFloatText(value=1.0, min=0.0, max=1.0, step=0.1, description='Epsilon:')

    output = widgets.Output()

    sarsa = SarsaApp(env, initial_q_table)

    def on_click_fn(obj):
        plt.close()
        output.clear_output(True)

        with output:
            sarsa.next_step()

    def on_click_finish_episode_fn(obj):
        plt.close()
        output.clear_output(True)
        with output:
            sarsa.finish_episode()

    def on_textbox_value_change_fn(obj):
        plt.close()
        output.clear_output(True)
        with output:
            sarsa.update_epsilon(obj.owner.value)

    btn.on_click(on_click_fn)
    finish_episode_btn.on_click(on_click_finish_episode_fn)
    epsilon_textbox.observe(on_textbox_value_change_fn)

    display(btn, finish_episode_btn, epsilon_textbox)
    display(output)


