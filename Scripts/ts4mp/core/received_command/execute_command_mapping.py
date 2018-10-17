from server_commands.clock_commands import set_speed, request_pause, unrequest_pause, toggle_pause_unpause
from server_commands.interaction_commands import has_choices, generate_choices, generate_phone_choices, select_choice, cancel_mixer_interaction, cancel_super_interaction, push_interaction
from server_commands.lighting_commands import set_color_and_intensity
from server_commands.sim_commands import set_active_sim
from server_commands.ui_commands import ui_dialog_respond, ui_dialog_pick_result, ui_dialog_text_input
from server_commands.career_commands import find_career, select_career
from ts4mp.core.notifications import mp_chat


PERFORM_COMMAND_FUNCTIONS = {
    "has_choices"             : has_choices,
    "generate_choices"        : generate_choices,
    "generate_phone_choices"  : generate_phone_choices,
    "select_choice"           : select_choice,
    "cancel_mixer_interaction": cancel_mixer_interaction,
    "cancel_super_interaction": cancel_super_interaction,
    "push_interaction"        : push_interaction,
    "set_speed"               : set_speed,
    "request_pause"           : request_pause,
    "unrequest_pause"         : unrequest_pause,
    "toggle_pause_unpause"    : toggle_pause_unpause,
    "set_active_sim"          : set_active_sim,
    "mp_chat"                 : mp_chat,
    "ui_dialog_respond"       : ui_dialog_respond,
    "ui_dialog_pick_result"   : ui_dialog_pick_result,
    "ui_dialog_text_input"    : ui_dialog_text_input,
    "set_color_and_intensity" : set_color_and_intensity,
    "find_career"            : find_career,
    "select_career"          : select_career
}